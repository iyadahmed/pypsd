from io import BytesIO
from typing import BinaryIO

from .color import read_color
from .color_mode import _read_color_mode_data
from .exif import read_exif_data_1_resource
from .grid_guide_info import read_guide_resource_block
from .header import _read_header
from .print_scale import read_print_scale
from .resolution_info import read_resolution_info
from .resource_blocks import iter_resource_blocks
from .resource_ids import ResourceID
from .slices import read_slices, read_descriptor_structure
from .thumbnail import read_thumbnail_resource
from .path import read_path_resource_block
from .utils import read_uint32, read_uint16, read_uchar, read_unicode_string, read_double


def read_caption_digest(buf: BinaryIO):
    rsa_md5_digest = buf.read()
    assert len(rsa_md5_digest) == 16


def read_descriptor_with_version_check(buf: BinaryIO):
    descriptor_version = read_uint32(buf)
    assert descriptor_version == 16
    read_descriptor_structure(buf)


def read_print_info(buf: BinaryIO):
    read_descriptor_with_version_check(buf)


def read_print_style(buf: BinaryIO):
    read_descriptor_with_version_check(buf)


def read_origin_path_info(buf: BinaryIO):
    read_descriptor_with_version_check(buf)


def read_xmp_metadata(buf: BinaryIO):
    buf.read()  # File info in XML format


def read_global_angle(buf: BinaryIO):
    angle = read_uint32(buf)
    assert 0 <= angle <= 359


def read_global_altitude(buf: BinaryIO):
    altitude = read_uint32(buf)


def read_print_flags(buf: BinaryIO):
    print_flags = buf.read()


def read_print_flags_info(buf: BinaryIO):
    version = read_uint16(buf)
    assert version == 1
    center_crop_marks = read_uchar(buf)
    assert read_uchar(buf) == 0
    bleed_width_value = read_uint32(buf)
    bleed_width_scale = read_uint16(buf)


def read_color_halftoning_info(buf: BinaryIO):
    buf.read()


def read_color_transfer_function(buf: BinaryIO):
    buf.read()


def read_layer_state_info(buf: BinaryIO):
    target_layer_index = read_uint16(buf)


def read_layers_group_info(buf: BinaryIO):
    groups_ids_bytes = buf.read()
    num_bytes = len(groups_ids_bytes)
    assert (num_bytes % 2) == 0
    for i in range(0, num_bytes, 2):
        gid = int.from_bytes(groups_ids_bytes[i: i + 2], "big", signed=False)


def read_layer_groups_enabled_id(buf: BinaryIO):
    buf.read()


def read_layer_selection_ids(buf: BinaryIO):
    count = read_uint16(buf)
    for _ in range(count):
        layer_id = read_uint32(buf)


def read_url_list(buf: BinaryIO):
    count = read_uint32(buf)
    for _ in range(count):
        url_id = read_uint32(buf)
        url = read_unicode_string(buf)


def read_pixel_aspect_ratio(buf: BinaryIO):
    version = read_uint32(buf)
    assert version in (1, 2)
    x_over_y = read_double(buf)


def read_icc_profile(buf: BinaryIO):
    raw_icc_file = buf.read()


def read_document_id_seed(buf: BinaryIO):
    seed = read_uint32(buf)


def read_version_info(buf: BinaryIO):
    version = read_uint32(buf)
    has_real_merged_data = read_uchar(buf)
    writer_name = read_unicode_string(buf)
    reader_name = read_unicode_string(buf)
    file_version = read_uint32(buf)


def read_alpha_channel_names(buf: BinaryIO):
    while True:
        n = buf.read(1)[0]
        if n == 0:
            break
        name = buf.read(n)


def read_unicode_alpha_channel_names(buf: BinaryIO):
    # FIXME: there's a null at the end??
    name = read_unicode_string(buf)


def read_alpha_identifiers(buf: BinaryIO):
    length = read_uint32(buf)
    for _ in range(length):
        identifier = buf.read(4)


