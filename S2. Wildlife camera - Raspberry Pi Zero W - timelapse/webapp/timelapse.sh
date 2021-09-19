#! /bin/bash

awb_value=$1
interval=$2
period=$3

now=$(date +"%T")
echo "Timelapse start: $now"

rm -r /home/pi/timelapse_img/* &&
# pkill -f app.py &&
# sudo ifconfig wlan0 down &&

raspistill -t $interval -tl $period -awb $awb_value -hf -vf -w 1920 -h 1080  -o /home/pi/timelapse_img/img_%06d.jpg &
pid=$!
wait $pid

now=$(date +"%T")
echo "Timelapse done: $now"

# sudo halt
