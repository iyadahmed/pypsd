from enum import IntEnum
from typing import BinaryIO

from pypsd.utils import read_uchar, read_uint32


class VHSelect(IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1


def read_guide_resource_block(buffer: BinaryIO):
    version = read_uint32(buffer)
    assert version == 1
    grid_horizontal = read_uint32(buffer)
    grid_vertical = read_uint32(buffer)
    num_of_guide_resource_block = read_uint32(buffer)
    for _ in range(num_of_guide_resource_block):
        guide_location = read_uint32(buffer)
        guide_direction = VHSelect(read_uchar(buffer))
