import logging
import time
from threading import Thread


def thread1_main():
    while True:
        print("thread 1")
        time.sleep(1)


def thread2_main():
    while True:
        print("thread 2")
        time.sleep(1)


thread1 = Thread(target=thread1_main, name="thread1_main")
thread1.start()

thread2 = Thread(target=thread2_main, name="thread2_main")
thread2.start()

time.sleep(100)

# logging.basicConfig(level=logging.INFO, filename="dashboard.log")
#
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
#
#
# logging.info(0x18)
# logging.info(abs(1000-5000))

# BYTES1 = b"\xC8\xC8"
# BYTES2 = b"\xCC\xCC"
#
# BYTES = BYTES1 + BYTES2
#
# print(BYTES)

# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument('-b', '--baud', default=1000, type=int, )
# parser.add_argument('-ss', '--serialsize', default=10, type=int)
# parser.add_argument('-bs', '--buffersize', default=256, type=int)
# args = parser.parse_args()
#
#
# print(args.baud)
# print(args.serialsize)
# print(args.buffersize)

# from construct import (BitsInteger, ByteSwapped, BitStruct, Array)
#
# channelsStructure = ByteSwapped(
#     BitStruct("channels" / Array(16, BitsInteger(11)))
# )
#
# # struct = channelsStructure.build({"channels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 99]})
# # print(struct)
#
# var1 = b'\x0fp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
# var2 = b'cp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
# data1 = channelsStructure.parse(var1)
# print(data1)
# data2 = channelsStructure.parse(var2)
# print(data2)


from crsf_parser.payloads import PacketsTypes
from crsf_parser import crsf_frame
from crsf_parser.handling import crsf_build_frame

# frame = crsf_build_frame(
#     PacketsTypes.RC_CHANNELS_PACKED,
#     {"channels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
# )
#
# data = crsf_frame.parse(frame)
# print(crsf_frame.header.data_offset)
# print(data, type(data))
# print(frame, len(frame), type(frame))
