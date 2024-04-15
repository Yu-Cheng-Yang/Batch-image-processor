from matplotlib import font_manager
import wx

from uibase.ycwxEntryWidgets import LabeledEntryPanel
from uibase.ycwxColorSelectorPanel import ColorSelectorPanel
from ycLocalize import localize

class ImageFontSelector(wx.Panel):
    def __init__(self, parent, font_name = 'Arial', font_size = 9, font_color = (0, 0, 0), is_bold = False, is_italic = False, color_label = 'Select Color', **kwargs):
        super().__init__(parent, **kwargs)
        self.font = wx.Font(font_size, wx.FONTFAMILY_DEFAULT, 
                            wx.FONTSTYLE_ITALIC  if is_italic else wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD if is_bold else wx.FONTWEIGHT_NORMAL,
                            faceName = font_name)
        self.color = font_color

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label = wx.StaticText(self, label=localize('Font'))
        self.entry = wx.TextCtrl(self, value = font_name, style=wx.TE_READONLY)
        self.button = wx.Button(self, label = localize('Select') + '...')
        self.button.Bind(wx.EVT_BUTTON, self.on_font_select)
        
        hbox.Add(self.label, 0, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.entry, 1, flag=wx.LEFT | wx.RIGHT, border = 8)
        hbox.Add(self.button, 0, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(hbox, 1, wx.EXPAND | wx.LEFT | wx.Right)
        vbox.AddSpacer(8)
        self.font_size_entry = LabeledEntryPanel(self, label_text = localize('Font Size'), default_value=font_size)
        vbox.Add(self.font_size_entry, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)

        self.bold_checkbox = wx.CheckBox(self, label = localize('Bold'))
        self.bold_checkbox.SetValue(is_bold)
        vbox.Add(self.bold_checkbox, 1, wx.EXPAND | wx.LEFT)

        self.italic_checkbox = wx.CheckBox(self, label = localize('Italic'))
        self.italic_checkbox.SetValue(is_italic)
        vbox.Add(self.italic_checkbox, 1, wx.EXPAND | wx.LEFT)

        self.color_selector = ColorSelectorPanel(self, color_label, self.color)
        vbox.Add(self.color_selector, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)

        self.SetSizer(vbox)

    def get_tabbed_widgets(self):
        tabbed_widgets = [self.entry, self.button]
        tabbed_widgets.extend(self.font_size_entry.get_tabbed_widgets())
        tabbed_widgets.extend([self.bold_checkbox, self.italic_checkbox])
        tabbed_widgets.extend(self.color_selector.get_tabbed_widgets())
        return tabbed_widgets

    def get_color(self):
        return self.color_selector.get_color()

    def get_font(self):
        return self.font
    
    def get_font_size(self):
        return self.font_size_entry.get_value()
    
    def is_bold(self):
        return self.bold_checkbox.GetValue()

    def is_italic(self):
        return self.italic_checkbox.GetValue()

    def on_font_select(self, evnet):
        in_font_data = wx.FontData()
        
        if self.bold_checkbox.GetValue():
            self.font.SetWeight(wx.FONTWEIGHT_BOLD)
        else:
            self.font.SetWeight(wx.FONTWEIGHT_NORMAL)
        if self.italic_checkbox.GetValue():
            self.font.SetStyle(wx.FONTSTYLE_ITALIC)
        else:
            self.font.SetStyle(wx.FONTSTYLE_NORMAL)
            
        self.font.SetPointSize(self.font_size_entry.get_value())
        
        in_font_data.SetInitialFont(self.font)
        in_font_data.SetColour(self.get_color())
        
        dialog = wx.FontDialog(self, in_font_data)
        if dialog.ShowModal() == wx.ID_OK:
            out_font_data = dialog.GetFontData()
            self.font = out_font_data.GetChosenFont()  # Get the selected font
            self.color = out_font_data.GetColour()
            self.color_selector.set_color(self.color.Get(includeAlpha=False))
            self.bold_checkbox.SetValue(self.font.GetWeight() == wx.FONTWEIGHT_BOLD)
            self.italic_checkbox.SetValue(self.font.GetStyle() == wx.FONTSTYLE_ITALIC)
            self.entry.SetValue(self.font.GetFaceName())
            font = wx.Font(self.font)
            font.SetPointSize(10)
            self.entry.SetFont(font)
            self.font_size_entry.set_value(self.font.GetPointSize())
            self.entry.Refresh()
            self.font_size_entry.Refresh()
            self.bold_checkbox.Refresh()
            self.italic_checkbox.Refresh()

# get_font_path is used for drawing text in pillow image which needs font path
# matplotlib is used for querying the font file path.
# TODO: Maybe need a lightwight library for it or define a font manager only for retireving path.
def get_font_path(wxfont: wx.Font):
    font_name = wxfont.GetFaceName()
    font_size = wxfont.GetPointSize()  # Get the font size
    font_weight = 'bold' if wxfont.GetWeight() == wx.FONTWEIGHT_BOLD else 'normal'
    font_style = 'normal'
    if wxfont.GetStyle() == wx.FONTSTYLE_ITALIC:
        font_style = 'italic'
    elif wxfont.GetStyle() == wx.FONTSTYLE_SLANT:
        font_style = 'oblique'

    font_properties = font_manager.FontProperties(family=font_name, size=font_size, weight=font_weight, style=font_style)
    return font_manager.findfont(font_properties)

