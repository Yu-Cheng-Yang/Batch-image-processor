import os
import glob

import wx

from action.ycImageActionsPerformer import ImageActionsPerformer
from ui.ycwxImageListWidget import ImageListWidget
from ycLocalize import localize

#===============================================================
# Class ImageListWidgetFile
class ImageListWidgetFile(ImageListWidget):
    def __init__(self, parent, performer: ImageActionsPerformer, **kwargs):
        super().__init__(parent, [localize('File Name'), localize('Folder')], performer, read_only = True, **kwargs)
        self.add_button.SetToolTip(localize("Add image files"))
        self.set_title(localize('File List'))
    

    def select_files(self):
        filenames = []
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
        open_dialog = wx.FileDialog(self, localize("Open"), wildcard=wildcard, style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST)
        if open_dialog.ShowModal() == wx.ID_OK:
            filenames = open_dialog.GetFilenames()
            filenames.sort()

        open_dialog.Destroy()
        self._add_files(filenames)
        
    def select_folder(self):
        filenames = []
        folder_dialog = wx.DirDialog(self, localize("Choose a directory") + ":", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if folder_dialog.ShowModal() == wx.ID_OK:
            folder = folder_dialog.GetPath()
            # Get all image files in the folder
            image_patterns = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.dib', '*.tif', '*.tiff', '*.heic', '*.heif', '*.webp']
            
            # Loop through each pattern and collect files matching the pattern
            for pattern in image_patterns:
                # Use glob.glob to find files matching the pattern
                # os.path.join combines directory path and pattern in a system-independent way
                filenames.extend(glob.glob(os.path.join(folder, pattern)))
            
        folder_dialog.Destroy()
        self._add_files(filenames)

    def _init_list_items(self):
        filenames = self.performer.get_files()
        for filename in filenames:
            folder_name = os.path.dirname(filename)
            base_name = os.path.basename(filename)
            self._add_row([base_name, folder_name])
    
    def _on_add(self, event):
        self.menu = wx.Menu()
        
        # Add items to the menu
        self.add_file_item = self.menu.Append(wx.ID_ANY, localize('Add Files'))
        self.add_file_item_id = self.add_file_item.GetId()
        self.menu.Append(wx.ID_ANY, localize('Add Folder'))
        
        # Bind the menu item event
        self.menu.Bind(wx.EVT_MENU, self._on_add_menu_item)
        
        # Get the button object
        btn = event.GetEventObject()
        
        # Calculate position to show the menu at the bottom and aligned left of the button
        btn_pos = btn.GetPosition()
        btn_size = btn.GetSize()
        menu_position = (btn_pos.x, btn_pos.y + btn_size.y)
        
        # Show the menu at the calculated position
        self.PopupMenu(self.menu, menu_position)
        self.menu.Destroy()
        self.menu = None

        self._update_performer()
        self._update_button_images()
        
    def _on_add_menu_item(self, event):
        item_id = event.GetId()
        
        if self.add_file_item_id == item_id: # Add files
            self.select_files()
        else: # Add folder
            self.select_folder()

    def _add_files(self, filenames):
        if not filenames:
            return

        for filename in filenames:
            if filename in self.performer.get_files():
                continue
            self.performer.add_file(filename)
            folder_name = os.path.dirname(filename)
            base_name = os.path.basename(filename)
            index = self._add_row([base_name, folder_name])

        for i in self.get_selections():
            self.listctrl.Select(i, False)
        
        self.listctrl.Select(self.listctrl.GetItemCount() - 1)

        self._update_performer()
        self._update_button_images()
        
    def _get_selection_texts(self):
        texts = []
        selected_indexes = self.get_selections()
        for index in selected_indexes:
            file_name = os.path.join(self.listctrl.GetItemText(index, 1), self.listctrl.GetItemText(index))
            texts.append(file_name)
        return texts
            
    def _update_performer(self):
        new_files = []
        for index in range(self.listctrl.GetItemCount()):
            file_name = os.path.join(self.listctrl.GetItemText(index, 1), self.listctrl.GetItemText(index))
            new_files.append(file_name)
        self.performer.set_files(new_files)
