'''
All devices used by the robot
'''

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor
from pybricks.media.ev3dev import Font
from pybricks.parameters import Port, Direction
from spacey_drivebase import SpaceyDriveBase
from error_reporting import report

# Brick
brick = EV3Brick()

# Catching device errors
def attempt_connect(device, port, positive_direction=Direction.CLOCKWISE):
    try:
        if device == Motor:
            return device(port, positive_direction)
        return device(port)
    except Exception as e:
        if device == Motor:
            device_type = "Motor"
        elif device == ColorSensor:
            device_type = "Color sensor"
        else:
            pass

        if port == Port.A:
            port_num = "Port A"
        elif port == Port.B:
            port_num = "Port B"
        elif port == Port.C:
            port_num = "Port C"
        elif port == Port.D:
            port_num = "Port D"
        elif port == Port.S1:
            port_num = "Port 1"
        elif port == Port.S2:
            port_num = "Port 2"
        elif port == Port.S3:
            port_num = "Port 3"
        elif port == Port.S4:
            port_num = "Port 4"
        else:
            pass

        report(device_type + " is not connected to " + port_num, brick)


# Arm motor
# arm = Motor(Port.C)

# Left wheel motor
MotorL = attempt_connect(Motor, Port.A)

# Right wheel motor
MotorR = attempt_connect(Motor, Port.D)

# Wheel diameter (mm)
WHEEL_D = 43

# Track base (mm)
TRACK_B = 95

# Drivebase
base = SpaceyDriveBase(MotorL, MotorR, WHEEL_D, TRACK_B)

# Big arm
BigArm = attempt_connect(Motor, Port.C, positive_direction=Direction.COUNTERCLOCKWISE)

# Small arm
# SmallArm = attempt_connect(Motor, Port.C, positive_direction=Direction.COUNTERCLOCKWISE)

# Left light sensor
LightL = attempt_connect(ColorSensor, Port.S1)

# Right light sensor
LightR = attempt_connect(ColorSensor, Port.S4)
