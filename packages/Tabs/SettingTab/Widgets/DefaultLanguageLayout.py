from PySide2.QtWidgets import QHBoxLayout, QLabel

from packages.Tabs.SettingTab.Widgets.AudioLanguageOrderButton import AudioLanguageOrderButton
from packages.Tabs.SettingTab.Widgets.LanguagesComboBox import LanguagesComboBox
from packages.Tabs.SettingTab.Widgets.SubtitleLanguageOrderButton import SubtitleLanguageOrderButton


class DefaultLanguageLayout:
    def __init__(self, label_name, languages_list, default_language):
        super().__init__()
        self.all_labels_first_column_list = []
        self.all_labels_second_column_list = []
        self.label = QLabel(label_name)
        self.current_default_language = default_language
        self.current_languages_list = languages_list
        self.languages_comboBox = LanguagesComboBox(items_list=languages_list,
                                                    default_item=default_language)
        self.setup_all_labels_list()
        if self.label.text().find("Subtitle") != -1:
            self.setting_button = SubtitleLanguageOrderButton(current_language_list=languages_list)
            self.setup_label_width_first_column()
        else:
            self.setting_button = AudioLanguageOrderButton(current_language_list=languages_list)
            self.setup_label_width_second_column()
        self.setup_layout()
        self.setting_button.new_language_list_signal.connect(self.update_language_list)

    def setup_all_labels_list(self):
        self.all_labels_first_column_list.append("Audios Extensions: ")
        self.all_labels_second_column_list.append("Subtitles Extensions: ")

    def setup_layout(self):
        return
        self.addWidget(self.label, stretch=0)
        self.addWidget(self.languages_comboBox, stretch=1)
        self.addWidget(self.setting_button, stretch=0)

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

    def update_language_list(self, new_list):
        self.current_languages_list = new_list
        if self.current_default_language not in new_list:
            self.current_default_language = new_list[0]
        self.languages_comboBox.clear()
        self.languages_comboBox.addItems(self.current_languages_list)
        self.languages_comboBox.setCurrentIndex(self.current_languages_list.index(self.current_default_language))
