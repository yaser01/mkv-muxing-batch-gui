from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout, QShortcut

from packages.Tabs.AudioTab.Widgets.DeleteAudioButton import DeleteAudioButton
from packages.Tabs.AudioTab.Widgets.MoveAudioBottomButton import MoveAudioBottomButton
from packages.Tabs.AudioTab.Widgets.MoveAudioDownButton import MoveAudioDownButton
from packages.Tabs.AudioTab.Widgets.MoveAudioToButton import MoveAudioToButton
from packages.Tabs.AudioTab.Widgets.MoveAudioTopButton import MoveAudioTopButton
from packages.Tabs.AudioTab.Widgets.MoveAudioUpButton import MoveAudioUpButton
from packages.Tabs.GlobalSetting import GlobalSetting


class MatchAudioToolsLayout(QVBoxLayout):
    refresh_audio_table_signal = Signal()
    selected_audio_row_signal = Signal(int)

    def __init__(self, tab_index, parent=None):
        super().__init__()
        self.tab_index = tab_index
        self.audio_tab = parent
        self.move_audio_up_button = MoveAudioUpButton()
        self.move_audio_top_button = MoveAudioTopButton()
        self.move_audio_down_button = MoveAudioDownButton()
        self.move_audio_bottom_button = MoveAudioBottomButton()
        self.move_audio_to_button = MoveAudioToButton()
        self.delete_audio_button = DeleteAudioButton()
        self.setup_shortcuts()
        self.setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.move_audio_up_button.swap_happened_signal.connect(self.refresh_audio_table)
        self.move_audio_up_button.selected_row_after_swap.connect(self.change_selected_audio_row)
        self.move_audio_top_button.swap_happened_signal.connect(self.refresh_audio_table)
        self.move_audio_top_button.selected_row_after_swap.connect(self.change_selected_audio_row)
        self.move_audio_top_button.move_audio_to_top_signal.connect(
            self.update_global_audio_files_list_order_to_top)
        self.move_audio_up_button.move_audio_to_up_signal.connect(self.update_global_audio_files_list_order_to_up)
        self.move_audio_to_button.move_audio_to_position_signal.connect(
            self.update_global_audio_files_list_order_to_position)
        self.move_audio_down_button.move_audio_to_down_signal.connect(
            self.update_global_audio_files_list_order_to_down)
        self.move_audio_bottom_button.move_audio_to_bottom_signal.connect(
            self.update_global_audio_files_list_order_to_bottom)
        self.move_audio_down_button.swap_happened_signal.connect(self.refresh_audio_table)
        self.move_audio_down_button.selected_row_after_swap.connect(self.change_selected_audio_row)
        self.move_audio_bottom_button.swap_happened_signal.connect(self.refresh_audio_table)
        self.move_audio_bottom_button.selected_row_after_swap.connect(self.change_selected_audio_row)
        self.move_audio_to_button.swap_happened_signal.connect(self.refresh_audio_table)
        self.move_audio_to_button.selected_row_after_swap.connect(self.change_selected_audio_row)
        self.delete_audio_button.delete_happened_signal.connect(
            self.update_global_audio_files_list_order_deleting)
        self.delete_audio_button.selected_row_after_delete.connect(self.change_selected_audio_row)

    def setup_layout(self):
        self.addStretch()
        self.addWidget(self.move_audio_up_button)
        self.addSpacing(10)
        self.addWidget(self.move_audio_top_button)
        self.addSpacing(10)
        self.addWidget(self.move_audio_to_button)
        self.addSpacing(10)
        self.addWidget(self.move_audio_bottom_button)
        self.addSpacing(10)
        self.addWidget(self.move_audio_down_button)
        self.addSpacing(10)
        self.addWidget(self.delete_audio_button)
        self.addStretch()

    def set_selected_row(self, selected_row, max_index):
        self.move_audio_up_button.current_index = selected_row
        self.move_audio_up_button.max_index = max_index
        self.move_audio_top_button.current_index = selected_row
        self.move_audio_top_button.max_index = max_index
        self.move_audio_down_button.current_index = selected_row
        self.move_audio_down_button.max_index = max_index
        self.move_audio_bottom_button.current_index = selected_row
        self.move_audio_bottom_button.max_index = max_index
        self.move_audio_to_button.current_index = selected_row
        self.move_audio_to_button.max_index = max_index
        self.delete_audio_button.current_index = selected_row
        self.delete_audio_button.max_index = max_index

    # noinspection PyAttributeOutsideInit
    def setup_shortcuts(self):
        self.move_audio_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self.audio_tab)
        self.move_audio_up_shortcut.activated.connect(self.move_audio_up_button.clicked_button)

        self.move_audio_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self.audio_tab)
        self.move_audio_down_shortcut.activated.connect(self.move_audio_down_button.clicked_button)

        self.move_audio_top_shortcut = QShortcut(QKeySequence("Ctrl+PgUp"), self.audio_tab)
        self.move_audio_top_shortcut.activated.connect(self.move_audio_top_button.clicked_button)

        self.move_audio_bottom_shortcut = QShortcut(QKeySequence("Ctrl+PgDown"), self.audio_tab)
        self.move_audio_bottom_shortcut.activated.connect(self.move_audio_bottom_button.clicked_button)

        self.move_audio_to_shortcut = QShortcut(QKeySequence("Ctrl+M"), self.audio_tab)
        self.move_audio_to_shortcut.activated.connect(self.move_audio_to_button.clicked_button)

        self.delete_audio_shortcut = QShortcut(QKeySequence("Delete"), self.audio_tab)
        self.delete_audio_shortcut.activated.connect(self.delete_audio_button.clicked_button)

    def refresh_audio_table(self):
        self.refresh_audio_table_signal.emit()

    def change_selected_audio_row(self, new_selected_index):
        new_selected_index = min(new_selected_index, len(GlobalSetting.AUDIO_FILES_LIST[self.tab_index]) - 1)
        self.selected_audio_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_audio_up_button.setEnabled(False)
        self.move_audio_top_button.setEnabled(False)
        self.move_audio_down_button.setEnabled(False)
        self.move_audio_bottom_button.setEnabled(False)
        self.move_audio_to_button.setEnabled(False)
        self.delete_audio_button.setEnabled(False)

        self.move_audio_up_shortcut.setEnabled(False)
        self.move_audio_top_shortcut.setEnabled(False)
        self.move_audio_down_shortcut.setEnabled(False)
        self.move_audio_bottom_shortcut.setEnabled(False)
        self.move_audio_to_shortcut.setEnabled(False)
        self.delete_audio_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_audio_up_button.setEnabled(True)
        self.move_audio_top_button.setEnabled(True)
        self.move_audio_down_button.setEnabled(True)
        self.move_audio_bottom_button.setEnabled(True)
        self.move_audio_to_button.setEnabled(True)
        self.delete_audio_button.setEnabled(True)

        self.move_audio_up_shortcut.setEnabled(True)
        self.move_audio_top_shortcut.setEnabled(True)
        self.move_audio_down_shortcut.setEnabled(True)
        self.move_audio_bottom_shortcut.setEnabled(True)
        self.move_audio_to_shortcut.setEnabled(True)
        self.delete_audio_shortcut.setEnabled(True)

    def update_global_audio_files_list_order_to_top(self, index_to_move):
        temp_for_swap = GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index][0]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][0] = temp_for_swap

        temp_for_swap = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][0]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][0] = temp_for_swap

    def update_global_audio_files_list_order_to_up(self, index_to_move):
        temp_for_swap = GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move - 1]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move - 1] = temp_for_swap

        temp_for_swap = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                index_to_move - 1]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move - 1] = temp_for_swap

    def update_global_audio_files_list_order_to_position(self, list_of_old_and_new_index):
        old_index = list_of_old_and_new_index[0]
        new_index = list_of_old_and_new_index[1]
        temp_for_swap = GlobalSetting.AUDIO_FILES_LIST[self.tab_index][old_index]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][old_index] = \
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index][new_index]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][new_index] = temp_for_swap

        temp_for_swap = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][old_index]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][old_index] = \
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][new_index]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][new_index] = temp_for_swap

    def update_global_audio_files_list_order_to_down(self, index_to_move):
        temp_for_swap = GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move + 1]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move + 1] = temp_for_swap

        temp_for_swap = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                index_to_move + 1]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move + 1] = temp_for_swap

    def update_global_audio_files_list_order_to_bottom(self, index_to_move):
        index_last_file = len(GlobalSetting.AUDIO_FILES_LIST[self.tab_index]) - 1
        temp_for_swap = GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_last_file]
        GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_last_file] = temp_for_swap

        temp_for_swap = GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                index_last_file]
        GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_last_file] = temp_for_swap

    def update_global_audio_files_list_order_deleting(self, index_to_delete):
        del GlobalSetting.AUDIO_FILES_LIST[self.tab_index][index_to_delete]
        del GlobalSetting.AUDIO_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_delete]
        self.refresh_audio_table()
