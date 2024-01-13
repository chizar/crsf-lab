import sys
from time import sleep

import serial

print('args', sys.argv)
baud = 115200
if len(sys.argv) > 1:
    baud = sys.argv[1]
ser = serial.Serial("/dev/ttyS0", baud)  # Open port with baud rate
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
        if received_data[i] == 0xC8:
            print('0xC8 byte detected: Destination address or "sync" byte: Going to the flight controller')

            if len(received_data) <= i + 1:
                print('no frame length')
                continue
            framelen = received_data[i+1]
            print(f'frame length {framelen}')

            if len(received_data) <= i + 2:
                print('no type byte')
                continue
            type = received_data[i+2]
            print(f'type: {type} - ' + hex(type))
            if type != 0x16:
                continue

            if len(received_data) <= i + 3:
                print('no channel1 byte')
                continue

            ch01 = received_data[i + 3]
            print(f'channel1: {ch01} - ' + hex(ch01))



