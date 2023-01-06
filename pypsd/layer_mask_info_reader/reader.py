from typing import BinaryIO

from pypsd.layer_mask_info_reader.layer_record import _read_layer_record
from pypsd.utils import read_uint32, read_int16


def _read_layer_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    assert section_length != 0
    assert (section_length % 2) == 0

    layer_count = read_int16(buf)
    if layer_count < 0:
        # First alpha channel contains transparency data for merged results
        # when layer count is negative, according to PSD documentation
        layer_count = -layer_count

    for _ in range(layer_count):
        _read_layer_record(buf)


def read_layer_mask_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    if section_length == 0:
        return

    _read_layer_info(buf)
