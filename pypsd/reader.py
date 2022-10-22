from io import BytesIO

from .color_mode import _read_color_mode_data
from .header import _read_header
from .resource_blocks import iter_resource_blocks
from .resource_ids import ResourceID
from .slices import read_slices


def read_psd(filepath: str):
    with open(filepath, "rb") as file:

        # Header
        header = _read_header(file)
        _read_color_mode_data(file, header.color_mode)

        for rblock in iter_resource_blocks(file):
            buf = BytesIO(rblock.data)
            if rblock.rid == ResourceID.PS6_SLICES:
                read_slices(buf)
