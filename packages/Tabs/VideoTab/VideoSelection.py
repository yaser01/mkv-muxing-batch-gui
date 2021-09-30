from PySide2.QtCore import Signal

from packages.Startup.DefaultOptions import Default_Video_Extension
from packages.Tabs.GlobalSetting import *
from packages.Tabs.GlobalSetting import sort_names_like_windows, get_readable_filesize, get_files_names_absolute_list, \
    get_file_name_absolute_path
from packages.Tabs.VideoTab.Widgets.LoadingVideosInfoDialog import LoadingVideosInfoDialog
from packages.Tabs.VideoTab.Widgets.VideoClearButton import VideoClearButton
from packages.Tabs.VideoTab.Widgets.VideoDefaultDurationFPSComboBox import VideoDefaultDurationFPSComboBox
from packages.Tabs.VideoTab.Widgets.VideoExtensionsCheckableComboBox import VideoExtensionsCheckableComboBox
from packages.Tabs.VideoTab.Widgets.VideoInfoButton import VideoInfoButton
from packages.Tabs.VideoTab.Widgets.VideoSourceButton import VideoSourceButton
from packages.Tabs.VideoTab.Widgets.VideoSourceLineEdit import VideoSourceLineEdit
from packages.Tabs.VideoTab.Widgets.VideoTable import VideoTable
from packages.Widgets.InvalidPathDialog import *

# noinspection PyAttributeOutsideInit
from packages.Widgets.WarningDialog import WarningDialog


def get_files_size_list(files_list, folder_path):
    files_size_list = []
    for i in range(len(files_list)):
        file_name_absolute = get_file_name_absolute_path(file_name=files_list[i], folder_path=folder_path)
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


def get_files_size_with_absolute_path_list(files_name_absolute_path):
    files_size_list = []
    for i in range(len(files_name_absolute_path)):
        file_name_absolute = files_name_absolute_path[i]
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


def show_loading_dialog(new_videos_list):
    loading_videos_info_dialog = LoadingVideosInfoDialog(new_videos_list)
    loading_videos_info_dialog.execute()


class VideoSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()

    def __init__(self):
        super().__init__()
        self.video_source_label = QLabel()
        self.video_source_lineEdit = VideoSourceLineEdit()
        self.video_source_button = VideoSourceButton()
        self.video_clear_button = VideoClearButton()
        self.video_extensions_label = QLabel()
        self.video_default_duration_fps_label = QLabel()
        self.video_default_duration_fps_comboBox = VideoDefaultDurationFPSComboBox()
        self.video_extensions_comboBox = VideoExtensionsCheckableComboBox()
        self.video_info_button = VideoInfoButton()
        self.table = VideoTable()
        self.main_layout = QGridLayout()
        self.folder_path = ""
        self.drag_and_dropped_text = "[Drag & Drop Files]"
        self.folders_paths = []
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_size_list = []
        self.files_names_checked_list = []
        self.files_names_absolute_list_with_dropped_files = []
        self.current_video_extensions = [Default_Video_Extension]
        self.is_drag_and_drop = False
        self.setup_widgets()
        self.connect_signals()

    def setup_widgets(self):
        self.setup_video_source_label()
        self.setup_video_extensions_label()
        self.setup_video_default_duration_fps_label()
        self.setup_layouts()

    def setup_layouts(self):
        self.setup_main_layout()
        self.setLayout(self.main_layout)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.video_source_lineEdit.setText(new_path)
            self.update_files_lists(new_path)
            self.show_files_list()
        else:
            if self.is_drag_and_drop:
                self.video_source_lineEdit.stop_check_path = True
                self.video_source_lineEdit.setText(self.drag_and_dropped_text)
                self.video_source_lineEdit.stop_check_path = False

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            if self.is_drag_and_drop:
                new_files_absolute_path_list = []
                self.files_names_list = []
                self.folders_paths = []
                current_extensions = self.video_extensions_comboBox.currentData()
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
                            if os.path.dirname(file_absolute_path) not in self.folders_paths:
                                self.folders_paths.append(os.path.dirname(file_absolute_path))
                            break
                self.video_source_lineEdit.stop_check_path = True
                self.video_source_lineEdit.setText(self.drag_and_dropped_text)
                self.is_drag_and_drop = True
                self.folder_path = ""
                self.files_names_absolute_list = new_files_absolute_path_list.copy()
                self.files_size_list = get_files_size_with_absolute_path_list(new_files_absolute_path_list)
                self.files_names_absolute_list_with_dropped_files = new_files_absolute_path_list.copy()
                self.files_names_checked_list = ([True] * len(new_files_absolute_path_list))
                if len(new_files_absolute_path_list) > 0:
                    show_loading_dialog(new_files_absolute_path_list)
                self.video_source_lineEdit.stop_check_path = False
            else:
                self.video_source_lineEdit.setText("")
            return
        try:
            self.is_drag_and_drop = False
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
            self.files_names_absolute_list_with_dropped_files = self.files_names_absolute_list.copy()
            self.files_size_list = get_files_size_list(files_list=self.files_names_list, folder_path=self.folder_path)
            self.files_names_checked_list = ([True] * len(self.files_names_absolute_list))
            if len(self.files_names_absolute_list) > 0:
                show_loading_dialog(self.files_names_absolute_list)
        except Exception as e:
            invalid_path_dialog = InvalidPathDialog()
            invalid_path_dialog.execute()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        current_extensions = self.video_extensions_comboBox.currentData()
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

    def show_files_list(self):
        self.table.checking_row_updates = False
        self.table.show_files_list(files_names_list=self.files_names_list,
                                   files_names_checked_list=self.files_names_checked_list,
                                   files_size_list=self.files_size_list)
        self.table.checking_row_updates = True
        self.update_other_classes_variables()

    def update_other_classes_variables(self):
        self.change_global_last_path_directory()
        self.change_global_video_list()
        self.change_global_video_source_path()
        self.update_global_video_source_mkv_only()
        self.video_source_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_source_lineEdit.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_extensions_comboBox.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_clear_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_source_lineEdit.set_current_folder_path(self.folder_path)
        self.video_source_lineEdit.set_is_drag_and_drop(self.is_drag_and_drop)
        self.video_extensions_comboBox.set_current_folder_path(self.folder_path)
        self.video_extensions_comboBox.set_current_files_list(self.files_names_list)

    def check_extension_changes(self, new_extensions):
        if new_extensions != self.current_video_extensions:
            self.current_video_extensions = new_extensions
            self.update_files_lists(self.folder_path)
            self.show_files_list()

    def clear_files(self):
        self.folder_path = ""
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_size_list = []
        self.video_source_lineEdit.setText("")
        self.is_drag_and_drop = False
        self.files_names_checked_list = []
        self.show_files_list()

    def setup_video_source_label(self):
        self.video_source_label.setText("Video Source Folder:")

    def setup_video_extensions_label(self):
        self.video_extensions_label.setText("Video Extension:")

    def setup_video_default_duration_fps_label(self):
        self.video_default_duration_fps_label.setText("Default Duration/FPS:")

    def setup_main_layout(self):
        self.main_layout.addWidget(self.video_source_label, 0, 0)
        self.main_layout.addWidget(self.video_source_lineEdit, 0, 1, 1, 80)
        self.main_layout.addWidget(self.video_clear_button, 0, 81)
        self.main_layout.addWidget(self.video_source_button, 0, 82)
        self.main_layout.addWidget(self.video_extensions_label, 1, 0)
        self.main_layout.addWidget(self.video_extensions_comboBox, 1, 1)
        self.main_layout.addWidget(self.video_default_duration_fps_label, 1, 2)
        self.main_layout.addWidget(self.video_default_duration_fps_comboBox, 1, 3)
        self.main_layout.addWidget(self.video_info_button, 1, 4, 1, -1, alignment=Qt.AlignRight)
        self.main_layout.addWidget(self.table, 2, 0, 1, -1)

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace() and not self.is_drag_and_drop:
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def change_global_video_list(self):
        GlobalSetting.VIDEO_FILES_LIST = []
        GlobalSetting.VIDEO_FILES_SIZE_LIST = []
        GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST = []
        GlobalSetting.VIDEO_SOURCE_PATHS = []
        for i in range(len(self.files_names_list)):
            if self.files_names_checked_list[i]:
                GlobalSetting.VIDEO_FILES_LIST.append(self.files_names_list[i])
                GlobalSetting.VIDEO_FILES_SIZE_LIST.append(self.files_size_list[i])
                GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST.append(self.files_names_absolute_list[i])
                if os.path.dirname(self.files_names_absolute_list[i]) not in GlobalSetting.VIDEO_SOURCE_PATHS:
                    GlobalSetting.VIDEO_SOURCE_PATHS.append(os.path.dirname(self.files_names_absolute_list[i]))

    def update_checked_video(self, video_index):
        self.files_names_checked_list[video_index] = True
        self.change_global_video_list()
        self.update_global_video_source_mkv_only()

    def update_unchecked_video(self, video_index):
        self.files_names_checked_list[video_index] = False
        self.change_global_video_list()
        self.update_global_video_source_mkv_only()

    def update_global_video_source_mkv_only(self):
        All_MKV = True
        for file_name in GlobalSetting.VIDEO_FILES_LIST:
            file_extension_start_index = file_name.rfind(".")
            file_extension = file_name[file_extension_start_index + 1:]
            if file_extension.lower() != "mkv":
                All_MKV = False
                break
        GlobalSetting.VIDEO_SOURCE_MKV_ONLY = All_MKV

    def change_global_video_source_path(self):
        GlobalSetting.VIDEO_SOURCE_PATHS = self.folders_paths

    def connect_signals(self):
        self.video_source_button.clicked_signal.connect(self.update_folder_path)
        self.video_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.video_source_lineEdit.set_is_drag_and_drop_signal.connect(self.update_is_drag_and_drop)
        self.video_clear_button.clear_files_signal.connect(self.clear_files)
        self.video_extensions_comboBox.close_list.connect(self.check_extension_changes)
        self.table.drop_folder_and_files_signal.connect(self.update_files_with_drag_and_drop)
        self.table.update_checked_video_signal.connect(self.update_checked_video)
        self.table.update_unchecked_video_signal.connect(self.update_unchecked_video)
        self.tab_clicked_signal.connect(self.tab_clicked)

    def tab_clicked(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()

    def update_files_with_drag_and_drop(self, paths_list):
        duplicate_flag = False
        not_duplicate_files_absolute_path_list = []
        not_duplicate_files_list = []
        duplicate_files_list = []
        new_files_absolute_path_list = []
        current_extensions = self.video_extensions_comboBox.currentData()
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
                        if os.path.dirname(path) not in self.folders_paths:
                            self.folders_paths.append(os.path.dirname(path))
                        break
            else:
                if os.path.dirname(path) not in self.folders_paths:
                    self.folders_paths.append(os.path.dirname(path))
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
        self.video_source_lineEdit.stop_check_path = True
        self.video_source_lineEdit.setText(self.drag_and_dropped_text)
        self.is_drag_and_drop = True
        self.folder_path = ""
        self.files_names_absolute_list_with_dropped_files.extend(not_duplicate_files_absolute_path_list)
        self.files_names_absolute_list.extend(not_duplicate_files_absolute_path_list)
        self.files_size_list.extend(get_files_size_with_absolute_path_list(not_duplicate_files_absolute_path_list))
        self.files_names_checked_list.extend([True] * len(not_duplicate_files_absolute_path_list))
        self.show_files_list()
        if len(not_duplicate_files_absolute_path_list) > 0:
            show_loading_dialog(not_duplicate_files_absolute_path_list)
        self.video_source_lineEdit.stop_check_path = False
        if duplicate_flag:
            info_message = "One or more files have the same name with the old files will be " \
                           "skipped:"
            for file_name in duplicate_files_list:
                info_message += "\n" + file_name
            warning_dialog = WarningDialog(window_title="Duplicate files names", info_message=info_message,
                                           parent=self.window())
            warning_dialog.execute_wth_no_block()

    def disable_editable_widgets(self):
        self.video_extensions_comboBox.setEnabled(False)
        self.video_source_lineEdit.setEnabled(False)
        self.video_source_button.setEnabled(False)
        self.video_clear_button.setEnabled(False)
        self.video_default_duration_fps_comboBox.setEnabled(False)
        self.table.setAcceptDrops(False)
        self.table.disable_selection()

    def enable_editable_widgets(self):
        self.video_extensions_comboBox.setEnabled(True)
        self.video_source_lineEdit.setEnabled(True)
        self.video_source_button.setEnabled(True)
        self.video_clear_button.setEnabled(True)
        self.video_default_duration_fps_comboBox.setEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.enable_selection()

    def update_is_drag_and_drop(self, new_state):
        self.is_drag_and_drop = new_state
