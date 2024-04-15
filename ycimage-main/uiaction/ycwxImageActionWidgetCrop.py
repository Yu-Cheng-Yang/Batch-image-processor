import action.ycImageAction as ycImageAction
from uiaction.ycwxImageActionWidget import ImageActionWidget
from action.ycImageActionCrop import ImageActionCrop
from ycLocalize import localize

#===============================================================
# Class ImageActionFrameCrop
class ImageActionWidgetCrop(ImageActionWidget):
    def __init__(self, parent, action : ImageActionCrop, **kwargs):
        super().__init__(parent, action, **kwargs)
        self._update_layout()

    def _create_sub_widgets(self):
        super()._create_sub_widgets()
        self.top_entry = self.add_labeled_entry(localize('Top'), self.action.get_top(), False)
        self.left_entry = self.add_labeled_entry(localize('Right'), self.action.get_left(), False)
        self.bottom_entry = self.add_labeled_entry(localize('Bottom'), self.action.get_bottom(), False)
        self.right_entry = self.add_labeled_entry(localize('Right'), self.action.get_right(), False)
    
    def _show_sub_widgets(self):
        super()._show_sub_widgets()

    def _on_apply_internal(self):
        self.action.set_top(self.top_entry.get_value())
        self.action.set_left(self.left_entry.get_value())
        self.action.set_bottom(self.bottom_entry.get_value())
        self.action.set_right(self.right_entry.get_value())

