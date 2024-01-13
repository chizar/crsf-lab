import serial
from time import sleep

ser = serial.Serial("/dev/ttyS0", 115200)  # Open port with baud rate
while True:
    received_data = ser.read()  # read serial port
    sleep(0.03)
    data_left = ser.inWaiting()  # check for remaining byte
    received_data += ser.read(data_left)
    # print (received_data)                   #print received data
    print(len(received_data))
    # ser.write(received_data)  # transmit data serially
    # 0xC8
    for b in received_data:
        if b == 0xC8:
            print(b)

    print(" ---- ")



