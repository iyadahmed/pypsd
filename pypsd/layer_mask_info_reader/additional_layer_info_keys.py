from enum import Enum, unique


@unique
class AdditionalLayerKey(Enum):
    # Adjustment layer (Photoshop 4.0)
    # SOLID_COLOR = b"SoCo"
    # GRADIENT = b"GdFl"
    # PATTERN = b"PtFl"
    # BRIGHTNESS_CONTRAST = b"brit"
    # LEVELS = b"levl"
    # CURVES = b"curv"
    # EXPOSURE = b"expA"
    # VIBRANCE = b"vibA"
    # OLD_HUE = b"hue"
    # NEW_HUE = b"hue2"
    # COLOR_BALANCE = b"blnc"
    # BLACK_AND_WHITE = b"blwh"
    # PHOTO_FILTER = b"phfl"
    # CHANNEL_MIXER = b"mixr"
    # COLOR_LOOKUP = b"clrL"
    # INVERT = b"nvrt"
    # POSTERIZE = b"post"
    # THRESHOLD = b"thrs"
    # GRADIENT_MAP = b"grdm"
    # SELECTIVE_COLOR = b"selc"

    # Effects layer
    EFFECTS = b"lrFX"

    # Type Tool Info (Photoshop 5.0 and 5.5 only)
    TYPE_TOOL_PS5 = b"tySh"

    # Unicode layer name (Photoshop 5.0)
    UNICODE_LAYER_NAME = b"luni"

    # Layer ID (Photoshop 5.0)
    LAYER_ID = b"lyid"

    # Object-based effects layer info (Photoshop 6.0)
    OBJECT_BASED_EFFECTS = b"lfx2"

    # Patterns (Photoshop 6.0 and CS (8.0))
    PATTERN_1 = b"Patt"
    PATTERN_2 = b"Pat2"
    PATTERN_3 = b"Pat3"

    # Annotations (Photoshop 6.0)
    ANNOTATIONS = b"Anno"

    # Blend clipping elements (Photoshop 6.0)
    BLEND_CLIPPING_ELEMENTS = b"clbl"

    # Blend interior elements (Photoshop 6.0)
    BLEND_INTERIOR_ELEMENTS = b"infx"

    # Knockout setting (Photoshop 6.0)
    KNOCKOUT_SETTING = b"knko"

    # Protected setting (Photoshop 6.0)
    PROTECTED_SETTING = b"lspf"

    # Sheet color setting (Photoshop 6.0)
    SHEET_COLOR_SETTING = b"lclr"

    # Reference point (Photoshop 6.0)
    REFERENCE_POINT = b"fxrp"

    # Gradient settings (Photoshop 6.0)
    GRADIENT_SETTINGS = b"grdm"

    # Section divider setting (Photoshop 6.0)
    SECTION_DIVIDER_SETTNING = b"lsct"

    # Channel blending restrictions setting (Photoshop 6.0)
    CHANNEL_BLENDING_RESTRICTIONS_SETTING = b"brst"

    # Solid color sheet setting (Photoshop 6.0)
    SOLID_COLOR_SHEET_SETTING = b"SoCo"

    # Pattern fill setting (Photoshop 6.0)
    PATTERN_FILL_SETTING = b"PtFl"

    # Gradient fill setting (Photoshop 6.0)
    GRADIENT_FILL_SETTING = b"GdFl"

    # Vector mask setting (Photoshop 6.0)
    # Key is 'vmsk' or 'vsms'. If key is 'vsms' then we are writing for (Photoshop CS6) and the document will have a 'vscg' key.
    VECTOR_MASK_SETTING_1 = b"vmsk"
    VECTOR_MASK_SETTING_2 = b"vsms"

    # Type tool object setting (Photoshop 6.0)
    TYPE_TOOL = b"TySh"

    # Foreign effect ID (Photoshop 6.0)
    FOREIGN_EFFECT_ID = b"ffxi"

    # Layer name source setting (Photoshop 6.0)
    LAYER_NAME_SOURCE_SETTING = b"lnsr"

    # Pattern data (Photoshop 6.0)
    PATTERN_DATA = b"shpa"

    # Metadata setting (Photoshop 6.0)
    METADATA_SETTING = b"shmd"

    # Layer version (Photoshop 7.0)
    LAYER_VERSION = b"lyvr"

    # Transparency shapes layer (Photoshop 7.0)
    TRANSPARENCY_SHAPES_LAYER = b"tsly"

    # Layer mask as global mask (Photoshop 7.0)
    LAYER_MASK_AS_GLOBAL_MASK = b"lmgm"

    # Vector mask as global mask (Photoshop 7.0)
    VECTOR_MASK_AS_GLOBAL_MASK = b"vmgm"

    # Brightness and Contrast
    BRIGHTNESS_AND_CONTRAST = b"brit"

    # Channel Mixer
    CHANNEL_MIXER = b"mixr"

    # Color Lookup (Photoshop CS6)
    COLOR_LOOKUP = b"clrL"

    # Placed Layer (replaced by SoLd in Photoshop CS3)
    PLACED_LAYER = b"plLd"

    # Linked Layer
    LINKED_LAYER_1 = b"lnkD"
    LINKED_LAYER_2 = b"lnk2"
    LINKED_LAYER_3 = b"lnk3"

    # Photo Filter
    PHOTO_FILTER = b"phfl"

    # Black White (Photoshop CS3)
    BLACK_WHITE = b"blwh"

    # Content Generator Extra Data (Photoshop CS5)
    CONTENT_GENERATOR_EXTRA_DATA = b"CgEd"

    # Text Engine Data (Photoshop CS3)
    TEXT_ENGINE_DATA = b"Txt2"

    # Vibrance (Photoshop CS3)
    VIBRANCE = b"vibA"

    # Unicode Path Name (Photoshop CS6)
    UNICODE_PATH_NAME = b"pths"

    # Animation Effects (Photoshop CS6)
    ANIMATION_EFFECTS = b"anFX"

    # Filter Mask (Photoshop CS3)
    FILTER_MASK = b"FMsk"

    # Placed Layer Data (Photoshop CS3)
    PLACED_LAYER_DATA = b"SoLd"

    # Vector Stroke Data (Photoshop CS6)
    VECTOR_STROKE_DATA = b"vstk"

    # Vector Stroke Content Data (Photoshop CS6)
    VECTOR_STROKE_CONTENT_DATA = b"vscg"

    # Using Aligned Rendering (Photoshop CS6)
    USING_ALIGNED_RENDERING = b"sn2P"

    # Vector Origination Data (Photoshop CC)
    VECTOR_ORIGINATION_DATA = b"vogk"

    # Pixel Source Data (Photoshop CC)
    PIXEL_SOURCE_DATA_CC = b"PxSc"

    # Compositor Used (Photoshop 2020)
    COMPOSITOR_USED = b"cinf"

    # Pixel Source Data (Photoshop CC 2015)
    PIXEL_SOURCE_DATA_CC_15 = b"PxSD"

    # Artboard Data (Photoshop CC 2015)
    ARTBOARD_DATA_1 = b"artb"
    ARTBOARD_DATA_2 = b"artd"
    ARTBOARD_DATA_3 = b"abdd"

    # Smart Object Layer Data (Photoshop CC 2015)
    SMART_OBJECT_LAYER_DATA = b"SoLE"

    # Saving Merged Transparency
    SAVING_MERGED_TRANSPARENCY = b"Mtrn"
    SAVING_MERGED_TRANSPARENCY_16 = b"Mt16"
    SAVING_MERGED_TRANSPARENCY_32 = b"Mt32"

    # User Mask
    USER_MASK = b"LMsk"

    # Exposure
    EXPOSURE = b"expA"

    # Filter Effects
    FILTER_EFFECTS_1 = b"FXid"
    FILTER_EFFECTS_2 = b"FEid"
