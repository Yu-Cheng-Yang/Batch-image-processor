import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionRotate import ImageActionRotate

#===============================================================
# Class ImageActionFrameRotate
class ImageActionWidgetRotate(ImageActionWidget):
    def __init__(self, parent, action : ImageActionRotate, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()
        self.rotation_entry = self.add_labeled_entry('Rotation', self.action.get_rotation(), False)
        self.expand_checkbox = self.add_checkbox('Expand', self.action.get_expand() > 0, False)
        self.use_blur_checkbox = self.add_checkbox('Use Blur', self.action.get_use_blur(), False)
        self.fill_color = self.add_color_selector('Select Fill Color', self.action.get_fill_color())
        self.blur_radius_entry = self.add_labeled_entry('Blur Radius', self.action.get_blur_radius())
    
    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        self._show_widget(self.rotation_entry)
        self._show_widget(self.expand_checkbox)
        self._show_widget(self.use_blur_checkbox)
        if self.use_blur_checkbox.GetValue():
            self._show_widget(self.blur_radius_entry)
        else:
            self._show_widget(self.fill_color)
 
    def _on_apply_internal(self):
        self.action.set_rotation(float(self.rotation_entry.get_value()))
        fill_color = self.fill_color.get_color()
        self.action.set_expand(self.expand_checkbox.GetValue())

        self.action.set_use_blur(self.use_blur_checkbox.GetValue())
        if self.use_blur_checkbox.GetValue():
            self.action.set_blur_radius(self.blur_radius_entry.get_value())
        else:
            self.action.set_fill_color(self.fill_color.get_color())

