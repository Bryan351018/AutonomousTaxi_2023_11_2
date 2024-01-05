'''
All devices used by the robot
'''

from pybricks.ev3devices import Motor, GyroSensor, ColorSensor
from pybricks.parameters import Port
from spacey_drivebase import SpaceyDriveBase

# Arm motor
arm = Motor(Port.C)

# Left wheel motor
MotorL = Motor(Port.A)

# Right wheel motor
MotorR = Motor(Port.D)

# Wheel diameter (mm)
WHEEL_D = 43

# Track base (mm)
TRACK_B = 95

# Drivebase
base = SpaceyDriveBase(MotorL, MotorR, WHEEL_D, TRACK_B)

# Left light sensor
LightL = ColorSensor(Port.S1)

# Right light sensor
LightR = ColorSensor(Port.S2)
