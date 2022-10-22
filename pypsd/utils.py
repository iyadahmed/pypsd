from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class Rectangle:
    top: int
    left: int
    bottom: int
    right: int


def read_uint32(buffer: BinaryIO):
    data = buffer.read(4)
    assert len(data) == 4
    return int.from_bytes(data, "big", signed=False)


def read_int16(buffer: BinaryIO):
    data = buffer.read(2)
    assert len(data) == 2
    return int.from_bytes(data, "big", signed=True)


def read_uint16(buffer: BinaryIO):
    data = buffer.read(2)
    assert len(data) == 2
    return int.from_bytes(data, "big", signed=False)


def read_rectangle_uint32(buffer: BinaryIO):
    top = read_uint32(buffer)
    left = read_uint32(buffer)
    bottom = read_uint32(buffer)
    right = read_uint32(buffer)
    return Rectangle(top, left, bottom, right)


def read_uchar(buffer: BinaryIO):
    data = buffer.read(1)
    assert len(data) == 1
    return data[0]


def read_pascal_string(buffer: BinaryIO):
    string_length = buffer.read(1)[0]
    if string_length == 0:
        buffer.read(1)[0]
        return b""
    return buffer.read(string_length)


def read_unicode_string(buffer: BinaryIO):
    length = read_uint32(buffer)
    string_raw = buffer.read(length * 2)
    assert len(string_raw) == length * 2
    return string_raw.decode("utf-16")


def is_path_resource(resource_id: int):
    return 2000 <= resource_id <= 2997


def is_plugin_resource(resource_id: int):
    return 4000 <= resource_id <= 4999
