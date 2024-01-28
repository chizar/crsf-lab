#!/usr/bin/env python3

import argparse
import time
from threading import Thread

from asciimatics.screen import Screen
from serial import Serial
from parse_frame import extract_frame

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=425000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=200, type=int)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)

args = parser.parse_args()

SYNC_BYTE = 0xC8
FRAME_SIZE = 26
FRAME_TYPE_RC_CHANNELS_PACKED = 0x16

iteration = 0


last_channels_frame = bytearray()
total_frames = 0
last_read_size = 0
last_actual_frame_size = 0


def monitor_serial():
    global args, iteration, total_frames, last_read_size, last_actual_frame_size, last_channels_frame
    values_rest = b""

    with Serial(args.port, args.baud, timeout=args.timeout) as ser:

        while True:
            iteration += 1
            values = values_rest + ser.read(args.serialsize)
            values_rest = b""

            last_read_size = len(values)
            pos = 0
            for byte in values:
                if byte == SYNC_BYTE:
                    frame, values_rest = extract_frame(values, pos)
                    if frame is not None:
                        total_frames += 1
                        if frame[2] == FRAME_TYPE_RC_CHANNELS_PACKED:
                            last_channels_frame = frame
                pos += 1


def unpack(data, bitlen):
    mask = (1 << bitlen) - 1
    for chunk in zip(*[iter(data)] * bitlen):
        n = int.from_bytes(chunk, 'big')
        a = []
        for i in range(8):
            a.append(n & mask)
            n >>= bitlen
        yield from reversed(a)


def parse_channels(frame):
    sync_byte = frame[0]
    length = frame[1]
    frame_type = frame[2]  # 0x16 = channels

    payload = frame[3:25]
    swapped = payload[::-1]
    channels = unpack(swapped, 11)
    return [sync_byte, length, frame_type, list(channels)]


def dashboard(screen):
    global args, iteration, total_frames, last_read_size, last_actual_frame_size, last_channels_frame
    while True:
        if len(last_channels_frame) < 10:
            screen.print_at(f'len(last_channels_frame) is low', 0, 10)
        else:
            sync_byte, length, frame_type, channels = parse_channels(last_channels_frame)

            if len(channels) < 16:
                continue

            screen.print_at(f'CH01:{channels[0]:05d} '
                            f'CH02:{channels[1]:05d} '
                            f'CH03:{channels[2]:05d} '
                            f'CH04:{channels[3]:05d} '
                            f'CH05:{channels[4]:05d} '
                            f'CH06:{channels[5]:05d} '
                            f'CH07:{channels[6]:05d} '
                            f'CH08:{channels[7]:05d} '
                            f'CH09:{channels[8]:05d} '
                            f'CH10:{channels[9]:05d} '
                            f'CH11:{channels[10]:05d} '
                            f'CH12:{channels[11]:05d} '
                            f'CH13:{channels[12]:05d} '
                            f'CH14:{channels[13]:05d} '
                            f'CH15:{channels[14]:05d} '
                            f'CH16:{channels[15]:05d}'
                            , 0, 0)

            screen.print_at(f'last sync byte: {sync_byte:05d} ', 0, 1)
            screen.print_at(f'last payload length: {length:05d} ', 0, 2)
            screen.print_at(f'last frame type: {frame_type:05d} ', 0, 3)

        screen.refresh()
        time.sleep(0.100)


serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.start()

Screen.wrapper(dashboard)


