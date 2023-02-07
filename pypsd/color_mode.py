from enum import IntEnum
from typing import BinaryIO

from pypsd.utils import read_uint32

INDEXED_COLOR_DATA_LENGTH = 768


class ColorMode(IntEnum):
    Bitmap = 0
    Grayscale = 1
    Indexed = 2
    RGB = 3
    CMYK = 4
    Multichannel = 7
    Duotone = 8
    Lab = 9


def read_color_mode_data(buffer: BinaryIO, color_mode: ColorMode):
    color_data_length = read_uint32(buffer)
    if color_mode == ColorMode.Indexed:
        assert color_data_length == INDEXED_COLOR_DATA_LENGTH
        indexed_color_table = buffer.read(INDEXED_COLOR_DATA_LENGTH)
        # TODO: de-interleave and store indexed color table
        # it seems that color table is 256 RGB, non-interleaved,
        # so 256 red values, followed by 256 green, followed by 256 blue bytes
        # TIP: use strides :)
    elif color_mode == ColorMode.Duotone:
        # undocumented
        buffer.read(color_data_length)
    else:
        assert color_data_length == 0
