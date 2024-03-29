from enum import IntEnum
from io import BytesIO
from typing import BinaryIO

from pypsd.utils import read_uint16, read_uint32


class PathDataRecordType(IntEnum):
    # NOTE: Knots are bezier knots
    CLOSED_LENGTH = 0
    CLOSED_LINKED_KNOT = 1
    CLOSED_UNLINKED_KNOT = 2
    OPEN_LENGTH = 3
    OPEN_LINKED_KNOT = 4
    OPEN_UNLINKED_KNOT = 5
    PATH_FILL_RULE = 6
    CLIPBOARD = 7
    INITIAL_FILL_RULE = 8


def read_control_point_component(buf: BinaryIO):
    value = read_uint32(buf)
    # TODO: parse fixed point number
    return value


def read_control_point(buf: BinaryIO):
    y = read_control_point_component(buf)
    x = read_control_point_component(buf)
    return x, y


def read_path_record(buf: BinaryIO, record_type: PathDataRecordType):
    if record_type in (PathDataRecordType.OPEN_LENGTH, PathDataRecordType.CLOSED_LENGTH):
        num_bezier_knot_records = read_uint16(buf)
        assert len(buf.read(22)) == 22
        # NOTE: PSD documentation states that those 22 bytes should be all zeros
        # but some files do not adhere
    elif record_type in (
        PathDataRecordType.OPEN_LINKED_KNOT,
        PathDataRecordType.OPEN_UNLINKED_KNOT,
        PathDataRecordType.CLOSED_LINKED_KNOT,
        PathDataRecordType.CLOSED_UNLINKED_KNOT,
    ):
        # TODO: when storing these knots, also store their state (open/closed, linked/unlinked, etc)
        preceding = read_control_point(buf)
        anchor = read_control_point(buf)
        leaving = read_control_point(buf)
    else:
        buf.read(24)
        # raise NotImplementedError(record_type)


def read_path_resource_block(buf: BinaryIO):
    first_record_type = PathDataRecordType(read_uint16(buf))
    assert first_record_type == PathDataRecordType.PATH_FILL_RULE
    first_record_data = buf.read(24)
    assert len(first_record_data) == 24
    assert all(c == 0 for c in first_record_data)

    while True:
        record_type_bytes = buf.read(2)
        if len(record_type_bytes) == 0:
            return
        assert len(record_type_bytes) == 2
        record_type_int = int.from_bytes(record_type_bytes, "big", signed=False)
        record_type = PathDataRecordType(record_type_int)
        record_bytes = buf.read(24)
        if len(record_bytes) == 0:
            return
        assert len(record_bytes) == 24
        read_path_record(BytesIO(record_bytes), record_type)
