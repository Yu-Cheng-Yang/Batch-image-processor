
from enum import Enum
import wx

class BorderPanelType(Enum):
    NONE  = 0
    SOLID = 1
    DOTTED = 2
    LONG_DASH = 3
    SHORT_DASH = 4
    DOT_DASH = 5
    DOUBLE = 6
    GROOVE = 7
    RIDGE = 8
    INSET= 9
    OUTSET = 10
    
class BorderedPanel(wx.Panel):
    def __init__(self, parent, border_type = BorderPanelType.SOLID, border_color = (128, 128, 128), border_thickness = 1, **kwargs):
        super().__init__(parent, **kwargs)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.contained_widget = None
        self.border_type = border_type
        self.border_thickness = border_thickness
        self.border_width = self.get_border_width()

        self.color = border_color
        self.lighten_color = self.get_lighten_color(self.color, 1.6)

    def add_widget(self, widget):
        self.contained_widget = widget
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(widget, 1, wx.EXPAND | wx.ALL, border = self.border_width+1)
        self.SetSizer(sizer)

    def get_contained_widget(self):
        return self.contained_widget
    
    def get_lighten_color(self, rgb, factor=1.2):
        # Ensure the factor is at least 1
        factor = max(factor, 1)
        
        new_r = min(int(rgb[0] * factor), 255)
        new_g = min(int(rgb[1] * factor), 255)
        new_b = min(int(rgb[2] * factor), 255)
        
        return (new_r, new_g, new_b)

    def get_border_width(self):
        border_width = self.border_thickness
        if self.border_type == BorderPanelType.DOUBLE:
            border_width = self.border_thickness * 3
        elif self.border_type == BorderPanelType.GROOVE:
            border_width = self.border_thickness + 3
        elif self.border_type == BorderPanelType.RIDGE:
            border_width = self.border_thickness + 2
        elif self.border_type == BorderPanelType.INSET:
            border_width = self.border_thickness + 2
        elif self.border_type == BorderPanelType.OUTSET:
            border_width = self.border_thickness + 2
        elif self.border_type == BorderPanelType.NONE:
            border_width = 0

        return border_width
        
    def on_paint(self, event):
        pass
        dc = wx.PaintDC(self)
        dc.Clear()
        if self.border_type == BorderPanelType.NONE:
            return
        
        style = wx.PENSTYLE_SOLID
        if self.border_type == BorderPanelType.DOTTED:
            style = wx.PENSTYLE_DOT
        elif self.border_type == BorderPanelType.DOT_DASH:
            style = wx.PENSTYLE_DOT_DASH
        elif self.border_type == BorderPanelType.LONG_DASH:
            style = wx.PENSTYLE_LONG_DASH
        elif self.border_type == BorderPanelType.SHORT_DASH:
            style = wx.PENSTYLE_SHORT_DASH

        
        width, height = self.GetSize()

        dc.SetPen(wx.Pen(self.color, self.border_thickness, style))
        if self.border_type == BorderPanelType.SOLID :
            dc.DrawRectangle(0, 0, width - 1, height - 1)
        if (self.border_type == BorderPanelType.DOTTED or
            self.border_type == BorderPanelType.DOT_DASH or
            self.border_type == BorderPanelType.LONG_DASH or
            self.border_type == BorderPanelType.SHORT_DASH)  :
            dc.DrawLine(0, 0, width - 1, 0)
            dc.DrawLine(0, 0, 0, height - 1)
            dc.DrawLine(width - 1, 0, width - 1, height - 1)
            dc.DrawLine(0, height - 1, width - 1, height -1 )

        elif self.border_type == BorderPanelType.DOUBLE:
            dc.DrawRectangle(0, 0, width - 1, height - 1)
            width = width - 1 - self.border_thickness * 4
            height = height - 1 - self.border_thickness * 4
            dc.DrawRectangle(self.border_thickness * 2, self.border_thickness * 2, width, height)
        elif self.border_type == BorderPanelType.GROOVE:
            dc.DrawLine(0, 0, width - 1, 0)
            dc.DrawLine(0, 0, 0, height - 1)
            dc.DrawLine(3, height - 3, width - 3, height - 3)
            dc.DrawLine(width - 3, 3, width - 3, height - 3)

            dc.SetPen(wx.Pen(self.lighten_color, self.border_thickness, style))
            dc.DrawLine(1, 1, 1, height - 2)
            dc.DrawLine(1, 1, width - 2, 1)
            dc.DrawLine(width - 1, 1, width - 1, height - 1)
            dc.DrawLine(1, height -1 , width - 1 , height - 1)
        elif self.border_type == BorderPanelType.RIDGE:
            dc.SetPen(wx.Pen(self.lighten_color, self.border_thickness, style))
            dc.DrawRectangle(0, 0, width - 2, height - 2)
            dc.SetPen(wx.Pen(self.color, self.border_thickness, style))
            dc.DrawRectangle(1, 1, width - 1, height - 1)
        elif self.border_type == BorderPanelType.INSET:
            dc.DrawLine(0, 0, width - 1, 0)
            dc.DrawLine(0, 0, 0, height - 1)

            dc.SetPen(wx.Pen(self.lighten_color, self.border_thickness, style))
            dc.DrawLine(self.border_thickness, height - 1, width - 1, height - 1)
            dc.DrawLine(width - 1, self.border_thickness, width - 1, height - 1)
        elif self.border_type == BorderPanelType.OUTSET:
            dc.DrawLine(0, height - 1, width - 1, height - 1)
            dc.DrawLine(width - 1, 0, width - 1, height - 1)

            dc.SetPen(wx.Pen(self.lighten_color, self.border_thickness, style))
            dc.DrawLine(0, 0, width - 1, 0)
            dc.DrawLine(0, 0, 0, height - 1)