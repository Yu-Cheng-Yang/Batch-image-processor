import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionTransform import ImageActionTransform
from uibase.ycTypes import ImageTransformType

#===============================================================
# Class ImageActionWidgetTransform
class ImageActionWidgetTransform(ImageActionWidget):
    def __init__(self, parent, action : ImageActionTransform, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()

        self.transform_type_combo = self.add_labeled_enum_combobox('Transform Type', self.action.get_transform_type(), False)

        self.scale_entry = self.add_labeled_entry('Scale', self.action.get_scale())
        self.scale_resampling_type_combo = self.add_labeled_enum_combobox('Scale Resampling Type', self.action.get_scale_resampling_type())
        self.expand_border_entry = self.add_labeled_entry('Expand Border', self.action.get_expand_border())
        self.fill_color = self.add_color_selector('Expand Fill Color', self.action.get_expand_fill_color())
    
    def _show_sub_widgets(self):
        super()._show_sub_widgets()
        transform_type = self.transform_type_combo.get_value()
        if transform_type == ImageTransformType.SCALE:
            self._show_widget(self.scale_entry)
            self._show_widget(self.scale_resampling_type_combo)
        elif transform_type == ImageTransformType.EXPAND:
            self._show_widget(self.expand_border_entry)
            self._show_widget(self.fill_color)
 
    def _on_apply_internal(self):
        transform_type = self.transform_type_combo.get_value()
        self.action.set_transform_type(transform_type)
        if transform_type == ImageTransformType.SCALE:
            self.action.set_scale(self.scale_entry.get_value())
            self.action.set_scale_resampling_type(self.scale_resampling_type_combo.get_value())
        else:
            self.action.set_expand_border(self.expand_border_entry.get_value())
            self.action.set_expand_fill_color(self.fill_color.get_color())

