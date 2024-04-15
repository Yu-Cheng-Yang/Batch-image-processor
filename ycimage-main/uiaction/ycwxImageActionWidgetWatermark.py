import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionWatermark import ImageActionWatermark
from uibase.ycTypes import ImageWatermarkType

#===============================================================
# Class ImageActionWidgetWatermark
class ImageActionWidgetWatermark(ImageActionWidget):
    def __init__(self, parent, action : ImageActionWatermark, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()

        self.watermark_type_combo = self.add_labeled_enum_combobox('Watermark Type', self.action.get_watermark_type(), False)

        self.pos_x_entry = self.add_labeled_entry('Position X', self.action.get_position()[0], False)
        self.pos_y_entry = self.add_labeled_entry('Position Y', self.action.get_position()[1], False)
        self.rotation_entry = self.add_labeled_entry('Rotation', self.action.get_rotation(), False)
        self.transparency_entry = self.add_labeled_entry('Transparency (0~255)', self.action.get_transparency(), False)
        
        self.text = self.add_labeled_entry('Text', self.action.text)
        self.font_selector = self.add_font_selector(self.action.font_name, self.action.font_size,
                                                    self.action.text_color, self.action.is_bold,
                                                    self.action.is_italic, color_label = 'Text Color')
        self.image_file = self.add_file_selector(label_text = 'Select Image File', select_file = self.action.image_file)
    
    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        watermark_type = self.watermark_type_combo.get_value()
        if watermark_type == ImageWatermarkType.TEXT:
            self._show_widget(self.pos_x_entry)
            self._show_widget(self.pos_y_entry)
            self._show_widget(self.rotation_entry)
            self._show_widget(self.text)
            self._show_widget(self.font_selector)
        else:
            self._show_widget(self.image_file)
 
    def _on_apply_internal(self):
        self.action.set_position((self.pos_x_entry.get_value(), self.pos_y_entry.get_value()))
        self.action.set_rotation(float(self.rotation_entry.get_value()))
        watermark_type = self.watermark_type_combo.get_value()
        self.action.set_watermark_type(watermark_type)
        self.action.set_transparency(self.transparency_entry.get_value())
        if watermark_type == ImageWatermarkType.TEXT:
            self.action.set_text(self.text.get_value())
            self.action.set_text_color(self.font_selector.get_color()[:3])
            self.action.set_font_name(self.font_selector.get_font().GetFaceName())
            self.action.set_font_size(self.font_selector.get_font_size())
            self.action.set_is_bold(self.font_selector.is_bold())
            self.action.set_is_italic(self.font_selector.is_italic())
        else:
            self.action.set_image_file(self.image_file.get_file_name())

