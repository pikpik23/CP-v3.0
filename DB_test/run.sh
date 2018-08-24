#!/bin/bash

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk http://0.0.0.0:5000/ & export chropid=$!
osascript -e 'tell application "Google Chrome" to activate'