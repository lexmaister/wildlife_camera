#! /bin/bash

awb_value=$1

now=$(date +"%T")
echo "Snapshot start: $now"

raspistill -awb $awb_value -vf -hf -w 1280 -h 720 -o /home/pi/webapp/static/img/snapshot.jpg &
pid=$!
wait $pid

now=$(date +"%T")
echo "Snapshot done: $now"