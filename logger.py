from serial import Serial

SYNC_BYTE = 0xC8

with Serial("/dev/ttyS0", 1000, timeout=10) as ser:
    inputByteArray = bytearray()
    while True:
        values = ser.read(100)
        for byte in values:
            if byte == SYNC_BYTE:
                print("GOT SYNC BYTE")