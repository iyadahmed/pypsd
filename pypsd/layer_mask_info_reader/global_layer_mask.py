from enum import IntEnum
from io import BytesIO
from typing import BinaryIO

from pypsd.utils import read_uint32, read_uint16, read_uchar


class GlobalLayerKind(IntEnum):
    COLOR_SELECTED = 0
    COLOR_PROTECTED = 1
    VALUE_PER_LAYER = 128


def _read_global_layer_mask_info_inner(buf: BinaryIO):
    # "Overlay color space" (undocumented)
    assert len(buf.read(2)) == 2

    colors = [read_uint16(buf) for _ in range(4)]
    opacity = read_uint16(buf)
    assert 0 <= opacity <= 100

    kind = GlobalLayerKind(read_uchar(buf))


def read_global_layer_mask_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    if section_length == 0:
        return
    section_data = buf.read(section_length)
    assert len(section_data) == section_length
    _read_global_layer_mask_info_inner(BytesIO(section_data))
