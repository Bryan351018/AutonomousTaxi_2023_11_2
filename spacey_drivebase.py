'''
An improved version of pybrick's drivebase module
'''

from pybricks.parameters import Stop
import math

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

            self.motorL.run_angle(-motor_ang_spd, ang_dist, wait=False)
            self.motorR.run_angle(motor_ang_spd, ang_dist)

            # Brake
            self.brake(stopMode)
        # Go forever
        else:
            self.motorL.run(motor_ang_spd)
            self.motorR.run(motor_ang_spd)
