from enum import IntEnum
from typing import BinaryIO

from pypsd.utils import read_uint16


class ColorSpaceID(IntEnum):
    RGB = 0
    HSB = 1
    CMYK = 2
    LAB = 7
    GRAYSCALE = 8


def read_color(buf: BinaryIO):
    color_space = ColorSpaceID(read_uint16(buf))
    color_data_0 = read_uint16(buf)
    color_data_1 = read_uint16(buf)
    color_data_2 = read_uint16(buf)
    color_data_3 = read_uint16(buf)
