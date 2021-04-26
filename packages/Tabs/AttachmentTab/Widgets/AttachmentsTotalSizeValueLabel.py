import os

from PySide2.QtWidgets import QLabel

from packages.Tabs.GlobalSetting import get_readable_filesize


class AttachmentsTotalSizeValueLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText("0.0 B")
        self.total_size_bytes = 0
        self.total_size_readable = "0.0 B"

    def update_total_size(self, files_names_absolute_list):
        total_size_bytes = 0
        for i in range(len(files_names_absolute_list)):
            file_size = os.path.getsize(files_names_absolute_list[i])
            total_size_bytes += file_size
        self.total_size_bytes = total_size_bytes
        self.total_size_readable = get_readable_filesize(self.total_size_bytes)
        self.setText(self.total_size_readable)

    def set_total_size_zero(self):
        self.total_size_bytes = 0
        self.total_size_readable = "0.0 B"
        self.setText(self.total_size_readable)

    def attachment_checked(self, file_absolute_name):
        file_size = os.path.getsize(file_absolute_name)
        self.total_size_bytes += file_size
        self.total_size_readable = get_readable_filesize(self.total_size_bytes)
        self.setText(self.total_size_readable)

    def attachment_unchecked(self, file_absolute_name):
        file_size = os.path.getsize(file_absolute_name)
        self.total_size_bytes -= file_size
        self.total_size_readable = get_readable_filesize(self.total_size_bytes)
        self.setText(self.total_size_readable)
