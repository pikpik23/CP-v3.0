#!/bin/bash

git init
git config core.sparseCheckout true

# add remote
git remote add -f limited_origin git@github.com:pikpik23/Google-API-Experiments

# Add files to be downloaded
echo "GUI_Test/" >> .git/info/sparse-checkout
echo "pi_files/" >> .git/info/sparse-checkout

git pull limited_origin main
