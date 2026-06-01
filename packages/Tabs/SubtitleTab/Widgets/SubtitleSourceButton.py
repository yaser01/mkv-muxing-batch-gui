from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QPushButton

from packages.Startup import GlobalIcons
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.Widgets.ReloadSubtitleFilesDialog import (
    ReloadSubtitleFilesDialog,
)


class SubtitleSourceButton(QPushButton):
    clicked_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.hint_when_enabled = ""
        self.setIcon(GlobalIcons.SelectFolderIcon)
        self.is_there_old_files = False
        self.clicked.connect(self.open_select_folder_dialog)

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def open_select_folder_dialog(self):
        new_folder_path = ""
        proceed = True

        if self.is_there_old_files:
            reload_dialog = ReloadSubtitleFilesDialog(parent=self)
            reload_dialog.execute()
            if reload_dialog.result != "Yes":
                proceed = False

        if proceed:
            # Asegurar que el directorio inicial sea una cadena (no Path)
            start_dir = (
                str(GlobalSetting.LAST_DIRECTORY_PATH) if GlobalSetting.LAST_DIRECTORY_PATH else ""
            )
            # Usar argumentos posicionales (sin nombres) para evitar problemas
            temp_folder_path = QFileDialog.getExistingDirectory(
                self, "Elegir carpeta de subtítulos", start_dir
            )
            if temp_folder_path and not temp_folder_path.isspace():
                new_folder_path = str(Path(temp_folder_path))

        self.clicked_signal.emit(new_folder_path)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip(
                    "<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP
                )
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip(
                    "<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP
                )
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
