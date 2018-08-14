#!/bin/bash

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk http://127.0.0.1:5000/ & export chropid=$!
osascript -e 'tell application "Google Chrome" to activate'