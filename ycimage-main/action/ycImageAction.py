import os
import piexif

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

from ycLocalize import localize

from uibase.ycTypes import ActionType

def get_enum_from_name(enum_class, name):
    return next((item for item in enum_class if item.name == name), None)

def get_enum_value_index(enum_value):
    return next((item for item in enum_value.__class__ if item.value == enum_value), None)

# The enum values should be defined from 0 to len(enum_class) - 1 in order
def get_enum_from_index(enum_class, index):
    index = min(max(index, 0), len(enum_class) - 1)
    return enum_class(index)

def get_enum_export_name(enum_value):
    return ' '.join(name.capitalize() for name in enum_value.name.split('_'))

def get_enum_display_name(enum_value):
    return localize(get_enum_export_name(enum_value))

def get_enum_from_export_name(enum_class, name : str):
    return get_enum_from_name(enum_class, name.replace(' ', '_').upper())

def get_export_names_from_enum_class(enum_class):
    return [get_enum_export_name(item) for item in enum_class]

def get_display_names_from_enum_class(enum_class):
    return [get_enum_display_name(item) for item in enum_class]

# Load image and apply rotation in exif to image
def load_image(file_name, apply_transform = True):
    image, _ = load_image_and_exif(file_name, apply_transform, False)
    return image

# Load image and exif. Note: even transform is applied to the image, the rotation
# is still in exif_dict, user should process it carefully.
def load_image_and_exif(file_name, apply_transform = True, load_exif = True):
    register_heif_opener()
    
    # If file doesn't exist, return None image
    if not os.path.isfile(file_name):
        return None
    
    image = None
    try:
        image = Image.open(file_name)
    except:
        # Not image file or not supported format
        image = None

    # Get exif information before exif_transpose to get the rotation
    # First using exif in image info to get the information, if it fails,
    # using image.geteixf()
    # It seems image.getexif() doesn't work well
    exif_dict = {}
    if load_exif and image:
        exif_info = image.info['exif'] if 'exif' in image.info else None
        if exif_info:
            exif_dict = piexif.load(exif_info) if exif_info else None
        else:
            _, ext = os.path.splitext(file_name)
            ext = ext.lower()
            if ext == '.jpg' or ext == '.jpeg' or ext == '.tif' or ext == '.tiff':
                exif_dict = piexif.load(file_name)
            # exif = image.getexif()
            # exif_dict['0th'] = dict(exif.items())
    
    # when rotation is defined in exif, PIL image open and display image has a rotation
    # adjust the image based on exif rotation
    if image and apply_transform:
        image = ImageOps.exif_transpose(image)
    
    return image, exif_dict
    
def save_image(image, filename, quality = 95, exif_dict : dict = None):
    exif = None
    if not exif_dict: 
        # If no exif specified, the original exif infomation will be kept
        exif_dict = get_exif_dict(image)
    
    if exif_dict:
        exif = dump_exif_dict(exif_dict)
    
    # The image quality, on a scale from 1 (worst) to 95 (best).
    # In PIL, The default is 75. Values above 95 should be avoided;
    # 100 disables portions of the JPEG compression algorithm, and
    # results in large files with hardly any gain in image quality
    if image.mode == "RGBA":
        image = image.convert("RGB")
        
    if exif:
        image.save(filename, quality = quality, subsampling = 0, exif = exif)
    else:
        image.save(filename, quality = quality, subsampling = 0)

def get_exif_dict(image):
    image_exif_info = image.info['exif'] if 'exif' in image.info else None
    exif_dict = piexif.load(image_exif_info) if image_exif_info else None
    return exif_dict

# Walkaround for dump issue in piexif
def dump_exif_dict(exif_dict: dict) :
    undefined_tags = [
        # (34856, 'tuple'), # OECF
        (37121, 'tuple'), # ComponentsConfiguration
        # (37388, 'tuple'), # SpatialFrequencyResponse
        # (37389, 'tuple'), # Noise
        (37500, 'tuple'), # MakerNote
        (37510, 'tuple'), # UserComment
        (41729, 'int'),   # SceneType
        # (41730, 'tuple'), # CFAPattern
        # (41995, 'tuple'), # DeviceSettingDescription
        # (50341, 'tuple'), # PrintImageMatching
    ]
    for tag in undefined_tags:
        value = exif_dict['Exif'].get(tag[0])
        if value and tag[1] == 'tuple' and isinstance(value, tuple):
            exif_dict['Exif'][tag[0]] = ",".join([str(item) for item in value]).encode(errors="ignore")
        if value and tag[1] == 'int' and isinstance(value, int):
            exif_dict['Exif'][tag[0]] = str(value).encode(errors="ignore")

    exif_bytes = piexif.dump(exif_dict)   
     
    return exif_bytes

#===============================================================
# Class Action
class Action():
    def __init__(self, name):
        self.name = name

    def get_action_type(self):
        return None
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def is_image_action(self):
        return False

    def is_rename_action(self):
        return False

    def is_exif_action(self):
        return False

    def get_new_base_name(self, file_name : str, exif = None):
        return os.path.basename(file_name)

    def get_new_image(self, image: Image):
        return image
    
    def get_new_exif(self, exif):
        return exif
    
    def need_pre_process():
        return False
    
    def pre_process(self, files):
        pass
    
    def post_process(self):
        pass

    def validate(self):
        validate_result = []
        if self.name == '':
            validate_result.append(('Name', 'Name can\'t be empty'))
        self._validate_internal(validate_result)
        return validate_result

    def _validate_internal(self):
        pass

    def write_to_dict(self, dict):
        dict['ActionName'] = self.get_enum_export_name(self.get_action_type())
        dict['Name'] = self.name

    def read_from_dict(self, dict):
        assert dict['ActionName'] == self.get_enum_export_name(self.get_action_type())
        self.name = dict['Name']

    def get_enum_export_name(self, enum_value):
        return get_enum_export_name(enum_value)

    def get_enum_from_export_name(self, enum_class, name : str):
        return get_enum_from_export_name(enum_class, name)

#===============================================================
# Class ImageActionBase
class ImageAction(Action):
    def __init__(self, name):
        super().__init__(name)

    def is_image_action(self):
        return True
