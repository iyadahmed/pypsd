from dataclasses import dataclass
from enum import IntEnum, IntFlag, auto
from io import BytesIO
from typing import BinaryIO, List

from pypsd.layer_mask_info_reader.blend_mode_key import BlendModeKey
from pypsd.layer_mask_info_reader.layer_blending_ranges import _read_layer_blending_ranges_data
from pypsd.layer_mask_info_reader.layer_mask_data import _read_layer_mask_data
from pypsd.utils import read_uint32, read_int16, read_rectangle_uint32, read_uint16, read_uchar, Rectangle, read_int32


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


class ChannelID(IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2
    ALPHA = 3
    TRANSPARENCY_MASK = -1
    USER_SUPPLIED_MASK = -2
    REAL_USER_SUPPLIED_MASK = -3


@dataclass
class ChannelInfo:
    data_length: int


@dataclass
class ExtraLayerData:
    # TODO: add mask, blending ranges data and additional layer info data
    name: bytes


@dataclass
class LayerRecord:
    rect: Rectangle
    channel_count: int
    channels_info: List[ChannelInfo]
    extra_data: ExtraLayerData


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


def _read_extra_data(buf: BinaryIO):
    _read_layer_mask_data(buf)
    _read_layer_blending_ranges_data(buf)
    layer_name = _read_pascal_string_pad4(buf)
    # TODO: read "Additional Layer Information" structure
    additional_layer_info_data = buf.read()
    return ExtraLayerData(layer_name)


def _read_layer_record(buf: BinaryIO):
    top = read_int32(buf)
    left = read_int32(buf)
    bottom = read_int32(buf)
    right = read_int32(buf)

    rect = Rectangle(top, left, bottom, right)

    channel_count = read_uint16(buf)
    channels_info = []
    for _ in range(channel_count):
        channel_id = ChannelID(read_int16(buf))
        channel_data_length = read_uint32(buf)
        channels_info.append(ChannelInfo(channel_data_length))

    blend_mode_signature = buf.read(4)
    assert blend_mode_signature == b"8BIM"
    blend_mode_key = BlendModeKey(buf.read(4))

    opacity = read_uchar(buf)
    clipping = ClippingType(read_uchar(buf))
    flags = LayerRecordFlags(read_uchar(buf))

    # Filler byte
    assert read_uchar(buf) == 0

    extra_data_length = read_uint32(buf)
    extra_data_bytes = buf.read(extra_data_length)
    assert len(extra_data_bytes) == extra_data_length
    extra_data = _read_extra_data(BytesIO(extra_data_bytes))

    return LayerRecord(rect, channel_count, channels_info, extra_data)
