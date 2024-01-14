import sys

from serial import Serial

baud = 425000  #420000?
if len(sys.argv) > 1:
    baud = sys.argv[1]

size = 100
if len(sys.argv) > 2:
    size = int(sys.argv[2])

with Serial("/dev/ttyS0", baud, timeout=1) as ser:
    while True:
        values = ser.read(size)
        ser.write(values)
        print(len(values))
