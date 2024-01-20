'''
An improved version of pybrick's drivebase module
'''

from pybricks.parameters import Stop
from pybricks.tools import wait
import math

# Time epsilon, in ms (very small value)
T_EPS = 10
'''Time epsilon, in ms (very small value)'''

class SpaceyDriveBase:
    '''An improved version of pybrick's drivebase module'''
    def __init__(self, L, R, wheel_d, track_b):
        '''
        Construct a drivebase.

        PARAMETERS
        L: Left motor (Motor)
        R: Right motor (Motor)
        wheel_d: Diameter of the wheel, in mm (int)
        track_b: Track base, in mm (int)

        '''
        self.motorL = L
        self.motorR = R

        # Wheel diameter
        self.whl_d = wheel_d

        # Track base
        self.trk_b = track_b

        # Wheel circumference
        self.whl_circ = wheel_d * math.pi

        # Track circle circumference
        self.trk_circ = track_b * math.pi
    
    def brake(self, stopMode=Stop.BRAKE):
        '''
        Stops the base.

        PARAMETERS
        stopMode: braking mode (Stop). If set to None, does not brake. Default is Stop.BRAKE.
        '''
        if stopMode == Stop.BRAKE:
            self.motorL.brake()
            self.motorR.brake()
        elif stopMode == Stop.COAST:
            self.motorL.stop()
            self.motorR.stop()
        elif stopMode == Stop.HOLD:
            self.motorL.hold()
            self.motorR.hold()
        elif stopMode == None:
            pass
        else:
            raise ValueError(stopMode + "is not an acceptable brake mode")

    def straight(self, speed, dist=None, stopMode=Stop.BRAKE):
        '''
        Go straight for a given distance at a given speed, and then stops.

        PARAMETERS
        speed: Linear speed, in mm/s (int)
        dist: Distance to travel, in mm (int). Default is None, which makes it go straight forever.
        stopMode: braking mode (Stop). If set to None, does not brake. Default is Stop.BRAKE.
        '''
        # Angular speed
        ang_spd = speed / self.whl_circ * 360

        # Specific target
        if dist:
            # Angular distance
            ang_dist = dist / self.whl_circ * 360

            self.motorL.run_angle(ang_spd, ang_dist, wait=False)
            self.motorR.run_angle(ang_spd, ang_dist)
            self.brake(stopMode)
        # Go forever
        else:
            self.motorL.run(ang_spd)
            self.motorR.run(ang_spd)


    def turn(self, speed, angle=None, stopMode=Stop.BRAKE):
        '''
        Turn for a given angle at a given angular speed, and then stops.

        PARAMETERS
        speed: Angular speed, in deg/s (int)
        angle: Angle to turn, in deg (int). Default is None, which makes it turn forever.
        stopMode: braking mode (Stop). If set to None, does not brake. Default is Stop.BRAKE.
        '''

        # Motor angular speed
        motor_ang_spd = (speed * self.trk_b) / self.whl_d

        # Specific target
        if angle:
            # Running distance
            dist = self.trk_circ * (angle / 360)

            # Angular distance
            ang_dist = dist / self.whl_circ * 360

            self.motorL.run_angle(motor_ang_spd, ang_dist, wait=False)
            self.motorR.run_angle(-motor_ang_spd, ang_dist)

            # Brake
            self.brake(stopMode)
        # Go forever
        else:
            self.motorL.run(motor_ang_spd)
            self.motorR.run(-motor_ang_spd)

    def lineup(self, speed, ang_speed, sensorL, sensorR, iterations=10, thres=30, timeout=10000):
        '''
        Line up on the edge of the field that the robot is facing at.

        PARAMETERS
        speed: Speed, in mm/s (int)
        ang_speed: Angular speed, in deg/s (int)
        sensorL: Left light sensor
        sensorR: Right light sensor
        iterations: Number of line-up iterations
        thres: threshold between field and edge
        timeout: timeout, in ms
        '''

        case_count = 0
        case_num = 4
        last_case_num = 4

        while case_count < iterations:
            L_on_edge = sensorL.reflection() < thres
            R_on_edge = sensorR.reflection() < thres

            if case_num != last_case_num:
                case_count += 1
                last_case_num = case_num
                self.brake()

            # Robot fully out of field
            if L_on_edge and R_on_edge:
                self.straight(-speed)
                case_num = 1
            # Robot tilted right
            elif L_on_edge:
                self.turn(-ang_speed)
                case_num = 2
            # Robot tilted left
            elif R_on_edge:
                self.turn(ang_speed)
                case_num = 3
            # Robot fully in field
            else:
                self.straight(speed)
                case_num = 4

        self.brake()

    def lineside(self, speed, sensorL, sensorR, is_left, bias=30, thres=30):
        '''
        Line up the the side of the stage and move forward an infintesimal step aligned with it

        PARAMETERS
        speed: Speed, in mm/s (int)
        sensorL: Left light sensor
        sensorR: Right light sensor
        bias: Difference between left and right motor linear speeds (mm/s)
        timeout: timeout, in ms
        thres: threshold of the stage edge between two sensors
        '''
        # Original angular speed
        ang_spd_orig = speed / self.whl_circ * 360
        # Lower angular speed
        ang_spd_slower = (speed - bias) / self.whl_circ * 360

        # Sensor values
        Lvalue = sensorL.reflection()
        Rvalue = sensorR.reflection()

        # If one side of the robot is off the field
        if (abs(Lvalue - Rvalue) > thres):
            if is_left:
                self.motorL.run(ang_spd_orig)
                self.motorR.run(ang_spd_slower)
            else:
                self.motorL.run(ang_spd_slower)
                self.motorR.run(ang_spd_orig)
        else:
            if is_left:
                self.motorL.run(ang_spd_slower)
                self.motorR.run(ang_spd_orig)
            else:
                self.motorL.run(ang_spd_orig)
                self.motorR.run(ang_spd_slower)

        


    def straight_until_line(self, speed, sensorL, sensorR):
        '''
        Go straight until a black line is sensed

        PARAMETERS
        speed: Speed, in mm/s (int)
        sensorL: Left light sensor
        sensorR: Right light sensor
        timeout: timeout, in ms
        '''

        # Take mean measurement of light value on the table
        table_light = (sensorL.reflection() + sensorR.reflection()) / 2

        # Stop line threshold
        STOP_LINE_THRES = 40

        # Go until black line
        while (sensorL.reflection() + sensorR.reflection()) / 2 > table_light - STOP_LINE_THRES:
            self.lineside(speed, sensorL, sensorR, True)

        # Stop at black line
        self.brake(Stop.BRAKE)
        wait(2000)
