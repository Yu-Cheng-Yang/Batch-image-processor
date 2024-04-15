import os

import wx

import action.ycImageAction as ycImageAction
import action.ycImageActionsPerformer as ycImageActionsPerformer
from action.ycCreateAction import create_action
from ui.ycwxImageListWidget import ImageListWidget

from ycLocalize import localize
    
#===============================================================
# Class ImageListWdigetAction
class ImageListWidgetAction(ImageListWidget):
    def __init__(self, parent, performer: ycImageActionsPerformer.ImageActionsPerformer, **kwargs):
        super().__init__(parent, [localize('Action Name'), localize('Action Type')], performer, read_only = False, **kwargs)
        
        #self.action_type_display_names = ImageAction.get_display_names_from_enum_class(ImageAction.ActionType)
        #self.action_type_values = [member for member in ImageAction.ActionType]
        
        self.add_button.SetToolTip(localize("Add a new image action"))
        self.set_title(localize('Action List'))
     
    def _init_list_items(self):
        actions = self.performer.get_actions()
        for action in actions:
            action_name = action.get_name()
            action_type = ycImageAction.get_enum_display_name(action.get_action_type())
            self._add_row([action_name, action_type])

    def get_action(self, index):
        return self.performer.get_actions()[index] if 0 <= index < len(self.performer.get_actions()) else None
 
    def create_new_action(self, action_type):
        #action_type_name = ImageAction.get_enum_export_name(action_type)
        action_type_name = ycImageAction.get_enum_display_name(action_type)
        action = create_action(action_type, action_type_name)
        
        if action:
            action_name = self.performer.add_action(action)
            index = self._add_row([action_name, action_type_name])
            for i in self.get_selections():
                self.listctrl.Select(i, on=False)
            self.listctrl.Select(index)
            self._update_button_images()

    def create_new_action_from_display_name(self, display_name):
        action_type = None
        action_type_values = [member for member in ycImageAction.ActionType]
        action_type_display_names = ycImageAction.get_display_names_from_enum_class(ycImageAction.ActionType)
        
        for index, name in enumerate(action_type_display_names):
            if name ==  display_name:
                action_type = action_type_values[index]
                break
        if not action_type:
            print("Error in getting action type! Use first one.")
            action_type = self.action_type_values[0]
                                   
        self.create_new_action(action_type)
    
    def _on_add(self, event):
        self.menu = wx.Menu()
        
        # Add items to the menu
        action_type_display_names = ycImageAction.get_display_names_from_enum_class(ycImageAction.ActionType)
        for name in action_type_display_names:
            self.menu.Append(wx.ID_ANY, name)
        
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
        display_name = self.menu.FindItemById(item_id).GetItemLabelText()
        self.create_new_action_from_display_name(display_name)
        
    def _get_selection_texts(self):
        texts = []
        selected_indexes = self.get_selections()
        for index in selected_indexes:
            action_name = self.listctrl.GetItemText(index)
            texts.append(action_name)
        return texts

    def _update_performer(self):
        new_actions = []
        for index in range(self.listctrl.GetItemCount()):
            new_actions.append(self.performer.get_action_by_name(self.listctrl.GetItemText(index)))
        self.performer.set_actions(new_actions)

    def _on_end_label_edit(self, event):
        # This method is called when the user finishes editing a label
        new_label = event.GetLabel()
        item_index = event.GetIndex()
        for index in range(self.listctrl.GetItemCount()):
            if index != item_index:
                text = self.listctrl.GetItemText(index)
                if text == new_label:
                    wx.MessageBox(localize("This action name %s already exists.") % text, "Error", wx.OK | wx.ICON_ERROR)
                    event.Veto()  # Cancel the edit
            
        event.Skip()  # Important to allow the change to be accepted
