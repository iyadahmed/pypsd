from dataclasses import dataclass
from typing import BinaryIO
from io import BytesIO

from .utils import read_uint32, read_uint16, read_pascal_string
from .resource_ids import ResourceID, is_path_resource, is_plugin_resource
from .path import read_path_resource_block


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
        # FIXME: assertion error on some PSDs
        #       maybe pascal string reading has a bug and resources section data size for those is wrong?
        #       because there are still 8BIM after assertion,
        #       (you can check using image_resources_section_buf.find(b"8BIM")).
        # TODO: print names and check if padding pascal strings to even bytes solves it.
        #       yet that's it fix it

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
            read_path_resource_block(BytesIO(data))

        if is_plugin_resource(rid_num):
            continue

        rid = ResourceID(rid_num)

        yield ResourceBlock(rid, name, data)
