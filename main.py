import serial
import sys
from time import sleep

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
            framelen = received_data[i+1]
            print(f'frame length ${framelen}')





