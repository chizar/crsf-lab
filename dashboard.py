#!/usr/bin/env python3

from random import randint
from threading import Thread
import sys
import argparse
from typing import Container

from serial import Serial

from crsf_parser import CRSFParser, PacketValidationStatus
from crsf_parser.payloads import PacketsTypes
from asciimatics.screen import Screen
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=425000, type=int)
parser.add_argument('-ss', '--serialsize', default=200, type=int)
parser.add_argument('-be', '--bridgeenabled', default=False, type=bool)
parser.add_argument('-v', '--verbose', default=False, type=bool)
parser.add_argument('-d', '--dump', default=False, type=bool)
parser.add_argument('-ls', '--logsensitivity', default=50, type=int)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)
args = parser.parse_args()

channels_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
running = True


def dashboard(screen):
    while True:

        screen.print_at(f'CH01:{channels_state[0]:05d} '
                        f'CH02:{channels_state[1]:05d} '
                        f'CH03:{channels_state[2]:05d} '
                        f'CH04:{channels_state[3]:05d} '
                        f'CH05:{channels_state[4]:05d} '
                        f'CH06:{channels_state[5]:05d} '
                        f'CH07:{channels_state[6]:05d} '
                        f'CH08:{channels_state[7]:05d} '
                        f'CH09:{channels_state[8]:05d} '
                        f'CH10:{channels_state[9]:05d} '
                        f'CH11:{channels_state[10]:05d} '
                        f'CH12:{channels_state[11]:05d} '
                        f'CH13:{channels_state[12]:05d} '
                        f'CH14:{channels_state[13]:05d} '
                        f'CH15:{channels_state[14]:05d} '
                        f'CH16:{channels_state[15]:05d}', 0, 0)

        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            global running
            running = False
            return

        screen.refresh()


def start_dashboard():
    Screen.wrapper(dashboard)


def update_state(frame: Container, status: PacketValidationStatus) -> None:
    if status != PacketValidationStatus.VALID:  # TODO update valid/invalid counters
        return
    if frame.header.type != PacketsTypes.RC_CHANNELS_PACKED:  # TODO update types counters
        return

    global channels_state
    channels_state = frame.payload.channels


def monitor_serial():
    crsf_parser = CRSFParser(update_state)

    with Serial(args.port, args.baud) as ser:
        while True:

            global running
            if not running:
                return

            values = ser.read(args.serialsize)

            if args.bridgeenabled:
                ser.write(values)

            buffer = bytearray(values)

            if args.dump:
                print(values)
                print(buffer)

            crsf_parser.parse_stream(buffer)

            if args.verbose:
                stats = crsf_parser.get_stats()
                print("stats: ", stats)


dashboard_thread = Thread(target=start_dashboard, name="dashboard")
dashboard_thread.run()

serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.run()
