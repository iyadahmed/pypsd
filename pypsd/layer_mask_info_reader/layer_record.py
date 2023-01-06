from enum import IntEnum, IntFlag, auto
from io import BytesIO
from typing import BinaryIO

from pypsd.layer_mask_info_reader.blend_mode_key import BlendModeKey
from pypsd.layer_mask_info_reader.layer_blending_ranges import _read_layer_blending_ranges_data
from pypsd.layer_mask_info_reader.layer_mask_data import _read_layer_mask_data
from pypsd.utils import read_uint32, read_int16, read_rectangle_uint32, read_uint16, read_uchar


class ClippingType(IntEnum):
    BASE = 0
    NON_BASE = 1


class LayerRecordFlags(IntFlag):
    # NOTE: Hopefully this works, not proven yet
    TRANSPARENCY_PROTECTED = auto()
    VISIBLE = auto()
    OBSOLETE = auto()
    IS_4TH_BIT_USEFUL = auto()
    IRRELEVANT_PIXEL_DATA = auto()


def _read_pascal_string_pad4(buf: BinaryIO):
    """Reads a Pascal string padded to multiple of 4 bytes from buffer"""
    pascal_string_length = read_uchar(buf)
    pascal_string_length += 1  # Include byte that we have just read

    # Pad to multiple of 4 bytes
    if (pascal_string_length % 4) != 0:
        pascal_string_length = (pascal_string_length // 4 + 1) * 4

    # We already read a byte, so we need to read the rest
    pascal_string_length -= 1

    return buf.read(pascal_string_length)


def _read_layer_record(buf: BinaryIO):
    rect = read_rectangle_uint32(buf)
    channel_count = read_uint16(buf)
    for _ in range(channel_count):
        channel_id = read_int16(buf)
        channel_data_length = read_uint32(buf)
    blend_mode_signature = buf.read(4)
    assert blend_mode_signature == b"8BIM"
    blend_mode_key = BlendModeKey(buf.read(4))

    opacity = read_uchar(buf)
    clipping = ClippingType(read_uchar(buf))
    flags = LayerRecordFlags(read_uchar(buf))

    # Filler byte
    assert read_uchar(buf) == 0

    extra_data_length = read_uint32(buf)
    extra_data_buf = BytesIO(buf.read(extra_data_length))

    _read_layer_mask_data(extra_data_buf)
    _read_layer_blending_ranges_data(extra_data_buf)
    layer_name = _read_pascal_string_pad4(extra_data_buf)
