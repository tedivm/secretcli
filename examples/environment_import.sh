#!/usr/bin/env bash

# This script loads all key/value pairs. Using a bash shell and running `source ./environment_import.sh SECRET_NAME`
# will make the Secret values available as environmental variables.

for x in $(secretcli list $1); do
  VALUE=$(secretcli get $1 $x)
  export $x="$VALUE"
done
