FRAMERATE = 25 # Frames per second
# This value is tricky because it is not always the same as the framerate of the camera
# The camera I am using is supposed to be 30 fps, but 15 fps is the number that records correctly

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
# Dimensions of the video

MAX_KEEP_TIME = 14 * 24 * 60 * 60 # 14 days (in seconds)
MAX_FOOTAGE_SIZE = 5000 # in MB

# Maximum footage length and size can be specified. Any footage older that X seconds or larger than Y MB will be deleted.
# Can be set to None to disable this feature.

VIDEO_LENGTH = 60 # 30 seconds (in seconds)
# Videos are recorded in chunks of X seconds so that there will be less storage overflow.

REBOOT_ON_STOP = True
# Reboot the machine when the vehicle turns off