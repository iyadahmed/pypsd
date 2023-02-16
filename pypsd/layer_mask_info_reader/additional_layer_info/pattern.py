from typing import BinaryIO

from pypsd.utils import read_uint32


def read_pattern(buf: BinaryIO):
    pattern_length = read_uint32(buf)
    _version = read_uint32(buf)
    assert _version == 1
