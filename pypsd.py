# https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/

from enum import IntEnum
from io import BytesIO
from typing import BinaryIO


class ColorMode(IntEnum):
    Bitmap = 0
    Grayscale = 1
    Indexed = 2
    RGB = 3
    CMYK = 4
    Multichannel = 7
    Duotone = 8
    Lab = 9


class ResourceID(IntEnum):
    PS2_HEADER = 1000  # Obsolete Photoshop 2 only
    MACOSX_PRINT_MANAGER_PRINT_INFO_RECORD = 1001
    MACOSX_PAGE_FORMAT_INFO = 1002  # Obsolete No longer read by Photoshop
    PS2_INDEXED_COLOR_TABLE = 1003  # Obsolete Photoshop 2 only
    RESOLUTION_INFO = 1005
    ALPHA_CHANNEL_NAMES = 1006  # Names of the alpha channels as a series of Pascal strings.
    DISPLAY_INFO_1077 = 1007  # Obsolete
    CAPTION = 1008  # Caption as Pascal string

    # Border information.
    # Contains a fixed number (2 bytes real, 2 bytes fraction) for the border width,
    # and 2 bytes for border units (1 = inches, 2 = cm, 3 = points, 4 = picas, 5 = columns).
    BORDER_INFO = 1009

    BACKGROUND_COLOR = 1010
    PRINT_FLAGS = 1011
    GRAYSCALE_AND_MULTICHANNEL_HALFTONING_INFO = 1012
    COLOR_HALFTONING_INFO = 1013
    DUOTONE_HALFTONING_INFO = 1014
    GRAYSCALE_AND_MULTICHANNEL_TRANSFER_FUNCTION = 1015
    COLOR_TRANSFER_FUNCTIONS = 1016
    DUOTONE_TRANSFER_FUNCTIONS = 1017
    DUOTONE_IMAGE_INFORMATION = 1018
    DOT_RANGE = 1019  # Two bytes for the effective black and white values for the dot range
    UNNAMED1 = 1020  # Obsolete
    EPS_OPTIONS = 1021

    # Quick Mask information.
    # 2 bytes containing Quick Mask channel ID;
    # 1- byte boolean indicating whether the mask was initially empty.
    QUICK_MASK_INFO = 1022

    UNNAMED2 = 1023  # Obsolete

    # Layer state information.
    # 2 bytes containing the index of target layer (0 = bottom layer).
    LAYER_STATE_INFO = 1024

    WORKING_PATH = 1025

    # Layers group information.
    # 2 bytes per layer containing a group ID for the dragging groups.
    # Layers in a group have the same group ID.
    LAYERS_GROUP_INFO = 1026

    UNNAMED3 = 1027  # Obsolete
    IPTC_NAA_RECORD = 1028
    RAW_IMAGE_MODE = 1029
    JPEG_QUALITY = 1030  # Private

    PS4_GRID_AND_GUIDES_INFO = 1032
    PS4_THUMBNAIL = 1033
    PS4_COPYRIGHT_FLAG = 1034
    PS4_URL = 1035

    PS5_THUMBNAIL = 1036
    PS5_GLOBAL_ANGLE = 1037
    PS5_COLOR_SAMPLERS = 1038  # Obsolete
    PS5_ICC_PROFILE = 1039
    PS5_WATERMARK = 1040
    PS5_ICC_UNTAGGED_PROFILE = 1041
    PS5_EFFECTS_VISIBILITY = 1042
    PS5_SPOT_HALFTONE = 1043
    PS5_DOCUMENT_SPECIFIC_ID_SEED = 1044
    PS5_UNICODE_ALPHA_NAMES = 1045

    PS6_INDEXED_COLOR_TABLE_COUNT = 1046
    PS6_TRANSPARENCY_INDEX = 1047
    PS6_GLOBAL_ALTITUDE = 1049
    PS6_SLICES = 1050
    PS6_WORKFLOW_URL = 1051
    PS6_JUMP_TO_XPEP = 1052
    PS6_ALPHA_IDENTIFIERS = 1053
    PS6_URL_LIST = 1054
    PS6_VERSION_INFO = 1057

    PS7_EXIF_DATA_1 = 1058
    PS7_EXIF_DATA_3 = 1059
    PS7_XMP_METADATA = 1060
    PS7_CAPTION_DIGEST = 1061
    PS7_PRINT_SCALE = 1062

    PSCS_PIXEL_ASPECT_RATIO = 1064
    PSCS_LAYER_COMPS = 1065
    PSCS_ALTERNATE_DUOTONE_COLORS = 1066
    PSCS_ALTERNATE_SPOT_COLORS = 1067

    PSCS2_LAYER_SELECTION_IDS = 1069
    PSCS2_HDR_TONING_INFO = 1070
    PSCS2_PRINT_INFO = 1071
    PSCS2_LAYER_GROUPS_ENABLED_ID = 1072

    PSCS3_COLOR_SAMPLERS = 1073
    PSCS3_MEASUREMENT_SCALE = 1074
    PSCS3_TIMELINE_INFO = 1075
    PSCS3_SHEET_DISCLOSURE = 1076
    PSCS3_DISPLAY_INFO = 1077
    PSCS3_ONION_SKINS = 1078

    PSCS4_COUNT_INFO = 1080

    PSCS5_PRINT_INFO = 1082
    PSCS5_PRINT_STYLE = 1083
    PSCS5_MACOSX_PRINT_INFO = 1084
    PSCS5_WINDOWS_DEVMODE = 1085

    PSCS6_AUTO_SAVE_FILE_PATH = 1086
    PSCS6_AUTO_SAVE_FILE_FORMAT = 1087

    PSCC_PATH_SELECTION_STATE = 1088

    CLIPPING_PATH_NAME = 2999
    PSCC_ORIGIN_PATH_INFO = 3000

    IMAGE_READY_VARIABLES = 7000
    IMAGE_READY_DATASETS = 7001
    IMAGE_READY_DEFAULT_SELECTION_STATE = 7002
    IMAGE_READY_7_ROLLOVER_EXPANSION_STATE = 7003
    IMAGE_READY_ROLLOVER_EXPANSION_STATE = 7004
    IMAGE_READY_SAVE_LAYER_SETTINGS = 7005
    IMAGE_READY_VERSION = 7006

    PSCS3_LIGHTROOM_WORKFLOW = 8000
    PRINT_FLAGS_INFO = 10_000


