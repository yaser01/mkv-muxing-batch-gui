import os
from pathlib import Path

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLineEdit

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.AudioTab.Widgets.ReloadAudioFilesDialog import ReloadAudioFilesDialog
from packages.Widgets.InvalidPathDialog import InvalidPathDialog


class AudioSourceLineEdit(QLineEdit):
    edit_finished_signal = Signal(str)
    set_is_drag_and_drop_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Enter Audio Folder Path")
        self.setClearButtonEnabled(True)
        self.setText("")
        self.stop_check_path = False
        self.is_there_old_files = False
        self.is_drag_and_drop = False
        self.current_folder_path = ""
        self.hint_when_enabled = ""
        self.editingFinished.connect(self.check_new_path)

    def set_is_drag_and_drop(self, new_state):
        self.is_drag_and_drop = new_state

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def set_current_folder_path(self, new_path):
        self.current_folder_path = new_path

    def set_text_safe_change(self, new_text):
        self.stop_check_path = True
        self.setText(new_text)
        self.stop_check_path = False

    def check_new_path(self):
        new_path = self.text()
        if self.isModified() and not self.stop_check_path:
            self.stop_check_path = True
            if os.path.isdir(new_path):
                if Path(new_path) != Path(self.current_folder_path):
                    new_path = str(Path(new_path))
                    if self.is_there_old_files:
                        reload_dialog = ReloadAudioFilesDialog()
                        reload_dialog.execute()
                        if reload_dialog.result == "Yes":
                            self.is_drag_and_drop = False
                            self.set_is_drag_and_drop_signal.emit(False)
                            self.stop_check_path = True
                            self.setText(new_path)
                        else:
                            new_path = self.current_folder_path
                            self.stop_check_path = True
                            self.setText(self.current_folder_path)
                    else:
                        self.is_drag_and_drop = False
                        self.set_is_drag_and_drop_signal.emit(False)
                        self.stop_check_path = True
                        self.setText(new_path)
                else:
                    self.stop_check_path = True
                    self.setText(self.current_folder_path)
            else:
                if new_path == "" or new_path.isspace() or self.is_drag_and_drop:
                    self.stop_check_path = True
                    self.setText(self.current_folder_path)
                else:
                    invalid_path_dialog = InvalidPathDialog()
                    invalid_path_dialog.execute()
                    self.stop_check_path = True
                    self.setText(self.current_folder_path)
                new_path = ""
            self.edit_finished_signal.emit(new_path)
        self.stop_check_path = False

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
