from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout, QShortcut

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.Widgets.DeleteSubtitleButton import DeleteSubtitleButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleBottomButton import MoveSubtitleBottomButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleDownButton import MoveSubtitleDownButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleToButton import MoveSubtitleToButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleTopButton import MoveSubtitleTopButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleUpButton import MoveSubtitleUpButton


class MatchSubtitleToolsLayout(QVBoxLayout):
    refresh_subtitle_table_signal = Signal()
    selected_subtitle_row_signal = Signal(int)

    def __init__(self, tab_index, parent=None):
        super().__init__()
        self.tab_index = tab_index
        self.max_subtitle_index = -1
        self.subtitle_tab = parent
        self.move_subtitle_up_button = MoveSubtitleUpButton()
        self.move_subtitle_top_button = MoveSubtitleTopButton()
        self.move_subtitle_down_button = MoveSubtitleDownButton()
        self.move_subtitle_bottom_button = MoveSubtitleBottomButton()
        self.move_subtitle_to_button = MoveSubtitleToButton()
        self.delete_subtitle_button = DeleteSubtitleButton()
        self.setup_shortcuts()
        self.setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.move_subtitle_up_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_up_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_top_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_top_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_top_button.move_subtitle_to_top_signal.connect(
            self.update_global_subtitle_files_list_order_to_top)
        self.move_subtitle_up_button.move_subtitle_to_up_signal.connect(
            self.update_global_subtitle_files_list_order_to_up)
        self.move_subtitle_to_button.move_subtitle_to_position_signal.connect(
            self.update_global_subtitle_files_list_order_to_position)
        self.move_subtitle_down_button.move_subtitle_to_down_signal.connect(
            self.update_global_subtitle_files_list_order_to_down)
        self.move_subtitle_bottom_button.move_subtitle_to_bottom_signal.connect(
            self.update_global_subtitle_files_list_order_to_bottom)
        self.move_subtitle_down_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_down_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_bottom_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_bottom_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_to_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_to_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.delete_subtitle_button.delete_happened_signal.connect(
            self.update_global_subtitle_files_list_order_deleting)
        self.delete_subtitle_button.selected_row_after_delete.connect(self.change_selected_subtitle_row)

    def setup_layout(self):
        self.addStretch()
        self.addWidget(self.move_subtitle_up_button)
        self.addSpacing(10)
        self.addWidget(self.move_subtitle_top_button)
        self.addSpacing(10)
        self.addWidget(self.move_subtitle_to_button)
        self.addSpacing(10)
        self.addWidget(self.move_subtitle_bottom_button)
        self.addSpacing(10)
        self.addWidget(self.move_subtitle_down_button)
        self.addSpacing(10)
        self.addWidget(self.delete_subtitle_button)
        self.addStretch()

    def set_selected_row(self, selected_row, max_index):
        self.max_subtitle_index = max_index
        self.move_subtitle_up_button.current_index = selected_row
        self.move_subtitle_up_button.max_index = max_index
        self.move_subtitle_top_button.current_index = selected_row
        self.move_subtitle_top_button.max_index = max_index
        self.move_subtitle_down_button.current_index = selected_row
        self.move_subtitle_down_button.max_index = max_index
        self.move_subtitle_bottom_button.current_index = selected_row
        self.move_subtitle_bottom_button.max_index = max_index
        self.move_subtitle_to_button.current_index = selected_row
        self.move_subtitle_to_button.max_index = max_index
        self.delete_subtitle_button.current_index = selected_row
        self.delete_subtitle_button.max_index = max_index

    # noinspection PyAttributeOutsideInit
    def setup_shortcuts(self):
        self.move_subtitle_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self.subtitle_tab)
        self.move_subtitle_up_shortcut.activated.connect(self.move_subtitle_up_button.clicked_button)

        self.move_subtitle_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self.subtitle_tab)
        self.move_subtitle_down_shortcut.activated.connect(self.move_subtitle_down_button.clicked_button)

        self.move_subtitle_top_shortcut = QShortcut(QKeySequence("Ctrl+PgUp"), self.subtitle_tab)
        self.move_subtitle_top_shortcut.activated.connect(self.move_subtitle_top_button.clicked_button)

        self.move_subtitle_bottom_shortcut = QShortcut(QKeySequence("Ctrl+PgDown"), self.subtitle_tab)
        self.move_subtitle_bottom_shortcut.activated.connect(self.move_subtitle_bottom_button.clicked_button)

        self.move_subtitle_to_shortcut = QShortcut(QKeySequence("Ctrl+M"), self.subtitle_tab)
        self.move_subtitle_to_shortcut.activated.connect(self.move_subtitle_to_button.clicked_button)

        self.delete_subtitle_shortcut = QShortcut(QKeySequence("Delete"), self.subtitle_tab)
        self.delete_subtitle_shortcut.activated.connect(self.delete_subtitle_button.clicked_button)

    def refresh_subtitle_table(self):
        self.refresh_subtitle_table_signal.emit()

    def change_selected_subtitle_row(self, new_selected_index):
        new_selected_index = min(new_selected_index, len(GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index]) - 1)
        self.selected_subtitle_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_subtitle_up_button.setEnabled(False)
        self.move_subtitle_top_button.setEnabled(False)
        self.move_subtitle_down_button.setEnabled(False)
        self.move_subtitle_bottom_button.setEnabled(False)
        self.move_subtitle_to_button.setEnabled(False)
        self.delete_subtitle_button.setEnabled(False)

        self.move_subtitle_up_shortcut.setEnabled(False)
        self.move_subtitle_top_shortcut.setEnabled(False)
        self.move_subtitle_down_shortcut.setEnabled(False)
        self.move_subtitle_bottom_shortcut.setEnabled(False)
        self.move_subtitle_to_shortcut.setEnabled(False)
        self.delete_subtitle_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_subtitle_up_button.setEnabled(True)
        self.move_subtitle_top_button.setEnabled(True)
        self.move_subtitle_down_button.setEnabled(True)
        self.move_subtitle_bottom_button.setEnabled(True)
        self.move_subtitle_to_button.setEnabled(True)
        self.delete_subtitle_button.setEnabled(True)

        self.move_subtitle_up_shortcut.setEnabled(True)
        self.move_subtitle_top_shortcut.setEnabled(True)
        self.move_subtitle_down_shortcut.setEnabled(True)
        self.move_subtitle_bottom_shortcut.setEnabled(True)
        self.move_subtitle_to_shortcut.setEnabled(True)
        self.delete_subtitle_shortcut.setEnabled(True)

    def update_global_subtitle_files_list_order_to_top(self, index_to_move):
        while index_to_move > 0:
            temp_for_swap = GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move]
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move] = \
                GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move - 1]
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move - 1] = temp_for_swap

            temp_for_swap = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
                GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                    index_to_move - 1]
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move - 1] = temp_for_swap
            index_to_move -= 1

    def update_global_subtitle_files_list_order_to_up(self, index_to_move):
        temp_for_swap = GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move - 1]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move - 1] = temp_for_swap

        temp_for_swap = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                index_to_move - 1]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move - 1] = temp_for_swap

    def update_global_subtitle_files_list_order_to_position(self, list_of_old_and_new_index):
        old_index = list_of_old_and_new_index[0]
        new_index = list_of_old_and_new_index[1]
        temp_for_swap = GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][old_index]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][old_index] = \
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][new_index]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][new_index] = temp_for_swap

        temp_for_swap = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][old_index]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][old_index] = \
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][new_index]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][new_index] = temp_for_swap

    def update_global_subtitle_files_list_order_to_down(self, index_to_move):
        temp_for_swap = GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move + 1]
        GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move + 1] = temp_for_swap

        temp_for_swap = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                index_to_move + 1]
        GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move + 1] = temp_for_swap

    def update_global_subtitle_files_list_order_to_bottom(self, index_to_move):
        while index_to_move < self.max_subtitle_index:
            temp_for_swap = GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move]
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move] = \
                GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move + 1]
            GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_move + 1] = temp_for_swap

            temp_for_swap = GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move]
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move] = \
                GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][
                    index_to_move + 1]
            GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_move + 1] = temp_for_swap
            index_to_move += 1

    def update_global_subtitle_files_list_order_deleting(self, index_to_delete):
        del GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index][index_to_delete]
        del GlobalSetting.SUBTITLE_FILES_ABSOLUTE_PATH_LIST[self.tab_index][index_to_delete]
        self.refresh_subtitle_table()
