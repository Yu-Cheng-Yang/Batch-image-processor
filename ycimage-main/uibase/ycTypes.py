from enum import Enum

class ActionType(Enum):
    CROP            = 0
    ENHANCE         = 1
    FILTER          = 2 
    RESIZE          = 3
    ROTATE          = 4
    TRANSFORM       = 5
    WATERMARK       = 6
    RENAME          = 7

class ImageWatermarkType(Enum):
    TEXT = 0
    IMAGE = 1
    
class ImageResizeType(Enum):
    SCALE  = 0
    WIDTH = 1
    HEIGHT = 2
    WIDTH_AND_HEIGHT = 3
    SQUARE = 4

class ImageResamplingType(Enum):
    BICUBIC  = 1
    BILINEAR = 2
    BOX      = 3
    HAMMING  = 4
    LANCZOS  = 5
    NEAREST  = 6

class ImageTransformType(Enum):
    FLIP      = 0
    MIRROR    = 1
    INVERT    = 2
    GRAYSCALE = 3
    SCALE     = 4
    EXPAND    = 5

class ImageEnhanceType(Enum):
    BRIGHTNESS  = 0
    COLOR       = 1
    CONTRAST    = 2
    SHARPNESS   = 3

class ImageFilterType(Enum):
    PREDEFINED_FILTER = 0
    STANDARD_FILTER   = 1
    
class ImagePredefinedFilterType(Enum):
    BLUR               = 0
    CONTOUR            = 1 
    DETAIL             = 2
    EDGE_ENHANCE       = 3 
    EDGE_ENHANCE_MORE  = 4
    EMBOSS             = 5 
    FIND_EDGES         = 6
    SHARPEN            = 7
    SMOOTH             = 8
    SMOOTH_MORE        = 9

class ImageStandardFilterType(Enum):
    BOX_BLUR      = 0
    GAUSSIAN_BLUR = 1
    MAX_FILTER    = 2
    MEDIAN_FILTER = 3
    MIN_FILTER    = 4
    MODE_FILTER   = 5
    RANK_FILTER   = 6
    UNSHARP_MASK  = 7
    
class RenameType(Enum):
    REMOVE    = 0
    REPLACE   = 1
    ADD       = 2
    ORDER     = 3
    
class RenameAddType(Enum):
    PREFIX  = 0
    SUFFIX  = 1
    INSERT_POSITION = 2
    INSERT_BEFORE   = 3
    INSERT_AFTER    = 4

class RenameRemoveType(Enum):
    LEFT_TRUNCATE    = 0
    RIGHT_TRUNCATE   = 1
    SUBSTRING_REMOVE = 2

class RenameReplaceType(Enum):
    NORMAL = 0
    REGEX  = 1
    ALL    = 2

class RenameOrderPositionType(Enum):
    PREFIX  = 0
    SUFFIX  = 1
    INSERT  = 2

class RenameOrderByType(Enum):
    FILE_LIST           = 0
    FILE_NAME           = 1
    FILE_CREATION_TIME  = 2
    FILE_SIZE           = 3
    FILE_EXIF_TIME      = 4

class RenameOccurrenceType(Enum):
    FIRST  = 0
    SECOND = 1
    THIRD  = 2
    LAST   = 4
    ALL    = 5
