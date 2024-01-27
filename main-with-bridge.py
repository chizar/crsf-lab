#!/usr/bin/env python3

import sys
import argparse
from typing import Container

from serial import Serial

from crsf_parser import CRSFParser, PacketValidationStatus
from crsf_parser.payloads import PacketsTypes

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=1000, type=int)
parser.add_argument('-ss', '--serialsize', default=10, type=int)
parser.add_argument('-be', '--bridgeenabled', default=False, type=bool)
parser.add_argument('-v', '--verbose', default=False, type=bool)
parser.add_argument('-d', '--dump', default=False, type=bool)
parser.add_argument('-ls', '--logsensitivity', default=50, type=int)
parser.add_argument('-p', '--port', default="/dev/ttyS0", type=str)

args = parser.parse_args()

oldChannels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def print_frame(frame: Container, status: PacketValidationStatus) -> None:
    if status != PacketValidationStatus.VALID:
        return
    if frame.header.type != PacketsTypes.RC_CHANNELS_PACKED:
        return

    channels = frame.payload.channels

    if (abs(oldChannels[0] - channels[0]) < args.logsensitivity and
            abs(oldChannels[1] - channels[1]) < args.logsensitivity and
            abs(oldChannels[2] - channels[2]) < args.logsensitivity and
            abs(oldChannels[3] - channels[3]) < args.logsensitivity and
            abs(oldChannels[4] - channels[4]) < args.logsensitivity and
            abs(oldChannels[5] - channels[5]) < args.logsensitivity and
            abs(oldChannels[6] - channels[6]) < args.logsensitivity and
            abs(oldChannels[7] - channels[7]) < args.logsensitivity and
            abs(oldChannels[8] - channels[8]) < args.logsensitivity and
            abs(oldChannels[9] - channels[9]) < args.logsensitivity and
            abs(oldChannels[10] - channels[10]) < args.logsensitivity and
            abs(oldChannels[11] - channels[11]) < args.logsensitivity and
            abs(oldChannels[12] - channels[12]) < args.logsensitivity and
            abs(oldChannels[13] - channels[13]) < args.logsensitivity and
            abs(oldChannels[14] - channels[14]) < args.logsensitivity and
            abs(oldChannels[15] - channels[15]) < args.logsensitivity):
        return
    oldChannels[0] = channels[0]
    oldChannels[1] = channels[1]
    oldChannels[2] = channels[2]
    oldChannels[3] = channels[3]
    oldChannels[4] = channels[4]
    oldChannels[5] = channels[5]
    oldChannels[6] = channels[6]
    oldChannels[7] = channels[7]
    oldChannels[8] = channels[8]
    oldChannels[9] = channels[9]
    oldChannels[10] = channels[10]
    oldChannels[11] = channels[11]
    oldChannels[12] = channels[12]
    oldChannels[13] = channels[13]
    oldChannels[14] = channels[14]
    oldChannels[15] = channels[15]

    print(f'CH01:{channels[0]:05d} '
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
          f'CH16:{channels[15]:05d}')



crsf_parser = CRSFParser(print_frame)

with Serial(args.port, args.baud) as ser:
    while True:
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

