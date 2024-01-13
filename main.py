from operator import contains
from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial
import sys

from crsf_parser.payloads import PacketsTypes
from crsf_parser.handling import crsf_build_frame


baud = 425000  #420000?
if len(sys.argv) > 1:
    baud = sys.argv[1]

def print_frame(frame: Container, status: PacketValidationStatus) -> None:
    if status != PacketValidationStatus.VALID:
        return
    if frame.header.type != PacketsTypes.RC_CHANNELS_PACKED:
        return

    channels = frame.payload.channels

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

with Serial("/dev/ttyS0", baud) as ser:
    inputByteArray = bytearray()
    while True:
        values = ser.read(100)
        inputByteArray.extend(values)
        crsf_parser.parse_stream(inputByteArray)
