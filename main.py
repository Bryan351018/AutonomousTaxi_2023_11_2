#!/usr/bin/env pybricks-micropython
from pybricks.media.ev3dev import SoundFile, Font
from pybricks.tools import wait
from devices import brick
from error_reporting import report
from pybricks.parameters import Color

# Time epsilon, in ms (very small value)
T_EPS = 10
'''Time epsilon, in ms (very small value)'''

try:
    from pybricks.parameters import Stop
    from barcode_scanner import BarCodeScanner, evalPassengerDest
    from devices import *

    # Set state of robotic arm
    def setArm(motor, activated):
        # Speed of the robotic arm
        ARM_SPEED = 3000

        # Target rotation angle
        TARGET_ANGLE = 90

        '''Set the state of the robotic arm. activated=True represents down, and activated=False represents up.'''
        # if activated:
        #     motor.run_target(ARM_SPEED, 0)
        # else:
        #     motor.run_target(ARM_SPEED, TARGET_ANGLE)
        if activated:
            motor.run_until_stalled(-ARM_SPEED, Stop.BRAKE)
        else:
            motor.run_until_stalled(ARM_SPEED, Stop.BRAKE)

    # Preload screen
    brick.light.on(Color.YELLOW)
    brick.speaker.beep(440, 100)
    brick.screen.draw_text(0, 0, "All Systems OK.")
    brick.screen.draw_text(0, 20, "Press any button")
    brick.screen.draw_text(0, 40, "to start.")
    while len(brick.buttons.pressed()) == 0:
        wait(T_EPS)
    brick.screen.clear()
    brick.screen.draw_text(0, 0, "Running.")
    brick.speaker.beep(880, 50)
    brick.light.on(Color.GREEN)


    # Reset arms
    setArm(BigArm, False)
    # setArm(SmallArm, False)

    # Barcode scanner object
    scanner = BarCodeScanner(LightL, LightR, base)

    # Base move and turn speeds
    BASE_SPD = 150
    BASE_TURN_SPD = 1000

    # Passenger 2 destination
    PASS_2_DEST = "A"

    # Passenger 3 destination
    pass_3_dest = ""

    # Set passenger 3 destination
    def set_dest(dest):
        global pass_3_dest
        pass_3_dest = dest

    bits = scanner.readbits(evalPassengerDest(set_dest))

    # Turn robot to the right
    base.turn(BASE_TURN_SPD, 90)

    # Line up at edge of table
    base.straight(BASE_SPD, 80, None)
    base.lineup(BASE_SPD/2, 50, LightL, LightR, iterations=8)

    # Turn right and go to black line, then get first passenger
    base.turn(BASE_TURN_SPD, 90)
    base.straight_until_line(BASE_SPD, LightL, LightR, True, BASE_SPD/6, end_callback=lambda:setArm(BigArm, True))
    base.turn(BASE_TURN_SPD, 10)

    # Drop first passenger
    base.straight(BASE_SPD, 460)
    base.lineup(BASE_SPD/2, 50, LightL, LightR, iterations=8)

    base.turn(BASE_TURN_SPD, 90)
    base.straight(BASE_SPD, 160)
    base.turn(BASE_TURN_SPD, -90)
    setArm(BigArm, False)
    base.straight(BASE_SPD, 80)
    base.straight(BASE_SPD, -80)

    # Go to other black line
    base.turn(BASE_TURN_SPD, 90)
    base.straight(BASE_SPD, 200)
    base.lineup(BASE_SPD/2, 50, LightL, LightR, iterations=8)
    base.turn(BASE_TURN_SPD, 90)
    base.straight_until_line(BASE_SPD, LightL, LightR, True, BASE_SPD/6, end_callback=lambda:setArm(BigArm, True))

    # Send passenger 2
    if PASS_2_DEST == "A":
        pass
    elif PASS_2_DEST == "B":
        pass
    elif PASS_2_DEST == "C":
        pass
    else:
        raise ValueError("Invalid passenger 2 destination \"" + PASS_2_DEST + "\"")
    
    # Go to location of passenger 3
    base.straight(BASE_SPD, 1150)
    base.lineup(BASE_SPD/2, 50, LightL, LightR, iterations=8)

    # Infinite pause to keep the program running
    while True:
        wait(T_EPS)
    

# Error reporting
except Exception as e:
    report(e, brick)
