from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QGroupBox,
)

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.SetupThems import get_dark_palette, get_light_palette
from packages.Tabs.AudioTab.Widgets.AudioClearButton import AudioClearButton
from packages.Tabs.AudioTab.Widgets.AudioDelayDoubleSpinBox import AudioDelayDoubleSpinBox
from packages.Tabs.AudioTab.Widgets.AudioExtensionsCheckableComboBox import AudioExtensionsCheckableComboBox
from packages.Tabs.AudioTab.Widgets.AudioLanguageComboBox import AudioLanguageComboBox
from packages.Tabs.AudioTab.Widgets.AudioMuxAtTop import AudioMuxAtTop
from packages.Tabs.AudioTab.Widgets.AudioSetDefaultCheckBox import AudioSetDefaultCheckBox
from packages.Tabs.AudioTab.Widgets.AudioSetForcedCheckBox import AudioSetForcedCheckBox
from packages.Tabs.AudioTab.Widgets.AudioSourceButton import AudioSourceButton
from packages.Tabs.AudioTab.Widgets.AudioSourceLineEdit import AudioSourceLineEdit
from packages.Tabs.AudioTab.Widgets.AudioTrackNameLineEdit import AudioTrackNameLineEdit
from packages.Tabs.AudioTab.Widgets.MatchAudioLayout import MatchAudioLayout
from packages.Tabs.GlobalSetting import *
from packages.Widgets.InvalidPathDialog import *
from packages.Widgets.WarningDialog import WarningDialog
from packages.Widgets.YesNoDialog import *


