@echo off
set GH_ACCESS_TOKEN=
set ARK_META_REPO=../PMArkive
set ARK_STORAGE_DIR=../ark
set GIT_SSH=ssh -i %USERPROFILE%/.ssh/id_ed25519_arkive

python.exe forksyncer2.py
