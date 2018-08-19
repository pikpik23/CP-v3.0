#!/bin/bash

git fetch limited_origin main

git reset FETCH_HEAD

git clean -df

sudo chmod 777 -R ./
