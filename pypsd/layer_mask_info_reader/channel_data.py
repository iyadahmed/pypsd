from enum import IntEnum
from io import BytesIO
from itertools import islice, repeat
from struct import Struct
from typing import BinaryIO, List

from pypsd.utils import Rectangle, read_int16, read_uint16


class CompressionType(IntEnum):
    RAW = 0
    RLE = 1
    ZIP = 2
    ZIP_PREDICT = 3


def uncompress_rle(buf: memoryview) -> List[int]:
    uncompressed_data = []
    buf_iter = iter(buf)
    for c in buf_iter:
        n = (c - 256) if c > 127 else c

        if 0 <= n <= 127:
            uncompressed_data += islice(buf_iter, 1 + n)

        elif -127 <= n <= -1:
            uncompressed_data += repeat(next(buf_iter), 1 - n)

    return uncompressed_data


def read_channel_data(buf: BinaryIO, layer_rect: Rectangle):
    compression_type = CompressionType(read_int16(buf))

    width = layer_rect.right - layer_rect.left
    height = layer_rect.bottom - layer_rect.top

    if compression_type == CompressionType.RAW:
        size = width * height
        assert size > 0
        assert (size % 2) == 0
        data = buf.read(size)
        assert len(data) == size
        assert len(buf.read()) == 0  # Assert that all data was read (no more remaining data)

    elif compression_type == CompressionType.RLE:
        num_scan_lines = layer_rect.bottom - layer_rect.top
        if num_scan_lines == 0:
            return
        assert num_scan_lines > 0, (num_scan_lines, layer_rect.bottom, layer_rect.top)

        byte_counts = []
        for _ in range(num_scan_lines):
            byte_counts.append(read_uint16(buf))

        data = []
        for n in byte_counts:
            compressed_row = buf.read(n)
            data += uncompress_rle(memoryview(compressed_row))

        assert len(buf.read()) == 0

    else:
        raise NotImplementedError(compression_type)

    # NOTE: in rare cases, data length can be not enough to construct image
    # (len(data) != width * height)

    # Uncomment to display image
    # from PIL import Image

    # im = Image.frombytes("L", (width, height), bytes(data))
    # im.show()
