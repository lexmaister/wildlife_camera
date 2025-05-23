#!/usr/bin/env python3

from gpiozero import MotionSensor

pir = MotionSensor(17)
print('Activated PIR sensor on GPIO_17 pin, wait for motion...')
pir.wait_for_motion()
print("Motion detected!")
