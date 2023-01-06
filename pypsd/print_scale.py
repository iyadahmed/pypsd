from typing import BinaryIO
from enum import IntEnum

from .utils import read_uint16, read_float


class PrintScaleStyle(IntEnum):
    CENTERED = 0
    SIZE_TO_FIT = 1
    USER_DEFINED = 2


def read_print_scale(buffer: BinaryIO):
    style = PrintScaleStyle(read_uint16(buffer))
    x = read_float(buffer)
    y = read_float(buffer)
    scale = read_float(buffer)
