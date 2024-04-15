import os

import wx

import action.ycImageAction as ycImageAction
from action.ycImageActionsPerformer import ImageActionsPerformer
from ui.ycwxImagePreviewPanel import ImagePreviewNotebook

from uiaction.ycwxCreateActionWidget import create_action_widget
from ui.ycwxImageListWidgetAction import ImageListWidgetAction
from ui.ycwxImageListWidgetFile import ImageListWidgetFile
from ui.ycwxBulkImagePropertiesDialog import BulkImagePropertiesDialog
from uibase.ycwxBorderedPanel import BorderPanelType, BorderedPanel
from ui.ycwxTaskDialog import TaskDialog
from ycLocalize import get_language, set_language, localize
from ycConfig import load_config, get_config, get_config_image_background_color

class BulkImageFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, size=(1024, 768))
        self.SetMinSize((1024, 768))
        self.sub_border_type = BorderPanelType.INSET
        self.panel = wx.Panel(self)
        self.performer = ImageActionsPerformer('Untitled.bip')
        self.performer.set_image_background_color(get_config_image_background_color())
        
        self.update_title()
        self._init_layout()
        self._init_menu()
        #self._init_toolbar()

        self.CreateStatusBar(number=3)
        self.SetStatusText(localize("Ready"), 0)  # Set text in the first field
        
    def update_action_view(self, action, refresh = True):
        if self.action == action:
            # No need create new ation widget.
            return
        
        self.action = action
        if self.action_detail_view:
            self.action_detail_view.Destroy()

        self.action_detail_view = create_action_widget(self.action_view_panel, self.action)
        self.action_detail_view.set_apply_callback(self._on_action_apply)
        self.action_view_panel.add_widget(self.action_detail_view)

        if refresh:
            self.action_view_panel.Refresh()
            self.action_view_panel.Layout()

    def _init_menu(self):
        menuBar = wx.MenuBar()

        # Project menu
        project_menu = wx.Menu()

        new_item = project_menu.Append(wx.ID_NEW, localize("New"), localize("Create a new project"))
        new_item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16, 16)))
        open_item = project_menu.Append(wx.ID_OPEN, localize("Open"), localize("Open an existing project"))
        open_item.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16, 16)))
        save_item = project_menu.Append(wx.ID_SAVE, localize("Save"), localize("Save project"))
        save_as_item = project_menu.Append(wx.ID_SAVEAS, localize("Save As") + "...", localize("Save as a project"))
        preferences_item = project_menu.Append(wx.ID_HELP, localize("Preferences"), localize("Project preferences"))
        
        project_menu.AppendSeparator()
        exit_item = project_menu.Append(wx.ID_EXIT, localize("Exit"), localize("Exit application"))

        self.Bind(wx.EVT_MENU, self._on_new, new_item)
        self.Bind(wx.EVT_MENU, self._on_open, open_item)
        self.Bind(wx.EVT_MENU, self._on_save, save_item)
        self.Bind(wx.EVT_MENU, self._on_save_as, save_as_item)
        self.Bind(wx.EVT_MENU, self._on_preferences, preferences_item)
        self.Bind(wx.EVT_MENU, self._on_exit, exit_item)
        self.Bind(wx.EVT_SIZE, self._on_resize)
        
        # File menu
        file_menu = wx.Menu()
        add_file_item = file_menu.Append(wx.ID_ANY, localize("Add Files"), localize("Add files to file list"))
        add_folder_item = file_menu.Append(wx.ID_ANY, localize("Add Folder"), localize("Add image files in folder to File List"))
        self.Bind(wx.EVT_MENU, self._on_add_files, add_file_item)
        self.Bind(wx.EVT_MENU, self._on_add_folder, add_folder_item)

        # Action menu
        action_menu = wx.Menu()
        self.action_submenu = wx.Menu()
        
        action_type_display_names = ycImageAction.get_display_names_from_enum_class(ycImageAction.ActionType)
        for name in action_type_display_names:
            self.action_submenu.Append(wx.ID_ANY, name)
        
        # Bind the menu item event
        self.action_submenu.Bind(wx.EVT_MENU, self._on_add_action_item)
        
        # Add the sub-menu to the main menu
        action_menu.AppendSubMenu(self.action_submenu, localize('Add'), localize('Create an action and add to action list'))

        # Run menu
        run_menu = wx.Menu()
        run_item = run_menu.Append(wx.ID_ANY, localize("Run Project"), localize("Run Project"))
        self.Bind(wx.EVT_MENU, self._on_run, run_item)

        menuBar.Append(project_menu, localize("Project"))
        menuBar.Append(file_menu, localize("File"))
        menuBar.Append(action_menu, localize("Action"))
        menuBar.Append(run_menu, localize("Run"))
        
        self.SetMenuBar(menuBar)

    def _on_add_action_item(self, event):
        item_id = event.GetId()
        display_name = self.action_submenu.FindItemById(item_id).GetItemLabelText()
        self.action_list_view.create_new_action_from_display_name(display_name)
    
    def _init_toolbar(self):
        # Create the toolbar
        self.toolbar = self.CreateToolBar(style=wx.TB_HORIZONTAL | wx.RAISED_BORDER | wx.TB_FLAT)
        self.toolbar.SetBackgroundColour(wx.Colour(80, 80, 80, 255))

        # First group of tools
        tool_new = self._create_toolbar_item(localize('New'), wx.ART_NEW, localize('New'))
        tool_open = self._create_toolbar_item(localize('Open'), wx.ART_FILE_OPEN, localize('Open'))
        tool_save = self._create_toolbar_item(localize('Save'), wx.ART_FILE_SAVE, localize('Save'))
        tool_save_as = self._create_toolbar_item(localize('Save As'), wx.ART_FILE_SAVE_AS, localize('Save As'))
        tool_properties = self._create_toolbar_item(localize('Properties'), wx.ART_EXECUTABLE_FILE, localize('Properties'))
        self.toolbar.AddSeparator() 

        tool_run = self._create_toolbar_item(localize('Run'), wx.ART_INFORMATION, localize('Run'))
        self.toolbar.AddSeparator()

        tool_help = self._create_toolbar_item(localize('Help'), wx.ART_HELP, localize('Help'))

        self.Bind(wx.EVT_TOOL, self._on_new, tool_new)
        self.Bind(wx.EVT_TOOL, self._on_open, tool_open)
        self.Bind(wx.EVT_TOOL, self._on_save, tool_save)
        self.Bind(wx.EVT_TOOL, self._on_save_as, tool_save_as)
        self.Bind(wx.EVT_TOOL, self._on_properties, tool_properties)
        #self.Bind(wx.EVT_TOOL, self.on_run, tool_run)

        self.toolbar.Realize()
    
    def _init_layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox_upper = wx.BoxSizer(wx.HORIZONTAL)
        hbox_lower = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create file view panel
        self.file_list_panel = self._create_bordered_panel()
        self.file_list_view = ImageListWidgetFile(self.file_list_panel, self.performer)
        self.file_list_view.set_selection_callback(self._on_file_select)
        self.file_list_panel.add_widget(self.file_list_view)

        # Create action list view panel
        self.action_list_panel = self._create_bordered_panel()
        self.action_list_view = ImageListWidgetAction(self.action_list_panel, self.performer)
        self.action_list_view.set_selection_callback(self._on_action_select)
        self.action_list_panel.add_widget(self.action_list_view)

        self.static_line = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL)
        self.action = None

        # Create image view panel
        self.image_view_panel = self._create_bordered_panel()
        self.image_view = ImagePreviewNotebook(self.image_view_panel)
        self.image_view.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._on_image_view_tab_change)
        self.image_view_panel.add_widget(self.image_view)
        self.image_view.set_image_background_color(get_config_image_background_color())
        
        # Create action view panel
        self.action_view_panel = self._create_bordered_panel()
        self.action_detail_view = None
        self.update_action_view(self.action, False)

        hbox_upper.Add(self.file_list_panel, 1, wx.EXPAND | wx.ALL, border=8) 
        hbox_upper.Add(self.image_view_panel, 1, wx.EXPAND | wx.ALL, border=8) 

        hbox_lower.Add(self.action_list_panel, 1, wx.EXPAND | wx.ALL, border=8) 
        hbox_lower.Add(self.action_view_panel, 1, wx.EXPAND | wx.ALL, border=8) 

        vbox.Add(hbox_upper, 1, wx.EXPAND | wx.ALL, border=8) 
        vbox.Add(self.static_line, 0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
        vbox.Add(hbox_lower, 1, wx.EXPAND | wx.ALL, border=8)
        
        self.panel.SetSizer(vbox)

    def _on_new(self, event):
        self.performer = ImageActionsPerformer('Untitled.bip')
        self.performer.set_image_background_color(get_config_image_background_color())

        self.update_layout_with_performer()
        self.image_view.set_image_background_color(get_config_image_background_color())
        
    def _on_open(self, event):
        with wx.FileDialog(self, localize("Open project file"), wildcard="Project files (*.bip)|*.bip",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                project_name = fileDialog.GetPath()
                self.performer.load_from_json(project_name)
                self.performer.set_project_name(project_name)
                self.update_layout_with_performer()
                self.update_title()

    def _on_save(self, event):
        project_name = self.performer.get_project_name()
        if project_name == 'Untitled.bip':
            with wx.FileDialog(None, localize("Save project file"), wildcard="Project files (*.bip)|*.bip",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_OK:
                    project_name = fileDialog.GetPath()
        
        self.performer.set_name(os.path.basename(project_name))
        self.performer.save_as_json(project_name)
        self.update_title()

    def _on_save_as(self, event):
        project_name = self.performer.get_name() + 'bip'
        with wx.FileDialog(None, localize("Save as project file"), wildcard="Project files (*.bip)|*.bip",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_OK:
                project_name = fileDialog.GetPath()
                self.performer.set_name(os.path.basename(project_name))
                self.performer.save_as_json(project_name)
                self.update_title()

    def _on_preferences(self, event):
        old_lang = get_language()
        old_image_backgroundcolor = get_config("ImageBackgroundColor")
        
        dlg = BulkImagePropertiesDialog(self, localize("Properties"), self.performer)
        if dlg.ShowModal() == wx.ID_OK:
            image_backgroundcolor = self.performer.get_image_background_color()
            if old_image_backgroundcolor != image_backgroundcolor:
                self.image_view.set_image_background_color(image_backgroundcolor)
        dlg.Destroy()
        
        if not (get_language() == old_lang):
            wx.MessageBox(localize("Please restart to make language change work"), "Info", wx.OK | wx.ICON_INFORMATION)    

    def _on_exit(self, event):
        self.Close(True)
        
    def _on_add_files(self, event):
        self.file_list_view.select_files()

    def _on_add_folder(self, event):
        self.file_list_view.select_folder()
        
    def _on_run(self, event):
        dialog = TaskDialog(None, title=localize("Bulk Images Processing"), performer=self.performer)
        dialog.start_background_task()  # Start task with 10 items
        dialog.ShowModal()
    
    def _on_file_select(self, selections):
        filename = None
        preview = None
        
        # update original image view
        if selections and len(selections) == 1:
            filename = self.performer.get_file(selections[0])
                
        self.image_view.set_image_file(filename)

        # Update preview image view
        image = self.image_view.get_original_image()
        if image:
            action_selections = self.action_list_view.get_selections()
            if action_selections and len(action_selections) == 1:
                image = image.copy()
                preview = self.performer.get_image_from_actions(image, action_selections[0])
        self.image_view.set_preview_image(preview)

        # Update Status bar
        self.update_status_bar()

    def _on_action_select(self, selections):
        action = None
        preview = None
        if selections and len(selections) == 1:
            action_index = selections[0]
            action = self.performer.get_actions()[action_index]
            
            image = self.image_view.get_original_image()
            if image:
                image = image.copy()
                preview = self.performer.get_image_from_actions(image, action_index)
            
            self.update_rename_information(action_index)
            
        self.image_view.set_preview_image(preview)
        self.update_action_view(action)
        self.update_status_bar()

    def update_rename_information(self, action_index):
        # Update rename listctrl
        renamed_files = []
        files = self.performer.get_files()
        actions = self.performer.get_actions()[:action_index+1]
        for action in actions:
            action.pre_process(files)
        for file in files:
            _, renamed_file = self.performer.get_target_file_name(file, action_index)
            renamed_files.append(renamed_file)
        for action in actions:
            action.post_process()
            
        self.image_view.set_renamed_files([os.path.basename(file) for file in files], renamed_files)
        
    def _on_action_apply(self, action):
        image = self.image_view.get_original_image()
        if action and image:
            image = image.copy()
            for index, item in enumerate(self.performer.get_actions()):
                if item.get_name() == action.get_name():
                    preview = self.performer.get_image_from_actions(image, index)
                    self.image_view.set_preview_image(preview)
                    self.update_status_bar()
                    break

        if action.is_rename_action():
            for action_index, action_in_list in enumerate(self.performer.get_actions()):
                if action == action_in_list:
                    break
            self.update_rename_information(action_index)
            
    def _on_resize(self, event):
        self.Refresh()
        self.Layout()
        event.Skip()
        # Wait for all resize ready on child widgets and update status bar
        wx.CallAfter(self.update_status_bar)

    def _on_image_view_tab_change(self, event):
        self.update_status_bar()

    def update_layout_with_performer(self):
        self.file_list_view.set_performer(self.performer)
        self.action_list_view.set_performer(self.performer)
        self.image_view.set_image_file(None)
        self.image_view.set_preview_image(None)
        self.update_action_view(None, True)
    
    def update_title(self):
        title =  os.path.basename(self.performer.get_name())     
        self.SetTitle(localize("Bulk Image Processor") + f"- %s" % title)
        
    def update_status_bar(self):
        if self.StatusBar:
            status_info = self.image_view.get_status_information()
            if len(status_info) == 3:
                self.SetStatusText(status_info[0], 0)
                self.SetStatusText(status_info[1], 1)
                self.SetStatusText(status_info[2], 2)
            else:
                self.SetStatusText("", 0)
                self.SetStatusText("", 1)
                self.SetStatusText("", 2)

    def _create_toolbar_item(self, label, art, short_help):
        tool_item = self.toolbar.AddTool(toolId=wx.ID_ANY, label=label, bitmap=wx.ArtProvider.GetBitmap(art, wx.ART_TOOLBAR, (24, 24)), shortHelp=short_help)
        
    def _create_bordered_panel(self):
        return BorderedPanel(self.panel, self.sub_border_type)

if __name__ == '__main__':
    
    load_config()
    app = wx.App(False)
    frame = BulkImageFrame()
    frame.Show()
    app.MainLoop()
