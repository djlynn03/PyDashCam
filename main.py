from pickle import FRAME
import cv2
import datetime
import time
from dtypes import *

VIDEO_LENGTH = 1 * 60 * 60 # 1 hour (3600 seconds)
FRAMERATE = 30 # Frames per second
# Video size should be 300-400 MB for 60 minutes at 30 fps for 640x480
# May need adjustment for different video size and framerate

vid = cv2.VideoCapture(0)

size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
result = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'MP4V'), FRAMERATE, size) # Result video

def save(frame_queue):
    result.write(frame_queue.dequeue())
    return result

buffer = FrameQueue(FRAMERATE * VIDEO_LENGTH) # Buffer queue to contain the last n frames, where n = framerate * video length

while vid.isOpened():
    ret, frame = vid.read()
    
    cv2.putText(frame, datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S"), (5, int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow('frame', frame)

    buffer.enqueue(frame)
    buffer.foreach(save(buffer))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# while not buffer.is_empty():
#     result.write(buffer.dequeue())
    
# vid.release()
# result.release()
# cv2.destroyAllWindows()