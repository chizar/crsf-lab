#!/usr/bin/env python3

import argparse

from serial import Serial

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=425000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=200, type=int)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)

args = parser.parse_args()

SYNC_BYTE = 0xC8
FRAME_SIZE = 26

iteration = 0
last_pos = 0

valuesRest = b""

with Serial(args.port, args.baud, timeout=args.timeout) as ser:
    inputByteArray = bytearray()
    total = 0
    while True:
        iteration += 1
        values = valuesRest + ser.read(args.serialsize)

        size = len(values)
        pos = 0
        for byte in values:
            if byte == SYNC_BYTE:

                frame = values[pos:pos + FRAME_SIZE]
                if len(frame) < FRAME_SIZE:
                    valuesRest = frame
                    continue

                frame_size = len(frame)
                last_pos = pos
                total += 1
                print(f'iteration {iteration:05d}; sync {total} found on {pos}, frame size {frame_size}, total size {size}')
                print(frame)
            pos += 1
