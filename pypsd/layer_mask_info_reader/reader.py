from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO

from pypsd.layer_mask_info_reader.additional_layer_info.reader import read_additional_layer_info
from pypsd.layer_mask_info_reader.global_layer_mask import read_global_layer_mask_info
from pypsd.layer_mask_info_reader.layer_info import LayerInfo, read_layer_info
from pypsd.utils import read_uint32


@dataclass
class LayerMaskInfo:
    info: LayerInfo
    # TODO: "global" and "additional" info


def read_layer_mask_info(buf: BinaryIO):
    section_length = read_uint32(buf)
    if section_length == 0:
        return
    section_data = buf.read(section_length)
    assert len(section_data) == section_length

    section_buf = BytesIO(section_data)
    layer_info = read_layer_info(section_buf)
    read_global_layer_mask_info(section_buf)
    read_additional_layer_info(section_buf)

    # Assert no remaining data
    assert len(section_buf.read()) == 0

    return LayerMaskInfo(layer_info)
