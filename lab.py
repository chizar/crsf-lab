import logging
import time
from threading import Thread
from construct import (
    Array,
    BitStruct,
    BitsInteger,
    ByteSwapped
)
#
# GPS = 0x02
# BATTERY_SENSOR = 0x08
# HEARTBEAT = 0x0B
# VIDEO_TRANSMITTER = 0x0F
# LINK_STATISTICS = 0x14
# RC_CHANNELS_PACKED = 0x16
# ATTITUDE = 0x1E
# print(GPS)
# print(BATTERY_SENSOR)
# print(HEARTBEAT)
# print(VIDEO_TRANSMITTER)
# print(LINK_STATISTICS)
# print(RC_CHANNELS_PACKED)
# print(ATTITUDE)

#
# payload_rc_channels_packed = ByteSwapped(
#     BitStruct("channels" / Array(16, BitsInteger(11)))
# )
#
buffer = bytearray(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'")
# sync_byte = buffer[0]
# length = buffer[1]
# frame_type = buffer[2]  # 0x16 = channels
# # channels = buffer[3:19]
#
print(f'length: {buffer[0]}')
print(f'type: {buffer[1]}')
print(f'crc: {buffer[-1]}')
channels = buffer[3:25]
# crc = buffer[-1]
# start = time.time()
# for i in range(0, 10000):
#     parsed_channels = payload_rc_channels_packed.parse(channels)
# end = time.time()
# print(f'struct took {end-start}')
#
# #
# print(parsed_channels.channels)
# # print(parsed_channels.channels[0])
# # print(parsed_channels.channels[15])
#
#
#
def unpack(data, bitlen):
    mask = (1 << bitlen) - 1
    for chunk in zip(*[iter(data)] * bitlen):
        n = int.from_bytes(chunk, 'big')
        a = []
        for i in range(8):
            a.append(n & mask)
            n >>= bitlen
        yield from reversed(a)


def parse_channels(data):
    swapped = data[::-1]
    return unpack(swapped, 11)
#
#
# # print(f'frame length {length}, actual length {actual_length}')
#
start = time.time()
for i in range(0, 10000):
    unpacked = parse_channels(channels)
end = time.time()
print(f'took {end-start}')
#
#
#
print(list(unpacked))
# #
# # for i in range(0, 16):
# #
# #     print(f'CH[{i}]{swapped_channels[i]}')
#
#
# # def thread1_main():
# #     while True:
# #         print("thread 1")
# #         time.sleep(1)
# #
# #
# # def thread2_main():
# #     while True:
# #         print("thread 2")
# #         time.sleep(1)
# #
# #
# # thread1 = Thread(target=thread1_main, name="thread1_main")
# # thread1.start()
# #
# # thread2 = Thread(target=thread2_main, name="thread2_main")
# # thread2.start()
# #
# # time.sleep(100)
#
# # logging.basicConfig(level=logging.INFO, filename="dashboard.log")
# #
# # logging.debug('This is a debug message')
# # logging.info('This is an info message')
# # logging.warning('This is a warning message')
# # logging.error('This is an error message')
# # logging.critical('This is a critical message')
# #
# #
# # logging.info(0x18)
# # logging.info(abs(1000-5000))
#
# # BYTES1 = b"\xC8\xC8"
# # BYTES2 = b"\xCC\xCC"
# #
# # BYTES = BYTES1 + BYTES2
# #
# # print(BYTES)
#
# # import argparse
# #
# # parser = argparse.ArgumentParser()
# # parser.add_argument('-b', '--baud', default=1000, type=int, )
# # parser.add_argument('-ss', '--serialsize', default=10, type=int)
# # parser.add_argument('-bs', '--buffersize', default=256, type=int)
# # args = parser.parse_args()
# #
# #
# # print(args.baud)
# # print(args.serialsize)
# # print(args.buffersize)
#
# # from construct import (BitsInteger, ByteSwapped, BitStruct, Array)
# #
# # channelsStructure = ByteSwapped(
# #     BitStruct("channels" / Array(16, BitsInteger(11)))
# # )
# #
# # # struct = channelsStructure.build({"channels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 99]})
# # # print(struct)
# #
# # var1 = b'\x0fp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
# # var2 = b'cp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
# # data1 = channelsStructure.parse(var1)
# # print(data1)
# # data2 = channelsStructure.parse(var2)
# # print(data2)
#
#
# from crsf_parser.payloads import PacketsTypes
# from crsf_parser import crsf_frame
# from crsf_parser.handling import crsf_build_frame
#
# # frame = crsf_build_frame(
# #     PacketsTypes.RC_CHANNELS_PACKED,
# #     {"channels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
# # )
# #
# # data = crsf_frame.parse(frame)
# # print(crsf_frame.header.data_offset)
# # print(data, type(data))
# # print(frame, len(frame), type(frame))
