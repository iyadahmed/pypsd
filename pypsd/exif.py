from enum import IntEnum
from typing import BinaryIO

from .utils import read_uint32, read_uint16


# Reference:
# https://www.media.mit.edu/pia/Research/deepview/exif.html#TiffHeader


class DataFormat(IntEnum):
    UNSIGNED_BYTE = 1
    ASCII_STRING = 2
    UNSIGNED_SHORT = 3
    UNSIGNED_LONG = 4
    UNSIGNED_RATIONAL = 5
    SIGNED_BYTE = 6
    UNDEFINED = 7
    SIGNED_SHORT = 8
    SIGNED_LONG = 9
    SIGNED_RATIONAL = 10
    SINGLE_FLOAT = 11
    DOUBLE_FLOAT = 12


class CameraOrientation(IntEnum):
    UPPER_LEFT = 1
    LOWER_RIGHT = 3
    UPPER_RIGHT = 6
    LOWER_LEFT = 8
    UNDEFINED = 9


class ResolutionUnit(IntEnum):
    NONE = 1
    INCH = 2
    CM = 3


class YCbCrPos(IntEnum):
    PIXEL_ARRAY_CENTER = 1
    DATUM_POINT = 2


class IFD0Tag(IntEnum):
    IMAGE_DESCRIPTION = 0x010E
    MANUFACTURER = 0x010F
    MODEL = 0x0110
    ORIENTATION = 0x0112
    X_RES = 0x011A
    Y_RES = 0x011B
    RES_UNIT = 0x0128
    FIRMWARE_VERSION = 0x0131
    DATE_TIME = 0x0132
    WHITE_POINT = 0x013E
    PRIMARY_CHROMATICITIES = 0x013F
    YCBCR_COEFF = 0x0211
    YCBCR_POS = 0x0213
    REF_BW = 0x0214
    COPYRIGHT = 0x8298
    SUB_IFD_OFFSET = 0x8769


def read_exif_data_1_resource(buf: BinaryIO):
    assert buf.read(2) == b"MM"
    assert buf.read(2) == b"\x00\x2A"
    zeroth_ifd_offset = read_uint32(buf)
    if zeroth_ifd_offset == 8:
        num_entries = read_uint16(buf)
        for _ in range(num_entries):
            tag_number = IFD0Tag(read_uint16(buf))
            data_format = DataFormat(read_uint16(buf))
            num_components = read_uint32(buf)
            data_value_or_offset_bytes = buf.read(4)
            if tag_number == IFD0Tag.ORIENTATION:
                orientation = CameraOrientation(int.from_bytes(data_value_or_offset_bytes[:2], "big", signed=False))
            # TODO: parse rest of data and store it

        next_ifd_offset = read_uint32(buf)
        # TODO: read rest of data (tip: use buf.seek)
    else:
        raise NotImplementedError
