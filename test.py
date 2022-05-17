from gpiozero import Button


def start():
    print("started")
    
def stop():
    print("stopped")

btn = Button(2)
btn.when_activated = start
btn.when_deactivated = stop