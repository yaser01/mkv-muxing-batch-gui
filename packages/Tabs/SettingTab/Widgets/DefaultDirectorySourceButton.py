from pathlib import Path

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton, QFileDialog

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting


class DefaultDirectorySourceButton(QPushButton):
    new_directory_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalFiles.SelectFolderIcon)
        self.clicked.connect(self.open_select_folder_dialog)

    def open_select_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, caption="Choose Video Folder",
                                                       dir=GlobalSetting.LAST_DIRECTORY_PATH)
        if folder_path == "" or folder_path.isspace():
            return
        folder_path = str(Path(folder_path))
        self.new_directory_signal.emit(folder_path)
