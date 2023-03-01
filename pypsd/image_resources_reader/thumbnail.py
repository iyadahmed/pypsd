from enum import IntEnum
from typing import BinaryIO

from pypsd.utils import read_uint16, read_uint32


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

    # Uncomment to display thumbnail
    # from PIL import Image
    # from io import BytesIO
    #
    # image = Image.open(BytesIO(jfif_data))
    # image.show()
