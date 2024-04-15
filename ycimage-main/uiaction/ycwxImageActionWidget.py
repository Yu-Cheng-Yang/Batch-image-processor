import wx

import action.ycImageAction as ycImageAction
from uibase.ycwxEntryWidgets import LabeledEntryPanel, LabeledEnumCombobox
from uibase.ycwxColorSelectorPanel import ColorSelectorPanel
from uibase.ycwxImageFontSelector import ImageFontSelector
from uibase.ycwxImageFileSelector import ImageFileSelector
from ycLocalize import localize
from uibase.ycwxImageCheckBox import ImageCheckBox

#===============================================================
# Class ImageActionWidget
class ImageActionWidget(wx.Panel):
    def __init__(self, parent, action, vertical_space = 10, **kwargs):
        super().__init__(parent, -1, **kwargs)
        #self.SetScrollbars(1, 1, 1, 1)
        self.action = action
        self.vertical_space = vertical_space
        self.widget_to_spacer = {}
        self.dynamic_show_widgets = []
        self.apply_callback = None

        self.tabbed_widgets = []
        
        self.Bind(wx.EVT_SIZE, self.on_resize)
        
        self._create_widgets()
    
        font_size = 10
        font_family = wx.FONTFAMILY_SWISS  # A sans-serif font
        font_style = wx.FONTSTYLE_NORMAL
        font_weight = wx.FONTWEIGHT_BOLD
        font_face_name = ""  # Default face name
        
        # Create a wx.Font object
        font = wx.Font(font_size, font_family, font_style, font_weight, faceName=font_face_name)
        self.SetFont(font)

        self._update_layout()
        
    def _create_widgets(self):
        action_type_name = ''
        if self.action:
            action_type_name = ycImageAction.get_enum_display_name(self.action.get_action_type()) if self.action else ''
        self.label_action = wx.StaticText(self, label=localize("Action")+ ": " + action_type_name)
        self.button_apply = wx.Button(self, label=localize("Apply"))
        self.static_line = wx.StaticLine(self, style = wx.LI_HORIZONTAL)
        
        # Bind    
        self.button_apply.Bind(wx.EVT_BUTTON, self._on_apply)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddSpacer(15)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.hbox.Add(self.label_action, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.hbox.AddStretchSpacer()
        self.hbox.Add(self.button_apply, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(self.hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border = 15)
        #self.add_spacer_panel()
        vbox.AddSpacer(self.vertical_space)
        vbox.Add(self.static_line, 0, wx.EXPAND| wx.RIGHT | wx.LEFT, border = 15)

        self.sub_window = wx.ScrolledWindow(self, -1)
        self.sub_window.SetScrollbars(1, 1, 1, 1)

        self.sub_vbox = wx.BoxSizer(wx.VERTICAL)
        self._create_sub_widgets()

        self.add_spacer_panel()
        if len(self.tabbed_widgets) > 0:
            self.tabbed_widgets[0].SetFocus()

        self.sub_window.SetSizer(self.sub_vbox)

        vbox.Add(self.sub_window, 1, wx.EXPAND| wx.RIGHT | wx.LEFT, border = 0)
        
        self.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_tab_pressed)
        
    def on_tab_pressed(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            # Check if Shift is held down for reverse tabbing
            shiftPressed = event.ShiftDown()
            currentFocus = wx.Window.FindFocus()
            if currentFocus:
                currentIndex = self.tabbed_widgets.index(currentFocus)
                if shiftPressed:
                    # Focus previous widget
                    newIndex = (currentIndex - 1) % len(self.tabbed_widgets)
                else:
                    # Focus next widget
                    newIndex = (currentIndex + 1) % len(self.tabbed_widgets)
                self.tabbed_widgets[newIndex].SetFocus()
                self.tabbed_widgets[newIndex].Raise()
            event.Skip(False) # Prevent further processing to override default tab behavior
        else:
            event.Skip() # Allow other keys to be processed normally

    def set_font_recursive(self, parent, font):
        parent.SetFont(font)
        for child in parent.GetChildren():
            if isinstance(child, wx.Window):
                child.SetFont(font)
            
            if isinstance(child, wx.Window):
                self.set_font_recursive(child, font)
                     
    def set_font(self, font):
        self.set_font_recursive(self, font)
        self.Layout()
        self.Refresh()

    def set_apply_callback(self, callback):
        self.apply_callback = callback

    def on_resize(self, event):
        self.Refresh()
        event.Skip()

    # Used for creating sub widgets in inherite class
    def _create_sub_widgets(self):
        pass
    
    def _show_widgets(self):
        # Forget all widgets
        for widget in self.dynamic_show_widgets:
            self._show_widget(widget, False)

        # Show title
        action_type_name = ycImageAction.get_enum_display_name(self.action.get_action_type()) if self.action else ''
        self.label_action.SetLabelText(localize("Action") + ": " + action_type_name)
        self.label_action.Show(True)
        self.button_apply.Show(self.action != None)
        self.static_line.Show(True)
        
        # Show sub widgets for inherite class
        self._show_sub_widgets()

    # Show sub widgets for inherite class
    def _show_sub_widgets(self):
        pass

    def on_update_layout(self, event):
        self._update_layout()
        
    def _update_layout(self):
        self._show_widgets()
        self.Layout()
        self.Refresh()
        
    def _on_apply(self, event):
        self._on_apply_internal()
        if self.apply_callback:
            self.apply_callback(self.action)
    
    def _on_apply_internal(self):
        pass
        #print('Should be overrid in inherite class')
    
    def _get_export_names_from_enum(self, enum_class):
        return ycImageAction.get_export_names_from_enum_class(enum_class)

    def _get_enum_from_export_name(self, enum_class, name : str):
        return ycImageAction.get_enum_from_export_name(enum_class, name)
    
    def _get_enum_class_display_names(enum_value):
        return ycImageAction.get_export_names_from_enum_class(enum_value.__class__)
    
    def add_labeled_enum_combobox(self, label_text, enum_value, dynamic_show = True):
        type_combobox = LabeledEnumCombobox(self.sub_window, localize(label_text), enum_value, self.on_update_layout)
        self._add_to_vertical_resizer(type_combobox)
        if dynamic_show:
            self.dynamic_show_widgets.append(type_combobox)
            
        return type_combobox

    def add_labeled_entry(self, label_text, value, dynamic_show = True):
        entry = LabeledEntryPanel(self.sub_window, localize(label_text), value)
        self._add_to_vertical_resizer(entry)
        if dynamic_show:
            self.dynamic_show_widgets.append(entry)
        return entry

    def add_color_selector(self, label_text, select_color, dynamic_show = True):
        color_selector = ColorSelectorPanel(self.sub_window, localize(label_text), select_color)
        self._add_to_vertical_resizer(color_selector)
        if dynamic_show:
            self.dynamic_show_widgets.append(color_selector)
        return color_selector

    def add_file_selector(self, label_text, select_file, dynamic_show = True):
        file_selector = ImageFileSelector(self.sub_window, localize(label_text), select_file)
        self._add_to_vertical_resizer(file_selector)
        if dynamic_show:
            self.dynamic_show_widgets.append(file_selector)
        return file_selector

    def add_font_selector(self, font_name = 'Arial', font_size = 9, font_color = (0, 0, 0),
                          is_bold = False, is_italic = False, color_label = 'Select Color',
                          dynamic_show = True):
        font_selector = ImageFontSelector(self.sub_window, font_name = font_name, font_size = font_size,
                                             font_color = font_color, is_bold = is_bold,
                                             is_italic = is_italic, color_label = localize(color_label))
        self._add_to_vertical_resizer(font_selector)
        if dynamic_show:
            self.dynamic_show_widgets.append(font_selector)
        return font_selector

    def add_checkbox(self, label_text, value, dynamic_show = True):
        checkbox = ImageCheckBox(self.sub_window, label = localize(label_text))
        checkbox.SetValue(value)
        if dynamic_show:
            self.dynamic_show_widgets.append(checkbox)
        self._add_to_vertical_resizer(checkbox)
        checkbox.Bind(wx.EVT_CHECKBOX, self.on_update_layout)
        return checkbox

    def add_spacer_panel(self):
        spacer_panel = wx.Panel(self.sub_window, size=(-1, self.vertical_space))
        #spacer_panel.SetBackgroundColour(self.GetBackgroundColour())
        self.sub_vbox.Add(spacer_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)  # Add with proportion 0 to maintain fixed height
        return spacer_panel
    
    def _add_to_vertical_resizer(self, widget):
        # Add a spacer panel
        spacer_panel = self.add_spacer_panel()
        self.sub_vbox.Add(widget, flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 15)
        self.widget_to_spacer[widget] = spacer_panel

        self.tabbed_widgets.extend(widget.get_tabbed_widgets())
            
    def _show_widget(self, widget, show = True):
        widget.Show(show)
        if widget in self.widget_to_spacer:
            self.widget_to_spacer[widget].Show(show)
        
