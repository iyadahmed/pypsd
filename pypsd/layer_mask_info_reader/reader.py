from enum import IntEnum
from io import BytesIO
from struct import Struct
from typing import BinaryIO

from pypsd.layer_mask_info_reader.layer_record import _read_layer_record, LayerRecord
from pypsd.utils import read_uint32, read_int16, read_uint16, Rectangle

signed_char_reader = Struct("b")

# TODO: split to multiple files


class CompressionType(IntEnum):
    RAW = 0
    RLE = 1
    ZIP = 2
    ZIP_PREDICT = 3


def _read_rle(buf: BinaryIO, num_scan_lines: int):
    pass
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
    compression_type = CompressionType(read_uint16(buf))

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

    else:
        raise NotImplementedError(compression_type)


def _read_layer_record_channels(buf: BinaryIO, layer_record: LayerRecord):
    for channel_info in layer_record.channels_info:
        channel_data = buf.read(channel_info.data_length)
        assert len(channel_data) == channel_info.data_length

        if len(channel_data) == 2:
            # Skip empty channel data (only contains compression type)
            continue

        channel_data_buf = BytesIO(channel_data)
        _read_channel_data(channel_data_buf, layer_record.rect)


def _read_n_layer_records(buf: BinaryIO, n: int):
    return [_read_layer_record(buf) for _ in range(n)]


def _read_layer_info_section(buf: BinaryIO):
    layer_count = read_int16(buf)
    first_alpha_contains_merged_transparency = (layer_count < 0)
    layer_count = abs(layer_count)
    layer_records = _read_n_layer_records(buf, layer_count)
    for lr in layer_records:
        _read_layer_record_channels(buf, lr)


def _read_layer_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    assert section_length != 0
    assert (section_length % 2) == 0

    section_data = buf.read(section_length)
    assert len(section_data) == section_length

    section_buf = BytesIO(section_data)
    _read_layer_info_section(section_buf)


def read_layer_mask_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    if section_length == 0:
        return
    section_data = buf.read(section_length)
    assert len(section_data) == section_length

    section_buf = BytesIO(section_data)
    _read_layer_info(section_buf)
    # TODO: "Global layer mask info"
    # TODO: "Tagged blocks"
