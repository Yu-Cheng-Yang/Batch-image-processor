import wx

class ImageCheckBox(wx.CheckBox):
    def __init__(self, parent, label):
        super().__init__(parent, label=label)
        
    def get_tabbed_widgets(self):
        return [self]
