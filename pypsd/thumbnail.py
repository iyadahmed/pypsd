from enum import IntEnum
from typing import BinaryIO

from .utils import read_uint32, read_uint16


class ThumbnailFormat(IntEnum):
    RAW_RGB = 0
    JPEG_RGB = 1


def read_thumbnail_resource(buf: BinaryIO):
    thumbnail_format = ThumbnailFormat(read_uint32(buf))
    width_pixels = read_uint32(buf)
    height_pixels = read_uint32(buf)
    width_bytes = read_uint32(buf)  # = (width * bits_per_pixel + 31) / 32 * 4
    total_size = read_uint32(buf)  # = width_bytes * height * planes
    size_after_compression = read_uint32(buf)
    bits_per_pixel = read_uint16(buf)
    assert bits_per_pixel == 24
    number_of_planes = read_uint16(buf)
    assert number_of_planes == 1
    jfif_data = buf.read()

    if (size_after_compression % 2) == 1:
        # Not mentioned in docs, but it seems that size after compression is padded to be even
        size_after_compression += 1

    assert len(jfif_data) == size_after_compression
