from dataclasses import dataclass
from typing import Optional

from pypsd.color_mode import read_color_mode_data
from pypsd.header import read_header
from pypsd.image_resources_reader.reader import read_image_resources
from pypsd.layer_mask_info_reader.reader import LayerMaskInfo, read_layer_mask_info


@dataclass
class PSD:
    layer_mask_info: Optional[LayerMaskInfo]
    # TODO: image resources and color mode data


def read_psd(filepath: str):
    with open(filepath, "rb") as file:
        header = read_header(file)
        read_color_mode_data(file, header.color_mode)
        read_image_resources(file)
        layer_mask_info = read_layer_mask_info(file)
        return PSD(layer_mask_info)
