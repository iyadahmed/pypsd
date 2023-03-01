from io import BytesIO
from typing import BinaryIO

from pypsd.layer_mask_info_reader.additional_layer_info.filter_mask import read_filter_mask
from pypsd.layer_mask_info_reader.additional_layer_info.keys import AdditionalLayerKey
from pypsd.layer_mask_info_reader.additional_layer_info.pattern import read_pattern
from pypsd.layer_mask_info_reader.additional_layer_info.text_engine_data import read_text_engine_data
from pypsd.layer_mask_info_reader.additional_layer_info.unicode_path_name import read_unicode_path_name
from pypsd.utils import read_int32, read_uint32


def read_additional_layer_info_block(buf: BinaryIO, key: AdditionalLayerKey):
    if key == AdditionalLayerKey.PATTERN_1:
        read_pattern(buf)

    elif key == AdditionalLayerKey.TEXT_ENGINE_DATA:
        read_text_engine_data(buf)

    elif key == AdditionalLayerKey.FILTER_MASK:
        read_filter_mask(buf)

    elif key == AdditionalLayerKey.UNICODE_PATH_NAME:
        read_unicode_path_name(buf)

    else:
        raise NotImplementedError(key)


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

        if data_length == 0:
            continue

        # In docs it says "rounded to an even byte count"
        # it turned out to be rounded to multiples of 4 :D
        if (data_length % 4) != 0:
            # round up to a multiple of 4
            data_length = (data_length // 4 + 1) * 4

        data = buf.read(data_length)
        assert len(data) == data_length

        read_additional_layer_info_block(BytesIO(data), key)
