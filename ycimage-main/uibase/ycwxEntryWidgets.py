from enum import Enum
import wx
import action.ycImageAction as ycImageAction

#===============================================================
# Class IntEntry
class IntValidator(wx.Validator):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return IntValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if text == "":
            return True  # Allow empty string

        try:
            int(text)
            return True
        except ValueError:
            wx.MessageBox("This field must contain an integer.", "Error")
            return False

    def OnChar(self, event):
        """Filter out non-numeric key strokes."""
        key_code = event.GetKeyCode()
        
        # Allow ASCII numerics and control characters
        if key_code < wx.WXK_SPACE or key_code == wx.WXK_DELETE or chr(key_code).isdigit():
            event.Skip()
            return
        
        # Ignore non-numeric characters
        if not chr(key_code).isdigit():
            return

        # Allow navigation keys
        if key_code in [wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_TAB]:
            event.Skip()
 
    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.
                     
class IntEntry(wx.TextCtrl):
    def __init__(self, parent, default_value='', **kwargs):
        super().__init__(parent, validator = IntValidator(), **kwargs)
        self.SetValue('')
        if isinstance(default_value, int):
            self.SetValue(str(default_value))
        elif isinstance(default_value, str):
            try:
                _ = int(default_value)
                self.SetValue(default_value)
            except:
                pass

# Class IntEntry
class FloatValidator(wx.Validator):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return FloatValidator()

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        if text == "":
            return True  # Allow empty string

        try:
            float(text)
            return True
        except ValueError:
            wx.MessageBox("This field must contain a floating-point number.", "Error")
            return False

    def OnChar(self, event):
        key_code = event.GetKeyCode()
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()

        # Allow control characters and decimal points if there isn't one already
        if key_code < wx.WXK_SPACE or key_code == wx.WXK_DELETE or key_code > 255:
            event.Skip()
            return

        # Allow digits, one decimal point, and backspace
        if chr(key_code).isdigit() or key_code == wx.WXK_BACK or (chr(key_code) == '.' and '.' not in text):
            event.Skip()
            return

        # If not a digit, deletion, decimal point (if one is not already present), or navigation key,
        # do not propagate the event further.
        return

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

class FloatEntry(wx.TextCtrl):
    def __init__(self, parent, default_value='', **kwargs):
        super().__init__(parent, validator = FloatValidator(), **kwargs)
        self.SetValue('')
        if isinstance(default_value, float):
            self.SetValue(str(default_value))
        elif isinstance(default_value, str):
            try:
                _ = float(default_value)
                self.SetValue(default_value)
            except:
                pass

#===============================================================
# Class LabeledEntryPanel
class LabeledEntryPanel(wx.Panel):
    def __init__(self, parent, label_text, default_value = '', **kwargs):
        super().__init__(parent, **kwargs)
        self.default_value = default_value
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label = wx.StaticText(self, label=label_text)
        hbox.Add(self.label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hbox.AddSpacer(10)

        self.entry = None
        if isinstance(default_value, int):
            self.entry = IntEntry(self, default_value, **kwargs)
        elif isinstance(default_value, float):
            self.entry = FloatEntry(self, default_value, **kwargs)
        else:
            self.entry = wx.TextCtrl(self, **kwargs)
            self.entry.SetValue(default_value)
        hbox.Add(self.entry, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        self.SetSizer(hbox)
     
    def get_tabbed_widgets(self):
        return [self.entry]
 
    def get_entry(self):
        return self.entry
    
    def get_value(self):
        if isinstance(self.default_value, int):
            return int(self.entry.GetValue())
        elif isinstance(self.default_value, float):
            return float(self.entry.GetValue())

        return self.entry.GetValue()
    
    def set_value(self, value):
        if isinstance(self.default_value, int):
            try:
                self.entry.SetValue(str(int(value)))
            except:
                print('Wrong value type set for IntEnty')
        elif isinstance(self.default_value, float):
            try:
                self.entry.SetValue(str(float(value)))
            except:
                print('Wrong value type set for FloatEnty')
        if isinstance(self.default_value, str):
            self.entry.SetValue(value)
        else:
            try:
                self.entry.SetValue(str(value))
            except:
                print("Wrong value type for LabeledEntryPanel")
        
#===============================================================
# Class LabeledEnumCombobox
class LabeledEnumCombobox(wx.Panel):
    def __init__(self, parent, label_text, enum_value, callback = None, **kwargs):
        super().__init__(parent)
        self.enum_value_class = enum_value.__class__
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)  
        # Create the Label widget and pack it to the left side
        self.label = wx.StaticText(self, label=label_text)
        hbox.Add(self.label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        
        # Create the Combobox widget with provided values
        values = ycImageAction.get_display_names_from_enum_class(self.enum_value_class)
        self.comboBox = wx.ComboBox(self, choices=values, style=wx.CB_READONLY)
        enum_index = list(self.enum_value_class).index(enum_value)
        self.comboBox.SetSelection(enum_index)
        if callback:
            self.comboBox.Bind(wx.EVT_COMBOBOX, callback)
        hbox.Add(self.comboBox, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL, border=8)
        self.SetSizer(hbox)
        
    def get_tabbed_widgets(self):
        return [self.comboBox]
 
    def get_combo_box(self):
        return self.comboBox
    
    def get_value(self):
        return list(self.enum_value_class)[self.comboBox.GetSelection()]

