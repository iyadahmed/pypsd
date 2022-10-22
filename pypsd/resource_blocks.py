from dataclasses import dataclass
from typing import BinaryIO
from io import BytesIO

from .utils import read_uint32, read_uint16, read_pascal_string
from .resource_ids import ResourceID


@dataclass
class ResourceBlock:
    rid: ResourceID
    name: bytes
    data: bytes


def iter_resource_blocks(buffer: BinaryIO):

    image_resources_section_length = read_uint32(buffer)
    image_resources_section_buf = BytesIO(buffer.read(image_resources_section_length))

    while True:
        image_resource_block_signature = image_resources_section_buf.read(4)
        if len(image_resource_block_signature) == 0:
            break

        assert image_resource_block_signature == b"8BIM"

        rid = ResourceID(read_uint16(image_resources_section_buf))
        name = read_pascal_string(image_resources_section_buf)

        data_size = read_uint32(image_resources_section_buf)
        if (data_size % 2) == 1:
            data_size += 1
        data = image_resources_section_buf.read(data_size)

        yield ResourceBlock(rid, name, data)
