import os
import time
import stat
import platform

import ycExifDisplayInformation
import action.ycImageAction as ycImageAction
import wx

from ycLocalize import localize

from PIL import Image

def wxImageToPilImage(wx_image):
    """Convert wx.Image to PIL.Image."""
    # Ensure the image is in RGB format
    if wx_image.HasAlpha():
        wx_image = wx_image.ConvertAlphaToMask()
        image_mode = 'RGBA'
    else:
        image_mode = 'RGB'
    
    # Get the size of the image
    width, height = wx_image.GetSize()
    
    # Get the image data as a bytes object
    image_data = wx_image.GetDataBuffer() if image_mode == 'RGB' else wx_image.GetAlphaBuffer()
    
    # Create a PIL.Image from the image data
    pil_image = Image.frombuffer(image_mode, (width, height), image_data, "raw", image_mode, 0, 1)
    
    return pil_image

def is_hidden(filepath):
    if platform.system() == "Windows":
        try:
            import win32api
            import win32con
            attrs = win32api.GetFileAttributes(filepath)
            return bool(attrs & win32con.FILE_ATTRIBUTE_HIDDEN)
        except ImportError:
            print("pywin32 module not installed. Unable to check hidden attribute on Windows.")
            return False
    else:
        return os.path.basename(filepath).startswith(".")

def get_formatted_time(time1):
    mod_time = time.localtime(time1)
    formatted_time = time.strftime("%B %e, %Y, %H:%M:%S", mod_time)
    return formatted_time

def get_file_information(file_path, wx_image):
    info = {}
    if not file_path:
        return info
    
    try:
        file_stats = os.stat(file_path)

        info['File Name'] = os.path.basename(file_path)
        info['Directory'] = os.path.dirname(file_path)
        if file_stats.st_size > 1024 * 1024:
            info['File Size'] = f'%.2f MB' % (file_stats.st_size/(1024*1024))
        else:
            info['File Size'] = f'%.2f KB' % (file_stats.st_size/1024)

        if wx_image:
            width, height = wx_image.GetSize()
            info['Image Size'] = f'%s x %s' % (width, height)
        else:
            width, height = wx_image.GetSize()
            info['Image Size'] = '0 x 0'

        is_writable = file_stats.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)    
        info['Read Only'] = 'Yes' if not is_writable else 'No'
        info['Hidden'] = 'Yes' if is_hidden(file_path) else 'No'

        info['Last Modified Time'] = get_formatted_time(file_stats.st_mtime)
        info['Last Accessed Time'] = get_formatted_time(file_stats.st_atime)
        info['Creation time'] = get_formatted_time(file_stats.st_ctime)
  
        return info
    except OSError as e:
        pass
    
    return info

def get_wx_image_from_pil_image(pil_image):
    if not pil_image:
        return None

    wx_image = wx.Image(pil_image.size[0], pil_image.size[1])
    wx_image.SetData(pil_image.convert("RGB").tobytes())
    return wx_image

# PIL can support more formats. so use pillow load image and convert to wx image
def load_wx_image_from_file(file_name):
    pil_image = ycImageAction.load_image(file_name)
    return get_wx_image_from_pil_image(pil_image)

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.wx_image = None
        self.wx_bitmap_image = None
        self.scale = 1.0

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def set_image(self, wx_image):
        self.wx_image = wx_image
        self.build_display_image()        
        self.Refresh()

    def get_image(self):
        return self.wx_image
    
    def get_scale(self):
        return self.scale
    
    def get_size(self):
        return self.wx_image.GetSize() if self.wx_image else (0, 0)
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        if self.wx_bitmap_image:
            this_size = self.GetSize()
            bitmap_size = self.wx_bitmap_image.GetSize()
            pos_x = int((this_size.width - bitmap_size.GetWidth()) / 2)
            pos_y = int((this_size.height - bitmap_size.GetHeight()) / 2)

            dc.DrawBitmap(self.wx_bitmap_image, pos_x, pos_y, True)

    def on_resize(self, event):
        self.build_display_image()
        self.Refresh()
        event.Skip()
    
    # Display image is the scaled image when original image is larger than the panel    
    def build_display_image(self):
        this_size = self.GetSize()
        
        self.wx_bitmap_image = None
        if self.wx_image:
            scale_image = self.wx_image
            img_width, img_height = self.wx_image.GetSize()
            if img_width > this_size.width or img_height > this_size.height:
                scale1 = img_width / this_size.width
                scale2 = img_height / this_size.height
                scale = scale1 if scale1 > scale2 else scale2
                img_width = int(img_width / scale)
                img_height = int(img_height / scale)
                    
                scale_image = self.wx_image.Scale(img_width, img_height, wx.IMAGE_QUALITY_HIGH)
                self.scale = 1.0 / scale
            
            # Convert to bitmap
            self.wx_bitmap_image = wx.Bitmap(scale_image)

