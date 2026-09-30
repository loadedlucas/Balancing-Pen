from time import sleep
import RPi.GPIO as GPIO
from MotorHelper import spin



DIR = 20
STEP = 21
CW = 0
CCW = 1
SPR = 200 # Steps per revlution (360 / 1.8 = 200)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CCW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {
    "Full": (0, 0, 0),
    "Half": (1, 0, 0),
    "1/4": (0, 1, 0),
    "1/8": (1, 1, 0),
    "1/16": (0, 0, 1),
    "1/32": (1, 0, 1)
    }
GPIO.output(MODE, RESOLUTION["1/4"])

for i in range(50):
    spin(160, CW, STEP, DIR)
    sleep(0.2)
    spin(160, CCW, STEP, DIR)
    sleep(0.2)
