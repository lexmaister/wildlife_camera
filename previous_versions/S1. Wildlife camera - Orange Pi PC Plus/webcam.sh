#!/bin/bash

while true; do
    DATE=$(date +"%Y-%m-%d_%H:%M:%S")
    fswebcam -d /dev/video1 -r 1280x1024 /home/alex/webcam/img/img_$DATE.jpg
    sleep 6.5
done