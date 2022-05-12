# PyDashCam
Dash cam software for a Raspberry Pi with a webcam
Should be compatible with most USB webcams

# Features
- Displays date and time in the video
- Captures the last 60 minutes of video while the program is running (can be changed as needed). Please note that you will need more storage space based on the framerate, video length, and frame dimensions
- This program is designed to be run when the Raspberry Pi turns on. The video is continuously saved as the program runs. If the Raspberry Pi turns off for any reason, the video will be saved, even if the video has not yet reached the maximum length.