class ImagePreviewNotebook(wx.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.filename = None
        self.original_image = None
        self.preview_image = None
        self.exif_dict = None

        self.create_tabs()

    def get_original_image(self):
        return self.original_image
    
    def set_image_background_color(self, color):
        self.tab_image.SetBackgroundColour(color)
        self.tab_preview.SetBackgroundColour(color)
        self.Refresh()

    def set_image_file(self, filename):
        self.filename = filename
        if filename:
            self.original_image, self.exif_dict = ycImageAction.load_image_and_exif(filename)
            wx_image = get_wx_image_from_pil_image(self.original_image)
        else:   
            self.original_image = None
            self.exif_dict = None
            wx_image = None
         
        self.tab_image.set_image(wx_image)
        self.populate_exif_information()
        self.populate_file_information()
        
    def set_preview_image(self, pil_image):
        self.preview_image = pil_image
        wx_image = get_wx_image_from_pil_image(pil_image)
        self.tab_preview.set_image(wx_image)

    def set_renamed_files(self, files, renamed_files):
        self.listctrl_rename.DeleteAllItems()
        index = 0
        for file, renamed_file in zip(files, renamed_files):
            self.listctrl_rename.InsertItem(index, file)
            self.listctrl_rename.SetItem(index, 1, renamed_file)
            index = index + 1
        
    def create_tabs(self):
        self.tab_image = ImagePanel(self)
        self.tab_image.SetBackgroundColour(wx.Colour(40, 40, 40, 255))
        self.tab_image.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)
            
        self.AddPage(self.tab_image, localize('Original Image'))

        self.tab_preview = ImagePanel(self)
        self.tab_preview.SetBackgroundColour(wx.Colour(40, 40, 40, 255))
        self.tab_preview.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)

        self.AddPage(self.tab_preview, localize('Preview Image'))

        # Add exif information tab
        self.listctrl_exif = self.add_list_tab(localize('Exif'), [localize('Key'), localize('Value')])
    
        # Add file information tab
        self.listctrl_file = self.add_list_tab(localize('File Info'), [localize('Key'), localize('Value')])

        # Add rename tab
        self.listctrl_rename = self.add_list_tab(localize('Rename'), [localize('Name'), localize('Rename')])

    def add_list_tab(self, title, column_names):
        tab = wx.Panel(self)
        listctrl = wx.ListCtrl(tab, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        listctrl.Bind(wx.EVT_SIZE, self.on_listctrl_resize)
        
        listctrl.InsertColumn(0, column_names[0])
        listctrl.InsertColumn(1, column_names[1])
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(listctrl, 1, wx.EXPAND)
        tab.SetSizer(sizer)

        self.AddPage(tab, title)
        return listctrl

    def on_show_in_viwer(self, event, object):
        pil_image = None
        if object == self.tab_image:
            pil_image = self.original_image
        elif object == self.tab_preview:
            pil_image = self.preview_image
        if pil_image:
            pil_image.show()
            
    def on_right_click(self, event):
        menu = wx.Menu()
        item1 = menu.Append(-1, "Show in Viewer")
        
        # Bind menu item events
        self.Bind(wx.EVT_MENU, lambda evt, object=event.GetEventObject(): self.on_show_in_viwer(evt, object), item1)

        # Show the context menu
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()  # Destroy the menu after use
        
    def on_listctrl_resize(self, event):
        # Call event.Skip() to allow the list control to process the event as well and actually perform the resize
        event.Skip()
        
        listctrl = event.GetEventObject()
        # Dynamically adjust column widths here
        total_width = listctrl.GetClientSize().width
        col_count = listctrl.GetColumnCount()
        for col in range(col_count):
            listctrl.SetColumnWidth(col, total_width // col_count)

    def populate_exif_information(self):
        if self.listctrl_exif:
            self.listctrl_exif.DeleteAllItems()

        if self.exif_dict:
            exif_Info = ycExifDisplayInformation.ExifDisplayInformation(exif_dict = self.exif_dict)
            exif_display_dict = exif_Info.get_display_dict()

            section_title_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

            index = 0
            for key, value in exif_display_dict.items():
                if value:
                    # insert section title
                    self.listctrl_exif.InsertItem(index, key)
                    self.listctrl_exif.SetItemTextColour(index, wx.RED)
                    self.listctrl_exif.SetItemFont(index, section_title_font)
                    index = index + 1
                    for key1, value1 in value.items():
                        self.listctrl_exif.InsertItem(index, '    ' + key1)
                        self.listctrl_exif.SetItem(index, 1, value1)
                        index = index + 1

    def populate_file_information(self):
        self.listctrl_file.DeleteAllItems()
        info = get_file_information(self.filename, self.tab_image.get_image())
        index = 0
        for key, value in info.items():
            self.listctrl_file.InsertItem(index, key)
            self.listctrl_file.SetItem(index, 1, value if isinstance(value, str) else str(value))
            index = index + 1
    
    def get_status_information(self):
        status = []
        tab_index = self.GetSelection()
        tab = None
        if tab_index == 0:
            if self.filename:
                status.append(localize('File name') + ': ' + os.path.basename(self.filename))
            else:
                status.append('')

            tab = self.tab_image
        elif tab_index == 1:
            status.append('')
            tab = self.tab_preview
        
        if tab:
            if tab.get_image():
                size = tab.get_size()
                status.append(localize('Image size') + ': ' + str(tab.get_size()[0]) + ' x ' + str(tab.get_size()[1]))
                status.append(localize('Scale') + ': ' + str(int(100 * tab.get_scale())) + '%')

        return status

class TestFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title=localize("Notebook Example"), size=(800, 600))
        self.filter_index = 0

        self.button = wx.Button(self, label = localize('Open File'))
        self.button.Bind(wx.EVT_BUTTON, self.on_open_dialog)
        self.notebook = ImagePreviewNotebook(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.button, 0, wx.EXPAND | wx.LEFT)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        self.Show()

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
        open_dialog = wx.FileDialog(self, localize("Open"), wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        open_dialog.SetFilterIndex(self.filter_index)
        if open_dialog.ShowModal() == wx.ID_OK:
            filename = open_dialog.GetPath()
            self.filter_index= open_dialog.GetFilterIndex()
            self.notebook.set_image_file(filename)

        open_dialog.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()
