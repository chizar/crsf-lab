from unittest import TestCase
import crc


class Test(TestCase):
    def test_frame_crc(self):
        result = crc.frame_crc(
            b"\xc8\x18\x16\xe0\x03\x9f+\xc0\xf7\x8b_\xfc\xe2\x17\xbf\xf8E\xf9\xca\x07\x00\x00\x0c|\xe2'")

        self.assertEqual(39, result)
