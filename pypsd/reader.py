from pypsd.color_mode import _read_color_mode_data
from pypsd.header import _read_header
from pypsd.image_resources_reader.reader import read_image_resources
from pypsd.layer_mask_info_reader.reader import read_layer_mask_info


def read_psd(filepath: str):
    with open(filepath, "rb") as file:
        header = _read_header(file)
        _read_color_mode_data(file, header.color_mode)
        read_image_resources(file)
        read_layer_mask_info(file)
