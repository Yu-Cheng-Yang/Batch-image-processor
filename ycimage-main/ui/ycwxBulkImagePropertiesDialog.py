import os

import wx
from wx.lib.imageutils import grayOut, stepColour

from action.ycImageActionsPerformer import ImageActionsPerformer
from uibase.ycwxEntryWidgets import LabeledEntryPanel, LabeledEnumCombobox
from uibase.ycwxColorSelectorPanel import ColorSelectorPanel
from ycLocalize import localize, get_language, set_language
from ycConfig import get_config, update_config, get_config_image_background_color

class BulkImagePropertiesDialog(wx.Dialog):
    def __init__(self, parent, title, performer : ImageActionsPerformer):
        super(BulkImagePropertiesDialog, self).__init__(parent, title=title, size=(600, 480))
        
        self.performer = performer        

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Folder selection input
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        label_description = wx.StaticText(panel, label=localize("Description"))
        vbox.Add(label_description, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.description = wx.TextCtrl(panel, id=-1, value= performer.get_description(), pos=wx.DefaultPosition,
                            size=(-1,100),
                            style= wx.TE_MULTILINE | wx.SUNKEN_BORDER | wx.HSCROLL)
        
        vbox.Add(self.create_custom_border_sizer(self.description), flag=wx.EXPAND | wx.TOP, border = 10)

        label_output = wx.StaticText(panel, label=localize("Output"))
        vbox.Add(label_output, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        label_foler = wx.StaticText(panel, label=localize("Folder") + ":")
        self.folderPath = wx.TextCtrl(panel)
        self.folderPath.SetValue(performer.get_output_folder())
        self.browseBtn = wx.Button(panel, label=localize("Browse" + "..."))
        self.browseBtn.Bind(wx.EVT_BUTTON, self.on_browse)

        hbox1.Add(label_foler, flag=wx.RIGHT, border=8)
        hbox1.Add(self.folderPath, proportion=1)
        hbox1.Add(self.browseBtn, flag=wx.LEFT, border=5)
        
        vbox.Add(self.create_custom_border_sizer(hbox1), flag=wx.EXPAND | wx.TOP, border = 10)

        self.quality = LabeledEntryPanel(panel, localize('Image Quality:'), performer.get_output_quality())
        self.format = LabeledEnumCombobox(panel, localize('Image Format:'), performer.get_output_format())

        self.checkbox = wx.CheckBox(panel, label = localize('Preserve Exif information'))
        self.checkbox.SetValue(True)
        
        self.image_background_color =  ColorSelectorPanel(panel, localize('Select image background color'), get_config_image_background_color())
        
        lang_hbox = wx.BoxSizer(wx.HORIZONTAL)  
        # Create the Label widget and pack it to the left side
        lang_label = wx.StaticText(panel, label=localize("Select Language"))
        lang_hbox.Add(lang_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        
        self.lang = get_language()
        self.lang_choices = ["English", "French - Français", "Chinese - 简体中文"]
        self.lang_abbrs = ["en", "fr", "zh-cn"]
        lang_index = 0
        for index, abbr in enumerate(self.lang_abbrs):
            if abbr == self.lang:
                lang_index = index
                break
        
        self.lang_comboBox = wx.ComboBox(panel, choices=self.lang_choices, style=wx.CB_READONLY)
        self.lang_comboBox.SetSelection(lang_index)
        self.lang_comboBox.Bind(wx.EVT_COMBOBOX, self.on_language_select)
        lang_hbox.Add(self.lang_comboBox, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)

        vbox.Add(self.create_custom_border_sizer(self.quality), flag=wx.EXPAND | wx.TOP, border = 10)
        vbox.Add(self.create_custom_border_sizer(self.format), flag=wx.EXPAND | wx.TOP, border = 10)
        vbox.Add(self.create_custom_border_sizer(self.checkbox), flag=wx.EXPAND | wx.TOP, border = 10)
        vbox.Add(self.image_background_color, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border = 10)
        vbox.Add(lang_hbox, flag=wx.EXPAND|wx.LEFT | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # Buttons
        btnSizer = wx.StdDialogButtonSizer()
        okBtn = wx.Button(panel, wx.ID_OK)
        cancelBtn = wx.Button(panel, wx.ID_CANCEL)
        btnSizer.AddButton(okBtn)
        btnSizer.AddButton(cancelBtn)
        btnSizer.Realize()
        vbox.Add(btnSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        
        panel.SetSizer(vbox)
        
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    def create_custom_border_sizer(self, widget):
        custom_border_sizer = wx.BoxSizer(wx.HORIZONTAL)
        custom_border_sizer.AddSpacer(30)
        custom_border_sizer.Add(widget, 1, wx.EXPAND)
        custom_border_sizer.AddSpacer(30)
        return custom_border_sizer
        
    def on_browse(self, event):
        # Create and show a DirDialog
        dlg = wx.DirDialog(self, localize("Choose a directory") + ":")
        if dlg.ShowModal() == wx.ID_OK:
            # Set the folder path in the TextCtrl
            self.folderPath.SetValue(dlg.GetPath())
        dlg.Destroy()

    def get_values(self):
        # Return the folder path and Text2 value
        return self.folderPath.GetValue(), self.txt2.GetValue()

    def on_ok(self, event):
        folder_path = self.folderPath.GetValue()
        if folder_path and not os.path.exists(folder_path):
            wx.MessageBox(localize("The folder does not exist. Please enter a valid folder path."), "Error", wx.OK | wx.ICON_ERROR)
        else:
            self.performer.set_description(self.description.GetValue())
            self.performer.set_output_folder(self.folderPath.GetValue())
            self.performer.set_output_format(self.format.get_value())
            self.performer.set_output_quality(self.quality.get_value())
            self.performer.set_image_background_color(self.image_background_color.get_color())
            self.EndModal(wx.ID_OK)  # Only close the dialog if validation passes

            config1 = {}
            config1["Language"] = self.lang
            color = self.image_background_color.get_color()
            config1["ImageBackgroundColor"]= str(color[0]) + "," + str(color[1]) + "," + str(color[2])
            update_config(config1)
            
    def on_language_select(self, event):
        index = self.lang_comboBox.GetSelection()
        self.lang = self.lang_abbrs[index]
        set_language(self.lang)
        
        