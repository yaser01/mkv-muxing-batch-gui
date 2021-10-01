from PySide2.QtWidgets import QHBoxLayout, QLabel

from packages.Tabs.SettingTab.ClearSourceButton import ClearSourceButton
from packages.Tabs.SettingTab.DefaultDirectoryLineEdit import DefaultDirectoryLineEdit
from packages.Tabs.SettingTab.DefaultDirectorySourceButton import DefaultDirectorySourceButton


class DefaultDirectoryLayout(QHBoxLayout):
    def __init__(self, label_name):
        super().__init__()
        self.all_labels_list = []
        self.label = QLabel(label_name)
        self.lineEdit = DefaultDirectoryLineEdit()
        self.source_button = DefaultDirectorySourceButton()
        self.clear_source_button = ClearSourceButton()
        self.setup_all_labels_list()
        self.setup_label_width()
        self.setup_layout()
        self.connect_signals()

    def setup_all_labels_list(self):
        self.all_labels_list.append("Videos Directory: ")
        self.all_labels_list.append("Subtitles Directory: ")
        self.all_labels_list.append("Audios Directory: ")
        self.all_labels_list.append("Attachments Directory: ")
        self.all_labels_list.append("Chapters Directory: ")

    def setup_label_width(self):
        width_to_be_fixed = 0
        for i in range(len(self.all_labels_list)):
            width_to_be_fixed = max(width_to_be_fixed, self.label.fontMetrics().boundingRect(
                self.all_labels_list[i]).width())
        self.label.setMinimumWidth(width_to_be_fixed + 5)

    def setup_layout(self):
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)
        self.addWidget(self.clear_source_button)
        self.addWidget(self.source_button)

    def connect_signals(self):
        self.source_button.new_directory_signal.connect(self.lineEdit.setText)
        self.clear_source_button.clear_signal.connect(self.lineEdit.clear)
