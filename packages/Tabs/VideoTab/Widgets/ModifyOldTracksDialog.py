from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel

from packages.Startup.GlobalIcons import InfoIcon
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import GlobalSetting, convert_string_integer_to_two_digit_string
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.ModifyOldTracksTabsManager import ModifyOldTracksTabsManager
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.TrackInfoTable import TrackInfoTable
from packages.Widgets.InfoDialog import InfoDialog
from packages.Widgets.MyDialog import MyDialog


def show_info_dialog():
    info_dialog = InfoDialog(window_title="Conflicting with other settings",
                             info_message="Using this window will limits/disable the use of the following options:<br>"
                                          "1- <b>Mux After Track</b> in Subtitle/Audio Tabs.<br>"
                                          "2- <b>Only Keep Those Subtitles/Audios</b> By [Track Id, Track Name, "
                                          "Track Language] in Muxing Tab.<br> "
                                          "3- <b>Make This Subtitle/Audio Default</b> By [Track Id, Track Name, "
                                          "Track Language] in Muxing Tab.<br> "
                                          "This is necessary because above options also [depends on/modify] old track "
                                          "in "
                                          "someway.<br> "
                                          "Also Adding new subtitles/audios with options: (set default/forced) "
                                          "will override options: (set default/forced) shown here.<br> "
                                          "<u>In short</u> you have to know what you are doing :D</div>")
    info_dialog.execute()


class ModifyOldTracksDialog(MyDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modify Old Tracks")
        self.instructions_label = QLabel()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.reset_button = QPushButton("Reset To Default")
        self.old_tracks_tabs = ModifyOldTracksTabsManager()
        self.track_info_label = QLabel("Information About Tracks:")
        self.info_button = QPushButton(text="")
        self.info_button.setIcon(InfoIcon)
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.reset_button = QPushButton("Reset To Default")
        self.track_info_table = TrackInfoTable()
        self.track_info_table.update_video_name(GlobalSetting.VIDEO_FILES_LIST)
        self.main_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.info_layout = QHBoxLayout()
        self.setup_instructions_label()
        self.setup_layouts()
        self.setup_window_dimension()
        self.disable_question_mark_window()
        self.enable_maximize_mark_window()
        self.setLayout(self.main_layout)
        self.connect_signals()

    def setup_layouts(self):
        self.setup_info_layout()
        self.setup_buttons_layout()
        self.setup_main_layout()

    def setup_info_layout(self):
        self.info_layout.addWidget(self.info_button)
        self.info_layout.addWidget(self.instructions_label, stretch=10)

    def setup_buttons_layout(self):
        self.buttons_layout.addStretch(stretch=3)
        self.buttons_layout.addWidget(self.reset_button, stretch=2)
        self.buttons_layout.addWidget(self.ok_button, stretch=2)
        self.buttons_layout.addWidget(self.cancel_button, stretch=2)
        self.buttons_layout.addStretch(stretch=3)

    def setup_window_dimension(self):
        self.setMinimumWidth(screen_size.width() // 1.5)
        self.setMinimumHeight(screen_size.height() // 2.5)

    def setup_main_layout(self):
        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addWidget(self.old_tracks_tabs)
        self.main_layout.addWidget(self.track_info_label)
        self.main_layout.addWidget(self.track_info_table)
        self.main_layout.addLayout(self.buttons_layout)

    def setup_instructions_label(self):
        self.instructions_label.setTextFormat(Qt.RichText)
        instructions_text = "Here you can modify/disable old tracks even reorder tracks by using [Ctrl+Up/Down Arrow] " \
                            "to move track up/down."

        no_editing_text = "<br>Editing is <b>Disabled</b> because job queue has unfinished jobs."
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            instructions_text += no_editing_text
        self.instructions_label.setText(instructions_text)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def enable_maximize_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, on=True)

    def connect_signals(self):
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.restore_defaults)
        self.old_tracks_tabs.current_selected_track_changed.connect(self.update_showed_track_info)
        self.old_tracks_tabs.currentChanged.connect(self.update_current_tab)
        self.info_button.clicked.connect(show_info_dialog)

    def restore_defaults(self):
        self.old_tracks_tabs.restore_defaults()

    def save_settings(self):
        self.old_tracks_tabs.save_settings()
        self.close()

    def update_showed_track_info(self, new_info):
        track_type, track_id = new_info
        if track_type == "subtitle" and self.old_tracks_tabs.currentIndex() == 1:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO.copy())
            self.track_info_label.setText(
                f"Information About Subtitle Track [{convert_string_integer_to_two_digit_string(track_id)}] Across "
                f"Videos:")
            self.track_info_table.setup_info(track_id=track_id)
        elif track_type == "audio" and self.old_tracks_tabs.currentIndex() == 2:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO.copy())
            self.track_info_label.setText(
                f"Information About Audio Track [{convert_string_integer_to_two_digit_string(track_id)}] Across Videos:")
            self.track_info_table.setup_info(track_id=track_id)
        elif track_type == "video" and self.old_tracks_tabs.currentIndex() == 0:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO.copy())
            self.track_info_label.setText(
                f"Information About Video Track [{convert_string_integer_to_two_digit_string(track_id)}] Across Videos:")
            self.track_info_table.setup_info(track_id=track_id)

    def update_current_tab(self, tab_id):
        if tab_id == 0:
            self.old_tracks_tabs.video_tab.table_focused()
        elif tab_id == 1:
            self.old_tracks_tabs.subtitle_tab.table_focused()
        elif tab_id == 2:
            self.old_tracks_tabs.audio_tab.table_focused()

    def execute(self):
        self.exec_()
