'''
A barcode scanner
'''

from pybricks.tools import wait
from pybricks.parameters import Stop

# Width of each bar (mm)
BAR_WIDTH = 30

# Number of bars
BAR_COUNT = 3

# Reading speed (mm/s)
READ_SPD = 500

def noEscape(b):
    return False

class BarCodeScanner:
    '''
    A barcode scanner
    '''
    def __init__(self, L, R, B):
        '''
        Construct a barcode scanner.

        PARAMETERS
        L: Left sensor (ColorSensor)
        R: Right sensor (ColorSensor)
        B: The drivebase to control when reading bits (SpaceyDriveBase)
        '''
        self.Lsensor = L
        self.Rsensor = R
        self.base = B

        # Bits of the barcode. False = White = 0, True = Black = 1
        self.bits = []

    def readbits(self, quickescape=noEscape):
        '''
        Construct a barcode scanner.

        PARAMETERS
        quickescape: a function f(b) that takes an array of bits read as input, and returns a boolean value, when each bit is read. If quickescape returns False, the reading continues. Otherwise, the read stops.

        RETURN VALUE
        Array of bits read, where False = White = 0, True = Black = 1
        '''
        # Clear bits
        self.bits = []

        # Advance to first bit


        self.base.straight(READ_SPD, stopMode=None)

        # Take measurement of start line
        startLineRef = self.Lsensor.reflection()

        # Time epsilon, in ms (very small value)
        T_EPS = 10
        '''Time epsilon, in ms (very small value)'''

        # Threshold between start line and white bit (%)
        REF_THRES = 20

        # Threshold between white bit and black bit (%)
        BIT_REF_THRES = 60

        while startLineRef - self.Lsensor.reflection() < REF_THRES:
            wait(T_EPS)

        self.base.straight(READ_SPD, BAR_WIDTH / 2, stopMode=None)

        for i in range(BAR_COUNT):
            # Read a bit (using left sensor)
            ref = self.Lsensor.reflection()

            # Black bit
            if ref < 100 - REF_THRES - BIT_REF_THRES:
                self.bits.append(True)
            # White bit
            else:
                self.bits.append(False)

            # Drive forward a fixed step
            self.base.straight(READ_SPD, BAR_WIDTH, stopMode=None)

            if i > 0 and quickescape(self.bits):
                break

        return self.bits

# Passenger destination evaluation
def evalPassengerDest(receiver):
    def escape(bits):
        if len(bits) > 2:
            if bits[:2] == [False, False]:
                receiver("A")
                return True
            if bits[:2] == [True, False]:
                receiver("B")
                return True
            if bits[:2] == [True, True]:
                receiver("C")
                return True

            if bits == [False, True, False]:
                receiver("A")
                return True
            if bits == [False, True, True]:
                receiver("B")
                return True
        else:
            return False
            
    return escape
