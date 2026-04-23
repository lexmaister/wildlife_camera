#! /bin/bash

awb_value=$1

now=$(date +"%T")
echo "Snapshot start: $now"

libcamera-still --awb $awb_value --width 1280 --height 720 -o /home/pi/webapp/static/img/snapshot.jpg &
pid=$!
wait $pid

now=$(date +"%T")
echo "Snapshot done: $now"
