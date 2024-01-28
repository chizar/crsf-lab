def extract_frame(buffer, pos):
    buffer_size = len(buffer)
    if buffer_size < pos + 1 + 1:
        values_rest = buffer[pos:buffer_size]
        return [None, values_rest]  # no length byte
    length = buffer[pos + 1]

    if buffer_size < pos + length + 1:
        values_rest = buffer[pos:buffer_size]
        return [None, values_rest]   # not a full frame length

    frame = buffer[pos:pos + length + 2]  # one for length, one for type, one for CRC
    return [frame, b""]


def unpack(data, bitlen):
    mask = (1 << bitlen) - 1
    for chunk in zip(*[iter(data)] * bitlen):
        n = int.from_bytes(chunk, 'big')
        a = []
        for i in range(8):
            a.append(n & mask)
            n >>= bitlen
        yield from reversed(a)


def parse_channels_frame(frame):
    sync_byte = frame[0]
    length = frame[1]
    crc = frame[-1]

    payload = frame[3:length+1]
    swapped = payload[::-1]
    channels = unpack(swapped, 11)
    return [sync_byte, length, crc, list(channels)]
