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
KEEP_TIME = 30 # 60 seconds
MAX_FOOTAGE_SIZE = 10 # in MB

MODE = ['DEBUG', 'PROD'][1]
RASPBERRY_PI_CONNECTED = MODE == 'PROD'
vehicle_on = Button(2)

def start_video():
    print("starting")
    vid = cv2.VideoCapture(0)

    size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result = cv2.VideoWriter('video/' + name + '.mp4', cv2.VideoWriter_fourcc(*'MP4V'), FRAMERATE, size) # Result video

    def save(frame_queue):
        result.write(frame_queue.dequeue())
        return result
    
    def stop():
        vid.release()
        print("stopping")
        return
    
    buffer = FrameQueue(FRAMERATE * VIDEO_LENGTH) # Buffer queue to contain the last n frames, where n = framerate * video length
    vehicle_on.when_deactivated = stop
    
    while vid.isOpened():
        ret, frame = vid.read()

        cv2.putText(frame, datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"), (5, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if MODE == 'DEBUG':
            cv2.imshow('frame', frame)

        buffer.enqueue(frame)
        buffer.foreach(save(buffer))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
        
        clean_files(KEEP_TIME, MAX_FOOTAGE_SIZE)

    # while not buffer.is_empty():
    #     result.write(buffer.dequeue())

    vid.release()
    result.release()
    
# Detect when the vehicle is running
if RASPBERRY_PI_CONNECTED:
    vehicle_on.when_activated = start_video(vehicle_on)
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