INDEXED_COLOR_DATA_LENGTH = 768

indexed_color_table = None


def is_path_resource(resource_id: int):
    return 2000 <= resource_id <= 2997


def is_plugin_resource(resource_id: int):
    return 4000 <= resource_id <= 4999


def read_pascal_string(file: BinaryIO):
    length = max(file.read(1)[0], 1)
    # TODO: investigate the even size padding
    return file.read(length)


def read_unicode_string(file: BinaryIO):
    length = int.from_bytes(file.read(4), "big", signed=False)
    string = file.read(length * 2).decode("utf-8")
    n0, n1 = file.read(2)  # Read two byte null at end of string
    assert (n0 == 0) and (n1 == 0)
    return string


with open("/home/iyad/Desktop/placeholders-with-frames_ungrouped_color.psd", "rb") as file:

    # Header

    signature = file.read(4)
    assert signature == b"8BPS"

    version = int.from_bytes(file.read(2), "big", signed=False)
    assert version == 1

    _reserved = int.from_bytes(file.read(6), "big", signed=False)
    assert _reserved == 0

    channels_num = int.from_bytes(file.read(2), "big", signed=False)
    assert 1 <= channels_num <= 56

    image_height_pixels = int.from_bytes(file.read(4), "big", signed=False)
    assert (
        image_height_pixels <= 30_000
    )  # NOTE: PSD max is 30,000, while PSB format spec supports up to 300,000

    image_width_pixels = int.from_bytes(file.read(4), "big", signed=False)
    assert (
        image_width_pixels <= 30_000
    )  # NOTE: PSD max is 30,000, while PSB format spec supports up to 300,000

    depth = int.from_bytes(file.read(2), "big", signed=False)
    assert depth in (1, 8, 16, 32)

    color_mode = ColorMode(int.from_bytes(file.read(2), "big", signed=False))

    # Color Mode Data Section

    color_data_length = int.from_bytes(file.read(4), "big", signed=False)
    if color_mode == ColorMode.Indexed:
        assert color_data_length == INDEXED_COLOR_DATA_LENGTH
        indexed_color_table = file.read(INDEXED_COLOR_DATA_LENGTH)
        # TODO: de-interleave indexed color table
        # it seems that color table is 256 RGB, non-interleaved, so 256 red values, followed by 256 green, followed by 256 blue bytes
    elif color_mode == ColorMode.Duotone:
        # undocumented
        file.read(color_data_length)
    else:
        assert color_data_length == 0

    # Image Resources Section

    image_resources_section_length = int.from_bytes(file.read(4), "big", signed=False)
    image_resources_section_buf = BytesIO(file.read(image_resources_section_length))

    ## Image Resource Block
    while True:
        image_resource_signature = image_resources_section_buf.read(4)
        if len(image_resource_signature) == 0:
            break

        assert image_resource_signature == b"8BIM"
        image_resource_id = ResourceID(
            int.from_bytes(image_resources_section_buf.read(2), "big", signed=False)
        )
        image_resource_name = read_pascal_string(image_resources_section_buf)
        image_resource_data_length = int.from_bytes(
            image_resources_section_buf.read(4), "big", signed=False
        )
        # Data is padded to even length
        if (image_resource_data_length % 2) == 1:
            image_resource_data_length += 1

        image_resource_data = image_resources_section_buf.read(image_resource_data_length)
        image_resource_data_buf = BytesIO(image_resource_data)

        if image_resource_id == ResourceID.PS6_SLICES:
            slices_version = int.from_bytes(image_resource_data_buf.read(4), "big", signed=False)
            if slices_version in (7, 8):
                descriptor_version = int.from_bytes(
                    image_resource_data_buf.read(4), "big", signed=False
                )
            elif slices_version == 6:
                # TODO
                raise NotImplementedError
            else:
                raise RuntimeError(
                    f"Invalid PSD, slices version should be 6, 7 or 8, found {slices_version} instead."
                )
