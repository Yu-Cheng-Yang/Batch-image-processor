import wx
import threading
import time
import os

from action.ycImageActionsPerformer import ImageActionsPerformer

class TaskDialog(wx.Dialog):
    def __init__(self, parent, title, performer: ImageActionsPerformer):
        super(TaskDialog, self).__init__(parent, title=title, size=(800, 500))
        self.performer = performer
        self.target_folder = "E:/work/result"
        self.performer.set_output_folder(self.target_folder)
        self.init_ui()
        self.task_running = False
        self.task_paused = False

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        folder_label = wx.StaticText(self, label = "Target Foldre:   " + self.performer.get_output_folder())
        self.open_folder_button = wx.Button(self, label="Open target folder")
        self.open_folder_button.Bind(wx.EVT_BUTTON, self.on_open_folder)
        
        hbox.Add(folder_label, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        hbox.AddStretchSpacer()
        hbox.Add(self.open_folder_button, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Use a ListCtrl for displaying items and their status
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "File Name", width = 200)
        self.list_ctrl.InsertColumn(1, "Folder", width = 250)
        self.list_ctrl.InsertColumn(2, "Target name", width = 250)
        self.list_ctrl.InsertColumn(3, "Status", wx.LIST_FORMAT_RIGHT, 60)

        self.progress_text = wx.StaticText(self, label="0% Completed")
        self.progress_bar = wx.Gauge(self, range=100)

        self.pause_button = wx.Button(self, label="Pause")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Cancel")

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.pause_button, flag=wx.RIGHT, border=5)
        button_sizer.Add(self.cancel_button)

        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.progress_text, flag=wx.ALL, border=10)
        vbox.Add(self.progress_bar, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(button_sizer, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)

        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.on_pause, self.pause_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)

        self.populate_list()

    def populate_list(self):
        files = self.performer.get_files()
        self.num_items = len(files)
        for file in files:
            base_name = os.path.basename(file)
            folder = os.path.dirname(file)
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), base_name)
            self.list_ctrl.SetItem(index, 1, folder)
            self.list_ctrl.SetItem(index, 2, base_name)
            self.list_ctrl.SetItem(index, 3, "Waiting")

    def update_list_item_status(self, index, status):
        self.list_ctrl.SetItem(index, 3, status)
        if status == "Processing":
            self.list_ctrl.SetItemTextColour(index, wx.Colour("magenta"))
        elif status == "Finish":
            self.list_ctrl.SetItemTextColour(index, wx.Colour("blue"))
        else:  # Waiting
            self.list_ctrl.SetItemTextColour(index, wx.Colour("black"))
        
        if index < self.num_items - 1:
            self.list_ctrl.EnsureVisible(index + 1)  # Ensure the current item is visible

    def on_pause(self, event):
        if self.task_paused:
            self.task_paused = False
            self.pause_button.SetLabel("Pause")
        else:
            self.task_paused = True
            self.pause_button.SetLabel("Resume")

    def start_background_task(self):
        self.task_running = True
        self.thread = threading.Thread(target=self.background_task, args=(self.performer,))
        self.thread.start()

    def background_task(self, performer):
        files = performer.get_files()
        actions = self.performer.get_actions()
        num_files = len(files)
        for i in range(num_files):
            while self.task_paused:
                time.sleep(0.1)  # Wait while the task is paused
            if not self.task_running:
                break
            wx.CallAfter(self.update_list_item_status, i, "Processing")
            #time.sleep(1)  # Simulating work for each item
            if self.performer.process_file(files[i]):        
                wx.CallAfter(self.update_list_item_status, i, "Finish")
            else:
                wx.CallAfter(self.update_list_item_status, i, "Fail")
                
            wx.CallAfter(self.update_progress, (i + 1) * 100 / num_files)
        wx.CallAfter(self.end_task)

    def update_progress(self, percentage):
        self.progress_bar.SetValue(int(percentage))
        self.progress_text.SetLabel(f"{int(percentage)}% Completed")

    def on_cancel(self, event):
        is_finish = not self.task_running
        self.end_task()
        if is_finish:
            self.Destroy()

    def end_task(self):
        self.task_running = False
        self.task_paused = False
        self.pause_button.Disable()
        self.cancel_button.SetLabel("Ok")
     
    def on_open_folder(self, event):
        folderPath = self.performer.get_output_folder()
        if os.path.exists(folderPath):
            # Open folder using the default application
            if os.name == "nt":  # for Windows
                os.startfile(folderPath)
            elif os.name == "posix":  # for Linux, MacOS
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", folderPath])
        else:
            wx.MessageBox(f"The folder {folderPath} does not exist.", "Error", wx.OK | wx.ICON_ERROR)
 