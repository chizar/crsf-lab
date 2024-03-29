import sys
from time import sleep
from construct import (BitsInteger, ByteSwapped, BitStruct, Array)

import serial

print('args', sys.argv)
baud = 420000
if len(sys.argv) > 1:
    baud = sys.argv[1]
ser = serial.Serial("/dev/ttyS0", baud, )  # Open port with baud rate
ch01 = 0
ch02 = 0
ch03 = 0
ch04 = 0
ch05 = 0
ch06 = 0
ch07 = 0
ch08 = 0
ch09 = 0
ch10 = 0

channelsFrameStructure = ByteSwapped(
    BitStruct("channels" / Array(16, BitsInteger(11)))
)

while True:
    received_data = ser.read()  # read serial port
    sleep(0.03)
    data_left = ser.inWaiting()  # check for remaining byte
    received_data += ser.read(data_left)
    # print (received_data)                   #print received data
    # print(len(received_data))
    # ser.write(received_data)  # transmit data serially
    # 0xC8
    # for i = 0 to len(received_data):
    for i in range(len(received_data)):
        if received_data[i] != 0xC8:
            continue

        # print('0xC8 byte detected: Destination address or "sync" byte: Going to the flight controller')
        if len(received_data) <= i + 1:
            # print('no frame length')
            continue
        framelen = received_data[i+1]
        # print(f'frame length {framelen}')

        if len(received_data) <= i + 2:
            # print('no type byte')
            continue
        payloadType = received_data[i + 2]
        if payloadType != 0x16:
            continue

        if len(received_data) < i + 2 + framelen:  # skip incomplete frame
            continue

        channelsFrameBytes = received_data[i + 2:framelen]

        if len(channelsFrameBytes) < 22:  # skip incomplete frame
            continue

        changes = False

        channels = channelsFrameStructure.parse(channelsFrameBytes)

        channel = 1
        if len(channelsFrameBytes) <= channel:
            # print('no channel1 byte')
            continue
        new_ch01 = channelsFrameBytes[channel]
        # print(f'channel1: {ch01} - ' + hex(ch01))
        if new_ch01 != ch01:
            ch01 = new_ch01
            changes = True

        channel = 2
        if len(channelsFrameBytes) <= channel:
            # print('no channel2 byte')
            continue
        new_ch02 = channelsFrameBytes[channel]
        # print(f'channel2: {ch02} - ' + hex(ch02))
        if new_ch02 != ch02:
            ch02 = new_ch02
            changes = True

        channel = 3
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch03 = channelsFrameBytes[channel]
        if new_ch03 != ch03:
            ch03 = new_ch03
            changes = True

        channel = 4
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch04 = channelsFrameBytes[channel]
        if new_ch04 != ch04:
            ch04 = new_ch04
            changes = True

        channel = 5
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch05 = channelsFrameBytes[channel]
        if new_ch05 != ch05:
            ch05 = new_ch05
            changes = True

        channel = 6
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch06 = channelsFrameBytes[channel]
        if new_ch06 != ch06:
            ch06 = new_ch06
            changes = True

        channel = 7
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch07 = channelsFrameBytes[channel]
        if new_ch07 != ch07:
            ch07 = new_ch07
            changes = True

        channel = 8
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch08 = channelsFrameBytes[channel]
        if new_ch08 != ch08:
            ch08 = new_ch08
            changes = True

        channel = 9
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch09 = channelsFrameBytes[channel]
        if new_ch09 != ch09:
            ch09 = new_ch09
            changes = True

        channel = 10
        if len(channelsFrameBytes) <= channel:
            continue
        new_ch10 = channelsFrameBytes[channel]
        if new_ch10 != ch10:
            ch10 = new_ch10
            changes = True

        if changes:
            print(f'CH01:{channels.channels[0]:05d} '
                  f'CH02:{channels.channels[1]:05d} '
                  f'CH03:{channels.channels[2]:05d} '
                  f'CH04:{channels.channels[3]:05d} '
                  f'CH05:{channels.channels[4]:05d} '
                  f'CH06:{channels.channels[5]:05d} '
                  f'CH07:{channels.channels[6]:05d} '
                  f'CH08:{channels.channels[7]:05d} '
                  f'CH09:{channels.channels[8]:05d} '
                  f'CH10:{channels.channels[9]:05d} '
                  f'CH11:{channels.channels[10]:05d} '
                  f'CH12:{channels.channels[11]:05d} '
                  f'CH13:{channels.channels[12]:05d} '
                  f'CH14:{channels.channels[13]:05d} '
                  f'CH15:{channels.channels[14]:05d} '
                  f'CH16:{channels.channels[15]:05d}')