# noinspection PyAttributeOutsideInit
class AudioSelectionSetting(QGroupBox):
    tab_clicked_signal = Signal()

    is_there_old_files_signal = Signal(bool)

    def __init__(self, tab_index):
        super().__init__()
        self.tab_index = tab_index
        self.create_properties()
        self.create_global_properties()
        self.create_widgets()
        self.setup_widgets()
        self.connect_signals()

    def create_widgets(self):
        self.audio_source_label = QLabel("Audio Source Folder:")
        self.audio_language_label = QLabel("Language:")
        self.audio_extension_label = QLabel("Audio Extension:")
        self.audio_delay_label = QLabel("Delay:")
        # self.audio_tab_comboBox = AudioTabComboBox()
        self.audio_source_lineEdit = AudioSourceLineEdit()
        self.audio_source_button = AudioSourceButton()
        self.audio_clear_button = AudioClearButton()
        self.audio_extensions_comboBox = AudioExtensionsCheckableComboBox()
        self.audio_language_comboBox = AudioLanguageComboBox(self.tab_index)
        self.audio_track_name_lineEdit = AudioTrackNameLineEdit(self.tab_index)
        self.audio_delay_spin = AudioDelayDoubleSpinBox(self.tab_index)
        self.audio_set_forced_checkBox = AudioSetForcedCheckBox(self.tab_index)
        self.audio_set_default_checkBox = AudioSetDefaultCheckBox(self.tab_index)
        self.audio_mux_at_top_checkBox = AudioMuxAtTop(self.tab_index)
        self.audio_match_layout = MatchAudioLayout(parent=self, tab_index=self.tab_index)
        self.audio_options_layout = QHBoxLayout()
        self.audio_set_default_forced_layout = QHBoxLayout()
        # self.MainLayout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.setObjectName("main_groupBox")
        self.setStyleSheet(
            "QGroupBox#main_groupBox {subcontrol-origin: margin;left: 3px;padding: 3px 0px 3px 0px;}")
        self.audio_match_groupBox = QGroupBox("Audio Matching")
        self.audio_match_groupBox.setLayout(self.audio_match_layout)

    def setup_widgets(self):
        self.setup_audio_main_groupBox()
        self.setup_layouts()

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        # self.audio_main_groupBox.toggled.connect(self.activate_tab)
        self.audio_source_button.clicked_signal.connect(self.update_folder_path)
        self.audio_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.audio_source_lineEdit.set_is_drag_and_drop_signal.connect(self.update_is_drag_and_drop)
        self.audio_extensions_comboBox.close_list.connect(self.check_extension_changes)
        self.audio_match_layout.sync_audio_files_with_global_files_after_swap_delete_signal.connect(
            self.sync_audio_files_with_global_files)
        self.tab_clicked_signal.connect(self.tab_clicked)
        self.audio_match_layout.audio_table.drop_folder_and_files_signal.connect(
            self.update_files_with_drag_and_drop)
        self.audio_clear_button.clear_files_signal.connect(self.clear_files)

    def create_global_properties(self):
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index] = []
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index] = []
        GlobalSetting.AUDIO_TRACK_NAME[self.tab_index] = ""
        GlobalSetting.AUDIO_DELAY[self.tab_index] = 0.0
        GlobalSetting.AUDIO_TAB_ENABLED[self.tab_index] = False
        GlobalSetting.AUDIO_SET_DEFAULT[self.tab_index] = False
        GlobalSetting.AUDIO_SET_FORCED[self.tab_index] = False
        GlobalSetting.AUDIO_SET_AT_TOP[self.tab_index] = False
        GlobalSetting.AUDIO_LANGUAGE[self.tab_index] = DefaultOptions.Default_Audio_Language

    def create_properties(self):
        self.folder_path = ""
        self.drag_and_dropped_text = "[Drag & Drop Files]"
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_names_absolute_list_with_dropped_files = []
        self.current_audio_extensions = DefaultOptions.Default_Audio_Extensions
        self.is_drag_and_drop = False

    def setup_layouts(self):
        self.setup_audio_check_default_forced_layout()
        self.setup_audio_options_layout()
        self.setup_main_layout()
        # self.setLayout(self.MainLayout)
        # self.MainLayout.addWidget(self.audio_tab_comboBox)
        # self.MainLayout.addWidget(self.audio_main_groupBox)

    def setup_audio_check_default_forced_layout(self):
        self.audio_set_default_forced_layout.addWidget(self.audio_set_default_checkBox)
        self.audio_set_default_forced_layout.addWidget(self.audio_set_forced_checkBox)
        self.audio_set_default_forced_layout.addWidget(self.audio_mux_at_top_checkBox)

    def setup_audio_options_layout(self):
        self.audio_options_layout.addWidget(self.audio_extensions_comboBox, 2)
        self.audio_options_layout.addWidget(self.audio_language_label)
        self.audio_options_layout.addWidget(self.audio_language_comboBox, 4)
        self.audio_options_layout.addWidget(self.audio_track_name_lineEdit, 2)
        self.audio_options_layout.addWidget(self.audio_delay_label)
        self.audio_options_layout.addWidget(self.audio_delay_spin)
        self.audio_options_layout.addSpacing(10)
        self.audio_options_layout.addLayout(self.audio_set_default_forced_layout)
        self.audio_options_layout.addStretch()

    def setup_main_layout(self):
        pass
        self.main_layout.addWidget(self.audio_source_label, 0, 0)
        self.main_layout.addWidget(self.audio_source_lineEdit, 0, 1, 1, 1)
        self.main_layout.addWidget(self.audio_clear_button, 0, 2, 1, 1)
        self.main_layout.addWidget(self.audio_source_button, 0, 3)
        self.main_layout.addWidget(self.audio_extension_label, 1, 0)
        self.main_layout.addLayout(self.audio_options_layout, 1, 1, 1, 3)
        self.main_layout.addWidget(self.audio_match_groupBox, 2, 0, 1, -1)

    def setup_audio_main_groupBox(self):
        self.setLayout(self.main_layout)
        # self.audio_main_groupBox.setTitle("Audios")
        # self.audio_main_groupBox.setCheckable(True)
        # self.audio_main_groupBox.setChecked(True)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.audio_source_lineEdit.set_text_safe_change(new_path)
            self.update_files_lists(new_path)
            self.show_audio_files_list()
        else:
            if self.is_drag_and_drop:
                self.audio_source_lineEdit.set_text_safe_change(self.drag_and_dropped_text)

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            if self.is_drag_and_drop:
                new_files_absolute_path_list = []
                self.files_names_list = []
                current_extensions = self.audio_extensions_comboBox.currentData()
                for file_absolute_path in self.files_names_absolute_list_with_dropped_files:
                    if os.path.isdir(file_absolute_path):
                        continue
                    if os.path.getsize(file_absolute_path) == 0:
                        continue
                    temp_file_name = os.path.basename(file_absolute_path)
                    for j in range(len(current_extensions)):
                        temp_file_extension_start_index = temp_file_name.rfind(".")
                        if temp_file_extension_start_index == -1:
                            continue
                        temp_file_extension = temp_file_name[temp_file_extension_start_index + 1:]
                        if temp_file_extension.lower() == current_extensions[j].lower():
                            new_files_absolute_path_list.append(file_absolute_path)
                            self.files_names_list.append(os.path.basename(file_absolute_path))
                            break
                self.audio_source_lineEdit.stop_check_path = True
                self.audio_source_lineEdit.setText(self.drag_and_dropped_text)
                self.is_drag_and_drop = True
                self.folder_path = ""
                self.files_names_absolute_list = new_files_absolute_path_list.copy()
                self.files_names_absolute_list_with_dropped_files = new_files_absolute_path_list.copy()
                self.audio_source_lineEdit.stop_check_path = False
            else:
                self.audio_source_lineEdit.set_text_safe_change("")
            return
        try:
            self.is_drag_and_drop = False
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
            self.files_names_absolute_list_with_dropped_files = self.files_names_absolute_list.copy()
        except Exception as e:
            invalid_path_dialog = InvalidPathDialog()
            invalid_path_dialog.execute()

    def check_extension_changes(self, new_extensions):
        if self.current_audio_extensions != new_extensions:
            self.current_audio_extensions = new_extensions
            self.update_files_lists(self.folder_path)
            self.show_audio_files_list()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        current_extensions = self.audio_extensions_comboBox.currentData()
        result = []
        for i in range(len(temp_files_names)):
            if os.path.isdir(temp_files_names_absolute[i]):
                continue
            if os.path.getsize(temp_files_names_absolute[i]) == 0:
                continue
            for j in range(len(current_extensions)):
                temp_file_extension_start_index = temp_files_names[i].rfind(".")
                if temp_file_extension_start_index == -1:
                    continue
                temp_file_extension = temp_files_names[i][temp_file_extension_start_index + 1:]
                if temp_file_extension.lower() == current_extensions[j].lower():
                    result.append(temp_files_names[i])
                    break
        return result

    def show_audio_files_list(self):
        self.update_other_classes_variables()
        self.audio_match_layout.show_audio_files()

    def update_other_classes_variables(self):
        # self.change_global_last_path_directory()
        self.change_global_audio_list()
        self.audio_source_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.audio_source_lineEdit.set_is_there_old_file(len(self.files_names_list) > 0)
        self.audio_extensions_comboBox.set_is_there_old_file(len(self.files_names_list) > 0)
        self.audio_clear_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.audio_source_lineEdit.set_current_folder_path(self.folder_path)
        self.audio_source_lineEdit.set_is_drag_and_drop(self.is_drag_and_drop)
        self.audio_extensions_comboBox.set_current_folder_path(self.folder_path)
        self.audio_extensions_comboBox.set_current_files_list(self.files_names_list)
        self.is_there_old_files_signal.emit(len(self.files_names_list) > 0)

    def clear_files(self):
        self.folder_path = ""
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_names_absolute_list_with_dropped_files = []
        self.audio_source_lineEdit.set_text_safe_change("")
        self.is_drag_and_drop = False
        self.show_audio_files_list()

    def change_global_audio_list(self):
        GlobalSetting.AUDIO_TAB_ENABLED[self.tab_index] = len(self.files_names_list) > 0
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index] = self.files_names_list
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index] = self.files_names_absolute_list

    def show_video_files_list(self):
        self.audio_match_layout.show_video_files()

    def activate_tab(self, on):
        if on:
            self.show_video_files_list()
        else:
            self.audio_source_lineEdit.set_text_safe_change("")
            self.audio_match_layout.clear_tables()
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.current_audio_extensions = DefaultOptions.Default_Audio_Extensions
            self.audio_extensions_comboBox.setData(self.current_audio_extensions)
            self.audio_track_name_lineEdit.setText("")
            self.audio_set_forced_checkBox.setChecked(False)
            self.audio_set_default_checkBox.setChecked(False)
            self.is_drag_and_drop = False
            self.audio_source_lineEdit.set_is_drag_and_drop(False)
            self.audio_delay_spin.setValue(0)
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index] = []
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index] = []
            GlobalSetting.AUDIO_TRACK_NAME[self.tab_index] = ""
            GlobalSetting.AUDIO_DELAY[self.tab_index] = 0.0
            GlobalSetting.AUDIO_SET_DEFAULT[self.tab_index] = False
            GlobalSetting.AUDIO_SET_FORCED[self.tab_index] = False
            GlobalSetting.AUDIO_SET_AT_TOP[self.tab_index] = False
            GlobalSetting.AUDIO_TAB_ENABLED[self.tab_index] = False
            GlobalSetting.AUDIO_LANGUAGE[self.tab_index] = ""

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.RightButton:
            self.audio_match_layout.clear_audio_selection()
        if (QMouseEvent.buttons() == Qt.RightButton or QMouseEvent.buttons() == Qt.LeftButton) and (
                self.audio_source_lineEdit.text() == ""):
            self.audio_source_lineEdit.set_text_safe_change(self.folder_path)
        return QWidget.mousePressEvent(self, QMouseEvent)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.show_video_files_list()

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace() and not self.is_drag_and_drop:
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def tab_clicked(self):
        self.show_audio_files_list()
        self.show_video_files_list()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.update_audio_set_default_forced_state()
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()
            self.update_audio_set_default_forced_state()

    def update_audio_set_default_forced_state(self):
        self.audio_set_default_checkBox.update_check_state()
        self.audio_set_forced_checkBox.update_check_state()

    def disable_editable_widgets(self):
        self.audio_source_lineEdit.setEnabled(False)
        self.audio_source_button.setEnabled(False)
        self.audio_extensions_comboBox.setEnabled(False)
        self.audio_language_comboBox.setEnabled(False)
        self.audio_track_name_lineEdit.setEnabled(False)
        self.audio_delay_spin.setEnabled(False)
        self.audio_set_default_checkBox.setEnabled(False)
        self.audio_set_forced_checkBox.setEnabled(False)
        self.setCheckable(False)
        self.audio_clear_button.setEnabled(False)
        self.audio_mux_at_top_checkBox.setEnabled(False)
        self.audio_match_layout.disable_editable_widgets()

    def enable_editable_widgets(self):
        self.audio_source_lineEdit.setEnabled(True)
        self.audio_source_button.setEnabled(True)
        self.audio_extensions_comboBox.setEnabled(True)
        self.audio_language_comboBox.setEnabled(True)
        self.audio_track_name_lineEdit.setEnabled(True)
        self.audio_delay_spin.setEnabled(True)
        self.audio_set_default_checkBox.setEnabled(True)
        self.audio_set_forced_checkBox.setEnabled(True)
        self.audio_clear_button.setEnabled(True)
        self.audio_mux_at_top_checkBox.setEnabled(True)
        self.audio_match_layout.enable_editable_widgets()

    def sync_audio_files_with_global_files(self):
        self.files_names_list = GlobalSetting.AUDIO_FILES_LIST[self.tab_index]
        self.files_names_absolute_list = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index]
        self.update_other_classes_variables()

    def update_files_with_drag_and_drop(self, paths_list):
        duplicate_flag = False
        not_duplicate_files_absolute_path_list = []
        not_duplicate_files_list = []
        duplicate_files_list = []
        new_files_absolute_path_list = []
        current_extensions = self.audio_extensions_comboBox.currentData()
        for path in paths_list:
            if os.path.isfile(path):
                if os.path.getsize(path) == 0:
                    continue
                temp_file_name = os.path.basename(path)
                for j in range(len(current_extensions)):
                    temp_file_extension_start_index = temp_file_name.rfind(".")
                    if temp_file_extension_start_index == -1:
                        continue
                    temp_file_extension = temp_file_name[temp_file_extension_start_index + 1:]
                    if temp_file_extension.lower() == current_extensions[j].lower():
                        new_files_absolute_path_list.append(path)
                        break
            else:
                new_files_absolute_path_list.extend(
                    sort_names_like_windows(get_files_names_absolute_list(self.get_files_list(path), path)))

        for new_file_name in new_files_absolute_path_list:
            if os.path.basename(new_file_name).lower() in map(str.lower, self.files_names_list):
                duplicate_flag = True
                duplicate_files_list.append(os.path.basename(new_file_name))
            else:
                not_duplicate_files_absolute_path_list.append(new_file_name)
                not_duplicate_files_list.append(os.path.basename(new_file_name))
                self.files_names_list.append(os.path.basename(new_file_name))
        self.audio_source_lineEdit.stop_check_path = True
        self.audio_source_lineEdit.setText(self.drag_and_dropped_text)
        self.is_drag_and_drop = True
        self.folder_path = ""
        self.files_names_absolute_list_with_dropped_files.extend(not_duplicate_files_absolute_path_list)
        self.files_names_absolute_list.extend(not_duplicate_files_absolute_path_list)
        self.show_audio_files_list()
        self.audio_source_lineEdit.stop_check_path = False
        if duplicate_flag:
            info_message = "One or more files have the same name with the old files will be " \
                           "skipped:"
            for file_name in duplicate_files_list:
                info_message += "\n" + file_name
            warning_dialog = WarningDialog(window_title="Duplicate files names", info_message=info_message,
                                           parent=self.window())
            warning_dialog.execute_wth_no_block()

    def update_is_drag_and_drop(self, new_state):
        self.is_drag_and_drop = new_state

    def set_default_directory(self):
        self.audio_source_lineEdit.set_text_safe_change(DefaultOptions.Default_Audio_Directory)
        self.update_folder_path(DefaultOptions.Default_Audio_Directory)
        self.audio_source_lineEdit.check_new_path()

    def update_theme_mode_state(self):
        if DefaultOptions.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet(
            "QGroupBox#main_groupBox {subcontrol-origin: margin;left: 3px;padding: 3px 0px 3px 0px;}")
