from enum import IntEnum
from struct import Struct
from typing import BinaryIO

from pypsd.utils import read_uint16, Rectangle, read_int16

signed_char_reader = Struct("b")


class CompressionType(IntEnum):
    RAW = 0
    RLE = 1
    ZIP = 2
    ZIP_PREDICT = 3


def _read_rle(buf: BinaryIO, num_scan_lines: int):
    byte_counts = []
    for _ in range(num_scan_lines):
        bc = read_uint16(buf)
        byte_counts.append(bc)

    data = buf.read()
    # TODO: read RLE correctly
    # byte_counts = []
    # for _ in range(num_scan_lines):
    #     byte_counts.append(read_uint16(buf))
    #
    #
    # uncompressed_scan_lines = []
    # for _ in range(num_scan_lines):
    #     header_byte = buf.read(1)
    #     assert len(header_byte) == 1
    #     n, = signed_char_reader.unpack(header_byte)
    #     if n == -128:
    #         continue
    #     elif 0 <= n <= 127:
    #         data = buf.read(1 + n)
    #         assert len(data) == (1 + n)
    #         uncompressed_scan_lines.append(data)
    #     elif -127 <= n <= -1:
    #         # One byte of data, repeated (1 − n) times in the decompressed output
    #         data = buf.read(1)[0]
    #         uncompressed_scan_lines.append([data] * (1 - n))
    #
    # return uncompressed_scan_lines


def _read_channel_data(buf: BinaryIO, layer_rect: Rectangle):
    compression_type = CompressionType(read_int16(buf))

    if compression_type == CompressionType.RAW:
        width = (layer_rect.right - layer_rect.left)
        height = (layer_rect.bottom - layer_rect.top)
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

        _read_rle(buf, num_scan_lines)
        rest = len(buf.read())
        assert rest == 0, rest

    else:
        raise NotImplementedError(compression_type)
