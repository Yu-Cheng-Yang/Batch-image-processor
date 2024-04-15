
from PIL import Image, ImageFilter

from action.ycImageAction import ImageAction
from uibase.ycTypes import ActionType, ImageFilterType,ImagePredefinedFilterType, ImageStandardFilterType

#===============================================================
# Class ImageActionFilter
class ImageActionFilter(ImageAction):
    def __init__(self, name, filter_type : ImageFilterType = ImageFilterType.PREDEFINED_FILTER,
                 filter_predefined_type : ImagePredefinedFilterType = ImagePredefinedFilterType.BLUR,
                 filter_standard_type: ImageStandardFilterType = ImageStandardFilterType.BOX_BLUR):
        super().__init__(name)
        self.filter_type = filter_type
        self.predefined_type = filter_predefined_type
        self.standard_type = filter_standard_type
        self.radius = 2
        self.percent = 150
        self.threshold = 3
        self.rank = 0
        self.size = 3
        
    def get_action_type(self):
        return ActionType.FILTER

    def get_filter_type(self):
        return self.filter_type

    def set_filter_type(self, filter_type : ImageFilterType):
        self.filter_type = filter_type
    
    def get_predefined_type(self):
        return self.predefined_type

    def set_predefined_type(self, predefined_type : ImagePredefinedFilterType):
        self.predefined_type = predefined_type

    def get_standard_type(self):
        return self.standard_type

    def set_standard_type(self, standard_type : ImageStandardFilterType):
        self.standard_type = standard_type

    def get_radius(self):
       return self.radius
    
    def set_radius(self, radius):
        self.radius = radius
        
    def get_percent(self):
       return self.percent
    
    def set_percent(self, percent):
        self.percent = percent
        
    def get_threshold(self):
       return self.threshold
    
    def set_threshold(self, threshold):
        self.threshold = threshold
        
    def get_rank(self):
        return self.rank
       
    def set_rank(self, rank):
        self.rank = rank
        
    def get_size(self):
        return self.size
    
    def set_size(self, size):
        self.size = size

    def get_new_image(self, image: Image):
        if self.filter_type == ImageFilterType.PREDEFINED_FILTER:
            if self.predefined_type == ImagePredefinedFilterType.BLUR:
               image = image.filter(ImageFilter.BLUR)
            elif self.predefined_type == ImagePredefinedFilterType.CONTOUR:
               image = image.filter(ImageFilter.CONTOUR)
            elif self.predefined_type == ImagePredefinedFilterType.DETAIL:
               image = image.filter(ImageFilter.DETAIL)
            elif self.predefined_type == ImagePredefinedFilterType.EDGE_ENHANCE:
               image = image.filter(ImageFilter.EDGE_ENHANCE)
            elif self.predefined_type == ImagePredefinedFilterType.EDGE_ENHANCE_MORE:
               image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            elif self.predefined_type == ImagePredefinedFilterType.EMBOSS:
               image = image.filter(ImageFilter.EMBOSS)
            elif self.predefined_type == ImagePredefinedFilterType.SHARPEN:
               image = image.filter(ImageFilter.SHARPEN)
            elif self.predefined_type == ImagePredefinedFilterType.FIND_EDGES:
               image = image.filter(ImageFilter.FIND_EDGES)
            elif self.predefined_type == ImagePredefinedFilterType.SMOOTH:
               image = image.filter(ImageFilter.SMOOTH)
            elif self.predefined_type == ImagePredefinedFilterType.SMOOTH_MORE:
               image = image.filter(ImageFilter.SMOOTH_MORE)
        else:
            if self.standard_type == ImageStandardFilterType.BOX_BLUR:
               image = image.filter(ImageFilter.BoxBlur(self.radius))
            elif self.standard_type == ImageStandardFilterType.GAUSSIAN_BLUR:
               image = image.filter(ImageFilter.GaussianBlur(self.radius))
            elif self.standard_type == ImageStandardFilterType.MAX_FILTER:
               image = image.filter(ImageFilter.MaxFilter(self.size))
            elif self.standard_type == ImageStandardFilterType.MEDIAN_FILTER:
               image = image.filter(ImageFilter.MedianFilter(self.size))
            elif self.standard_type == ImageStandardFilterType.MIN_FILTER:
               image = image.filter(ImageFilter.MinFilter(self.size))
            elif self.standard_type == ImageStandardFilterType.MODE_FILTER:
               image = image.filter(ImageFilter.ModeFilter(self.size))
            elif self.standard_type == ImageStandardFilterType.RANK_FILTER:
               image = image.filter(ImageFilter.RankFilter(self.size, self.rank))
            elif self.standard_type == ImageStandardFilterType.UNSHARP_MASK:
               image = image.filter(ImageFilter.UnsharpMask(self.radius, self.percent, self.threshold))
            
        return image

    def write_to_dict(self, dict):
        ImageAction.write_to_dict(self, dict)
        dict['FilterType'] = self.get_enum_export_name(self.filter_type)
        if self.filter_type == ImageFilterType.PREDEFINED_FILTER:
            dict["PredefinedType"] = self.get_enum_export_name(self.predefined_type)
        else:
            dict["StandardType"] = self.get_enum_export_name(self.standard_type)
            if self.standard_type == ImageStandardFilterType.BOX_BLUR:
               dict["Radius"] = self.radius
            elif self.standard_type == ImageStandardFilterType.GAUSSIAN_BLUR:
               dict["Radius"] = self.radius
            elif self.standard_type == ImageStandardFilterType.MAX_FILTER:
               dict["Size"] = self.size
            elif self.standard_type == ImageStandardFilterType.MEDIAN_FILTER:
               dict["Size"] = self.size
            elif self.standard_type == ImageStandardFilterType.MIN_FILTER:
               dict["Size"] = self.size
            elif self.standard_type == ImageStandardFilterType.MODE_FILTER:
               dict["Size"] = self.size
            elif self.standard_type == ImageStandardFilterType.RANK_FILTER:
               dict["Size"] = self.size
               dict["Rank"] = self.rank
            elif self.standard_type == ImageStandardFilterType.UNSHARP_MASK:
               dict["Radius"] = self.radius
               dict["Percent"] = self.percent
               dict["Threshold"] = self.threshold

    def read_from_dict(self, dict):
        ImageAction.read_from_dict(self, dict)
        self.filter_type = self.get_enum_from_export_name(ImageFilterType, dict['FilterType'])
        if self.filter_type == ImageFilterType.PREDEFINED_FILTER:
            self.predefined_type = self.get_enum_from_export_name(ImagePredefinedFilterType, dict["PredefinedType"])
        else:
            self.standard_type = self.get_enum_from_export_name(ImageStandardFilterType, dict["StandardType"])
            if self.standard_type == ImageStandardFilterType.BOX_BLUR:
               self.radius = dict["Radius"]
            elif self.standard_type == ImageStandardFilterType.GAUSSIAN_BLUR:
               self.radius = dict["Radius"]
            elif self.standard_type == ImageStandardFilterType.MAX_FILTER:
               self.size = dict["Size"] 
            elif self.standard_type == ImageStandardFilterType.MEDIAN_FILTER:
               self.size = dict["Size"] 
            elif self.standard_type == ImageStandardFilterType.MIN_FILTER:
               self.size = dict["Size"] 
            elif self.standard_type == ImageStandardFilterType.MODE_FILTER:
               self.size = dict["Size"] 
            elif self.standard_type == ImageStandardFilterType.RANK_FILTER:
               self.size = dict["Size"] 
               self.rank = dict["Rank"] 
            elif self.standard_type == ImageStandardFilterType.UNSHARP_MASK:
               self.radius = dict["Radius"]
               self.percent = dict["Percent"]
               self.threshold = dict["Threshold"]
