from io import BytesIO
from typing import BinaryIO

from pypsd.layer_mask_info_reader.channel_data import _read_channel_data
from pypsd.layer_mask_info_reader.layer_record import _read_layer_record, LayerRecord
from pypsd.utils import read_uint32, read_int16


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
