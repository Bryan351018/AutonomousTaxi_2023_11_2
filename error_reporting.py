'''
Reporting errors on the brick
'''

from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font
from pybricks.tools import wait
from pybricks.parameters import Color

def report(error, brick):
    brick.light.on(Color.RED)
    print(error)

    if isinstance(error, str):
        text = error
    else:
        text = str(error)

    WRAP_WIDTH = 46
    output = ""
    cur_wrap = 0
    cur_pos = 0

    for char in text:
        output += char

        if char == "\n":
            cur_wrap = 0
        else:
            cur_wrap += 1
        
        if cur_wrap >= WRAP_WIDTH and cur_pos + 1 <= len(text) - 1 and text[cur_pos + 1] != "\n":
            output += "\n"
            cur_wrap = 0
        
        cur_pos += 1

    brick.screen.set_font(Font(None, 3))
    brick.screen.print(output, end="")

    brick.speaker.play_notes(["A2/4", "D#3/4"], 60)

    # Time epsilon, in ms (very small value)
    T_EPS = 10

    # Infinite pause to keep the program running
    while True:
        wait(T_EPS)
