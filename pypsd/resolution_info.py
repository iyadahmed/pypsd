from enum import IntEnum
from typing import BinaryIO

from pypsd.utils import read_fixed_point_number, read_int16


class ResUnit(IntEnum):
    PIXELS_PER_INCH = 1
    PIXELS_PER_CM = 2


class DisplayUnit(IntEnum):
    INCHES = 1
    CM = 2
    POINTS = 3
    PICAS = 4
    COLUMNS = 5


def read_resolution_info(buf: BinaryIO):
    horizontal_resolution = read_fixed_point_number(buf)
    h_res_unit = ResUnit(read_int16(buf))
    width_unit = DisplayUnit(read_int16(buf))
    vertical_resolution_ppi = read_fixed_point_number(buf)
    v_res_unit = ResUnit(read_int16(buf))
    height_unit = DisplayUnit(read_int16(buf))
