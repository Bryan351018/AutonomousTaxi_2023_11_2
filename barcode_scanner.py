'''
A barcode scanner
'''

# Width of each bar
BAR_WIDTH = 3

# Number of bars
BAR_COUNT = 3

# Reading speed (mm/s)
READ_SPD = 50

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

        for i in range(BAR_COUNT):
            # Read a bit (using left sensor)
            # TBD

            # Drive forward a fixed step
            self.base.straight(READ_SPD, BAR_WIDTH)

            if i > 0 and quickescape(self.bits):
                break

        return self.bits
