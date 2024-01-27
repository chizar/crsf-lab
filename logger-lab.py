#!/usr/bin/env python3

import argparse
import time
from threading import Thread

from asciimatics.screen import Screen
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


last_frame = bytearray()
total_frames = 0
last_read_size = 0
last_actual_frame_size = 0


def monitor_serial():
    global args, iteration, total_frames, last_read_size, last_actual_frame_size, last_frame
    values_rest = b""

    with Serial(args.port, args.baud, timeout=args.timeout) as ser:

        while True:
            iteration += 1
            values = values_rest + ser.read(args.serialsize)

            last_read_size = len(values)
            pos = 0
            for byte in values:
                if byte == SYNC_BYTE:

                    frame = values[pos:pos + FRAME_SIZE]
                    if len(frame) < FRAME_SIZE:
                        values_rest = frame
                        continue

                    last_actual_frame_size = len(frame)
                    total_frames += 1
                    # print(f'iteration {iteration:05d}; sync {total_frames} found on {pos}, '
                    #       f'frame size {last_actual_frame_size}, total size {last_read_size}')
                    # print(frame)
                    last_frame = frame
                pos += 1


def dashboard(screen):
    global args, iteration, total_frames, last_read_size, last_actual_frame_size, last_frame
    while True:
        screen.print_at(last_frame, 0, 0)
        screen.refresh()
        time.sleep(0.100)


serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.start()

Screen.wrapper(dashboard)


