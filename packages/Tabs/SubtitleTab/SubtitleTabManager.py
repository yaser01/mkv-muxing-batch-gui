from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.SubtitleSelection import SubtitleSelectionSetting
from packages.Tabs.SubtitleTab.Widgets.SubtitleTabComboBox import SubtitleTabComboBox
from packages.Tabs.SubtitleTab.Widgets.SubtitleTabDeleteButton import SubtitleTabDeleteButton


class SubtitleTabManager(GlobalSetting):
    activation_signal = Signal(bool)
    tab_clicked_signal = Signal()

    def __init__(self):
        super().__init__()
        self.subtitle_tabs = []
        self.subtitle_tabs_indices = []
        self.current_index_counter = 0
        self.current_tab_index = 0
        self.subtitle_tab_comboBox = SubtitleTabComboBox()
        self.subtitle_tab_delete_button = SubtitleTabDeleteButton()
        self.MainLayout = QVBoxLayout()
        self.subtitle_tab_setting_layout = QHBoxLayout()
        self.setLayout(self.MainLayout)
        self.subtitle_tabs.append(SubtitleSelectionSetting(self.current_index_counter))
        self.subtitle_tabs_indices.append(self.current_index_counter)
        self.current_index_counter += 1
        self.current_subtitle_tab = self.subtitle_tabs[-1]
        self.current_subtitle_tab.is_there_old_files_signal.connect(self.update_is_there_old_files)
        self.current_subtitle_tab.is_there_old_files_signal.connect(self.update_is_subtitle_enabled)
        self.subtitle_tab_setting_layout.addWidget(self.subtitle_tab_comboBox)
        self.subtitle_tab_setting_layout.addWidget(self.subtitle_tab_delete_button)
        self.subtitle_tab_setting_layout.addStretch(1)
        self.MainLayout.addLayout(self.subtitle_tab_setting_layout)
        self.MainLayout.addWidget(self.current_subtitle_tab)
        self.subtitle_tab_delete_button.hide()
        self.activation_signal.emit(True)
        self.connect_signals()

    def connect_signals(self):
        self.subtitle_tab_comboBox.current_tab_changed_signal.connect(self.change_current_tab)
        self.subtitle_tab_comboBox.create_new_tab_signal.connect(self.create_new_tab)
        self.subtitle_tab_delete_button.remove_tab_signal.connect(self.delete_current_tab)
        self.tab_clicked_signal.connect(self.tab_clicked)

    def change_current_tab(self, tab_index):
        real_index = self.subtitle_tabs_indices[tab_index]
        self.MainLayout.replaceWidget(self.current_subtitle_tab, self.subtitle_tabs[tab_index])
        self.current_subtitle_tab.hide()
        self.subtitle_tabs[tab_index].show()
        self.current_subtitle_tab = self.subtitle_tabs[tab_index]
        self.current_tab_index = real_index
        if real_index == 0:
            self.subtitle_tab_delete_button.hide()
        else:
            self.subtitle_tab_delete_button.show()
        self.subtitle_tab_delete_button.set_is_there_old_file(len(GlobalSetting.SUBTITLE_FILES_LIST[real_index]) > 0)
        self.current_subtitle_tab.tab_clicked_signal.emit()

    def create_new_tab(self):
        self.subtitle_tabs.append(SubtitleSelectionSetting(self.current_index_counter))
        self.subtitle_tabs_indices.append(self.current_index_counter)
        self.current_tab_index = self.current_index_counter
        self.current_index_counter += 1
        self.MainLayout.replaceWidget(self.current_subtitle_tab, self.subtitle_tabs[-1])
        self.current_subtitle_tab.hide()
        self.subtitle_tabs[-1].show()
        self.current_subtitle_tab = self.subtitle_tabs[-1]
        self.current_subtitle_tab.is_there_old_files_signal.connect(self.update_is_there_old_files)
        self.current_subtitle_tab.is_there_old_files_signal.connect(self.update_is_subtitle_enabled)
        self.subtitle_tab_delete_button.show()
        self.current_subtitle_tab.tab_clicked_signal.emit()

    def delete_current_tab(self):
        index_to_delete = self.current_tab_index
        index_in_list = self.subtitle_tabs_indices.index(self.current_tab_index)
        previous_tab_index = index_in_list - 1
        self.MainLayout.replaceWidget(self.subtitle_tabs[index_in_list], self.subtitle_tabs[previous_tab_index])
        self.subtitle_tab_comboBox.delete_tab(index_in_list)
        self.subtitle_tabs[index_in_list].hide()
        self.subtitle_tabs[index_in_list].deleteLater()
        self.subtitle_tabs.remove(self.subtitle_tabs[index_in_list])
        self.current_subtitle_tab = self.subtitle_tabs[previous_tab_index]
        self.current_subtitle_tab.show()
        self.subtitle_tabs_indices.remove(index_to_delete)
        GlobalSetting.SUBTITLE_FILES_LIST.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_DELAY.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_TRACK_NAME.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_SET_DEFAULT.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_SET_FORCED.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_SET_AT_TOP.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_TAB_ENABLED.pop(index_to_delete, None)
        GlobalSetting.SUBTITLE_LANGUAGE.pop(index_to_delete, None)
        self.current_tab_index = self.subtitle_tabs_indices[previous_tab_index]

    def update_is_there_old_files(self, new_state):
        self.subtitle_tab_delete_button.set_is_there_old_file(new_state)

    def update_is_subtitle_enabled(self):
        for state in GlobalSetting.SUBTITLE_TAB_ENABLED.values():
            if state:
                self.activation_signal.emit(True)
                GlobalSetting.SUBTITLE_ENABLED = True
                return
        GlobalSetting.SUBTITLE_ENABLED = False
        self.activation_signal.emit(False)

    def tab_clicked(self):
        self.current_subtitle_tab.tab_clicked_signal.emit()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.subtitle_tab_delete_button.setEnabled(False)
            self.subtitle_tab_comboBox.hide_new_tab_option()
        else:
            self.subtitle_tab_delete_button.setEnabled(True)
            self.subtitle_tab_comboBox.show_new_tab_option()

    def set_default_directory(self):
        for subtitle_tab in self.subtitle_tabs:
            subtitle_tab.set_default_directory()

    def update_theme_mode_state(self):
        self.subtitle_tab_comboBox.update_theme_mode_state()
        for subtitle_tab in self.subtitle_tabs:
            subtitle_tab.update_theme_mode_state()
