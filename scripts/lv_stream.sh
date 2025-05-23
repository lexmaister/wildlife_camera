#!/bin/bash

echo "Starting Streaming Server"
rpicam-vid -t 0 -n --codec mjpeg --listen -o tcp://0.0.0.0:8888 || true && 
echo "Streaming Server Is Closed"

