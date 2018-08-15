#!/bin/bash

cd ../

git read-tree -mu HEAD

git fetch --all
git reset --hard limited_origin/main


git remote update
git fetch limited_origin main

sudo chmod 777 -R ../../