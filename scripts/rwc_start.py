#!/usr/bin/env python3
"""
The script to provide Raspberry Wildlife Camera functionality
"""

import os
from time import sleep
from datetime import datetime as dt
import argparse
from gpiozero import MotionSensor
from picamera2 import Picamera2


SNAPSHOT = 'snapshot'
CLIP = 'clip'





# def clip():
#     '''Take video clip and save to current session path'''
#     print('---> Start taking clip...')
#     video_config = picam2.create_video_configuration()
#     fn = f"vid_{dt.now()}.jpg"
#     picam2.capture_file(os.path.join(session_path, fn))
#     print(f'---> Shapshot is saved: {fn!r}')



class RWC:
    '''Class Raspberry Pi Wildlife Camera'''
    def __init__(self, mode: str, clip_duration: int):
        '''Init a Raspberry Pi Wildlife Camera class instance:
        
        Parameters:
            * mode(str): capture mode: snapshot or clip
            * clip_duration(int): desired video clip duration in seconds
        '''
        self.mode = mode
        self.clip_dur = clip_duration
        self.session_dir = self.make_session_dir()
        
        self.cam = Picamera2()
        if mode == SNAPSHOT:
            config = self.cam.create_still_configuration({"size": (2592,1944)})
        elif mode == CLIP:
            config = self.cam.create_video_configuration({"size": (1920,1080)})

        self.cam.configure(config)
        self.cam.start(show_preview=False)
        sleep(1)
        print('---> Camera is configured')

        self.pir = MotionSensor(
            pin=17, 
            queue_len=1, 
            sample_rate=1
        )
        print('---> PIR-sensor is configured on GPIO_17 pin')

    def make_session_dir(self) -> str:
        '''Create a directory to save grabbed images / clips
        
        Returns:
            * path to directory including './img/' base path
        '''
        if not os.path.exists('img'):
            os.mkdir('img')

        dt_start = dt.now().strftime('%Y-%m-%d_%H.%M.%S')
        session_dir = f'img/{dt_start}'
        if not os.path.exists(session_dir):
            os.mkdir(session_dir)

        print(f'---> Session directory: {session_dir}')
        return session_dir

    def get_free_space(self) -> int:
        '''Calculate free space in session directory
        
        Returns:
            * available space in megabytes
        '''
        stat = os.statvfs(self.session_dir)
        free_mb = (stat.f_bavail * stat.f_frsize) / 1024 / 1024
        print(f'---> Available space: {free_mb:.1f} Mb')
        return free_mb

    def snapshot(self):
        '''Take a snapshot and save to current session directory'''
        print('---> Start taking snapshot...')
        fn = f"img_{dt.now()}.jpg"
        self.cam.capture_file(os.path.join(self.session_dir, fn))
        print(f'---> Shapshot is saved: {fn!r}')

    def clip(self, bitrate=10000000):
        '''Take a clip and save to current session directory'''
        print('---> Start taking vlip...')
        fn = f"img_{dt.now()}.h264"
        encoder = H264Encoder(bitrate)
        self.cam.start_recording(encoder, os.path.join(self.session_dir, fn))
        sleep(self.clip_dur)
        self.cam.stop_recording()
        print(f'---> Clip is saved: {fn!r}')
    
    def run(self):
        '''Start the main loop'''
        while True:
            if self.pir.value > 0:
                if self.mode == SNAPSHOT:
                    self.snapshot()
                else:
                    self.clip()

                if self.get_free_space() < 100:
                    print('!!! STOP - not enough space to proceed grabbing !!!')
                    break
            else:
                sleep(1)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='rwc_start.py',
        description='Capture wonderful moments of life in the wild nature with Raspberry Pi Wildlife Camera',
        add_help=True
        )
    parser.add_argument(
        '-m', '--mode', 
        choices=[SNAPSHOT, CLIP], 
        default=CLIP,
        type=str,
        help='Capture mode [snapshot, clip], default: clip',
        metavar='MODE'
        )
    parser.add_argument(
        '-d', '--duration', 
        default=10,
        type=int,
        help='Clip duration in seconds, default: 10',
        metavar='N'
        )

    args = parser.parse_args()
    mode = args.mode
    clip_dur = args.duration
    print(f'---> Start with parameters: mode = {mode!r}, clip duration = {clip_dur}')

    rwc = RWC(mode=mode, clip_duration=clip_dur)
    rwc.run()