import wx

class ImageFileSelector(wx.Panel):
    def __init__(self, parent, label_text = 'Select Image File', select_file = '', **kwargs):
        super().__init__(parent, **kwargs)
        self.select_file = select_file
        self.filter_index = 0

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label = wx.StaticText(self, label=label_text)
        self.file_entry = wx.TextCtrl(self)
        self.file_entry.SetValue(select_file)
        self.button = wx.Button(self, label = 'Select...')
        self.button.Bind(wx.EVT_BUTTON, self.on_open_dialog)
        
        hbox.Add(self.label, 0, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.file_entry, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=8)
        hbox.Add(self.button, 0, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(hbox)

    def get_tabbed_widgets(self):
        return [self.file_entry, self.button]

    def get_file_name(self):
        return self.select_file
    
    def on_open_dialog(self, evnet):
        wildcard = (
            "JPG files (*.jpg;*.jpeg;*.jpe;*.jfif)|*.jpg;*.jpeg;*.jpe;*.jfif|"
            "PNG files (*.png)|*.png|"
            "Bitmap files (*.bmp;*.dib)|*.bmp;*.dib|"
            "GIF files (*.gif)|*.gif|"
            "TIFF files (*.tif;*.tiff)|*.tif;*.tiff|"
            "HEIC files (*.heic)|*.heic|"
            "WEBP files (*.webp)|*.webp|"
            "All files (*.*)|*.*"
        )
        open_dialog = wx.FileDialog(self, "Open", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        open_dialog.SetFilterIndex(self.filter_index)
        if open_dialog.ShowModal() == wx.ID_OK:
            filename = open_dialog.GetPath()
            self.filter_index = open_dialog.GetFilterIndex()
            self.file_entry.SetValue(filename)
            self.select_file= filename
            self.file_entry.Refresh()

        open_dialog.Destroy()

