import wx
from action.ycImageActionsPerformer import ImageActionsPerformer

#===============================================================
# Class ImageListWidget
class ImageListWidget(wx.Panel):
    def __init__(self, parent, header_columns, performer: ImageActionsPerformer, read_only = True, **kwargs):
        super().__init__(parent, **kwargs)
        self.performer = performer
        self.id = 0
        self.select_callback = None
        self.read_only = read_only
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.title_label = wx.StaticText(self, label = 'List')
        # Define the font attributes
        font_size = 12
        font_family = wx.FONTFAMILY_SWISS  # A sans-serif font
        font_style = wx.FONTSTYLE_NORMAL
        font_weight = wx.FONTWEIGHT_BOLD
        font_face_name = ""  # Default face name
        
        # Create a wx.Font object
        font = wx.Font(font_size, font_family, font_style, font_weight, faceName=font_face_name)
        
        # Set the font of the StaticText widget
        self.title_label.SetFont(font)

        self.hbox.Add(self.title_label, 0, wx.LEFT, border = 8)
        self.hbox.AddStretchSpacer()
        
        self.image_up = self._get_button_bitmap(wx.ART_GO_UP)
        self.image_down =  self._get_button_bitmap(wx.ART_GO_DOWN)
        self.image_remove =  self._get_button_bitmap(wx.ART_DELETE) 
        self.image_add =  self._get_button_bitmap(wx.ART_PLUS)
        
        self.image_up_gray   = self._get_button_grey_bitmap(self.image_up)
        self.image_down_gray = self._get_button_grey_bitmap(self.image_down)
        self.image_remove_gray = self._get_button_grey_bitmap(self.image_remove) 

        self.up_button = self._add_image_button('Up', self.image_up, self._on_move_up)
        self.down_button = self._add_image_button('Down', self.image_down, self._on_move_down)
        self.remove_button = self._add_image_button('Remove', self.image_remove, self._on_remove)
        self.add_button = self._add_image_button('Add', self.image_add, self._on_add, True)
    
        self.vbox.AddSpacer(5)
        self.vbox.Add(self.hbox, 0, wx.EXPAND | wx.ALL)
        
        # Create Treeview and insert all file names in it
        if not self.read_only:
            self.listctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.LC_EDIT_LABELS)
            self.listctrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, self._on_end_label_edit)
        else:
            self.listctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
            # By default, this style LC_EDIT_LABELS is set to True, allowing label editing
            # Need remove this flag
            self.listctrl.SetWindowStyleFlag(self.listctrl.GetWindowStyleFlag() & ~wx.LC_EDIT_LABELS)
            
        for col, text in enumerate(header_columns):
            self.listctrl.InsertColumn(col, text, width=wx.LIST_AUTOSIZE)
        
        self.listctrl.SetColumnWidth(0, -2)
        self.listctrl.SetColumnWidth(1, -2)

        self._init_list_items()

        self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_select)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_deselect)
        self.listctrl.Bind(wx.EVT_SIZE, self._on_resize)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_right_click)

        item_count = self.listctrl.GetItemCount()
        if item_count > 0:
            # Select the first item
            self.listctrl.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        self.vbox.Add(self.listctrl, 1, wx.EXPAND| wx.ALL, border = 5)
        
        self.SetSizer(self.vbox)
        
        # Update button images
        self._update_button_images()
    
    def set_selection_callback(self, callback):
        self.select_callback = callback
        
    def set_title(self, title):
        self.title_label.SetLabelText(title)

    def set_performer(self, performer):
        self.performer = performer
        self.listctrl.DeleteAllItems()
        self._init_list_items()
        self.Refresh()
        
    def _get_button_bitmap(self, art_type):
        return wx.ArtProvider.GetBitmap(art_type, wx.ART_OTHER, (16, 16))
    
    def _get_button_grey_bitmap(self, bitmap):
        wx_grey_bitmap = None
        if bitmap:
            wx_image = bitmap.ConvertToImage()
            wx_grey_image = wx_image.ConvertToGreyscale()
            wx_grey_bitmap = wx.Bitmap(wx_grey_image)
        
        return wx_grey_bitmap
    
    def _on_resize(self, event):
        # Call event.Skip() to allow the list control to process the event as well and actually perform the resize
        event.Skip()
        
        # Dynamically adjust column widths here
        total_width = self.listctrl.GetClientSize().width
        col_count = self.listctrl.GetColumnCount()
        for col in range(col_count):
            self.listctrl.SetColumnWidth(col, total_width // col_count)
        self.Refresh()

    def _init_list_items(self):
        pass
    
    def get_selections(self):
        selections = []
        index = self.listctrl.GetFirstSelected()
        while index != -1:
            selections.append(index)
            index = self.listctrl.GetNextSelected(index)
        return selections
    
    def _add_image_button(self, label, image, click_callback, finish = False):
        button = wx.Button(self, label = '', size = (24, 24))
        button.SetBitmap(image)
        self.hbox.AddSpacer(5)
        if finish:
            self.hbox.Add(button, 0)
            self.hbox.AddSpacer(5)
        else:
            self.hbox.Add(button, 0, wx.RIGHT)
        button.Bind(wx.EVT_BUTTON, click_callback)
        return button
            
    def _swap_items(self, index1, index2):
        # Swap the items at index1 and index2
        for col in range(self.listctrl.GetColumnCount()):
            item1 = self.listctrl.GetItemText(index1, col)
            item2 = self.listctrl.GetItemText(index2, col)
            self.listctrl.SetItem(index1, col, item2)
            self.listctrl.SetItem(index2, col, item1)

    def _on_move_up(self, event):
        selected_indexes = self.get_selections()
        # if more than 1 item is selected and the selection hit the top, do nothing
        if not selected_indexes or selected_indexes[0] == 0:
            return
        
        # Move selected items up if possible
        for i in selected_indexes:
            self._swap_items(i, i-1)

        # Update selection to moved items
        for i in selected_indexes:
            self.listctrl.Select(i, on=False)  # Deselect all initially selected
        for i in [x-1 if x != 0 else 0 for x in selected_indexes]:  # Adjust for moved items
            self.listctrl.Select(i)
            
        self._update_performer()
        self._update_button_images()

    def _on_move_down(self, event):
        selected_indexes = self.get_selections()
        if not selected_indexes or selected_indexes[-1] == self.listctrl.GetItemCount() - 1:
            return

        for i in reversed(selected_indexes):
            self._swap_items(i, i+1)
        
        for i in selected_indexes:
            self.listctrl.Select(i, on=False)  # Deselect all initially selected

        for i in [x+1 if x != self.listctrl.GetItemCount() - 1 else x for x in selected_indexes]:
            self.listctrl.Select(i)
            
        self._update_performer()
        self._update_button_images()

    def _on_remove(self, event):
        selected_indexes = self.get_selections()
        if not selected_indexes:
            return

        for index in reversed(selected_indexes):
            self.listctrl.DeleteItem(index)
        
        self._update_performer()
        self._update_button_images()

    def _on_add(self, event):
        pass

    def _get_selection_texts(self):
        return []

    def _on_select(self, event):
        if self.select_callback:
            self.select_callback((self.get_selections())) 
        self._update_button_images()
 
    def _on_deselect(self, event):
        texts = self._get_selection_texts()
        if self.select_callback:
            self.select_callback(texts) 
        self._update_button_images()

    def _update_button_images(self):
        selected_indexes = self.get_selections()
        if not selected_indexes:
            self.up_button.SetBitmap(self.image_up_gray)
            self.down_button.SetBitmap(self.image_down_gray)
            self.remove_button.SetBitmap(self.image_remove_gray)
        else:
            self.remove_button.SetBitmap(self.image_remove)
            self.up_button.SetBitmap(self.image_up_gray if selected_indexes[0] == 0 else self.image_up)
            self.down_button.SetBitmap(self.image_down_gray if selected_indexes[-1] == self.listctrl.GetItemCount()-1 else self.image_down)

    def _add_row(self, columns):
        index = None
        if columns:
            index = self.listctrl.InsertItem(self.listctrl.GetItemCount(), columns[0])
            for col, column in enumerate(columns[1:]):
                self.listctrl.SetItem(index, col+1, column)
                
        return index
        
    def _update_performer(self):
        pass

    def _on_end_label_edit(self, event):
        event.Skip()  # Important to allow the change to be accepted

    def _on_right_click(self, event):
        index = event.GetIndex()
        
        if index == -1:
            return
        
        menu = wx.Menu()
        move_up_item = menu.Append(wx.ID_ANY, "Move up")
        move_down_item = menu.Append(wx.ID_ANY, "Move down")
        remove_item = menu.Append(wx.ID_ANY, "Remove")
        if not self.read_only:
            rename_item = menu.Append(wx.ID_ANY, "Rename")

        # Bind the menu item selection event
        self.Bind(wx.EVT_MENU, self._on_move_up, move_up_item)
        self.Bind(wx.EVT_MENU, self._on_move_down, move_down_item)
        self.Bind(wx.EVT_MENU, self._on_remove, remove_item)
        if not self.read_only:
            self.Bind(wx.EVT_MENU, lambda evt, idx=event.GetIndex(): self._on_rename(evt, idx), rename_item)
        
        selected_indexes = self.get_selections()
        if not selected_indexes or selected_indexes[0] == 0:
            move_up_item.Enable(False)
        if not selected_indexes or selected_indexes[-1] == self.listctrl.GetItemCount() - 1:
            move_down_item.Enable(False)
        if not selected_indexes:
            remove_item.Enable(False)
            
        point = event.GetPoint()

        # Approximate height of each row in the ListCtrl
        row_height = self.listctrl.GetItemRect(0).height

        # Adjust the Y position to the bottom of the clicked row
        adjusted_point = wx.Point(point.x, point.y + 2 * row_height)
        
        # Show the context menu
        self.PopupMenu(menu, adjusted_point)
        menu.Destroy()

    def _on_rename(self, event, item_index):
        # Start editing the label of the item
        self.listctrl.EditLabel(item_index)

    def _onKeyCharHook(self, event):
        # Check if Ctrl+A is pressed
        if event.GetKeyCode() == 65 and event.ControlDown():  # 65 is the key code for 'A'
            for i in range(self.listctrl.GetItemCount()):
                self.listctrl.Select(i)
        else:
            event.Skip()  # Skip the event to allow other key processing
