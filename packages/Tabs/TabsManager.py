from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTabWidget, QHBoxLayout, QWidget

from packages.Startup import ColorThems
from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.SetupThems import get_dark_palette, get_light_palette
from packages.Tabs.AttachmentTab.AttachmentSelection import AttachmentSelectionSetting
from packages.Tabs.AudioTab.AudioTabManager import AudioTabManager
from packages.Tabs.ChapterTab.ChapterSelection import ChapterSelectionSetting
from packages.Tabs.MuxSetting.MuxSetting import MuxSettingTab
from packages.Tabs.SettingTab.SettingButton import SettingButton
from packages.Tabs.SubtitleTab.SubtitleTabManager import SubtitleTabManager
from packages.Tabs.VideoTab.VideoSelection import VideoSelectionSetting
from packages.Widgets.ThemeButton import ThemeButton


def get_activate_and_disabled_color_according_to_current_theme():
    if DefaultOptions.Dark_Mode:
        activate_color = ColorThems.Dark_Text_Color
        disabled_color = ColorThems.Dark_Text_Color_Disabled
    else:
        activate_color = ColorThems.Light_Text_Color
        disabled_color = ColorThems.Light_Text_Color_Disabled
    return activate_color, disabled_color


class TabsManager(QTabWidget):
    task_bar_start_muxing_signal = Signal()
    update_task_bar_progress_signal = Signal(int)
    update_task_bar_paused_signal = Signal()
    update_task_bar_clear_signal = Signal()
    theme_changed_signal=Signal()
    def __init__(self):
        super().__init__()
        self.video_tab = VideoSelectionSetting()
        self.subtitle_tab = SubtitleTabManager()
        self.audio_tab = AudioTabManager()
        self.attachment_tab = AttachmentSelectionSetting()
        self.chapter_tab = ChapterSelectionSetting()
        self.mux_setting_tab = MuxSettingTab()
        self.tabs_ids = {
            "Video": 0,
            "Subtitle": 1,
            "Audio": 2,
            "Chapter": 3,
            "Attachment": 4,
            "Mux Setting": 5,
        }
        self.tabs_status = [True, True, False, False, False, True]
        self.add_tabs()

        self.setting_button = SettingButton()
        self.theme_button = ThemeButton()
        self.button_layout = QHBoxLayout()
        self.buttons_widget = QWidget()
        self.button_layout.addWidget(self.theme_button)
        self.button_layout.addWidget(self.setting_button)
        self.buttons_widget.setLayout(self.button_layout)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.setCornerWidget(self.buttons_widget, Qt.TopRightCorner)
        self.setStyleSheet("QTabWidget::right-corner{bottom: 2px;}")
        self.connect_signals()
        self.setup_tabs_theme()

    def add_tabs(self):
        self.addTab(self.video_tab, "Videos")
        self.addTab(self.subtitle_tab, "Subtitles")
        self.addTab(self.audio_tab, "Audios")
        self.addTab(self.chapter_tab, "Chapters")
        self.addTab(self.attachment_tab, "Attachments")
        self.addTab(self.mux_setting_tab, "Mux Setting")

    def set_tab_color(self, tab_index, color_string):
        self.tabBar().setTabTextColor(tab_index, QColor(*color_string))

    def connect_signals(self):
        self.attachment_tab.activation_signal.connect(self.change_attachment_activated_state)
        self.subtitle_tab.activation_signal.connect(self.change_subtitle_activated_state)
        self.audio_tab.activation_signal.connect(self.change_audio_activated_state)
        self.chapter_tab.activation_signal.connect(self.change_chapter_activated_state)
        self.mux_setting_tab.start_muxing_signal.connect(self.start_muxing)
        self.mux_setting_tab.update_task_bar_progress_signal.connect(self.update_task_bar_progress_signal.emit)
        self.mux_setting_tab.update_task_bar_paused_signal.connect(self.update_task_bar_paused_signal.emit)
        self.mux_setting_tab.update_task_bar_clear_signal.connect(self.update_task_bar_clear_signal.emit)
        self.currentChanged.connect(self.current_tab_changed)
        self.theme_button.dark_mode_updated_signal.connect(self.update_theme_mode_state)

    def start_muxing(self):
        self.task_bar_start_muxing_signal.emit()

    def setup_tabs_theme(self):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        self.set_tab_color(tab_index=self.tabs_ids["Video"], color_string=activate_color)
        self.set_tab_color(tab_index=self.tabs_ids["Subtitle"], color_string=activate_color)
        self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string=disabled_color)
        self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string=disabled_color)
        self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string=disabled_color)
        self.set_tab_color(tab_index=self.tabs_ids["Mux Setting"], color_string=activate_color)

    def change_attachment_activated_state(self, new_state):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string=activate_color)
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string=disabled_color)
        self.tabs_status[self.tabs_ids["Attachment"]] = new_state

    def change_subtitle_activated_state(self, new_state):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Subtitle"], color_string=activate_color)
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Subtitle"], color_string=disabled_color)
        self.tabs_status[self.tabs_ids["Subtitle"]] = new_state

    def change_audio_activated_state(self, new_state):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string=activate_color)
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string=disabled_color)
        self.tabs_status[self.tabs_ids["Audio"]] = new_state

    def change_chapter_activated_state(self, new_state):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string=activate_color)
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string=disabled_color)
        self.tabs_status[self.tabs_ids["Chapter"]] = new_state

    def update_theme_mode_state(self):
        self.theme_changed_signal.emit()
        self.video_tab.update_theme_mode_state()
        self.subtitle_tab.update_theme_mode_state()
        self.audio_tab.update_theme_mode_state()
        self.attachment_tab.update_theme_mode_state()
        self.mux_setting_tab.update_theme_mode_state()
        self.update_tabs_name_theme_mode_state()
        if DefaultOptions.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet("QTabWidget::right-corner{bottom: 2px;}")

    def update_tabs_name_theme_mode_state(self):
        activate_color, disabled_color = get_activate_and_disabled_color_according_to_current_theme()
        for tab_id in range(len(self.tabs_status)):
            tab_status = self.tabs_status[tab_id]
            if tab_status:
                self.set_tab_color(tab_index=tab_id, color_string=activate_color)
            else:
                self.set_tab_color(tab_index=tab_id, color_string=disabled_color)

    def current_tab_changed(self, index):
        if index == self.tabs_ids["Video"]:
            self.video_tab.tab_clicked_signal.emit()
        elif index == self.tabs_ids["Subtitle"]:
            self.subtitle_tab.tab_clicked_signal.emit()
        elif index == self.tabs_ids["Audio"]:
            self.audio_tab.tab_clicked_signal.emit()
        elif index == self.tabs_ids["Attachment"]:
            self.attachment_tab.tab_clicked_signal.emit()
        elif index == self.tabs_ids["Chapter"]:
            self.chapter_tab.tab_clicked_signal.emit()
        elif index == self.tabs_ids["Mux Setting"]:
            self.mux_setting_tab.tab_clicked_signal.emit()

    def set_default_directories(self):
        self.video_tab.set_default_directory()
        self.subtitle_tab.set_default_directory()
        self.audio_tab.set_default_directory()
        self.chapter_tab.set_default_directory()
        self.attachment_tab.set_default_directory()
        self.mux_setting_tab.set_default_directory()
