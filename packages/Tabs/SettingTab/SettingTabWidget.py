from PySide2.QtWidgets import QWidget, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QStyleFactory, \
    QGridLayout

from packages.Startup.DefaultOptions import Default_Video_Extensions, Default_Subtitle_Extensions, \
    Default_Audio_Extensions, Default_Chapter_Extensions, Default_Subtitle_Language, Default_Audio_Language
from packages.Startup.PreDefined import AllVideosExtensions, AllSubtitlesExtensions, AllAudiosExtensions, \
    AllChapterExtensions, AllSubtitlesLanguages, AllAudiosLanguages
from packages.Tabs.SettingTab.ClearSourceButton import ClearSourceButton
from packages.Tabs.SettingTab.DefaultDirectoryLineEdit import DefaultDirectoryLineEdit
from packages.Tabs.SettingTab.DefaultDirectorySourceButton import DefaultDirectorySourceButton
from packages.Tabs.SettingTab.DefaultDirectoryLayout import DefaultDirectoryLayout
from packages.Tabs.SettingTab.DefaultExtensionsLayout import DefaultExtensionsLayout
from packages.Tabs.SettingTab.DefaultLanguageLayout import DefaultLanguageLayout


class SettingTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.default_directories_groupBox = QGroupBox(self)
        self.default_extensions_groupBox = QGroupBox(self)
        self.default_languages_groupBox = QGroupBox(self)
        self.default_directories_layout = QVBoxLayout()
        self.default_extensions_layout = QGridLayout()
        self.default_languages_layout = QGridLayout()
        self.default_video_directory_layout = DefaultDirectoryLayout(label_name="Videos Directory: ")
        self.default_subtitle_directory_layout = DefaultDirectoryLayout(label_name="Subtitles Directory: ")
        self.default_audio_directory_layout = DefaultDirectoryLayout(label_name="Audios Directory: ")
        self.default_chapter_directory_layout = DefaultDirectoryLayout(label_name="Chapters Directory: ")
        self.default_attachment_directory_layout = DefaultDirectoryLayout(label_name="Attachments Directory: ")
        self.default_video_extensions_layout = DefaultExtensionsLayout(label_name="Videos Extensions: ",
                                                                       extensions_list=AllVideosExtensions,
                                                                       default_extensions_list=Default_Video_Extensions)
        self.default_subtitle_extensions_layout = DefaultExtensionsLayout(label_name="Subtitles Extensions: ",
                                                                          extensions_list=AllSubtitlesExtensions,
                                                                          default_extensions_list=Default_Subtitle_Extensions)
        self.default_audio_extensions_layout = DefaultExtensionsLayout(label_name="Audios Extensions: ",
                                                                       extensions_list=AllAudiosExtensions,
                                                                       default_extensions_list=Default_Audio_Extensions)
        self.default_chapter_extensions_layout = DefaultExtensionsLayout(label_name="Chapters Extensions: ",
                                                                         extensions_list=AllChapterExtensions,
                                                                         default_extensions_list=Default_Chapter_Extensions)

        self.default_subtitle_language_layout = DefaultLanguageLayout(label_name="Subtitle Language: ",
                                                                      languages_list=AllSubtitlesLanguages,
                                                                      default_language=Default_Subtitle_Language)
        self.default_audio_language_layout = DefaultLanguageLayout(label_name="Audio Language: ",
                                                                   languages_list=AllAudiosLanguages,
                                                                   default_language=Default_Audio_Language)
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
        self.main_layout.addWidget(self.default_directories_groupBox,stretch=0)
        self.main_layout.addWidget(self.default_extensions_groupBox,stretch=0)
        self.main_layout.addWidget(self.default_languages_groupBox,stretch=0)

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
        self.default_languages_groupBox.setTitle("Default Language")
        self.default_languages_groupBox.setLayout(self.default_languages_layout)

    def setup_default_directories_layout(self):
        self.default_directories_layout.addLayout(self.default_video_directory_layout)
        self.default_directories_layout.addLayout(self.default_subtitle_directory_layout)
        self.default_directories_layout.addLayout(self.default_audio_directory_layout)
        self.default_directories_layout.addLayout(self.default_chapter_directory_layout)
        self.default_directories_layout.addLayout(self.default_attachment_directory_layout)

    def setup_default_extensions_layout(self):
        self.default_extensions_layout.addLayout(self.default_video_extensions_layout, 0, 0)
        self.default_extensions_layout.addLayout(self.default_subtitle_extensions_layout, 0, 1)
        self.default_extensions_layout.addLayout(self.default_audio_extensions_layout, 1, 0)
        self.default_extensions_layout.addLayout(self.default_chapter_extensions_layout, 1, 1)

    def setup_default_languages_layout(self):
        self.default_languages_layout.addLayout(self.default_subtitle_language_layout, 0, 0)
        self.default_languages_layout.addLayout(self.default_audio_language_layout, 0, 1)

    def connect_signals(self):
        pass
