from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO

from .resource_blocks import iter_resource_blocks
from .utils import read_pascal_string, read_uint16, read_uint32
from .header import _read_header
from .color_mode import _read_color_mode_data
from .resource_ids import ResourceID


def read_psd(filepath: str):
    with open(filepath, "rb") as file:

        # Header
        header = _read_header(file)
        _read_color_mode_data(file, header.color_mode)

        for rblock in iter_resource_blocks(file):
            print(rblock.rid)
