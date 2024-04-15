
from PIL import Image, ImageEnhance

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType, ImageEnhanceType

#===============================================================
# Class ImageActionEnhance
class ImageActionEnhance(ImageAction):
    def __init__(self, name, enhance_type : ImageEnhanceType = ImageEnhanceType.COLOR, scale = 1.0):
        super().__init__(name)
        self.enhance_type = enhance_type
        self.scale = 1.0
        
    def get_action_type(self):
        return ActionType.ENHANCE

    def get_enhance_type(self):
        return self.enhance_type

    def set_enhance_type(self, enhance_type : ImageEnhanceType):
        self.enhance_type = enhance_type
    
    def get_scale(self):
        return self.scale
    
    def set_scale(self, scale):    
        self.scale = scale
        
    def get_new_image(self, image: Image):
        enhancer = None
        if self.enhance_type == ImageEnhanceType.COLOR:
           enhancer = ImageEnhance.Sharpness(image)
        elif self.enhance_type == ImageEnhanceType.CONTRAST:
           enhancer = ImageEnhance.Contrast(image)
        elif self.enhance_type == ImageEnhanceType.BRIGHTNESS:
           enhancer = ImageEnhance.Brightness(image)
        elif self.enhance_type == ImageEnhanceType.SHARPNESS:
           enhancer = ImageEnhance.Sharpness(image)

        if enhancer:
            image = enhancer.enhance(self.scale)
        
        return image

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['EnhanceType'] = self.get_enum_export_name(self.enhance_type)
        dict['Scale'] = self.scale

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.enhance_type = self.get_enum_from_export_name(ImageEnhanceType, dict['EnhanceType'])
        self.scale = dict['Scale']
