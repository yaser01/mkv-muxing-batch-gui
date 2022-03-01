from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QStyleFactory, \
    QGridLayout, QLabel, QHBoxLayout

from packages.Startup import GlobalFiles
from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.GlobalFiles import InfoIcon, InfoSettingIconPath, InfoIconPath
from packages.Startup.PreDefined import AllVideosExtensions, AllSubtitlesExtensions, AllAudiosExtensions, \
    AllChapterExtensions, AllSubtitlesLanguages, AllAudiosLanguages
from packages.Tabs.SettingTab.Widgets.AboutButton import AboutButton
from packages.Tabs.SettingTab.Widgets.DefaultDirectoryLayout import DefaultDirectoryLayout
from packages.Tabs.SettingTab.Widgets.DefaultExtensionsLayout import DefaultExtensionsLayout
from packages.Tabs.SettingTab.Widgets.DefaultLanguageLayout import DefaultLanguageLayout
from packages.Tabs.SettingTab.Widgets.DonateButton import DonateButton


class SettingTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.default_directories_groupBox = QGroupBox(self)
        self.default_extensions_groupBox = QGroupBox(self)
        self.default_languages_groupBox = QGroupBox(self)
        self.default_directories_layout = QVBoxLayout()
        self.default_extensions_layout = QGridLayout()
        self.default_languages_layout = QGridLayout()
        self.setting_info_layout = QHBoxLayout()
        self.default_video_directory_layout = DefaultDirectoryLayout(label_name="Videos Directory: ",
                                                                     default_directory=DefaultOptions.Default_Video_Directory)
        self.default_subtitle_directory_layout = DefaultDirectoryLayout(label_name="Subtitles Directory: ",
                                                                        default_directory=DefaultOptions.Default_Subtitle_Directory)
        self.default_audio_directory_layout = DefaultDirectoryLayout(label_name="Audios Directory: ",
                                                                     default_directory=DefaultOptions.Default_Audio_Directory)
        self.default_chapter_directory_layout = DefaultDirectoryLayout(label_name="Chapters Directory: ",
                                                                       default_directory=DefaultOptions.Default_Chapter_Directory)
        self.default_attachment_directory_layout = DefaultDirectoryLayout(label_name="Attachments Directory: ",
                                                                          default_directory=DefaultOptions.Default_Attachment_Directory)
        self.default_destination_directory_layout = DefaultDirectoryLayout(label_name="Destination Directory: ",
                                                                           default_directory=DefaultOptions.Default_Destination_Directory)
        self.default_video_extensions_layout = DefaultExtensionsLayout(label_name="Video Extensions: ",
                                                                       extensions_list=AllVideosExtensions,
                                                                       default_extensions_list=DefaultOptions.Default_Video_Extensions)
        self.default_subtitle_extensions_layout = DefaultExtensionsLayout(label_name="Subtitle Extensions: ",
                                                                          extensions_list=AllSubtitlesExtensions,
                                                                          default_extensions_list=DefaultOptions.Default_Subtitle_Extensions)
        self.default_audio_extensions_layout = DefaultExtensionsLayout(label_name="Audio Extensions: ",
                                                                       extensions_list=AllAudiosExtensions,
                                                                       default_extensions_list=DefaultOptions.Default_Audio_Extensions)
        self.default_chapter_extensions_layout = DefaultExtensionsLayout(label_name="Chapter Extensions: ",
                                                                         extensions_list=AllChapterExtensions,
                                                                         default_extensions_list=DefaultOptions.Default_Chapter_Extensions)

        self.default_subtitle_language_layout = DefaultLanguageLayout(label_name="Subtitle Language: ",
                                                                      languages_list=DefaultOptions.Default_Favorite_Subtitle_Languages,
                                                                      default_language=DefaultOptions.Default_Subtitle_Language)
        self.default_audio_language_layout = DefaultLanguageLayout(label_name="Audio Language: ",
                                                                   languages_list=DefaultOptions.Default_Favorite_Audio_Languages,
                                                                   default_language=DefaultOptions.Default_Audio_Language)
        self.setting_info_text_icon_label = QLabel()
        self.setting_info_text_icon_label.setPixmap(QPixmap(InfoIconPath))
        self.setting_info_text_label = QLabel("Changes will apply on next launch")
        self.setting_about_button = AboutButton()
        self.setting_donate_button = DonateButton()
        self.setting_info_layout.addWidget(self.setting_info_text_icon_label, stretch=0)
        self.setting_info_layout.addWidget(self.setting_info_text_label, stretch=1)
        self.setting_info_layout.addWidget(self.setting_donate_button, stretch=0, alignment=Qt.AlignRight)
        self.setting_info_layout.addWidget(self.setting_about_button, stretch=0, alignment=Qt.AlignRight)
        self.main_layout = QVBoxLayout()
        self.setup_main_layout()
        self.setLayout(self.main_layout)
        self.connect_signals()

    def setup_main_layout(self):
        self.setup_default_directories_groupBox()
        self.setup_default_extensions_groupBox()
        self.setup_default_languages_groupBox()
        self.setup_default_directories_layout()
        self.setup_default_extensions_layout()
        self.setup_default_languages_layout()
        self.main_layout.addWidget(self.default_directories_groupBox, stretch=0)
        self.main_layout.addWidget(self.default_extensions_groupBox, stretch=0)
        self.main_layout.addWidget(self.default_languages_groupBox, stretch=0)
        self.main_layout.addLayout(self.setting_info_layout, stretch=0)

    def setup_default_directories_groupBox(self):
        self.default_directories_groupBox.setStyle(QStyleFactory.create("windowsvista"))
        self.default_directories_groupBox.setTitle("Default Directories")
        self.default_directories_groupBox.setLayout(self.default_directories_layout)

    def setup_default_extensions_groupBox(self):
        self.default_extensions_groupBox.setStyle(QStyleFactory.create("windowsvista"))
        self.default_extensions_groupBox.setTitle("Default Extensions")
        self.default_extensions_groupBox.setLayout(self.default_extensions_layout)

    def setup_default_languages_groupBox(self):
        self.default_languages_groupBox.setStyle(QStyleFactory.create("windowsvista"))
        self.default_languages_groupBox.setTitle("Favorite Languages List")
        self.default_languages_groupBox.setLayout(self.default_languages_layout)

    def setup_default_directories_layout(self):
        self.default_directories_layout.addLayout(self.default_video_directory_layout)
        self.default_directories_layout.addLayout(self.default_subtitle_directory_layout)
        self.default_directories_layout.addLayout(self.default_audio_directory_layout)
        self.default_directories_layout.addLayout(self.default_chapter_directory_layout)
        self.default_directories_layout.addLayout(self.default_attachment_directory_layout)
        self.default_directories_layout.addLayout(self.default_destination_directory_layout)

    def setup_default_extensions_layout(self):
        self.default_extensions_layout.addLayout(self.default_video_extensions_layout, 0, 0)
        self.default_extensions_layout.addLayout(self.default_subtitle_extensions_layout, 0, 1)
        self.default_extensions_layout.addLayout(self.default_audio_extensions_layout, 1, 0)
        self.default_extensions_layout.addLayout(self.default_chapter_extensions_layout, 1, 1)

    def setup_default_languages_layout(self):
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.label, 0, 0)
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.languages_comboBox, 0, 1)
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.setting_button, 0, 2)
        self.default_languages_layout.addWidget(QLabel(" "), 0, 3)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.label, 0, 4)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.languages_comboBox, 0, 5)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.setting_button, 0, 6)
        self.default_languages_layout.setColumnStretch(0, 0)
        self.default_languages_layout.setColumnStretch(1, 1)
        self.default_languages_layout.setColumnStretch(2, 0)
        self.default_languages_layout.setColumnStretch(3, 0)
        self.default_languages_layout.setColumnStretch(4, 0)
        self.default_languages_layout.setColumnStretch(5, 1)
        self.default_languages_layout.setColumnStretch(6, 0)

    def connect_signals(self):
        pass
