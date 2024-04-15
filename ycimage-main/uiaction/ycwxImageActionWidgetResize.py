
import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionResize import ImageActionResize
from uibase.ycTypes import ImageResizeType
from ycLocalize import localize

#===============================================================
# Class ImageActionFrameResize
class ImageActionWidgetResize(ImageActionWidget):
    def __init__(self, parent, action : ImageActionResize, **kwargs):
        super().__init__(parent, action, **kwargs)
    
    def _create_sub_widgets(self):
        super()._create_sub_widgets()
        self.resize_type_combo = self.add_labeled_enum_combobox('Resize Type', self.action.get_resize_type(), False)
        self.resampling_combo = self.add_labeled_enum_combobox('Resampling Type', self.action.get_resampling(), False)
        self.scale_entry = self.add_labeled_entry('Scale', self.action.get_scale_value())
        self.width_entry = self.add_labeled_entry('Width', self.action.get_width())
        self.height_entry = self.add_labeled_entry('Height', self.action.get_height())
        self.length_entry = self.add_labeled_entry('Square Length', self.action.get_square_length())
        self.keep_aspect_ratio_checkbox = self.add_checkbox('Keep Aspect Ratio', self.action.get_keep_aspect_ratio())
        self.use_blur_checkbox = self.add_checkbox('Use Blur', self.action.get_use_blur())
        self.fill_color = self.add_color_selector('Select Fill Color', self.action.get_fill_color())
        self.blur_radius_entry = self.add_labeled_entry('Blur Radius', self.action.get_blur_radius())
        
    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        
        #self._show_widget(self.resize_type_combo)
        
        show_background_setting = False
        resize_type = self.resize_type_combo.get_value()
        if resize_type == ImageResizeType.SCALE:
            self._show_widget(self.scale_entry)
        elif resize_type == ImageResizeType.WIDTH:
            self._show_widget(self.width_entry)
        elif resize_type == ImageResizeType.HEIGHT:
            self._show_widget(self.height_entry)
        elif resize_type == ImageResizeType.WIDTH_AND_HEIGHT:
            self._show_widget(self.width_entry)
            self._show_widget(self.height_entry)
            show_background_setting = True
        elif resize_type == ImageResizeType.SQUARE:
            self._show_widget(self.length_entry)
            self._show_widget(self.keep_aspect_ratio_checkbox)
            show_background_setting = not self.keep_aspect_ratio_checkbox.GetValue()
        if show_background_setting:
            self._show_widget(self.use_blur_checkbox)
            if self.use_blur_checkbox.GetValue():
                self._show_widget(self.blur_radius_entry)
            else:
                self._show_widget(self.fill_color)

    def _on_apply_internal(self):
        resize_type = self.resize_type_combo.get_value()
        self.action.set_resize_type(resize_type)
        self.action.set_resampling(self.resampling_combo.get_value())
        set_background_setting = False
        if resize_type == ImageResizeType.SCALE:
            self.action.set_scale_value(self.scale_entry.get_value())
        elif resize_type == ImageResizeType.WIDTH:
            self.action.set_width(int(self.width_entry.get_value()))
        elif resize_type == ImageResizeType.HEIGHT:
            self.action.set_height(int(self.height_entry.get_value()))
        elif resize_type == ImageResizeType.WIDTH_AND_HEIGHT:
            self.action.set_width_and_height(self.width_entry.get_value(), self.height_entry.get_value())
            set_background_setting = True
        elif resize_type == ImageResizeType.SQUARE:
            self.action.set_square_length(int(self.length_entry.get_value()))
            set_background_setting = not self.keep_aspect_ratio_checkbox.GetValue()
            self.action.set_keep_aspect_ratio(self.keep_aspect_ratio_checkbox.GetValue())
        if set_background_setting:
            self.action.set_use_blur(self.use_blur_checkbox.GetValue())
            if self.use_blur_checkbox.GetValue():
                self.action.set_blur_radius(self.blur_radius_entry.get_value())
            else:
                self.action.set_fill_color(self.fill_color.get_color())
