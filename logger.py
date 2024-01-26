import argparse

from serial import Serial

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=1000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=10, type=int)

args = parser.parse_args()

SYNC_BYTE = 0xC8

iteration = 0
last_pos = 0

with Serial("/dev/ttyS0", args.baud, timeout=args.timeout) as ser:
    inputByteArray = bytearray()
    count = 0
    while True:
        iteration += 1
        values = ser.read(args.serialsize)
        size = len(values)
        pos = 0
        for byte in values:
            pos += 1
            if byte == SYNC_BYTE:
                frame_size = pos - last_pos
                last_pos = pos
                count += 1
                print(f'iteration {iteration:05d}; sync {count} found on {pos}, frame size {frame_size}, total size {size}')