def read_psd(filepath: str):
    with open(filepath, "rb") as file:

        # Header
        header = _read_header(file)
        _read_color_mode_data(file, header.color_mode)

        for rblock in iter_resource_blocks(file):
            buf = BytesIO(rblock.data)

            if rblock.rid == ResourceID.PS6_SLICES:
                read_slices(buf)

            elif rblock.rid == ResourceID.IPTC_NAA_RECORD:
                pass

            elif rblock.rid == ResourceID.PS7_CAPTION_DIGEST:
                read_caption_digest(buf)

            elif rblock.rid == ResourceID.PS7_XMP_METADATA:
                read_xmp_metadata(buf)

            elif rblock.rid == ResourceID.PSCS5_PRINT_INFO:
                read_print_info(buf)

            elif rblock.rid == ResourceID.PSCS5_PRINT_STYLE:
                read_print_style(buf)

            elif rblock.rid == ResourceID.RESOLUTION_INFO:
                read_resolution_info(buf)

            elif rblock.rid == ResourceID.PS7_PRINT_SCALE:
                read_print_scale(buf)

            elif rblock.rid == ResourceID.BACKGROUND_COLOR:
                read_color(buf)

            elif rblock.rid == ResourceID.PS5_GLOBAL_ANGLE:
                read_global_angle(buf)

            elif rblock.rid == ResourceID.PS6_GLOBAL_ALTITUDE:
                read_global_altitude(buf)

            elif rblock.rid == ResourceID.PRINT_FLAGS:
                read_print_flags(buf)

            elif rblock.rid == ResourceID.PRINT_FLAGS_INFO:
                read_print_flags_info(buf)

            elif rblock.rid == ResourceID.COLOR_HALFTONING_INFO:
                read_color_halftoning_info(buf)

            elif rblock.rid == ResourceID.COLOR_TRANSFER_FUNCTIONS:
                read_color_transfer_function(buf)

            elif rblock.rid == ResourceID.LAYER_STATE_INFO:
                read_layer_state_info(buf)

            elif rblock.rid == ResourceID.LAYERS_GROUP_INFO:
                read_layers_group_info(buf)

            elif rblock.rid == ResourceID.PSCS2_LAYER_GROUPS_ENABLED_ID:
                read_layer_groups_enabled_id(buf)

            elif rblock.rid == ResourceID.PSCS2_LAYER_SELECTION_IDS:
                read_layer_selection_ids(buf)

            elif rblock.rid == ResourceID.PS4_GRID_AND_GUIDES_INFO:
                read_guide_resource_block(buf)

            elif rblock.rid == ResourceID.PS6_URL_LIST:
                read_url_list(buf)

            elif rblock.rid == ResourceID.PSCS_PIXEL_ASPECT_RATIO:
                read_pixel_aspect_ratio(buf)

            elif rblock.rid == ResourceID.PS5_ICC_PROFILE:
                read_icc_profile(buf)

            elif rblock.rid == ResourceID.PS5_DOCUMENT_SPECIFIC_ID_SEED:
                read_document_id_seed(buf)

            elif rblock.rid == ResourceID.PS5_THUMBNAIL:
                read_thumbnail_resource(buf)

            elif rblock.rid == ResourceID.PS6_VERSION_INFO:
                read_version_info(buf)

            elif rblock.rid == ResourceID.PS7_EXIF_DATA_1:
                read_exif_data_1_resource(buf)

            elif rblock.rid == ResourceID.ALPHA_CHANNEL_NAMES:
                read_alpha_channel_names(buf)

            elif rblock.rid == ResourceID.PS5_UNICODE_ALPHA_NAMES:
                read_unicode_alpha_channel_names(buf)

            elif rblock.rid == ResourceID.PSCS3_DISPLAY_INFO:
                # Obsolete according to PSD documentation
                pass

            elif rblock.rid == ResourceID.PS6_ALPHA_IDENTIFIERS:
                read_alpha_identifiers(buf)

            elif rblock.rid == ResourceID.WORKING_PATH:
                read_path_resource_block(buf)

            elif rblock.rid == ResourceID.PSCC_ORIGIN_PATH_INFO:
                read_origin_path_info(buf)

            else:
                raise NotImplementedError(repr(rblock.rid))
