@echo off
set GH_ACCESS_TOKEN=
set ARK_META_REPO=../PMArkive
set ARK_STORAGE_DIR=../ark
:: the host in .ssh/config
set GITHUB_HOST=github_arkive
uv run forksyncer2.py
