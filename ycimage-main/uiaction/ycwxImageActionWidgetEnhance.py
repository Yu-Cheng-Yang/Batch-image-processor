import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionEnhance import ImageActionEnhance

#===============================================================
# Class ImageActionWidgetEnhance
class ImageActionWidgetEnhance(ImageActionWidget):
    def __init__(self, parent, action : ImageActionEnhance, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()

        self.enhance_type_combo = self.add_labeled_enum_combobox('Enhance Type', self.action.get_enhance_type(), dynamic_show = False)
        self.scale_entry = self.add_labeled_entry('Scale', self.action.get_scale(), False)
    
    def _on_apply_internal(self):
        enhance_type = self.enhance_type_combo.get_value()
        self.action.set_enhance_type(enhance_type)
        self.action.set_scale(self.scale_entry.get_value())

