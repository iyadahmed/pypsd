from typing import BinaryIO

from pypsd.layer_mask_info_reader.additional_layer_info_keys import AdditionalLayerKey
from pypsd.utils import read_uint32, read_int32


def read_additional_layer_info(buf: BinaryIO):
    while True:
        signature = buf.read(4)
        if len(signature) == 0:
            break

        assert signature in (b"8BIM", b"8B64"), signature

        key_bytes = buf.read(4)
        assert len(key_bytes) == 4

        key = AdditionalLayerKey(key_bytes)
        data_length = read_uint32(buf)

        # In docs it says "rounded to an even byte count"
        # it turned out to be rounded to multiples of 4 :D
        if (data_length % 4) != 0:
            # round up to a multiple of 4
            data_length = (data_length // 4 + 1) * 4

        data = buf.read(data_length)
        assert len(data) == data_length
