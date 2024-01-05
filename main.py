#!/usr/bin/env pybricks-micropython
from pybricks.media.ev3dev import SoundFile
from pybricks.parameters import Stop
from pybricks.tools import wait
from devices import *
from barcode_scanner import BarCodeScanner


# def setArm(activated):
#     # Speed of the robotic arm
#     ARM_SPEED = 3000

#     # Target rotation angle
#     TARGET_ANGLE = 135

#     '''Set the state of the robotic arm. activated=True represents down, and activated=False represents up.'''
#     if activated:
#         arm.run_target(ARM_SPEED, TARGET_ANGLE)
#     else:
#         arm.run_target(ARM_SPEED, 0)

# setArm(True)
# wait(3000)
# setArm(False)

try:

    # Barcode scanner object
    scanner = BarCodeScanner(LightL, LightR, base)

    # Time epsilon, in ms (very small value)
    T_EPS = 10
    '''Time epsilon, in ms (very small value)'''

    bits = scanner.readbits()

    for bit in bits:
        if bit:
            brick.speaker.play_notes(["F4/4", "A4/4", "B4/4", "D5/4"], tempo=200)
        else:
            brick.speaker.play_notes(["E4/4", "G4/4", "B4/4", "E5/4"], tempo=200)

    # Infinite pause to keep the program running
    while True:
        wait(T_EPS)
except:
    brick.speaker.play_file(SoundFile.ERROR)
