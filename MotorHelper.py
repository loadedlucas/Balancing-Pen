import RPi.GPIO as GPIO
from time import sleep

def spin(steps, direction, STEP_PIN, DIR_PIN):
    speed = 400 + 10 * steps
    MIN_DELAY = 1 / speed
    MAX_DELAY = MIN_DELAY * 3
    delay = MAX_DELAY
    j = 0
    GPIO.output(DIR_PIN, direction)
    for i in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        sleep(delay)
        if i <= steps / 4:
            delay = (4 * i / steps) * MIN_DELAY + (1 - (4 * i / steps)) * MAX_DELAY
        elif i >= 3 * steps / 4:
            delay = (1 - (4 * j / steps)) * MIN_DELAY + (4 * j / steps) * MAX_DELAY
            j += 1
    return