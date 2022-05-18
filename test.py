from gpiozero import Button


def start():
    print("started")
    
def stop():
    print("stopped")

btn = Button(2)
btn.when_pressed = start
btn.when_released = stop
while True:
    pass