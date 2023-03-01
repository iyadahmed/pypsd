from dataclasses import dataclass
from struct import Struct
from typing import BinaryIO

float_reader = Struct(">f")
double_reader = Struct(">d")
# "fixed number (2 bytes real, 2 bytes fraction)"
fixed_point_number_reader = Struct(">hh")


@dataclass
class Rectangle:
    top: int
    left: int
    bottom: int
    right: int


def read_float(buffer: BinaryIO):
    data = buffer.read(4)
    assert len(data) == 4
    return float_reader.unpack(data)[0]


def read_double(buffer: BinaryIO):
    data = buffer.read(8)
    assert len(data) == 8
    return double_reader.unpack(data)[0]


def read_fixed_point_number(buffer: BinaryIO):
    data = buffer.read(4)
    assert len(data) == 4
    return fixed_point_number_reader.unpack(data)


def read_uint32(buffer: BinaryIO):
    data = buffer.read(4)
    assert len(data) == 4
    return int.from_bytes(data, "big", signed=False)


def read_int32(buffer: BinaryIO):
    data = buffer.read(4)
    assert len(data) == 4
    return int.from_bytes(data, "big", signed=True)


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
    string_length += 1  # Include the byte we have just read when calculating padded length

    # Calculate padded length, we pad the length of total bytes to be even
    if (string_length % 2) == 1:
        string_length += 1

    # Remove the byte we have read because we need to read the rest
    string_length -= 1
    return buffer.read(string_length)


def read_unicode_string(buffer: BinaryIO):
    length = read_uint32(buffer)
    string_raw = buffer.read(length * 2)
    assert len(string_raw) == length * 2
    return string_raw.decode("utf-16-be")
