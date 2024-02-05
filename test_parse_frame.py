from unittest import TestCase

from parse_frame import extract_frame, parse_channels_frame, parse_altitude_frame
import math


class Test(TestCase):
    def test_extract_frame_exact(self):
        buffer = bytearray(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'")
        pos = 0
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'", frame)
        self.assertEqual(b"", rest)

    def test_extract_frame_prefix_suffix(self):
        buffer = bytearray(
            b"\x16\xe0\x03\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'\x16\xe0\x03")
        pos = 3
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'",
                         frame)
        self.assertEqual(b"", rest)

    def test_extract_frame_no_length_body(self):
        buffer = bytearray(b"\xc8")
        pos = 0
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(None, frame)
        self.assertEqual(b"\xc8", rest)

    def test_extract_frame_not_full_length(self):
        buffer = bytearray(b"\x16\xe0\x03\xc8\x18\x16\xe0\x03")
        pos = 3
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(None, frame)
        self.assertEqual(b"\xc8\x18\x16\xe0\x03", rest)

    def test_extract_frame_zero_length(self):
        buffer = bytearray(b"\xc8\x01")
        pos = 0
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(b"\xc8\x01", frame)
        self.assertEqual(b"", rest)

    def test_parse_channels_frame(self):
        buffer = bytearray(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'")
        sync_byte, length, crc, channels = parse_channels_frame(buffer)
        self.assertEqual(0xC8, sync_byte)
        self.assertEqual(24, length)
        self.assertEqual(39, crc)
        self.assertEqual(16, len(channels))

    #

    def test_parse_altitude_frame(self):
        buffer = bytearray(b'\xc8\x08\x1e\xf8^\xf7\x01\xb7\xbc\xc2')
        sync_byte, length, crc, altitude = parse_altitude_frame(buffer)
        self.assertEqual(0xC8, sync_byte)
        self.assertEqual(8, length)
        self.assertEqual(194, crc)

        self.assertEqual(63582, altitude.pitch)
        self.assertEqual(364.29802530008004, math.degrees(altitude.pitch/10000))

        self.assertEqual(63233, altitude.roll)
        self.assertEqual(362.2984025950734, math.degrees(altitude.roll/10000))

        self.assertEqual(47036, altitude.yaw)
        self.assertEqual(269.496428517734, math.degrees(altitude.yaw / 10000))


