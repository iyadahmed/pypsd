from .resource_blocks import iter_resource_blocks
from .header import _read_header
from .color_mode import _read_color_mode_data


def read_psd(filepath: str):
    with open(filepath, "rb") as file:

        # Header
        header = _read_header(file)
        _read_color_mode_data(file, header.color_mode)

        for rblock in iter_resource_blocks(file):
            print(rblock.rid)
