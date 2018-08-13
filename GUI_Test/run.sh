#!/bin/bash


#echo launching web server
#./app.py & 

#sleep 3

#echo launching Chrome
#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk --app=http://127.0.0.1:5000/

./app.py &
P1=$!
sleep 3
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://127.0.0.1:5000/ &
P2=$!
wait $P2
kill $P1