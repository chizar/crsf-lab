import sys
import argparse

from serial import Serial

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=1000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=10, type=int)

args = parser.parse_args()

SYNC_BYTE = 0xC8

with Serial("/dev/ttyS0", args.baud, timeout=args.timeout) as ser:
    inputByteArray = bytearray()
    while True:
        values = ser.read(args.serialsize)
        for byte in values:
            if byte == SYNC_BYTE:
                print("GOT SYNC BYTE")