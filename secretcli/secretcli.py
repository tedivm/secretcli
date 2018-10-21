import boto3
import click
import json
import os
import requests
import sys
import yaml


def get_secret(secret_name, region=None, raw=False):
    """Pull the specific secret down from the AWS Secrets Manager"""
    client = get_aws_client(region)

    # Depending on whether the secret was a string or binary, one of these fields will be populated
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = get_secret_value_response['SecretBinary'].decode("utf-8")

    if raw:
        return secret
    return yaml.load(secret)

def put_secret(secret_name, secret_value, region=None, raw=False):
    """Save the supplied value as the secret in the AWS Secrets Manager"""
    client = get_aws_client(region)
    if raw:
        secret_string = secret_value
    else:
        secret_string = json.dumps(secret_value)
    response = client.put_secret_value(
        SecretId=secret_name,
        SecretString=secret_string,
        VersionStages=[
            'AWSCURRENT'
        ]
    )

def get_region():
    """Extrapolate the preferred region when one isn't supplied"""
    boto3_session = boto3.session.Session()

    # Check for boto3/awscli default region.
    if boto3_session.region_name:
        return boto3_session.region_name

    # Check for specific environmental variable.
    if 'AWS_SECRETS_REGION' in os.environ:
        return os.environ['AWS_SECRETS_REGION']

    # If this is being called from an EC2 instance use its region.
    r = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=0.2)
    r.raise_for_status()
    data = r.json()
    return data['region']

def get_aws_client(region):
    """Return an initialized boto3 client pointing at the secretsmanager service"""
    if not region:
        region = get_region()

    return boto3.client(
        service_name='secretsmanager',
        region_name=region
    )


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.parent:
        click.echo(ctx.parent.get_help())


@cli.command(short_help="Print the default region used by this application")
def region():
    click.echo(get_region())


@cli.command(short_help="Initialize a new secret in the AWS Secrets Manager")
@click.argument('secret')
@click.option('-r', '--region', default=None)
@click.option('-d', '--description', default='')
def init(secret, region, description):
    client = get_aws_client(region)
    response = client.create_secret(
        Name=secret,
        Description=description,
        SecretString='{}'
    )


@cli.command(short_help="Get a specific value from the secret datastore")
@click.argument('secret')
@click.argument('key')
@click.option('-c', '--category', default=None)
@click.option('-r', '--region', default=None)
def get(secret, key, category, region):
    secret_data = get_secret(secret, region)
    if category:
        if category in secret_data:
            if key in secret_data[category]:
                click.echo(secret_data[category][key])
                sys.exit(0)
    if key in secret_data:
        click.echo(secret_data[key])
        sys.exit(0)
    sys.exit(1)


@cli.command(short_help="Set a specific value in the secret datastore")
@click.argument('secret')
@click.argument('key')
@click.argument('value')
@click.option('-c', '--category', default=None)
@click.option('-r', '--region', default=None)
def set(secret, key, value, category, region):
    secret_data = get_secret(secret, region)
    if category:
        if category not in secret_data:
            secret_data[category] = {}
        secret_data[category][key] = value
    else:
        secret_data[key] = value
    put_secret(secret, secret_data, region)


@cli.command(short_help="Remove a key from the secret datastore")
@click.argument('secret')
@click.argument('key')
@click.option('-c', '--category', default=None)
@click.option('-r', '--region', default=None)
def remove(secret, key, category, region):
    secret_data = get_secret(secret, region)
    if category:
        if category not in secret_data:
            sys.exit(0)
        if key in secret_data[category]:
            del secret_data[category][key]
    elif key not in secret_data:
        sys.exit(0)
    del secret_data[key]
    put_secret(secret, secret_data, region)


@cli.command(short_help="Set a specific value in the secret datastore")
@click.argument('secret')
@click.option('-c', '--category', default=None)
@click.option('-r', '--region', default=None)
def list(secret, category, region):
    secret_data = get_secret(secret, region)
    if category:
        if category in secret_data:
            secret_data = secret_data[category]
        else:
            sys.exit(1)
    for key in secret_data:
        click.echo(key)


@cli.command(short_help="Upload a replacement secrets file")
@click.argument('secret')
@click.argument('input', type=click.File('rb'))
@click.option('-r', '--region', default=None)
def upload(secret, input, region):
    content = input.read().decode("utf-8")
    put_secret(secret, content, region, raw=True)


@cli.command(short_help="Download the entire secrets file")
@click.argument('secret')
@click.argument('output', type=click.File('wb'), required=False)
@click.option('-r', '--region', default=None)
def download(secret, output, region):
    contents = get_secret(secret, region, raw=True)
    if not output:
        click.echo(contents)
    else:
        output.write(contents.encode('utf-8'))
        output.close()


if __name__ == '__main__':
    cli()
