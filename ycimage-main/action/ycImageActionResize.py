
from PIL import Image, ImageFilter

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType, ImageResizeType, ImageResamplingType

#===============================================================
# Class ImageActionResize
class ImageActionResize(ImageAction):
    def __init__(self, name):
        super().__init__(name)
        self.resize_type = ImageResizeType.SCALE
        self.scale = 1.0
        self.width = -1
        self.height = -1
        self.use_blur = False
        self.blur_radius = 10
        self.fill_color = (0, 0, 0)
        self.keep_aspect_ratio = True
        self.resampling = ImageResamplingType.NEAREST
        self.square_length = -1
        
    def get_action_type(self):
        return ActionType.RESIZE

    def get_resize_type(self):
        return self.resize_type
    
    def set_resize_type(self, type):
        self.resize_type = type

    def get_scale_value(self):
        return self.scale
    
    def set_scale_value(self, scale : float):
        assert scale > 0
        self.scale = scale
        self.resize_type = ImageResizeType.SCALE

    def get_size(self):
        return self.width, self.height
    
    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width : int):
        self.width = width

    def set_height(self, height : int):
        self.height = height

    def set_width_and_height(self, width : int, height : int):
        self.width = width
        self.height = height
    
    def get_square_length(self):
        return self.square_length
    
    def set_square_length(self, length : int):
        self.square_length = length

    def get_fill_color(self):
        return self.fill_color
    
    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def get_use_blur(self):
        return self.use_blur
    
    def set_use_blur(self, use_blur):
        self.use_blur = use_blur

    def get_blur_radius(self):
        return self.blur_radius
    
    def set_blur_radius(self, blur_radius):
        self.blur_radius = blur_radius
        
    def get_resampling(self):
        return self.resampling
    
    def set_resampling(self, resampling):
        self.resampling = resampling
    
    def get_keep_aspect_ratio(self):
        return self.keep_aspect_ratio
    
    def set_keep_aspect_ratio(self, keep_aspect_ratio):
        self.keep_aspect_ratio = keep_aspect_ratio
        
    def get_new_image(self, image: Image):
        image_width, image_height = image.size
        
        width = image_width
        height = image_height

        if self.resize_type == ImageResizeType.SCALE:
            if self.scale > 0:
                width = int(image_width * self.scale)
                height = int(image_height * self.scale)
                image = image.resize((width, height), Image.LANCZOS)
        elif self.resize_type == ImageResizeType.WIDTH:
            width = self.width
            if width > 0:
                height = int(width * image_height / image_width)
                image = image.resize((width, height), Image.LANCZOS)
        elif self.resize_type == ImageResizeType.HEIGHT:
            height = self.height
            if height > 0:
                width = int(height * image_width / image_height)
                image = image.resize((width, height), Image.LANCZOS)
        elif self.resize_type == ImageResizeType.WIDTH_AND_HEIGHT:
            image = self.resize_image_with_aspect_ratio(image, self.width, self.height)
        elif self.resize_type == ImageResizeType.SQUARE:
             length = image_width if self.height < image_width else image_height
             image = self.resize_image_with_aspect_ratio(image, length, length)
        return image

    def resize_image_with_aspect_ratio(self, image, width, height):
        # Calculate the ratio while keeping the aspect ratio
        original_width, original_height = image.size
        ratio = min(width/original_width, height/original_height)
        resized_width = int(original_width * ratio)
        resized_height = int(original_height * ratio)
        
        # Resize the original image
        img_resized = image.resize((resized_width, resized_height), self.resampling)
        
        if self.use_blur:
            new_img = image.resize((width, height), self.resampling)
            new_img = new_img.filter(ImageFilter.GaussianBlur(self.blur_radius))
        else:
            new_img = Image.new("RGB", (width, height), self.fill_color)
        
        # Calculate position to paste the resized image on the new image
        x = (width - resized_width) // 2
        y = (height - resized_height) // 2
        
        # Paste the resized image onto the new image
        new_img.paste(img_resized, (x, y))
        
        return new_img

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['ResizeType'] = self.get_enum_export_name(self.resize_type)
        dict['ResamplingType'] = self.get_enum_export_name(self.resampling)
        if self.resize_type == ImageResizeType.SCALE:
            dict['Scale'] = self.scale
        elif self.resize_type == ImageResizeType.WIDTH:
            dict['Width'] = self.width
        elif self.resize_type == ImageResizeType.HEIGHT:
            dict['Height'] = self.height
        elif self.resize_type == ImageResizeType.WIDTH_AND_HEIGHT:
            dict['Width'] = self.width
            dict['Height'] = self.height
            dict['KeepAspectRatio'] = self.keep_aspect_ratio
            if not self.keep_aspect_ratio:
                if self.use_blur:
                    dict['BackgroundType'] = 'Blur'
                    dict['BlurRadius'] = self.blur_radius
                else:
                    dict['BackgroundType'] = 'Fill Color'
                    dict['FillColor'] = self.fill_color
        elif self.resize_type == ImageResizeType.SQUARE:
            dict['SquareLength'] = self.square_length

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.resize_type = self.get_enum_from_export_name(ImageResizeType, dict['ResizeType'])
        self.resampling = self.get_enum_from_export_name(ImageResamplingType, dict['ResamplingType'])
        if self.resize_type == ImageResizeType.SCALE:
            self.scale = dict['Scale']
        elif self.resize_type == ImageResizeType.WIDTH:
            self.width = dict['Width']
        elif self.resize_type == ImageResizeType.HEIGHT:
            self.height = dict['Height']
        elif self.resize_type == ImageResizeType.WIDTH_AND_HEIGHT:
            self.width = dict['Width']
            self.height = dict['Height']
            self.keep_aspect_ratio = dict['KeepAspectRatio']
            if not self.keep_aspect_ratio:
                self.use_blur = True if dict['BackgroundType'] == 'Blur' else False
                if self.use_blur:
                    self.blur_radius = dict['BlurRadius']
                else:
                    self.fill_color = dict['FillColor']
        elif self.resize_type == ImageResizeType.SQUARE:
            self.square_length = dict['SquareLength']
