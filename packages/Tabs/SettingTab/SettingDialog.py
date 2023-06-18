import faulthandler
import json
from pathlib import Path

from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, \
    QGridLayout, QLabel, QPushButton
from packages.Startup.Options import Options, save_options
from packages.Startup.GlobalFiles import SettingJsonInfoFilePath, create_app_data_folder
from packages.Startup.GlobalIcons import SettingIcon
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.SettingTab.Widgets.SettingTabWidget import SettingTabWidget
from packages.Widgets.MyDialog import MyDialog

faulthandler.enable()


class SettingDialog(MyDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(SettingIcon)
        self.setWindowTitle("Options")
        self.setMinimumWidth(screen_size.width() // 1.9)
        self.message = QLabel()
        self.extra_message = QLabel()
        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.setting_tab_widget = SettingTabWidget()

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.setting_tab_widget, 0, 0, 1, 1)
        self.main_layout.addLayout(self.buttons_layout, 1, 0, 1, 1)
        self.main_layout.setRowStretch(1, 0)
        self.main_layout.setRowStretch(0, 0)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        pass

    def click_yes(self):
        self.result = "Yes"
        self.save_new_settings()
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def save_new_settings(self):
        new_default_video_directory = self.setting_tab_widget.default_video_directory_layout.lineEdit.text()
        new_default_subtitle_directory = self.setting_tab_widget.default_subtitle_directory_layout.lineEdit.text()
        new_default_audio_directory = self.setting_tab_widget.default_audio_directory_layout.lineEdit.text()
        new_default_chapter_directory = self.setting_tab_widget.default_chapter_directory_layout.lineEdit.text()
        new_default_attachment_directory = self.setting_tab_widget.default_attachment_directory_layout.lineEdit.text()
        new_default_destination_directory = self.setting_tab_widget.default_destination_directory_layout.lineEdit.text()

        new_default_video_extensions = self.setting_tab_widget.default_video_extensions_layout.extensions_checkable_comboBox.currentData()
        new_default_subtitle_extensions = self.setting_tab_widget.default_subtitle_extensions_layout.extensions_checkable_comboBox.currentData()
        new_default_audio_extensions = self.setting_tab_widget.default_audio_extensions_layout.extensions_checkable_comboBox.currentData()
        new_default_chapter_extensions = self.setting_tab_widget.default_chapter_extensions_layout.extensions_checkable_comboBox.currentData()

        new_default_subtitle_language = self.setting_tab_widget.default_subtitle_language_layout.languages_comboBox.currentText()
        new_default_audio_language = self.setting_tab_widget.default_audio_language_layout.languages_comboBox.currentText()

        new_default_subtitle_language_favorite_list = self.setting_tab_widget.default_subtitle_language_layout.current_languages_list.copy()
        new_default_audio_language_favorite_list = self.setting_tab_widget.default_audio_language_layout.current_languages_list.copy()

        Options.Default_Video_Directory = new_default_video_directory
        Options.Default_Video_Extensions = new_default_video_extensions
        Options.Default_Subtitle_Directory = new_default_subtitle_directory
        Options.Default_Subtitle_Extensions = new_default_subtitle_extensions
        Options.Default_Subtitle_Language = new_default_subtitle_language
        Options.Default_Audio_Directory = new_default_audio_directory
        Options.Default_Audio_Extensions = new_default_audio_extensions
        Options.Default_Audio_Language = new_default_audio_language
        Options.Default_Chapter_Directory = new_default_chapter_directory
        Options.Default_Chapter_Extensions = new_default_chapter_extensions
        Options.Default_Attachment_Directory = new_default_attachment_directory
        Options.Default_Destination_Directory = new_default_destination_directory
        Options.Default_Favorite_Subtitle_Languages = new_default_subtitle_language_favorite_list.copy()
        Options.Default_Favorite_Audio_Languages = new_default_audio_language_favorite_list.copy()
        save_options()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedHeight(self.size().height())

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def execute(self):
        self.exec_()
