from typing import BinaryIO
from enum import Enum

from .utils import read_uint32, read_unicode_string


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


def read_descriptor_structure_inner(buf: BinaryIO, ostype_key: DescriptorOSTypeKey):
    if ostype_key == DescriptorOSTypeKey.STRING:
        read_unicode_string(buf)
    elif ostype_key == DescriptorOSTypeKey.DESCRIPTOR:
        read_descriptor_structure(buf)
    elif ostype_key == DescriptorOSTypeKey.INT:
        read_uint32(buf)
    elif ostype_key == DescriptorOSTypeKey.LIST:
        read_list_structure(buf)
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


def read_slices(buf: BinaryIO):
    version = read_uint32(buf)
    if version in (7, 8):
        read_slices_version_7_8(buf)
    elif version == 6:
        raise NotImplementedError
    else:
        raise RuntimeError("Invalid slices version")
