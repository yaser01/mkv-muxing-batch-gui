from PySide2.QtCore import Signal

from packages.Startup.DefaultOptions import Default_Video_Extension
from packages.Tabs.GlobalSetting import *
from packages.Tabs.GlobalSetting import sort_names_like_windows, get_readable_filesize, get_files_names_absolute_list, \
    get_file_name_absolute_path
from packages.Tabs.VideoTab.Widgets.VideoExtensionsCheckableComboBox import VideoExtensionsCheckableComboBox
from packages.Tabs.VideoTab.Widgets.VideoSourceButton import VideoSourceButton
from packages.Tabs.VideoTab.Widgets.VideoSourceLineEdit import VideoSourceLineEdit
from packages.Tabs.VideoTab.Widgets.VideoTable import VideoTable
from packages.Widgets.InvalidPathDialog import *


# noinspection PyAttributeOutsideInit
def get_files_size_list(files_list, folder_path):
    files_size_list = []
    for i in range(len(files_list)):
        file_name_absolute = get_file_name_absolute_path(file_name=files_list[i], folder_path=folder_path)
        file_size_bytes = os.path.getsize(file_name_absolute)
        files_size_list.append(get_readable_filesize(size_bytes=file_size_bytes))
    return files_size_list


class VideoSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()

    def __init__(self):
        super().__init__()
        self.video_source_label = QLabel()
        self.video_source_lineEdit = VideoSourceLineEdit()
        self.video_source_button = VideoSourceButton()
        self.video_extensions_label = QLabel()
        self.video_extensions_comboBox = VideoExtensionsCheckableComboBox()
        self.table = VideoTable()
        self.main_layout = QGridLayout()
        self.folder_path = ""
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_size_list = []
        self.current_video_extensions = [Default_Video_Extension]
        self.setup_widgets()
        self.connect_signals()

    def setup_widgets(self):
        self.setup_video_source_label()
        self.setup_video_extensions_label()
        self.setup_layouts()

    def setup_layouts(self):
        self.setup_main_layout()
        self.setLayout(self.main_layout)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.video_source_lineEdit.setText(new_path)
            self.update_files_lists(new_path)
            self.show_files_list()

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            self.video_source_lineEdit.setText("")
            return
        try:
            self.folder_path = folder_path
            self.files_names_list = self.get_files_list(self.folder_path)
            self.files_names_absolute_list = get_files_names_absolute_list(self.files_names_list, self.folder_path)
            self.files_size_list = get_files_size_list(files_list=self.files_names_list, folder_path=self.folder_path)
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
        self.table.show_files_list(files_names_list=self.files_names_list, files_size_list=self.files_size_list)
        self.update_other_classes_variables()

    def update_other_classes_variables(self):
        self.change_global_last_path_directory()
        self.change_global_video_list()
        self.change_global_video_source_path()
        self.update_global_video_source_mkv_only()
        self.video_source_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_source_lineEdit.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_extensions_comboBox.set_is_there_old_file(len(self.files_names_list) > 0)
        self.video_source_lineEdit.set_current_folder_path(self.folder_path)
        self.video_extensions_comboBox.set_current_folder_path(self.folder_path)
        self.video_extensions_comboBox.set_current_files_list(self.files_names_list)

    def check_extension_changes(self, new_extensions):
        if new_extensions != self.current_video_extensions:
            self.current_video_extensions = new_extensions
            self.update_files_lists(self.folder_path)
            self.show_files_list()

    def setup_video_source_label(self):
        self.video_source_label.setText("Video Source Folder:")

    def setup_video_extensions_label(self):
        self.video_extensions_label.setText("Video Extension:")

    def setup_main_layout(self):
        self.main_layout.addWidget(self.video_source_label, 0, 0)
        self.main_layout.addWidget(self.video_source_lineEdit, 0, 1)
        self.main_layout.addWidget(self.video_source_button, 0, 2)
        self.main_layout.addWidget(self.video_extensions_label, 1, 0)
        self.main_layout.addWidget(self.video_extensions_comboBox, 1, 1)
        self.main_layout.addWidget(self.table, 2, 0, 1, -1)

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace():
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def change_global_video_list(self):
        GlobalSetting.VIDEO_FILES_LIST = self.files_names_list
        GlobalSetting.VIDEO_FILES_SIZE_LIST = self.files_size_list
        GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST = self.files_names_absolute_list

    def update_global_video_source_mkv_only(self):
        All_MKV = True
        for file_name in self.files_names_list:
            file_extension_start_index = file_name.rfind(".")
            file_extension = file_name[file_extension_start_index + 1:]
            if file_extension.lower() != "mkv":
                All_MKV = False
                break
        GlobalSetting.VIDEO_SOURCE_MKV_ONLY = All_MKV

    def change_global_video_source_path(self):
        GlobalSetting.VIDEO_SOURCE_PATH = Path(self.folder_path)

    def connect_signals(self):
        self.video_source_button.clicked_signal.connect(self.update_folder_path)
        self.video_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.video_extensions_comboBox.close_list.connect(self.check_extension_changes)
        self.table.drop_folder_signal.connect(self.update_folder_path)
        self.tab_clicked_signal.connect(self.tab_clicked)

    def tab_clicked(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()

    def disable_editable_widgets(self):
        self.video_extensions_comboBox.setEnabled(False)
        self.video_source_lineEdit.setEnabled(False)
        self.video_source_button.setEnabled(False)

    def enable_editable_widgets(self):
        self.video_extensions_comboBox.setEnabled(True)
        self.video_source_lineEdit.setEnabled(True)
        self.video_source_button.setEnabled(True)
