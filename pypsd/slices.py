from typing import BinaryIO
from enum import Enum

from .utils import read_uint32, read_unicode_string, read_rectangle_uint32, read_uchar


def read_4_or_string(buf: BinaryIO):
    length = read_uint32(buf)
    if length == 0:
        data = buf.read(4)
    else:
        data = buf.read(length)
    return data


class DescriptorOSTypeKey(Enum):
    REFERENCE = b"obj "
    DESCRIPTOR = b"Objc"
    LIST = b"VlLs"
    DOUBLE = b"doub"
    UNIT_FLOAT = b"UntF"
    STRING = b"TEXT"
    ENUM = b"enum"
    INT = b"long"
    LARGE_INT = b"comp"
    BOOL = b"bool"
    GLOBAL_OBJECT = b"GlbO"
    TYPE = b"type"
    GLBC = b"GlbC"
    ALIAS = b"alis"
    RAW_DATA = b"tdta"


class ReferenceOSTypeKey(Enum):
    PROPERTY = b"prop"
    CLASS = "Clss"
    ENUM_REF = b"Enmr"
    OFFSET = b"rele"
    IDENTIFIER = b"Idnt"
    INDEX = b"indx"
    NAME = b"name"


def read_reference_structure(buf: BinaryIO):
    num_items = read_uint32(buf)
    for _ in range(num_items):
        ostype_key = ReferenceOSTypeKey(buf.read(4))
        # TODO


def read_list_structure(buf: BinaryIO):
    num_items = read_uint32(buf)
    for _ in range(num_items):
        ostype_key = DescriptorOSTypeKey(buf.read(4))
        read_descriptor_structure_inner(buf, ostype_key)


def read_enumerated_descriptor(buf: BinaryIO):
    enum_type = read_4_or_string(buf)
    enum = read_4_or_string(buf)


def read_descriptor_structure_inner(buf: BinaryIO, ostype_key: DescriptorOSTypeKey):
    if ostype_key == DescriptorOSTypeKey.STRING:
        read_unicode_string(buf)
    elif ostype_key == DescriptorOSTypeKey.DESCRIPTOR:
        read_descriptor_structure(buf)
    elif ostype_key == DescriptorOSTypeKey.INT:
        read_uint32(buf)
    elif ostype_key == DescriptorOSTypeKey.LIST:
        read_list_structure(buf)
    elif ostype_key == DescriptorOSTypeKey.ENUM:
        read_enumerated_descriptor(buf)
    elif ostype_key == DescriptorOSTypeKey.BOOL:
        read_uchar(buf)
    else:
        raise NotImplementedError(ostype_key)


def read_descriptor_structure(buf: BinaryIO):
    name = read_unicode_string(buf)
    class_id = read_4_or_string(buf)
    num_items = read_uint32(buf)

    for _ in range(num_items):
        key = read_4_or_string(buf)
        ostype_key = DescriptorOSTypeKey(buf.read(4))
        read_descriptor_structure_inner(buf, ostype_key)


def read_slices_version_7_8(buf: BinaryIO):
    descriptor_version = read_uint32(buf)
    assert descriptor_version == 16

    read_descriptor_structure(buf)


def read_slices_resource_block(buf: BinaryIO):
    slice_id = read_uint32(buf)
    group_id = read_uint32(buf)
    origin = read_uint32(buf)
    if origin == 1:
        associated_layer_id = read_uint32(buf)
    name = read_unicode_string(buf)
    slice_type = read_uint32(buf)

    left = read_uint32(buf)
    top = read_uint32(buf)
    right = read_uint32(buf)
    bottom = read_uint32(buf)

    url = read_unicode_string(buf)
    target = read_unicode_string(buf)
    message = read_unicode_string(buf)
    alt_tag = read_unicode_string(buf)

    is_html_cell_text = bool(read_uchar(buf))
    cell_text = read_unicode_string(buf)
    horizontal_alignment = read_uint32(buf)
    vertical_alignment = read_uint32(buf)

    alpha = read_uchar(buf)
    red = read_uchar(buf)
    green = read_uchar(buf)
    blue = read_uchar(buf)

    descriptor_version = read_uint32(buf)
    assert descriptor_version == 16

    read_descriptor_structure(buf)


def read_slices_version_6(buf: BinaryIO):
    read_rectangle_uint32(buf)
    slices_group_name = read_unicode_string(buf)
    num_slices = read_uint32(buf)
    for _ in range(num_slices):
        read_slices_resource_block(buf)


def read_slices(buf: BinaryIO):
    version = read_uint32(buf)
    if version in (7, 8):
        read_slices_version_7_8(buf)
    elif version == 6:
        read_slices_version_6(buf)
    else:
        raise RuntimeError("Invalid slices version")
