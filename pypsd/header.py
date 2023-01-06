from typing import BinaryIO
from dataclasses import dataclass

from pypsd.color_mode import ColorMode
from pypsd.utils import read_int16, read_uint16, read_uint32


@dataclass
class Header:
    # Width and height of the image in pixels
    # NOTE: PSD max width or height is 30,000, while PSB format spec supports up to 300,000
    width: int
    height: int

    num_channels: int
    color_mode: ColorMode


def _read_header(buffer: BinaryIO):
    # TODO: move asserts to dataclass __post_init__?
    signature = buffer.read(4)
    assert signature == b"8BPS"

    version = read_uint16(buffer)
    assert version == 1

    _reserved = buffer.read(6)
    assert len(_reserved) == 6
    assert all(c == 0 for c in _reserved)

    num_channels = read_int16(buffer)
    assert 1 <= num_channels <= 56

    height = read_uint32(buffer)
    assert height <= 30_000

    width = read_uint32(buffer)
    assert width <= 30_000

    depth = read_uint16(buffer)
    assert depth in (1, 8, 16, 32)

    color_mode = ColorMode(read_uint16(buffer))

    return Header(width, height, num_channels, color_mode)
