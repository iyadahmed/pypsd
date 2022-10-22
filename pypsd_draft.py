# https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/

from dataclasses import asdict, dataclass
from enum import IntEnum
from io import BytesIO
from typing import BinaryIO, List
import json





class CompressionType(IntEnum):
    RAW = 0
    RLE = 1
    ZIP = 2
    ZIP_WITH_PREDICTION = 3


@dataclass
class ResourceBlock:
    pass


@dataclass
class ChannelInfo:
    channel_id: int
    channel_data_length: int


class ClippingType(IntEnum):
    BASE = 0
    NON_BASE = 1


@dataclass
class LayerRecord:
    rect: Rectangle
    num_channels: int
    channel_info: List[ChannelInfo]
    blend_mode_key: bytes
    opacity: int
    clipping: ClippingType
    name: bytes


def _read_image_resource_block(buffer: BinaryIO):
    signature = buffer.read(4)
    if len(signature) == 0:
        return
    assert signature == b"8BIM"
    identifier = ResourceID(read_uint16(buffer))
    name = read_pascal_string(buffer)
    data_length = read_uint32(buffer)

    # TODO: double check this logic
    if (data_length % 2) == 1:
        data_length += 1

    data_buf = BytesIO(buffer.read(data_length))
    if identifier == ResourceID.PS6_SLICES:
        slices_version = read_uint32(data_buf)
        if slices_version in (7, 8):
            descriptor_version = read_uint32(data_buf)
        elif slices_version == 6:
            raise NotImplementedError
        else:
            raise RuntimeError(
                f"Invalid PSD, slices version should be 6, 7 or 8, found {slices_version} instead."
            )

    return ResourceBlock()


def _read_image_resources_section(buffer: BinaryIO):
    data_length = read_uint32(buffer)
    data_buf = BytesIO(buffer.read(data_length))

    while True:
        block = _read_image_resource_block(data_buf)
        if block is None:
            break


def _read_layer_mask_adjustments_data(buffer: BinaryIO):
    # TODO: incomplete function
    size = read_uint32(buffer)
    if size == 0:
        return

    data_buf = BytesIO(buffer.read(size))

    rect = read_rectangle_uint32(data_buf)
    default_color = data_buf.read(1)[0]
    flags = data_buf.read(1)[0]
    if flags & (1 << 4):
        mask_parameters = data_buf.read(1)[0]

    if size == 20:
        _padding = data_buf.read(2)
    else:
        real_flags = data_buf.read(1)[0]
        real_user_mask_background = data_buf.read(1)[0]
        _rect = read_rectangle_uint32(data_buf)


def _read_layer_blending_ranges_data(buffer: BinaryIO, channels_count: int):
    data_length = read_uint32(buffer)
    data_buf = BytesIO(buffer.read(data_length))

    composite_gray_blend_source = data_buf.read(4)
    composite_gray_blend_destination_range = data_buf.read(4)
    for _ in range(channels_count):
        nth_channel_source_range = data_buf.read(4)
        nth_channel_destination_range = data_buf.read(4)

    assert len(data_buf.read()) == 0


def _read_layer_records(buffer: BinaryIO):
    rect = read_rectangle_uint32(buffer)
    channels_count = read_uint16(buffer)

    channel_info = []

    for _ in range(channels_count):
        channel_id = read_int16(buffer)
        channel_data_length = read_uint32(buffer)
        channel_info.append(ChannelInfo(channel_id, channel_data_length))

    blend_mode_signature = buffer.read(4)
    assert blend_mode_signature == b"8BIM"

    blend_mode_key = buffer.read(4)
    opacity = buffer.read(1)[0]
    clipping_type = ClippingType(buffer.read(1)[0])
    flags = buffer.read(1)[0]

    _filler = buffer.read(1)[0]
    assert _filler == 0

    extra_data_length = read_uint32(buffer)
    extra_data_buf = BytesIO(buffer.read(extra_data_length))

    _read_layer_mask_adjustments_data(extra_data_buf)
    _read_layer_blending_ranges_data(extra_data_buf, channels_count)
    layer_name = read_pascal_string(extra_data_buf)

    # assert len(extra_data_buf.read()) == 0

    return LayerRecord(
        rect, channels_count, channel_info, blend_mode_key, opacity, clipping_type, layer_name
    )


