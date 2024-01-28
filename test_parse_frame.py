from unittest import TestCase

from parse_frame import extract_frame


class Test(TestCase):
    def test_extract_frame_exact(self):
        buffer = bytearray(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'")
        pos = 0
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|", frame)
        self.assertEqual(b"", rest)

    def test_extract_frame_prefix_suffix(self):
        buffer = bytearray(
            b"\x16\xe0\x03\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2\xfc\xe2\x17\xbf'")
        pos = 3
        frame, rest = extract_frame(buffer, pos)
        self.assertEqual(b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|",
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
