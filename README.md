fork syncing script

create a github Personal Access Token at https://github.com/settings/tokens with all permissions for "repo" and drop in into access_token.secret

this will probably start a lot of annoying workflow shit... there's no api call afaik to disable workflows on a repo so you probably want to work the repo AND THEN disable actions on the repo... https://github.com/EXAMPLE/REPO/settings/actions AND THEN run the script...

example:
```
$ python3 forksyncer.py
Emu-Docs syncing master. commits AHEAD by: 29. moving to master_20210224_204839
FormatMii syncing master. commits AHEAD by: 1. moving to master_20210224_204849
NTRViewer syncing master. commits AHEAD by: 16. moving to master_20210224_204954
SMEncounterRNGTool syncing master. commits AHEAD by: 244. moving to master_20210224_205110
swiss-gc-1 creating new branch gcloader-debug at 6fdb2f12fba87a1efbac7e3cd14c7e1b7ef54cce
swiss-gc-1 syncing master. commits behind by: 484
swiss-gc-1 creating new branch recent-list at ec4c7807abaa68103f86bb9a7ae6581ebadffb28
swiss-gc-1 creating new branch threadedfilecopy at cf8c4e065dcc7fd3cf171d2737fc2d517d38a96d
teakra syncing apbp-fix. commits behind by: 49
teakra syncing master. commits behind by: 48
tinke syncing master. commits behind by: 17
tinycrystal syncing master. commits behind by: 573
TriggersPC syncing master. commits behind by: 3
TWiLightMenu syncing master. commits behind by: 2496
TWiLightMenu creating new branch onends at 5251924fad56601f4c2f431261cc22a6edf96338
vfdump creating new branch experimental at 9dacd4119b51136976357dafe82d37449ab9fc85
wii-gc-adapter-inject syncing master. commits behind by: 10
XCI-Explorer syncing master. commits behind by: 29
xyzzy-mod syncing master. commits behind by: 7
yuzu syncing master. commits behind by: 7094
```