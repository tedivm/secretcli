# secretcli

The secretcli project provides a simple to use command line interface to the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/). It is capable of uploading or downloading the entire secret as well as working with individual fields.

## Installing

This project is available on [pypi](https://pypi.org/project/secretcli/) and can be installed with pip.

`pip3 install secretcli`

## Usage

### Initializing a new Secret

New secrets are easy to initiate. This will create a new Secret in the AWS Secret Manager and store an empty javascript object as the first version.

```bash
$ secretcli init TestSecret
```

### Working with individual Keys

Additional Key/Value pairs can be added to the secret using a single command. Behind the scenes this downloads the existing database, updates it with the new key/value pair, and uploads it as the current version.

```bash
$ secretcli set TestSecret postgreshost 10.10.10.16
$ secretcli set TestSecret postgresuser postgres
$ secretcli set TestSecret postgrespassword super_secret_string
$ secretcli set TestSecret longstring "This is a string with spaces."
```

Retrieving values is just as simple. This can be useful when trying to use values in bash scripts.

```bash
$ secretcli get TestSecret postgreshost
10.10.10.16
$ secretcli get TestSecret postgresuser
postgres
$ secretcli get TestSecret postgrespassword
super_secret_string
```

Values can also be completely removed from the secret.

```bash
$ secretcli get TestSecret postgreshost
10.10.10.16
$ secretcli remove TestSecret postgreshost
$ secretcli get TestSecret postgreshost
```

To avoid passing the value directly into the console (potentially logging it in places like bash history) the `-s` flag can be passed and the value can be passed in interactively without displaying it.


```bash
$ secretcli set TestSecret postgrespassword -s
Value:
Repeat for confirmation:
$ secretcli get TestSecret postgrespassword
super_secret_string
```

### Working with entire Files

The entire Secret can be downloaded as a file. This command works regardless of the format of the file- Secrets that are not managed by `secretcli` can be downloaded using this tool.

```bash
$ secretcli download TestSecret ./secret_configuration.json
```

The file can also be uploaded- but be careful, it will be uploaded exactly as is without any verification of the json formatting.

```bash
$ secretcli upload TestSecret ./secret_configuration.json
```

## Datastore Format

`secretcli` stores data as a JSON Object in an attempt to be as interoperable as possible. Each `key` passed to `secretcli` is represented by a `key` in the JSON Object.

When storing in AWS Secret Manager `secretcli` uses the `SecretString` field in the AWS Secrets Manager. This allows the database to be viewed in the AWS Console both as a raw string and using the Key/Value table.
