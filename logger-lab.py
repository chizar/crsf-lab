#!/usr/bin/env python3

import argparse
import time
from threading import Thread

from asciimatics.screen import Screen
from serial import Serial

import dashboard_lines
from parse_frame import extract_frame, parse_channels_frame
from crc import frame_crc

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=425000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=200, type=int)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)
args = parser.parse_args()

SYNC_BYTE = 0xC8
FRAME_TYPE_RC_CHANNELS_PACKED = 0x16

serial_iterations = 0
last_channels_frame = bytearray()
last_frame_type = 0
total_frames = 0
last_read_size = 0
last_rest_size = 0
last_actual_frame_size = 0


def monitor_serial():
    global args, serial_iterations, total_frames, last_read_size, last_rest_size, last_actual_frame_size, last_channels_frame, last_frame_type
    values_rest = b""

    with Serial(args.port, args.baud, timeout=args.timeout) as ser:

        while True:
            serial_iterations += 1

            read_values = ser.read(args.serialsize)
            last_read_size = len(read_values)
            last_rest_size = len(values_rest)

            values = values_rest + read_values
            values_rest = b""

            pos = 0
            for byte in values:
                if byte == SYNC_BYTE:
                    frame, values_rest = extract_frame(values, pos)
                    if frame is not None:
                        total_frames += 1
                        if frame[1] > 1:  # size is greater than 1
                            last_frame_type = frame[2]
                            if last_frame_type == FRAME_TYPE_RC_CHANNELS_PACKED:
                                last_channels_frame = frame
                pos += 1


def dashboard(screen):
    global args, serial_iterations, total_frames, last_read_size, last_actual_frame_size, last_channels_frame, last_frame_type
    dashboard_iterations = 0
    crc_errors = 0
    while True:
        dashboard_iterations += 1
        local_last_channels_frame = last_channels_frame
        len_local_last_channels_frame = len(local_last_channels_frame)

        if len_local_last_channels_frame > 0:
            sync_byte, length, crc, channels = parse_channels_frame(local_last_channels_frame)
            actual_crc = frame_crc(local_last_channels_frame)
            if actual_crc != crc:
                crc_errors += 1

            if len(channels) == 16:
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
                                , 0, dashboard_lines.DASHBOARD_CHANNELS_LINE)

            screen.print_at(f'last sync byte: {sync_byte}', 0, dashboard_lines.DASHBOARD_LAST_SYNC_BYTE)
            screen.print_at(f'last payload length: {length}', 0, dashboard_lines.DASHBOARD_LAST_PAYLOAD_LENGTH)
            screen.print_at(f'last crc: {crc}', 0, dashboard_lines.DASHBOARD_LAST_CRC)

        screen.print_at(f'serial iterations: {serial_iterations}', 0, dashboard_lines.DASHBOARD_SERIAL_ITERATIONS)
        screen.print_at(f'total frames: {total_frames}', 0, dashboard_lines.DASHBOARD_TOTAL_FRAMES)
        screen.print_at(f'last frame type: {last_frame_type}', 0, dashboard_lines.DASHBOARD_LAST_FRAME_TYPE)
        screen.print_at(f'dashboard iterations: {dashboard_iterations}', 0, dashboard_lines.DASHBOARD_ITERATIONS)
        screen.print_at(f'len(last_channels_frame): {len_local_last_channels_frame}',
                        0, dashboard_lines.DASHBOARD_LAST_CHANNELS_FRAME_LEN)
        screen.print_at(f'last read size: {last_read_size}', 0, dashboard_lines.DASHBOARD_LAST_READ_SIZE)
        screen.print_at(f'last rest size: {last_rest_size}', 0, dashboard_lines.DASHBOARD_LAST_REST_SIZE)
        screen.print_at(f'crc errors: {crc_errors}', 0, dashboard_lines.DASHBOARD_CRC_ERRORS)
        screen.refresh()
        time.sleep(0.100)


serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.start()

Screen.wrapper(dashboard)


