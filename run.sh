#!/bin/sh
set -ev
read -r GH_ACCESS_TOKEN <<< $(bw list items --search 'github - PMArkive' | jq --raw-output '.[].fields[] | select(.name=="access token").value');
export GH_ACCESS_TOKEN

python3 forksyncer.py
