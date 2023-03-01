from typing import BinaryIO

from pypsd.utils import read_uint16


def read_filter_mask(buf: BinaryIO):
    color_space = buf.read(10)
    opacity = read_uint16(buf)
