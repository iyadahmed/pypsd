import sys
from dataclasses import dataclass
from io import BytesIO
from typing import BinaryIO

from pypsd.image_resources_reader.path import read_path_resource_block
from pypsd.image_resources_reader.resource_ids import ResourceID, is_path_resource, is_plugin_resource
from pypsd.utils import read_pascal_string, read_uint16, read_uint32


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

        if image_resource_block_signature != b"8BIM":
            print("Warning: Image resource block signature mismatch", file=sys.stderr)
            return

        rid_num = read_uint16(image_resources_section_buf)
        name = read_pascal_string(image_resources_section_buf)

        data_size = read_uint32(image_resources_section_buf)

        if data_size == 0:
            continue

        if (data_size % 2) == 1:
            data_size += 1
        data = image_resources_section_buf.read(data_size)

        # Very expensive check, uncomment to enable
        # assert b"8BIM" not in data

        if is_path_resource(rid_num):
            # TODO: move this read operation out
            read_path_resource_block(BytesIO(data))
        elif is_plugin_resource(rid_num):
            pass
        else:
            rid = ResourceID(rid_num)
            yield ResourceBlock(rid, name, data)
