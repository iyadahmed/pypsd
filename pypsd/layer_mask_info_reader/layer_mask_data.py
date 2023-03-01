from enum import IntFlag, auto
from typing import BinaryIO

from pypsd.utils import read_double, read_rectangle_uint32, read_uchar, read_uint32


class LayerMaskDataFlag(IntFlag):
    RELATIVE_POS = auto()  # "position relative to layer"
    DISABLED = auto()  # "layer mask disabled"
    INVERT = auto()  # "invert layer mask when blending (Obsolete)"

    # "indicates that the user mask actually came from rendering other data"
    RENDERED = auto()

    # "indicates that the user and/or vector masks have parameters applied to them"
    HAS_PARAMETERS = auto()


class MaskParametersFlag(IntFlag):
    USER_DENSITY = auto()
    USER_FEATHER = auto()
    VECTOR_DENSITY = auto()
    VECTOR_FEATHER = auto()


def read_layer_mask_data(buf: BinaryIO):
    size = read_uint32(buf)
    if size == 0:
        return
    rect = read_rectangle_uint32(buf)
    default_color = read_uchar(buf)
    assert default_color in (0, 255)

    flags = LayerMaskDataFlag(read_uchar(buf))

    if flags & LayerMaskDataFlag.HAS_PARAMETERS:
        mask_parameters = MaskParametersFlag(read_uchar(buf))
        if (mask_parameters & MaskParametersFlag.USER_DENSITY) or (mask_parameters & MaskParametersFlag.VECTOR_DENSITY):
            density = read_uchar(buf)
        elif (mask_parameters & MaskParametersFlag.USER_FEATHER) or (
            mask_parameters & MaskParametersFlag.VECTOR_FEATHER
        ):
            feather = read_double(buf)
        else:
            raise NotImplementedError

    if size == 20:
        # Padding
        assert len(buf.read(2)) == 2
    else:
        real_flags = read_uchar(buf)
        real_user_mask_background = read_uchar(buf)
        assert real_user_mask_background in (0, 255)
        rect2 = read_rectangle_uint32(buf)
