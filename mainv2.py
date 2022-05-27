import cv2
import datetime
import time
# from dtypes import *
from utils import *
from config import *
from gpiozero import Button
import io

from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
from threading import Thread

try:
    from signal import pause
except ImportError:
    print("signal is not installed or not supported on this platform")
    exit()

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as f:
            if ('raspberry' in str(f.read().lower())):
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
        
        self.vid = None
        self.result = None # Resulting video
        self.create_video() # Populates the result and vid variables
        
        self.trigger = trigger
        self.trigger.when_released = self.stop
        self.oldname = ""
        self.start_time = datetime.datetime.now()
        # used elapsed time instead of FPS because it's more accurate
        
        # TODO- make video record at 60 fps and edit later to make the video the correct length
        while self.vid.isOpened() and self.running and self.trigger.is_pressed:
            elapsed_start = datetime.datetime.now()
            self.ret, self.frame = self.vid.read()

            cv2.putText(self.frame, datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"), (5, int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Start new video if the current one has reached the maximum length
            if datetime.datetime.now() - self.start_time >= datetime.timedelta(seconds=VIDEO_LENGTH):
                print("Starting new video...")
                self.vid.release()
                self.result.release()
                
                # self.num_frames = 0
                self.start_time = datetime.datetime.now()
                clean_files(MAX_KEEP_TIME, MAX_FOOTAGE_SIZE)
                self.oldname = self.name
                self.create_video()
                print("New video created")
                thread = Thread(target=self.modify_video, args=(self.oldname, ))
                
                thread.start()
                thread.join()
                
                print("video normalized")
                continue
                
            self.result.write(self.frame)
                        

        self.vid.release()
        self.result.release()
    
    def stop(self):
        self.vid.release()
        print("stopping")
        self.running = False
        if REBOOT_ON_STOP:
            print("shutting down...")
            os.system("sudo shutdown now")
        return
    
    def create_video(self):
        self.vid = cv2.VideoCapture(-1) # -1 automatically selects the camera
        self.name = 'video/' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
        size = (VIDEO_WIDTH, VIDEO_HEIGHT) # default size is 640x480
        self.result = cv2.VideoWriter(self.name, cv2.VideoWriter_fourcc(*'mp4v'), FRAMERATE, size) # Result video
        
    def modify_video(self, video):
        clip = VideoFileClip(video)
        multiplier = clip.duration / VIDEO_LENGTH 
        clip = clip.set_fps(clip.fps * multiplier)
        final = clip.fx(vfx.speedx, multiplier)
        final.write_videofile(video)

vehicle_on = Button(3)
print("starting")
cap = Capture(vehicle_on)