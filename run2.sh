#!/bin/sh
set -ev
read -r GH_ACCESS_TOKEN <<< $(bw list items --search 'github - PMArkive' | jq --raw-output '.[].fields[] | select(.name=="access token").value');
export GH_ACCESS_TOKEN
export ARK_META_REPO="../PMArkive"
export ARK_STORAGE_DIR="../ark"
export GIT_SSH="ssh -i ~/.ssh/id_ed25519_arkive"

python3 forksyncer2.py
