from typing import BinaryIO

from pypsd.utils import read_uint32, read_uchar


def _read_range(buf: BinaryIO):
    b1 = read_uchar(buf)
    b2 = read_uchar(buf)
    w1 = read_uchar(buf)
    w2 = read_uchar(buf)
    return (b1, b2), (w1, w2)


def _read_layer_blending_ranges_data(buf: BinaryIO):
    length = read_uint32(buf)
    if length == 0:
        return

    # Composite gray blend source, 2 black values followed by 2 white values
    # Present but irrelevant for Lab & Grayscale
    _read_range(buf)

    # Composite gray blend destination range
    _read_range(buf)

    for _ in range((length - 8) // 4, 2):
        nth_channel_source_range = _read_range(buf)
        nth_channel_destination_range = _read_range(buf)
