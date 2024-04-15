
from PIL import Image, ImageFilter

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType
   
#===============================================================
# Class ImageActionRotate
class ImageActionRotate(ImageAction):
    def __init__(self, name, rotation = 0):
        super().__init__(name)
        self.rotation = rotation
        self.use_blur = False
        self.blur_radius = 10
        self.fill_color = (0, 0, 0)
        self.expand = 1
    
    def get_action_type(self):
        return ActionType.ROTATE

    def get_rotation(self):
        return self.rotation
    
    def set_rotation(self, rotation):
        self.rotation = rotation
        
    def get_expand(self):
        return self.expand
    
    def set_expand(self, expand):
        self.expand = expand

    def get_use_blur(self):
        return self.use_blur
    
    def set_use_blur(self, use_blur):
        self.use_blur = use_blur
        
    def get_blur_radius(self):
        return self.blur_radius
    
    def set_blur_radius(self, radius):
        self.blur_radius = radius
        
    def get_fill_color(self):
        return self.fill_color
    
    def set_fill_color(self, rgb):
        self.fill_color = rgb
        
    def get_new_image(self, image: Image):
        if self.use_blur:
            # Convert the original image to 'RGBA' to support transparency
            image_rgba = image.convert('RGBA')

            rotated_image = image_rgba.rotate(self.rotation, expand=self.expand, fillcolor=None)  # fillcolor=None ensures transparency

            # Create a blurred version of the original image
            # It's important to blur the image after resizing to match the rotated image's size for a proper background
            image = image.filter(ImageFilter.GaussianBlur(self.blur_radius)).convert('RGBA').resize(rotated_image.size)

            # Combine the blurred background with the rotated image
            image.paste(rotated_image, (0, 0), rotated_image)
        else:
            image = image.rotate(self.rotation,  expand = self.expand, fillcolor = self.fill_color)
        return image

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['Rotation'] = self.rotation
        dict['Expand'] = self.expand
        if self.use_blur:
            dict['BackgroundType'] = 'Blur'
            dict['BlurRadius'] = self.blur_radius
        else:
            dict['BackgroundType'] = 'Fill Color'
            dict['FillColor'] = self.fill_color

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.rotation = dict['Rotation']
        self.expand = dict['Expand']
        self.use_blur = True if dict['BackgroundType'] == 'Blur' else False
        if self.use_blur:
            self.blur_radius = dict['BlurRadius']
        else:
            self.fill_color = dict['FillColor']
