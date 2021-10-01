from PySide2.QtWidgets import QHBoxLayout, QLabel
from packages.Tabs.SettingTab.LanguagesComboBox import LanguagesComboBox


class DefaultLanguageLayout(QHBoxLayout):
    def __init__(self, label_name, languages_list, default_language):
        super().__init__()
        self.all_labels_first_column_list = []
        self.all_labels_second_column_list = []
        self.label = QLabel(label_name)
        self.languages_comboBox = LanguagesComboBox(items_list=languages_list,
                                                    default_item=default_language)
        self.setup_all_labels_list()
        self.setup_layout()
        if self.label.text().find("Subtitle") != -1:
            self.setup_label_width_first_column()
        else:
            self.setup_label_width_second_column()

    def setup_all_labels_list(self):
        self.all_labels_first_column_list.append("Audios Extensions: ")
        self.all_labels_second_column_list.append("Subtitles Extensions: ")

    def setup_layout(self):
        self.addWidget(self.label)
        self.addWidget(self.languages_comboBox)

    def setup_label_width_first_column(self):
        width_to_be_fixed = 0
        for i in range(len(self.all_labels_first_column_list)):
            width_to_be_fixed = max(width_to_be_fixed, self.label.fontMetrics().boundingRect(
                self.all_labels_first_column_list[i]).width())
        self.label.setFixedWidth(width_to_be_fixed + 3)

    def setup_label_width_second_column(self):
        width_to_be_fixed = 0
        for i in range(len(self.all_labels_second_column_list)):
            width_to_be_fixed = max(width_to_be_fixed, self.label.fontMetrics().boundingRect(
                self.all_labels_second_column_list[i]).width())
        self.label.setFixedWidth(width_to_be_fixed + 3)
