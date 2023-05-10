from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout

from packages.Tabs.AudioTab.AudioSelection import AudioSelectionSetting
from packages.Tabs.AudioTab.Widgets.AudioTabComboBox import AudioTabComboBox
from packages.Tabs.AudioTab.Widgets.AudioTabDeleteButton import AudioTabDeleteButton
from packages.Tabs.GlobalSetting import GlobalSetting


class AudioTabManager(GlobalSetting):
    activation_signal = Signal(bool)
    tab_clicked_signal = Signal()

    def __init__(self):
        super().__init__()
        self.audio_tabs = []
        self.audio_tabs_indices = []
        self.current_index_counter = 0
        self.current_tab_index = 0
        self.audio_tab_comboBox = AudioTabComboBox()
        self.audio_tab_delete_button = AudioTabDeleteButton()
        self.MainLayout = QVBoxLayout()
        self.audio_tab_setting_layout = QHBoxLayout()
        self.setLayout(self.MainLayout)
        self.audio_tabs.append(AudioSelectionSetting(self.current_index_counter))
        self.audio_tabs_indices.append(self.current_index_counter)
        self.current_index_counter += 1
        self.current_audio_tab = self.audio_tabs[-1]
        self.current_audio_tab.is_there_old_files_signal.connect(self.update_is_there_old_files)
        self.current_audio_tab.is_there_old_files_signal.connect(self.update_is_audio_enabled)
        self.audio_tab_setting_layout.addWidget(self.audio_tab_comboBox)
        self.audio_tab_setting_layout.addWidget(self.audio_tab_delete_button)
        self.audio_tab_setting_layout.addStretch(1)
        self.MainLayout.addLayout(self.audio_tab_setting_layout)
        self.MainLayout.addWidget(self.current_audio_tab)
        self.audio_tab_delete_button.hide()
        self.activation_signal.emit(True)
        self.connect_signals()

    def connect_signals(self):
        self.audio_tab_comboBox.current_tab_changed_signal.connect(self.change_current_tab)
        self.audio_tab_comboBox.create_new_tab_signal.connect(self.create_new_tab)
        self.audio_tab_delete_button.remove_tab_signal.connect(self.delete_current_tab)
        self.tab_clicked_signal.connect(self.tab_clicked)

    def change_current_tab(self, tab_index):
        real_index = self.audio_tabs_indices[tab_index]
        self.MainLayout.replaceWidget(self.current_audio_tab, self.audio_tabs[tab_index])
        self.current_audio_tab.hide()
        self.audio_tabs[tab_index].show()
        self.current_audio_tab = self.audio_tabs[tab_index]
        self.current_tab_index = real_index
        if real_index == 0:
            self.audio_tab_delete_button.hide()
        else:
            self.audio_tab_delete_button.show()
        self.audio_tab_delete_button.set_is_there_old_file(len(GlobalSetting.AUDIO_FILES_LIST[real_index]) > 0)
        self.current_audio_tab.tab_clicked_signal.emit()

    def create_new_tab(self):
        self.audio_tabs.append(AudioSelectionSetting(self.current_index_counter))
        self.audio_tabs_indices.append(self.current_index_counter)
        self.current_tab_index = self.current_index_counter
        self.current_index_counter += 1
        self.MainLayout.replaceWidget(self.current_audio_tab, self.audio_tabs[-1])
        self.current_audio_tab.hide()
        self.audio_tabs[-1].show()
        self.current_audio_tab = self.audio_tabs[-1]
        self.current_audio_tab.is_there_old_files_signal.connect(self.update_is_there_old_files)
        self.current_audio_tab.is_there_old_files_signal.connect(self.update_is_audio_enabled)
        self.audio_tab_delete_button.show()
        self.current_audio_tab.tab_clicked_signal.emit()

    def delete_current_tab(self):
        index_to_delete = self.current_tab_index
        index_in_list = self.audio_tabs_indices.index(self.current_tab_index)
        previous_tab_index = index_in_list - 1
        self.MainLayout.replaceWidget(self.audio_tabs[index_in_list], self.audio_tabs[previous_tab_index])
        self.audio_tab_comboBox.delete_tab(index_in_list)
        self.audio_tabs[index_in_list].hide()
        self.audio_tabs[index_in_list].deleteLater()
        self.audio_tabs.remove(self.audio_tabs[index_in_list])
        self.current_audio_tab = self.audio_tabs[previous_tab_index]
        self.current_audio_tab.show()
        self.audio_tabs_indices.remove(index_to_delete)
        GlobalSetting.AUDIO_FILES_LIST.pop(index_to_delete, None)
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST.pop(index_to_delete, None)
        GlobalSetting.AUDIO_DELAY.pop(index_to_delete, None)
        GlobalSetting.AUDIO_TRACK_NAME.pop(index_to_delete, None)
        GlobalSetting.AUDIO_SET_DEFAULT.pop(index_to_delete, None)
        GlobalSetting.AUDIO_SET_FORCED.pop(index_to_delete, None)
        GlobalSetting.AUDIO_SET_AT_TOP.pop(index_to_delete, None)
        GlobalSetting.AUDIO_TAB_ENABLED.pop(index_to_delete, None)
        GlobalSetting.AUDIO_LANGUAGE.pop(index_to_delete, None)
        self.current_tab_index = self.audio_tabs_indices[previous_tab_index]

    def update_is_there_old_files(self, new_state):
        self.audio_tab_delete_button.set_is_there_old_file(new_state)

    def update_is_audio_enabled(self):
        for state in GlobalSetting.AUDIO_TAB_ENABLED.values():
            if state:
                self.activation_signal.emit(True)
                GlobalSetting.AUDIO_ENABLED = True
                return
        GlobalSetting.AUDIO_ENABLED = False
        self.activation_signal.emit(False)

    def tab_clicked(self):
        self.current_audio_tab.tab_clicked_signal.emit()
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            self.audio_tab_delete_button.setEnabled(False)
            self.audio_tab_comboBox.hide_new_tab_option()
        else:
            self.audio_tab_delete_button.setEnabled(True)
            self.audio_tab_comboBox.show_new_tab_option()

    def set_default_directory(self):
        for audio_tab in self.audio_tabs:
            audio_tab.set_default_directory()
    def update_theme_mode_state(self):
        self.audio_tab_comboBox.update_theme_mode_state()
        for audio_tab in self.audio_tabs:
            audio_tab.update_theme_mode_state()