import wx
from ycLocalize import localize

#===============================================================
# Class ColorSelectorPanel
class ColorSelectorPanel(wx.Panel):
    def __init__(self, parent, label_text, select_color, **kwargs):
        super().__init__(parent, **kwargs)
        self.rgb = self._get_rgb_color(select_color)
        self.callback = None

        self.color_names = ['Black', 'White', 'Red', 'Green', 'Blue', 'Yellow', 'Brown', 'Orange', 'Pink', 'Purple', 'Grey', 'Custom']
        self.color_rgbs = []
        for color_name in self.color_names[:-1]:
            rgb = wx.ColourDatabase().Find(color_name).Get(includeAlpha = False)
            self.color_rgbs.append(rgb)

        index, self.color_name = self._get_color_name(self.rgb)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
                            
        # Define label
        self.label = wx.StaticText(self, label = localize(label_text))
        hbox.Add(self.label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        #self.label.pack(side=tk.LEFT, padx=(0, 10))
        
        # define combobox
        display_color_names = [localize(color_name) for color_name in self.color_names]
        
        self.combo_box = wx.ComboBox(self, choices=display_color_names, style=wx.CB_READONLY)
        hbox.Add(self.combo_box, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.combo_box.SetSelection(index)
        self.Bind(wx.EVT_COMBOBOX, self._on_color_select)
        #self.combo_box.pack(side=tk.LEFT)
        
        # Define color select button to trigger color selector
        self.button = wx.Button(self, label="")
        hbox.Add(self.button, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=8)
        self.button.SetBackgroundColour(self.rgb)
        self.button.Bind(wx.EVT_BUTTON, self._on_custom_color_select)
        #border.pack(side=tk.LEFT, padx=10)
        self.SetSizer(hbox)
    
    def get_tabbed_widgets(self):
        return [self.combo_box, self.button]
    
    def get_color(self):
        return self.rgb
    
    def set_color(self, rgb):
        self.rgb = rgb
        index, self.color_name= self._get_color_name(self.rgb)
        self.combo_box.SetSelection(index)
        self.button.SetBackgroundColour(wx.Colour(*self.rgb))  # Set button background
       
    def set_callback(self, callback):
        self.callback = callback

    def _on_color_select(self, event):
        index = self.combo_box.GetSelection()  # Correct method to get selected value
        if index == len(self.color_names)-1:
            return
        # Find the RGB value for the selected color name
        self.rgb = self.color_rgbs[index]
        self.button.SetBackgroundColour(wx.Colour(*self.rgb))  # Set button background
        if self.callback:
            self.callback(self.rgb)
                
    def _on_custom_color_select(self, event):
        # Popup color selector dialog and select color
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        dlg.GetColourData().SetColour(wx.Colour(self.rgb[0], self.rgb[1], self.rgb[2]))
        if dlg.ShowModal() == wx.ID_OK:
            self.set_color(dlg.GetColourData().GetColour().Get()[:3])
        dlg.Destroy() 

        if self.callback:
            self.callback(self.rgb)
     
    def _to_hex_color(self, rgb: tuple):
        return '#{:02x}{:02x}{:02x}'.format(*rgb) 
       
    def _get_color_name(self, color):
        # Assuming self.colors might have fewer elements than self.color_names
        index = 0
        for rgb, name in zip(self.color_rgbs, self.color_names):
            if color == rgb:
                return index, name
            index = index + 1

        # Return 'Custom' if the color wasn't found
        return index, 'Custom'
    
    # color can be hex color or tuple color or color name
    # return is rgb color
    def _get_rgb_color(self, color):
        rgb = color  # Default color
        try:
            if isinstance(color, str):
                if color.startswith('#') and len(color) >= 7:
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # Correct slicing
                else:
                    rgba_wx = wx.NamedColour(color)
                    rgb = rgba_wx.Get()[:3]  # Exclude alpha
            elif isinstance(color, tuple):
                rgb = color
        except Exception as e:
            print(f"Error processing selected color: {e}")
        return rgb

