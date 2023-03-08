from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO

from pypsd.layer_mask_info_reader.channel_data import read_channel_data
from pypsd.layer_mask_info_reader.layer_record import ChannelInfo, LayerRecord, read_layer_record
from pypsd.utils import read_int16, read_uint32


@dataclass
class Channel:
    info: ChannelInfo
    data: bytes


@dataclass
class Layer:
    channels: list[Channel]
    record: LayerRecord


@dataclass
class LayerInfo:
    does_first_alpha_channel_contain_merged_transparency: bool
    layers: list[Layer]


def read_layer_record_channels(buf: BinaryIO, layer_record: LayerRecord):
    channels: list[Channel] = []
    for channel_info in layer_record.channels_info:
        channel_data = buf.read(channel_info.data_length)
        assert len(channel_data) == channel_info.data_length

        if len(channel_data) == 2:
            # Skip empty channel data (only contains compression type)
            continue

        channel_data_buf = BytesIO(channel_data)
        data = read_channel_data(channel_data_buf, layer_record.rect)
        channels.append(Channel(channel_info, data))

    return channels


def read_n_layer_records(buf: BinaryIO, n: int):
    return [read_layer_record(buf) for _ in range(n)]


def read_layer_info_section(buf: BinaryIO):
    layer_count = read_int16(buf)
    does_first_alpha_channel_contain_merged_transparency = layer_count < 0
    layer_count = abs(layer_count)
    layer_records = read_n_layer_records(buf, layer_count)

    layers: list[Layer] = []
    for lr in layer_records:
        channels = read_layer_record_channels(buf, lr)
        layers.append(Layer(channels, lr))

    return LayerInfo(does_first_alpha_channel_contain_merged_transparency, layers)


def read_layer_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    assert section_length != 0
    assert (section_length % 2) == 0

    section_data = buf.read(section_length)
    assert len(section_data) == section_length

    section_buf = BytesIO(section_data)
    return read_layer_info_section(section_buf)
