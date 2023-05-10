from pathlib import Path

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton, QFileDialog

from packages.Startup import GlobalIcons
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.VideoTab.Widgets.ReloadVideoFilesDialog import ReloadVideoFilesDialog


class VideoSourceButton(QPushButton):
    clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.SelectFolderIcon)
        self.hint_when_enabled = ""
        self.is_there_old_files = False
        self.clicked.connect(self.open_select_folder_dialog)

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def open_select_folder_dialog(self):
        new_folder_path = ""
        if self.is_there_old_files:
            reload_dialog = ReloadVideoFilesDialog()
            reload_dialog.execute()
            if reload_dialog.result == "Yes":
                temp_folder_path = QFileDialog.getExistingDirectory(self, caption="Choose Video Folder",
                                                                    dir=GlobalSetting.LAST_DIRECTORY_PATH)
                new_folder_path = temp_folder_path
        else:
            temp_folder_path = QFileDialog.getExistingDirectory(self, caption="Choose Video Folder",
                                                                dir=GlobalSetting.LAST_DIRECTORY_PATH)
            new_folder_path = temp_folder_path

        if new_folder_path == "" or new_folder_path.isspace():
            new_folder_path = ""
        else:
            new_folder_path = str(Path(new_folder_path))

        self.clicked_signal.emit(new_folder_path)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
