#!/usr/bin/env python3

import argparse
import logging
import time
from threading import Thread
from typing import Container

from asciimatics.screen import Screen
from serial import Serial

from crsf_parser import CRSFParser, PacketValidationStatus
from crsf_parser.payloads import PacketsTypes

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=425000, type=int)
parser.add_argument('-ss', '--serialsize', default=100, type=int)
parser.add_argument('-be', '--bridgeenabled', default=False, type=bool)
parser.add_argument('-v', '--verbose', default=False, type=bool)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)
parser.add_argument('-ll', '--loglevel', default=20, type=int, help="default INFO = 20, ERROR = 40, WARN = 30, DEBUG = 10")
parser.add_argument('-lf', '--logfile', default="dashboard.log", type=str)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel, filename=args.logfile, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s]')

channels_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
running = True

def dashboard(screen):
    refresh_count = 0
    while True:
        refresh_count += 1
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
                        f'CH16:{channels_state[15]:05d} '
                        f'r:{refresh_count:5d} '
                        , 0, 0)

        global running

        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            running = False
            return

        if not running:
            return

        screen.refresh()
        # time.sleep(0.100)


def update_state(frame: Container, status: PacketValidationStatus) -> None:
    if status != PacketValidationStatus.VALID:  # TODO update valid/invalid counters
        return
    if frame.header.type != PacketsTypes.RC_CHANNELS_PACKED:  # TODO update types counters
        return

    global channels_state
    channels_state = frame.payload.channels


def monitor_serial():
    try:
        logging.info("Start serial thread")
        crsf_parser = CRSFParser(update_state)
        with Serial(args.port, args.baud) as ser:
            logging.info(f'Opened serial {args.port} at baud {args.baud}')
            while True:

                global running
                if not running:
                    return

                values = ser.read(args.serialsize)

                if args.bridgeenabled:
                    ser.write(values)

                buffer = bytearray(values)

                logging.debug('buffer {}', buffer)

                crsf_parser.parse_stream(buffer)

                # if args.verbose:
                #     stats = crsf_parser.get_stats()
                #     logging.info("stats: ", stats)

    except Exception:
        running = False
        logging.exception("error in monitor serial thread")


logging.info("Starting...")
serial_thread = Thread(target=monitor_serial, name="serial")
serial_thread.start()

Screen.wrapper(dashboard)

logging.info("Shutdown...")
serial_thread.join(10)
logging.info("Bye-bye")
exit(0)
