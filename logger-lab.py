#!/usr/bin/env python3

import argparse
from threading import Thread
import time

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

valuesRest = b""

last_frame = bytearray()
total_frames = 0
last_read_size = 0
last_actual_frame_size = 0


def monitor_serial():
    global args, iteration, total_frames, last_read_size, last_actual_frame_size, last_frame

    with Serial(args.port, args.baud, timeout=args.timeout) as ser:

        while True:
            iteration += 1
            values = valuesRest + ser.read(args.serialsize)

            last_read_size = len(values)
            pos = 0
            for byte in values:
                if byte == SYNC_BYTE:

                    frame = values[pos:pos + FRAME_SIZE]
                    if len(frame) < FRAME_SIZE:
                        valuesRest = frame
                        continue

                    last_actual_frame_size = len(frame)
                    total_frames += 1
                    # print(f'iteration {iteration:05d}; sync {total} found on {pos}, frame size {frame_size}, total size {size}')
                    # print(frame)
                    last_frame = frame
                pos += 1


serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.start()

time.sleep(10_000)
