# secretcli

The secretcli project provides a simple to use command line interface to the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/). It is capable of uploading or downloading the entire secret as well as working with individual fields.

## Usage

### Initializing a new Secret

New secrets are easy to initiate. This will create a new Secret in the AWS Secret Manager and store an empty javascript object as the first version.

```bash
$ secretscli init TestSecret
```

### Working with individual Keys

Additional Key/Value pairs can be added to the secret using a single command. Behind the scenes this downloads the existing database, updates it with the new key/value pair, and uploads it as the current version.

```bash
$ secretscli set TestSecret postgreshost 10.10.10.16
$ secretscli set TestSecret postgresuser postgres
$ secretscli set TestSecret postgrespassword super_secret_string
$ secretscli set TestSecret longstring "This is a string with spaces."
```

Retrieving values is just as simple. This can be useful when trying to use values in bash scripts.

```bash
$ secretscli get TestSecret postgreshost
10.10.10.16
$ secretscli get TestSecret postgresuser
postgres
$ secretscli get TestSecret postgrespassword
super_secret_string
```

Values can also be completely removed from the secret.

```bash
$ secretscli get TestSecret postgreshost
10.10.10.16
$ secretscli remove TestSecret postgreshost
$ secretscli get TestSecret postgreshost
```

### Working with entire Files

The entire Secret can be downloaded as a file. This command works regardless of the format of the file- Secrets that are not managed by `secretcli` can be downloaded using this tool.

```bash
$ secretscli download TestSecret ./secret_configuration.json
```

The file can also be uploaded- but be careful, it will be uploaded exactly as is without any verification of the json formatting.

```bash
$ secretscli upload TestSecret ./secret_configuration.json
```

## Datastore Format

`secretcli` stores data as a json object. It uses the `SecretString` field in the AWS Secrets Manager- saving it as a string allows the database to be viewed in the AWS Console.
