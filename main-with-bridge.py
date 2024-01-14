from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial
import sys

from crsf_parser.payloads import PacketsTypes
import sys
from typing import Container

from serial import Serial

from crsf_parser import CRSFParser, PacketValidationStatus
from crsf_parser.payloads import PacketsTypes

baud = 425000  #420000?
if len(sys.argv) > 1:
    baud = sys.argv[1]

size = 100
if len(sys.argv) > 2:
    size = int(sys.argv[2])

oldChannels = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def print_frame(frame: Container, status: PacketValidationStatus) -> None:
    if status != PacketValidationStatus.VALID:
        print("invalid pocket")
        return
    if frame.header.type != PacketsTypes.RC_CHANNELS_PACKED:
        return

    channels = frame.payload.channels

    if (oldChannels[0] == channels[0] and
            oldChannels[1] == channels[1] and
            oldChannels[2] == channels[2] and
            oldChannels[3] == channels[3] and
            oldChannels[4] == channels[4] and
            oldChannels[5] == channels[5] and
            oldChannels[6] == channels[6] and
            oldChannels[7] == channels[7] and
            oldChannels[8] == channels[8] and
            oldChannels[9] == channels[9] and
            oldChannels[10] == channels[10] and
            oldChannels[11] == channels[11] and
            oldChannels[12] == channels[12] and
            oldChannels[13] == channels[13] and
            oldChannels[14] == channels[14] and
            oldChannels[15] == channels[15]):
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

with Serial("/dev/ttyS0", baud, timeout=1) as ser:
    inputByteArray = bytearray()
    while True:
        values = ser.read(size)
        print("values: ", len(values))
        ser.write(values)
        print("inputByteArray b: ", len(inputByteArray))
        inputByteArray.extend(values)
        print("inputByteArray a: ", len(inputByteArray))
        crsf_parser.parse_stream(inputByteArray)
        print("inputByteArray aa: ", len(inputByteArray))


