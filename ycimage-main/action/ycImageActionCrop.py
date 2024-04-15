
from PIL import Image

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType

#===============================================================
# Class ImageActionCrop
class ImageActionCrop(ImageAction):
    def __init__(self, name):
        super().__init__(name)
        self.top = 0
        self.left = 0
        self.bottom = -1
        self.right = -1
    
    def get_action_type(self):
        return ActionType.CROP

    def get_left(self):
        return self.left

    def get_top(self):
        return self.top
    
    def get_right(self):
        return self.right
    
    def get_bottom(self):
        return self.bottom
    
    def set_bottom(self, bottom):
        if bottom < 0:
            bottom = -1
        self.bottom = bottom

    def set_box(self, left, top, right, bottom):
        self.set_left(left)
        self.set_top(top)
        self.set_right(right)
        self.set_borrom(bottom)
        
    def set_right(self, right):
        if right < 0:
            right = -1
        self.right = right

    def set_top(self, top):
        if top < 0 :
            self.top = 0
        else:
            self.top = top

    def set_left(self, left):
        if left < 0 :
            self.left = 0
        else:
            self.left = left

    def set_rectangle(self, left, top, right, bottom):
        self.set_top(top)
        self.set_left(left)
        self.set_bottom(bottom)
        self.set_right(right)
        
    def get_new_image(self, image: Image):
        image_width, image_height = image.size
        
        bottom = self.bottom if self.bottom > 0 else image_height
        right = self.right if self.right > 0 else image_width
        
        assert self.left < right or self.top <= bottom

        image = image.crop((self.left,  self.top, right, bottom))
        return image

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['Left'] = self.left
        dict['Top'] = self.top
        dict['Right'] = self.right
        dict['Bottom'] = self.bottom

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.top = dict['Top']
        self.left = dict['Left']
        self.bottom = dict['Bottom']
        self.right = dict['Right']
