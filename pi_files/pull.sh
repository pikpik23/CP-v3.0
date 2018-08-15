#!/bin/bash

cd ../
git read-tree -mu HEAD
git remote update
git fetch limited_origin main