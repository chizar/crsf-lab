import sys

from serial import Serial

baud = 425000  #420000?
if len(sys.argv) > 1:
    baud = sys.argv[1]

with Serial("/dev/ttyS0", baud, timeout=1) as ser:
    while True:
        values = ser.read(100)
        ser.write(values)
