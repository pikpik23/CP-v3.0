#!/bin/bash


#echo launching web server
#./app.py & 

#sleep 3

#echo launching Chrome
#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk --app=http://127.0.0.1:5000/

./app.py & export python=$!
sleep 3
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk=http://127.0.0.1:5000/ & export chropid=$!
osascript -e 'tell application "Google Chrome" to activate'
P2=$!
wait $P2
read -p "Press enter to kill"
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT