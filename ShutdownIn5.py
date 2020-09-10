#!/usr/bin/env python3
from gpiozero import Button, LED
from signal import pause
import os, sys

offGPIO = int(sys.argv[1]) if len(sys.argv) >= 2 else 5
holdTime = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
ledGPIO = int(sys.argv[3]) if len(sys.argv) >= 4 else 26

# the function called to shut down the RPI
def shutdown():
    os.system("sudo poweroff")


led = LED(ledGPIO)
led.on()
btn = Button(offGPIO,pull_up=True, hold_time=holdTime)
btn.when_held = shutdown
pause()    # handle the button presses in the background
