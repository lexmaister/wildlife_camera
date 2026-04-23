#! /bin/bash

awb_value=$1
interval=$2
period=$3

now=$(date +"%T")
echo "Timelapse start: $now"

rm -rf /home/pi/timelapse_img/* &&
# pkill -f app.py &&
# sudo ifconfig wlan0 down &&

libcamera-still --awb $awb_value --width 2592 --height 1944 -t $interval --timelapse $period -o /home/pi/timelapse_img/img_%06d.jpg &
pid=$!
wait $pid

now=$(date +"%T")
echo "Timelapse done: $now"

# sudo halt
