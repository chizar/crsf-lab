import argparse

from serial import Serial

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baud', default=1000, type=int)
parser.add_argument('-t', '--timeout', default=1, type=int)
parser.add_argument('-ss', '--serialsize', default=10, type=int)

args = parser.parse_args()

SYNC_BYTE = 0xC8
FRAME_SIZE = 30

iteration = 0
last_pos = 0

valuesRest = b""

with Serial("/dev/ttyS0", args.baud, timeout=args.timeout) as ser:
    inputByteArray = bytearray()
    count = 0
    while True:
        iteration += 1
        values = valuesRest + ser.read(args.serialsize)

        size = len(values)
        pos = 0
        for byte in values:
            if byte == SYNC_BYTE:

                frame = values[pos:pos + FRAME_SIZE]
                if len(frame) < FRAME_SIZE:
                    valuesRest = frame
                    continue

                frame_size = len(frame)
                last_pos = pos
                count += 1
                print(f'iteration {iteration:05d}; sync {count} found on {pos}, frame size {frame_size}, total size {size}')
                print(frame)
            pos += 1
