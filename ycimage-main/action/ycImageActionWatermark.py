import math

from matplotlib import font_manager
from PIL import Image, ImageFont, ImageDraw, ImageOps

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType, ImageWatermarkType

#===============================================================
# Class ImageWatermark
class ImageActionWatermark(ImageAction):
    def __init__(self, name):
        super().__init__(name)
        default_font = ImageFont.load_default()

        self.watermark_type = ImageWatermarkType.TEXT
        self.pos = (0, 0)
        self.rotation = 0.0
        self.text = ''
        self.text_color = (0, 0, 0)
        self.font_name = default_font.getname()[0]
        self.font_size = 10
        self.is_bold = not (default_font.getname()[1] == "Regular")
        self.is_italic = False
        self.image_file = ''
        self.transparency = 255

        
    def get_action_type(self):
        return ActionType.WATERMARK
    
    def get_watermark_type(self):
        return self.watermark_type

    def set_watermark_type(self, watermark_type):
        self.watermark_type = watermark_type
    
    def get_position(self):
        return self.pos
    
    def set_position(self, pos):
        self.pos = pos

    def get_rotation(self):
        return self.rotation
    
    def set_rotation(self, rotation: float):
        self.rotation = rotation

    def get_text(self):
        return self.text
      
    def set_text(self, text):
        self.text = text
        
    def get_text_color(self):
        return self.text_color
      
    def set_text_color(self, text_color):
        self.text_color = text_color

    def get_font_name(self):
        return self.font_name
    
    def set_font_name(self, font_name):
        self.font_name = font_name
        
    def get_font_size(self):
        return self.font_size
    
    def set_font_size(self, font_size):
        self.font_size = font_size

    def get_is_bold(self):
        return self.is_bold
    
    def set_is_bold(self, is_bold):
        self.is_bold = is_bold
        
    def get_is_italic(self):
        return self.is_italic
    
    def set_is_italic(self, is_italic):
        self.is_italic = is_italic

    def get_text_color(self):
        return self.text_color

    def set_text_color(self, rgb):
        self.text_color = rgb

    def get_image_file(self):
        return self.image_file
    
    def set_image_file(self, filename):
        self.image_file = filename

    def get_transparency(self):
        return self.transparency
    
    def set_transparency(self, transparency):
        self.transparency = transparency

    def _validate_internal(self):
        pass

    def new_position_after_rotation(self, x, y, width, height, angle, new_width, new_height):
        # Convert angle to radians
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        x1 = - width / 2
        y1 = - height / 2
        
        x2 = x1 * cos_angle - y1 * sin_angle
        y2 = x1 * sin_angle + y1 * cos_angle
        
        x3 = new_width / 2
        y3 = new_height / 2
        new_x = x - int(x2 + x3)
        new_y = y - int(y2 + y3)
        
        return new_x, new_y

    def get_new_image(self, image: Image):
        if self.watermark_type == ImageWatermarkType.TEXT:
            rgba_image = image.convert("RGBA")
            
            lines = self.text.splitlines()
            txt_image_width = 500
            txt_image_height = len(lines) * (self.font_size + 5)
            # Create a text image in grayscale
            font = ImageFont.truetype(self.get_font_path(), self.font_size)
            txt_image = Image.new('RGBA', image.size, (255, 255, 255, 0))
            
            draw = ImageDraw.Draw(txt_image)
            text_color = self.text_color + (self.transparency,)
            draw.text(self.pos, self.text,  font = font, fill = text_color, anchor="mm")
            rotate_text_image = txt_image if self.rotation == 0 else txt_image.rotate(self.rotation,  center=self.pos, expand=0)

            # Paste the text image to image
            image = Image.alpha_composite(rgba_image, rotate_text_image)

        else:
            image_watermark = ImageAction.load_image(self.image_file)
            if self.transparency == 255:
                if image_watermark:
                    image.paste(image_watermark, (self.pos[0], self.pos[1]), image_watermark)
            else:
                # Convert to RGBA
                image_watermark = image_watermark.convert("RGBA")
                alpha = self.transparency
                transparent_watermark = Image.new("RGBA", image_watermark.size)
                # Fill the transparent overlay with the overlay image and adjusted alpha
                for x in range(image_watermark.width):
                    for y in range(image_watermark.height):
                        r, g, b, _ = image_watermark.getpixel((x, y))
                        transparent_watermark.putpixel((x, y), (r, g, b, alpha))
                image.paste(transparent_watermark, (self.pos[0], self.pos[1]), transparent_watermark)
        return image

    def get_font_path(self):
        font_weight = 'bold' if self.is_bold else 'normal'
        font_style = 'italic' if self.is_italic else 'normal'

        font_properties = font_manager.FontProperties(family=self.font_name, size=self.font_size, weight=font_weight, style=font_style)
        return font_manager.findfont(font_properties)

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['WatermarkType'] = self.get_enum_export_name(self.watermark_type)
        dict['Position'] = self.pos
        dict['Rotation'] = self.rotation
        dict['Transparency'] = self.transparency
        if self.watermark_type == ImageWatermarkType.TEXT:
            dict['Text'] = self.text
            dict['Font'] = self.font_name
            dict['FontSize'] = self.font_size
            dict['TextColor'] = self.text_color
            dict['IsBold'] = self.is_bold
            dict['IsItalic'] = self.is_italic
        else:
            dict['ImageFile'] = self.image_file

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.watermark_type = self.get_enum_from_export_name(ImageWatermarkType, dict['WatermarkType'])
        self.pos = tuple(dict['Position'])
        self.rotation = dict['Rotation']
        self.transparency = dict['Transparency']
        if self.watermark_type == ImageWatermarkType.TEXT:
            self.text = dict['Text']
            self.font_name = dict['Font']
            self.font_size = dict['FontSize']
            self.is_bold = dict['IsBold']
            self.is_italic = dict['IsItalic']
            self.text_color = tuple(dict['TextColor'])
        else:
            self.image_file = dict['ImageFile']
