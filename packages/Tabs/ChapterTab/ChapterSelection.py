from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
)

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Tabs.ChapterTab.Widgets.ChapterExtensionsCheckableComboBox import ChapterExtensionsCheckableComboBox
from packages.Tabs.ChapterTab.Widgets.ChapterSourceButton import ChapterSourceButton
from packages.Tabs.ChapterTab.Widgets.ChapterClearButton import ChapterClearButton
from packages.Tabs.ChapterTab.Widgets.ChapterSourceLineEdit import ChapterSourceLineEdit
from packages.Tabs.ChapterTab.Widgets.MatchChapterLayout import MatchChapterLayout
from packages.Tabs.GlobalSetting import *
from packages.Widgets.InvalidPathDialog import *
from packages.Widgets.YesNoDialog import *
from packages.Widgets.WarningDialog import WarningDialog


# noinspection PyAttributeOutsideInit
class ChapterSelectionSetting(GlobalSetting):
    tab_clicked_signal = Signal()
    activation_signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.create_properties()
        self.create_widgets()
        self.setup_widgets()
        self.connect_signals()

    def create_widgets(self):
        self.chapter_source_label = QLabel("Chapter Source Folder:")
        self.chapter_extension_label = QLabel("Chapter Extension:")
        self.chapter_source_lineEdit = ChapterSourceLineEdit()
        self.chapter_source_button = ChapterSourceButton()
        self.chapter_clear_button = ChapterClearButton()
        self.chapter_extensions_comboBox = ChapterExtensionsCheckableComboBox()
        self.chapter_match_layout = MatchChapterLayout(parent=self)
        self.chapter_options_layout = QHBoxLayout()
        self.MainLayout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.chapter_main_groupBox = QGroupBox()
        self.chapter_match_groupBox = QGroupBox("Chapter Matching")
        self.chapter_match_groupBox.setLayout(self.chapter_match_layout)

    def setup_widgets(self):
        self.setup_chapter_main_groupBox()
        self.setup_layouts()

    # noinspection PyUnresolvedReferences
    def connect_signals(self):
        self.chapter_main_groupBox.toggled.connect(self.activate_tab)
        self.chapter_source_button.clicked_signal.connect(self.update_folder_path)
        self.chapter_source_lineEdit.edit_finished_signal.connect(self.update_folder_path)
        self.chapter_source_lineEdit.set_is_drag_and_drop_signal.connect(self.update_is_drag_and_drop)
        self.chapter_extensions_comboBox.close_list.connect(self.check_extension_changes)
        self.chapter_match_layout.sync_chapter_files_with_global_files_after_swap_signal.connect(
            self.sync_chapter_files_with_global_files)
        self.tab_clicked_signal.connect(self.tab_clicked)
        self.chapter_match_layout.chapter_table.drop_folder_and_files_signal.connect(
            self.update_files_with_drag_and_drop)
        self.chapter_clear_button.clear_files_signal.connect(self.clear_files)

    def create_properties(self):
        self.folder_path = ""
        self.drag_and_dropped_text = "[Drag & Drop Files]"
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_names_absolute_list_with_dropped_files = []
        self.current_chapter_extensions = DefaultOptions.Default_Chapter_Extensions
        self.is_drag_and_drop = False

    def setup_layouts(self):
        self.setup_chapter_options_layout()
        self.setup_main_layout()
        self.setLayout(self.MainLayout)
        self.MainLayout.addWidget(self.chapter_main_groupBox)

    def setup_chapter_options_layout(self):
        self.chapter_options_layout.addWidget(self.chapter_extensions_comboBox)
        self.chapter_options_layout.addStretch()

    def setup_main_layout(self):
        self.main_layout.addWidget(self.chapter_source_label, 0, 0)
        self.main_layout.addWidget(self.chapter_source_lineEdit, 0, 1, 1, 1)
        self.main_layout.addWidget(self.chapter_clear_button, 0, 2, 1, 1)
        self.main_layout.addWidget(self.chapter_source_button, 0, 3)
        self.main_layout.addWidget(self.chapter_extension_label, 1, 0)
        self.main_layout.addLayout(self.chapter_options_layout, 1, 1, 1, 3)
        self.main_layout.addWidget(self.chapter_match_groupBox, 2, 0, 1, -1)

    def setup_chapter_main_groupBox(self):
        self.chapter_main_groupBox.setParent(self)
        self.chapter_main_groupBox.setLayout(self.main_layout)
        self.chapter_main_groupBox.setTitle("Chapters")
        self.chapter_main_groupBox.setCheckable(True)
        self.chapter_main_groupBox.setChecked(True)

    def update_folder_path(self, new_path: str):
        if new_path != "":
            self.chapter_source_lineEdit.set_text_safe_change(new_path)
            self.update_files_lists(new_path)
            self.show_chapter_files_list()
        else:
            if self.is_drag_and_drop:
                self.chapter_source_lineEdit.set_text_safe_change(self.drag_and_dropped_text)

    def update_files_lists(self, folder_path):
        if folder_path == "" or folder_path.isspace():
            self.folder_path = ""
            if self.is_drag_and_drop:
                new_files_absolute_path_list = []
                self.files_names_list = []
                current_extensions = self.chapter_extensions_comboBox.currentData()
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
                self.chapter_source_lineEdit.stop_check_path = True
                self.chapter_source_lineEdit.setText(self.drag_and_dropped_text)
                self.is_drag_and_drop = True
                self.folder_path = ""
                self.files_names_absolute_list = new_files_absolute_path_list.copy()
                self.files_names_absolute_list_with_dropped_files = new_files_absolute_path_list.copy()
                self.chapter_source_lineEdit.stop_check_path = False
            else:
                self.chapter_source_lineEdit.set_text_safe_change("")
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
        if self.current_chapter_extensions != new_extensions:
            self.current_chapter_extensions = new_extensions
            self.update_files_lists(self.folder_path)
            self.show_chapter_files_list()

    def get_files_list(self, folder_path):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, folder_path)
        current_extensions = self.chapter_extensions_comboBox.currentData()
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

    def show_chapter_files_list(self):
        self.update_other_classes_variables()
        self.chapter_match_layout.show_chapter_files()

    def update_other_classes_variables(self):
        #self.change_global_last_path_directory()
        self.change_global_chapter_list()
        self.chapter_source_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.chapter_source_lineEdit.set_is_there_old_file(len(self.files_names_list) > 0)
        self.chapter_extensions_comboBox.set_is_there_old_file(len(self.files_names_list) > 0)
        self.chapter_clear_button.set_is_there_old_file(len(self.files_names_list) > 0)
        self.chapter_source_lineEdit.set_current_folder_path(self.folder_path)
        self.chapter_source_lineEdit.set_is_drag_and_drop(self.is_drag_and_drop)
        self.chapter_extensions_comboBox.set_current_folder_path(self.folder_path)
        self.chapter_extensions_comboBox.set_current_files_list(self.files_names_list)

    def clear_files(self):
        self.folder_path = ""
        self.files_names_list = []
        self.files_names_absolute_list = []
        self.files_names_absolute_list_with_dropped_files = []
        self.chapter_source_lineEdit.set_text_safe_change("")
        self.is_drag_and_drop = False
        self.show_chapter_files_list()

    def change_global_chapter_list(self):
        GlobalSetting.CHAPTER_FILES_LIST = self.files_names_list
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST = self.files_names_absolute_list

    def show_video_files_list(self):
        if self.chapter_main_groupBox.isChecked():
            self.chapter_match_layout.show_video_files()

    def activate_tab(self, on):
        if on:
            self.show_video_files_list()
        else:
            self.chapter_source_lineEdit.set_text_safe_change("")
            self.chapter_match_layout.clear_tables()
            self.folder_path = ""
            self.files_names_list = []
            self.files_names_absolute_list = []
            self.current_chapter_extensions = DefaultOptions.Default_Chapter_Extensions
            self.chapter_extensions_comboBox.setData(self.current_chapter_extensions)
            self.is_drag_and_drop = False
            self.chapter_source_lineEdit.set_is_drag_and_drop(False)
            GlobalSetting.CHAPTER_FILES_LIST = []
            GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST = []
            GlobalSetting.CHAPTER_TRACK_NAME = ""
            GlobalSetting.CHAPTER_DELAY = 0.0
            GlobalSetting.CHAPTER_SET_DEFAULT = False
            GlobalSetting.CHAPTER_SET_FORCED = False
            GlobalSetting.CHAPTER_LANGUAGE = ""
        self.activation_signal.emit(on)
        GlobalSetting.CHAPTER_ENABLED = on

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == Qt.RightButton:
            self.chapter_match_layout.clear_chapter_selection()
        if (QMouseEvent.buttons() == Qt.RightButton or QMouseEvent.buttons() == Qt.LeftButton) and (
                self.chapter_source_lineEdit.text() == ""):
            self.chapter_source_lineEdit.set_text_safe_change(self.folder_path)
        return QWidget.mousePressEvent(self, QMouseEvent)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        if self.chapter_main_groupBox.isChecked():
            self.show_video_files_list()

    def change_global_last_path_directory(self):
        if self.folder_path != "" and not self.folder_path.isspace() and not self.is_drag_and_drop:
            GlobalSetting.LAST_DIRECTORY_PATH = self.folder_path

    def tab_clicked(self):
        if self.chapter_main_groupBox.isChecked():
            self.show_chapter_files_list()
            self.show_video_files_list()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.disable_editable_widgets()
        else:
            self.enable_editable_widgets()

    def disable_editable_widgets(self):
        self.chapter_source_lineEdit.setEnabled(False)
        self.chapter_source_button.setEnabled(False)
        self.chapter_extensions_comboBox.setEnabled(False)
        self.chapter_clear_button.setEnabled(False)
        self.chapter_main_groupBox.setCheckable(False)
        self.chapter_match_layout.disable_editable_widgets()

    def enable_editable_widgets(self):
        self.chapter_source_lineEdit.setEnabled(True)
        self.chapter_source_button.setEnabled(True)
        self.chapter_extensions_comboBox.setEnabled(True)
        self.chapter_clear_button.setEnabled(True)
        if GlobalSetting.CHAPTER_ENABLED:
            self.chapter_main_groupBox.setCheckable(True)
        else:
            self.chapter_main_groupBox.setCheckable(True)
            GlobalSetting.CHAPTER_ENABLED = False
            self.chapter_main_groupBox.setChecked(GlobalSetting.CHAPTER_ENABLED)
        self.chapter_match_layout.enable_editable_widgets()

    def sync_chapter_files_with_global_files(self):
        self.files_names_list = GlobalSetting.CHAPTER_FILES_LIST
        self.files_names_absolute_list = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST
        self.update_other_classes_variables()

    def update_files_with_drag_and_drop(self, paths_list):
        duplicate_flag = False
        not_duplicate_files_absolute_path_list = []
        not_duplicate_files_list = []
        duplicate_files_list = []
        new_files_absolute_path_list = []
        current_extensions = self.chapter_extensions_comboBox.currentData()
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
        self.chapter_source_lineEdit.stop_check_path = True
        self.chapter_source_lineEdit.setText(self.drag_and_dropped_text)
        self.is_drag_and_drop = True
        self.folder_path = ""
        self.files_names_absolute_list_with_dropped_files.extend(not_duplicate_files_absolute_path_list)
        self.files_names_absolute_list.extend(not_duplicate_files_absolute_path_list)
        self.show_chapter_files_list()
        self.chapter_source_lineEdit.stop_check_path = False
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
        self.chapter_source_lineEdit.set_text_safe_change(DefaultOptions.Default_Chapter_Directory)
        self.chapter_source_lineEdit.check_new_path()
