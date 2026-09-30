from time import sleep
import pigpio

DIR = 20
STEP = 21

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set duty cycle frequency
pi.set_PWM_dutycycle(STEP, 128) # 128 means 50% on 50% off
pi.set_PWM_frequency(STEP, 500) # 500 pulses per second


def generate_ramp(ramp):
    # ramp is a list of lists of [Frequency, Steps]
    pi.wave_clear() # Clear existing waves
    length = len(ramp) # Number of ramp levels
    wid = [-1] * length
    
    # Generate wave per ramp level
    for i in range(length):
        frequency = ramp[i][0]
        micros = int(500000 / frequency)
        wf = []
        wf.append(pigpio.pulse(1 << STEP, 0, micros)) # Pulse on
        wf.append(pigpio.pulse(0, 1 << STEP, micros)) # Pulse off
        pi.wave_add_generic(wf)
        wid[i] = pi.wave_create()
    
    # Generate a chain of waves
    chain = []
    for i in range(length):
        steps = ramp[i][1]
        x = steps & 255
        y = steps >> 8
        chain += [255, 0, wid[i], 255, 1, x, y]
        
    pi.wave_chain(chain)
    
try:
    old_ramp = 0
    while True:
        new_ramp = pi.read(SWITCH)

# This file is not done yet, we had to abandon this idea for now, because it is time based, not distance/angle based