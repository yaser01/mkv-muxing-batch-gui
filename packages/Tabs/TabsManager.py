from PySide2.QtCore import Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTabWidget
from packages.Tabs.AttachmentTab.AttachmentSelection import AttachmentSelectionSetting
from packages.Tabs.AudioTab.AudioSelection import AudioSelectionSetting
from packages.Tabs.AudioTab.AudioTabManager import AudioTabManager
from packages.Tabs.ChapterTab.ChapterSelection import ChapterSelectionSetting
from packages.Tabs.MuxSetting.MuxSetting import MuxSettingTab
from packages.Tabs.SubtitleTab.SubtitleTabManager import SubtitleTabManager
from packages.Tabs.VideoTab.VideoSelection import VideoSelectionSetting


class TabsManager(QTabWidget):
    task_bar_start_muxing_signal = Signal()
    update_task_bar_progress_signal = Signal(int)
    update_task_bar_paused_signal = Signal()
    update_task_bar_clear_signal = Signal()

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
            "Attachment": 3,
            "Chapter": 4,
            "Mux Setting": 5,
        }
        self.add_tabs()
        self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string="#BABABA")
        self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string="#BABABA")
        self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string="#BABABA")
        self.connect_signals()

    def add_tabs(self):
        self.addTab(self.video_tab, "Videos")
        self.addTab(self.subtitle_tab, "Subtitles")
        self.addTab(self.audio_tab, "Audios")
        self.addTab(self.attachment_tab, "Attachments")
        self.addTab(self.chapter_tab, "Chapters")
        self.addTab(self.mux_setting_tab, "Mux Setting")

    def set_tab_color(self, tab_index, color_string):
        self.tabBar().setTabTextColor(tab_index, QColor(color_string))

    def connect_signals(self):
        self.attachment_tab.activation_signal.connect(self.change_attachment_activated_state)
        self.subtitle_tab.activation_signal.connect(self.change_subtitle_activated_state)
        self.audio_tab.activation_signal.connect(self.change_audio_activated_state)
        self.chapter_tab.activation_signal.connect(self.change_chapter_activated_state)
        self.mux_setting_tab.start_muxing_signal.connect(self.tt)
        self.mux_setting_tab.update_task_bar_progress_signal.connect(self.update_task_bar_progress_signal.emit)
        self.mux_setting_tab.update_task_bar_paused_signal.connect(self.update_task_bar_paused_signal.emit)
        self.mux_setting_tab.update_task_bar_clear_signal.connect(self.update_task_bar_clear_signal.emit)
        self.currentChanged.connect(self.current_tab_changed)

    def tt(self):
        self.task_bar_start_muxing_signal.emit()

    def change_attachment_activated_state(self, new_state):
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string="#000000")
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Attachment"], color_string="#BABABA")

    def change_subtitle_activated_state(self, new_state):
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Subtitle"], color_string="#000000")
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Subtitle"], color_string="#BABABA")

    def change_audio_activated_state(self, new_state):
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string="#000000")
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Audio"], color_string="#BABABA")

    def change_chapter_activated_state(self, new_state):
        if new_state:
            self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string="#000000")
        else:
            self.set_tab_color(tab_index=self.tabs_ids["Chapter"], color_string="#BABABA")

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
