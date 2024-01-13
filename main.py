import serial
from time import sleep

# ser = serial.Serial("/dev/ttyS0", 115200)  # Open port with baud rate
ser = serial.Serial("/dev/ttyS0", 420000)  # Open port with baud rate
while True:
    received_data = ser.read()  # read serial port
    sleep(0.03)
    data_left = ser.inWaiting()  # check for remaining byte
    received_data += ser.read(data_left)
    # print (received_data)                   #print received data
    print(len(received_data))
    ser.write(received_data)  # transmit data serially
