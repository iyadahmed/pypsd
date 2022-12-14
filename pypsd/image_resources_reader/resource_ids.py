from enum import IntEnum


def is_path_resource(resource_id: int):
    return 2000 <= resource_id <= 2997


def is_plugin_resource(resource_id: int):
    return 4000 <= resource_id <= 4999


class ResourceID(IntEnum):
    PS2_HEADER = 1000  # Obsolete Photoshop 2 only
    MACOSX_PRINT_MANAGER_PRINT_INFO_RECORD = 1001
    MACOSX_PAGE_FORMAT_INFO = 1002  # Obsolete No longer read by Photoshop
    PS2_INDEXED_COLOR_TABLE = 1003  # Obsolete Photoshop 2 only
    RESOLUTION_INFO = 1005

    # Names of the alpha channels as a series of Pascal strings.
    ALPHA_CHANNEL_NAMES = 1006

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

    # Two bytes for the effective black and white values for the dot range
    DOT_RANGE = 1019

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
