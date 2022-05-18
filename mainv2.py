import cv2
import datetime
import time
from dtypes import *
import os
from utils import *
from gpiozero import Button

VIDEO_LENGTH = 1 * 60 * 60 # 1 hour (3600 seconds)
FRAMERATE = 30 # Frames per second
# Video size should be 300-400 MB for 60 minutes at 30 fps for 640x480
# May need adjustment for different video size and framerate

# KEEP_TIME = 14 * 24 * 60 * 60 # 14 days (in seconds)
KEEP_TIME = 600 # 60 seconds
MAX_FOOTAGE_SIZE = 100 # in MB

MODE = ['DEBUG', 'PROD'][1]
RASPBERRY_PI_CONNECTED = MODE == 'PROD'


class Capture:
    def __init__(self, trigger: Button):
        self.running = True
        self.vid = cv2.VideoCapture(-1)
        self.size = (int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.result = cv2.VideoWriter('video/' + self.name + '.mp4', cv2.VideoWriter_fourcc(*'MP4V'), FRAMERATE, self.size) # Result video
        self.buffer = FrameQueue(FRAMERATE * VIDEO_LENGTH) # Buffer queue to contain the last n frames, where n = framerate * video length
        self.trigger = trigger
        trigger.when_released = self.stop
        
        while self.vid.isOpened() and self.running:
            self.ret, self.frame = self.vid.read()

            cv2.putText(self.frame, datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"), (5, int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            if MODE == 'DEBUG':
                cv2.imshow('frame', self.frame)

            self.buffer.enqueue(self.frame)
            self.buffer.foreach(self.save())
            if not RASPBERRY_PI_CONNECTED:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            print("running")
            
        # clean_files(KEEP_TIME, MAX_FOOTAGE_SIZE)

        # while not buffer.is_empty():
        #     result.write(buffer.dequeue())

        self.vid.release()
        self.result.release()

    def save(self):
        self.result.write(self.buffer.dequeue())
        return self.result
    
    def stop(self):
        self.vid.release()
        print("stopping")
        self.running = False
        return

vehicle_on = Button(2)
global cap 
cap = None

def start_video():
    print("starting")
    global cap
    cap = Capture(vehicle_on)

def stop_video():
    print("stopping")
    global cap
    del cap
    
# Detect when the vehicle is running
if RASPBERRY_PI_CONNECTED:
    vehicle_on.when_pressed = start_video
    vehicle_on.when_released = stop_video
    while True:
        pass
else:
    while True:
        print("waiting")
        cv2.waitKey(0)
        print("started")
        start_video()
    # vehicle_on.when_activated = set_state("RUNNING")
    
    # vehicle_on.when_deactivated = set_state("IDLE")
if RASPBERRY_PI_CONNECTED:
    cv2.destroyAllWindows()