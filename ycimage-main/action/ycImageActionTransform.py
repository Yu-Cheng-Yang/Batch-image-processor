
from PIL import Image, ImageOps

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType, ImageTransformType

#===============================================================
# Class ImageActionTransform
class ImageActionTransform(ImageAction):
    def __init__(self, name, transform_type = ImageTransformType.FLIP):
        super().__init__(name)
        self.transform_type = transform_type
        self.scale = 1.0
        self.scale_resampling_type = Image.Resampling.NEAREST
        self.expand_border = 0
        self.expand_fill_color = (0, 0, 0)
        
    def get_action_type(self):
        return ActionType.TRANSFORM

    def get_transform_type(self):
        return self.transform_type

    def set_transform_type(self, transform_type):
        self.transform_type = transform_type
    
    def get_scale(self):
        return self.scale
    
    def set_scale(self, scale):    
        self.scale = scale
        
    def get_scale_resampling_type(self):
        return self.scale_resampling_type
    
    def set_scale_resampling_type(self, scale_resampling_type):    
        self.scale_resampling_type = scale_resampling_type

    def get_expand_border(self):
        return self.expand_border

    def set_expand_border(self, border):
        self.expand_border = border if border >= 0 else 0
    
    def get_expand_fill_color(self):
        return self.expand_fill_color

    def set_expand_fill_color(self, fill_color):
        self.expand_fill_color = fill_color

    def get_new_image(self, image: Image):
        if self.transform_type == ImageTransformType.FLIP:
           image = ImageOps.flip(image)
        elif self.transform_type == ImageTransformType.MIRROR:
           image = ImageOps.mirror(image)
        elif self.transform_type == ImageTransformType.INVERT:
            if image.mode == "RGBA":
                # Invert doesn't support RGBA mode
                # Convert to RGB and invert it. 
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask = image.split()[3]) # 3 is the alpha channel
                image = ImageOps.invert(rgb_image)
            else:
                image = ImageOps.invert(image)
        elif self.transform_type == ImageTransformType.GRAYSCALE:
           image = ImageOps.grayscale(image)
        elif self.transform_type == ImageTransformType.EXPAND:
           image = ImageOps.expand(image, self.expand_border, self.expand_fill_color)
        elif self.transform_type == ImageTransformType.SCALE:
           image = ImageOps.scale(image, self.scale, self.scale_resampling_type)
        
        return image

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['TransformType'] = self.get_enum_export_name(self.transform_type)
        if self.transform_type == ImageTransformType.SCALE: 
            dict['Scale'] = self.scale
            dict['ScaleResamplingType'] = self.get_enum_export_name(self.scale_resampling_type)
        elif self.transform_type == ImageTransformType.EXPAND:
            dict['ExpandBorder'] = self.expand_border
            dict['ExpandFillColor'] = self.expand_fill_color

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.transform_type = self.get_enum_from_export_name(ImageTransformType, dict['TransformType'])
        if self.transform_type == ImageTransformType.SCALE: 
            self.scale = dict['Scale']
            self.scale_resampling_type = self.get_enum_from_export_name(dict['ScaleResamplingType'])
        elif self.transform_type == ImageTransformType.EXPAND:
            self.expand_border = dict['ExpandBorder']
            self.expand_fill = dict['ExpandFill']