def _unpack_bits_rle(data: bytes):
    output = []
    i = 0
    while i < len(data):
        count = data[i]
        assert 0 <= count <= 255
        if count >= 128:
            count = 256 - count
            for j in range(count + 1):
                output.append(data[i + 1])
            i += 1
        else:
            for j in range(count + 1):
                output.append(data[i + j + 1])
            i += count

        i += 1
    return output


def _unpack_bits_rle2(data: bytes):
    output = []
    i = 0
    while i < len(data) - 1:
        flag_counter = data[i]
        assert 0 <= flag_counter <= 255
        if flag_counter == 128:  # -128
            i += 1

        elif 0 <= flag_counter <= 127:  # positive
            output.extend(data[i + 1 : i + 1 + flag_counter + 1])
            i += flag_counter + 1 + 1

        elif 128 < flag_counter <= 255:  # negative
            for _ in range(256 - flag_counter + 1):
                output.append(data[i + 1])
            i += 2

        else:
            assert False
    return output


def test_unpack_bits_rle():
    compressed = "FE AA 02 80 00 2A FD AA 03 80 00 2A 22 F7 AA".split(" ")
    compressed_bytes = bytes(int(v, base=16) for v in compressed)
    uncompressed = " ".join(
        hex(v)[2:].upper().zfill(2) for v in _unpack_bits_rle2(compressed_bytes)
    )
    expected = "AA AA AA 80 00 2A AA AA AA AA 80 00 2A 22 AA AA AA AA AA AA AA AA AA AA"
    assert uncompressed == expected


test_unpack_bits_rle()


def _read_channel_image_data(buffer: BinaryIO, image_width: int, image_height: int):
    compression_type = CompressionType(read_uint16(buffer))
    if compression_type == CompressionType.RAW:
        buffer.read(image_width * image_height)
    elif compression_type == CompressionType.RLE:
        pass
        # for _ in range(image_height):
        #     byte_count = read_uint16(buffer)
        #     print(byte_count)
        #     compressed_row = buffer.read(byte_count)
        # assert len(compressed_row) == byte_count

        # uncompressed_row = _unpack_bits_rle2(compressed_row)
    else:
        raise NotImplementedError


from pprint import pprint


def _read_layer_info(buffer: BinaryIO):
    data_length = read_uint32(buffer)
    assert (data_length % 2) == 0

    data_buf = BytesIO(buffer.read(data_length))

    layer_count = read_int16(data_buf)

    records = [_read_layer_records(data_buf) for _ in range(layer_count)]

    for rec in records:
        height = rec.rect.bottom - rec.rect.top
        width = rec.rect.right - rec.rect.left
        for _ in range(rec.num_channels):
            compression_type = CompressionType(read_uint16(data_buf))
            if compression_type == CompressionType.RAW:
                data_buf.read(width * height)
            elif compression_type == CompressionType.RLE:
                for _ in range(height):
                    byte_count = read_uint16(data_buf)
                    data_buf.read(byte_count)
            else:
                raise NotImplementedError
        pprint(asdict(rec))

    # height, width = (rect.bottom - rect.top), (rect.right - rect.left)
    # assert height >= 0
    # assert width >= 0
    # _read_channel_image_data(data_buf, width, height)

    # assert len(data_buf.read()) == 0


def _read_layer_and_mask_info_section(buffer: BinaryIO):
    data_length = read_uint32(buffer)
    data_buf = BytesIO(buffer.read(data_length))

    _read_layer_info(data_buf)
