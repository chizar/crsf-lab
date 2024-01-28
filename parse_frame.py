def extract_frame(buffer, pos):
    buffer_size = len(buffer)
    if buffer_size < pos + 1 + 1:
        values_rest = buffer[pos:buffer_size]
        return [None, values_rest]  # no length byte
    length = buffer[pos + 1]

    if buffer_size < pos + length:
        values_rest = buffer[pos:buffer_size]
        return [None, values_rest]   # not a full frame length

    frame = buffer[pos:pos + length]
    return [frame, b""]
