import cv2
import datetime
from dtypes import *
from utils import *
from gpiozero import Button
import io

try:
    from signal import pause
except ImportError:
    print("signal is not installed or not supported on this platform")
    exit()

FRAMERATE = 15 # Frames per second
# This value is tricky because it is not always the same as the framerate of the camera
# The camera I am using is supposed to be 30 fps, but 15 fps is the number that records correctly

VIDEO_LENGTH = None # in seconds
# Can be used to specify the maximum length of a single video. If a video is recorded longer than this, only the last X seconds will be saved.

MAX_KEEP_TIME = 14 * 24 * 60 * 60 # 14 days (in seconds)
MAX_FOOTAGE_SIZE = 1000 # in MB
# Maximum footage length and size can be specified. Any footage older that X seconds or larger than Y MB will be deleted.
# Can be set to None to disable this feature.

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as f:
            if 'raspberrypi' in f.read().lower():
                return True
    except Exception:
        pass
    return False

RASPBERRY_PI_CONNECTED = is_raspberrypi()

if not RASPBERRY_PI_CONNECTED:
    print("This script is only compatible with Raspberry Pi")
    exit()
    
class Capture:
    def __init__(self, trigger: Button):
        self.running = True
        
        self.vid = cv2.VideoCapture(-1) # -1 automatically selects the camera
        
        
        self.name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.size = (int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))) # default size is 640x480

        self.result = cv2.VideoWriter('video/' + self.name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), FRAMERATE, self.size) # Result video
        
        self.buffer = None
        if VIDEO_LENGTH:
            self.buffer = FrameQueue(FRAMERATE * VIDEO_LENGTH) # Buffer queue to contain the last n frames, where n = framerate * video length
            
        self.trigger = trigger
        self.trigger.when_released = self.stop
        
        while self.vid.isOpened() and self.running and self.trigger.is_pressed:
            self.ret, self.frame = self.vid.read()

            cv2.putText(self.frame, datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"), (5, int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            if self.buffer:
                self.buffer.enqueue(self.frame)
                self.buffer.foreach(self.save())
            else:
                self.result.write(self.frame)

            
        clean_files(MAX_KEEP_TIME, MAX_FOOTAGE_SIZE)

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

# def stop_video():
#     print("stopping")
#     global cap
#     if cap:
#         cap.stop()
    
# Detect when the vehicle is running
if RASPBERRY_PI_CONNECTED:
    vehicle_on.when_pressed = start_video
    # vehicle_on.when_released = stop_video
    pause()
else:
    while True:
        print("waiting")
        cv2.waitKey(0)
        print("started")
        start_video()
    # vehicle_on.when_activated = set_state("RUNNING")
    
    # vehicle_on.when_deactivated = set_state("IDLE")
# if RASPBERRY_PI_CONNECTED:
#     cv2.destroyAllWindows()