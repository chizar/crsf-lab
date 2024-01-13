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
    print(
        f"""
    {status}
    {frame}
    """
    )


crsf_parser = CRSFParser(print_frame)
n = 10
v = 1
with Serial("/dev/ttyS0", baud, timeout=2) as ser:
    inputByteArray = bytearray()
    while True:
        # if n == 0:
        #     n = 10
        #     # frame = crsf_build_frame(
        #     #     PacketsTypes.BATTERY_SENSOR,
        #     #     {"voltage": v, "current": 1, "capacity": 100, "remaining": 100},
        #     # )
        #     # v += 1
        #     # ser.write(frame)
        # n = n - 1
        values = ser.read(100)
        inputByteArray.extend(values)
        crsf_parser.parse_stream(inputByteArray)