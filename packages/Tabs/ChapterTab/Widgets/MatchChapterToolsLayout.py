from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout, QShortcut

from packages.Tabs.ChapterTab.Widgets.DeleteChapterButton import DeleteChapterButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterBottomButton import MoveChapterBottomButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterDownButton import MoveChapterDownButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterToButton import MoveChapterToButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterTopButton import MoveChapterTopButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterUpButton import MoveChapterUpButton
from packages.Tabs.GlobalSetting import GlobalSetting


def update_global_chapter_files_list_order_to_top(index_to_move):
    while index_to_move > 0:
        temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[index_to_move]
        GlobalSetting.CHAPTER_FILES_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_LIST[index_to_move - 1]
        GlobalSetting.CHAPTER_FILES_LIST[index_to_move - 1] = temp_for_swap

        temp_for_swap = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move]
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[
            index_to_move - 1]
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move - 1] = temp_for_swap
        index_to_move -= 1


def update_global_chapter_files_list_order_to_up(index_to_move):
    temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[index_to_move]
    GlobalSetting.CHAPTER_FILES_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_LIST[index_to_move - 1]
    GlobalSetting.CHAPTER_FILES_LIST[index_to_move - 1] = temp_for_swap

    temp_for_swap = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[
        index_to_move - 1]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move - 1] = temp_for_swap


def update_global_chapter_files_list_order_to_position(list_of_old_and_new_index):
    old_index = list_of_old_and_new_index[0]
    new_index = list_of_old_and_new_index[1]
    temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[old_index]
    GlobalSetting.CHAPTER_FILES_LIST[old_index] = GlobalSetting.CHAPTER_FILES_LIST[new_index]
    GlobalSetting.CHAPTER_FILES_LIST[new_index] = temp_for_swap

    temp_for_swap = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[old_index]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[old_index] = \
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[new_index]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[new_index] = temp_for_swap


def update_global_chapter_files_list_order_to_down(index_to_move):
    temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[index_to_move]
    GlobalSetting.CHAPTER_FILES_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_LIST[index_to_move + 1]
    GlobalSetting.CHAPTER_FILES_LIST[index_to_move + 1] = temp_for_swap

    temp_for_swap = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[
        index_to_move + 1]
    GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move + 1] = temp_for_swap


def update_global_chapter_files_list_order_to_bottom(index_to_move):
    while index_to_move < len(GlobalSetting.CHAPTER_FILES_LIST) - 1:
        temp_for_swap = GlobalSetting.CHAPTER_FILES_LIST[index_to_move]
        GlobalSetting.CHAPTER_FILES_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_LIST[index_to_move + 1]
        GlobalSetting.CHAPTER_FILES_LIST[index_to_move + 1] = temp_for_swap

        temp_for_swap = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move]
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move] = GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[
            index_to_move + 1]
        GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_move + 1] = temp_for_swap
        index_to_move += 1


class MatchChapterToolsLayout(QVBoxLayout):
    refresh_chapter_table_signal = Signal()
    selected_chapter_row_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.chapter_tab = parent
        self.move_chapter_up_button = MoveChapterUpButton()
        self.move_chapter_top_button = MoveChapterTopButton()
        self.move_chapter_down_button = MoveChapterDownButton()
        self.move_chapter_bottom_button = MoveChapterBottomButton()
        self.move_chapter_to_button = MoveChapterToButton()
        self.delete_chapter_button = DeleteChapterButton()
        self.setup_shortcuts()
        self.setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.move_chapter_up_button.swap_happened_signal.connect(self.refresh_chapter_table)
        self.move_chapter_up_button.selected_row_after_swap.connect(self.change_selected_chapter_row)
        self.move_chapter_top_button.swap_happened_signal.connect(self.refresh_chapter_table)
        self.move_chapter_top_button.selected_row_after_swap.connect(self.change_selected_chapter_row)
        self.move_chapter_down_button.swap_happened_signal.connect(self.refresh_chapter_table)
        self.move_chapter_down_button.selected_row_after_swap.connect(self.change_selected_chapter_row)
        self.move_chapter_bottom_button.swap_happened_signal.connect(self.refresh_chapter_table)
        self.move_chapter_bottom_button.selected_row_after_swap.connect(self.change_selected_chapter_row)
        self.move_chapter_to_button.swap_happened_signal.connect(self.refresh_chapter_table)
        self.move_chapter_to_button.selected_row_after_swap.connect(self.change_selected_chapter_row)
        self.move_chapter_top_button.move_chapter_to_top_signal.connect(
            update_global_chapter_files_list_order_to_top)
        self.move_chapter_up_button.move_chapter_to_up_signal.connect(update_global_chapter_files_list_order_to_up)
        self.move_chapter_to_button.move_chapter_to_position_signal.connect(
            update_global_chapter_files_list_order_to_position)
        self.move_chapter_down_button.move_chapter_to_down_signal.connect(
            update_global_chapter_files_list_order_to_down)
        self.move_chapter_bottom_button.move_chapter_to_bottom_signal.connect(
            update_global_chapter_files_list_order_to_bottom)
        self.delete_chapter_button.delete_happened_signal.connect(
            self.update_global_chapter_files_list_order_deleting)
        self.delete_chapter_button.selected_row_after_delete.connect(self.change_selected_chapter_row)

    def setup_layout(self):
        self.addStretch()
        self.addWidget(self.move_chapter_up_button)
        self.addSpacing(10)
        self.addWidget(self.move_chapter_top_button)
        self.addSpacing(10)
        self.addWidget(self.move_chapter_to_button)
        self.addSpacing(10)
        self.addWidget(self.move_chapter_bottom_button)
        self.addSpacing(10)
        self.addWidget(self.move_chapter_down_button)
        self.addSpacing(10)
        self.addWidget(self.delete_chapter_button)
        self.addStretch()

    def set_selected_row(self, selected_row, max_index):
        self.move_chapter_up_button.current_index = selected_row
        self.move_chapter_up_button.max_index = max_index
        self.move_chapter_top_button.current_index = selected_row
        self.move_chapter_top_button.max_index = max_index
        self.move_chapter_down_button.current_index = selected_row
        self.move_chapter_down_button.max_index = max_index
        self.move_chapter_bottom_button.current_index = selected_row
        self.move_chapter_bottom_button.max_index = max_index
        self.move_chapter_to_button.current_index = selected_row
        self.move_chapter_to_button.max_index = max_index
        self.delete_chapter_button.current_index = selected_row
        self.delete_chapter_button.max_index = max_index

    # noinspection PyAttributeOutsideInit
    def setup_shortcuts(self):
        self.move_chapter_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self.chapter_tab)
        self.move_chapter_up_shortcut.activated.connect(self.move_chapter_up_button.clicked_button)

        self.move_chapter_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self.chapter_tab)
        self.move_chapter_down_shortcut.activated.connect(self.move_chapter_down_button.clicked_button)

        self.move_chapter_top_shortcut = QShortcut(QKeySequence("Ctrl+PgUp"), self.chapter_tab)
        self.move_chapter_top_shortcut.activated.connect(self.move_chapter_top_button.clicked_button)

        self.move_chapter_bottom_shortcut = QShortcut(QKeySequence("Ctrl+PgDown"), self.chapter_tab)
        self.move_chapter_bottom_shortcut.activated.connect(self.move_chapter_bottom_button.clicked_button)

        self.move_chapter_to_shortcut = QShortcut(QKeySequence("Ctrl+M"), self.chapter_tab)
        self.move_chapter_to_shortcut.activated.connect(self.move_chapter_to_button.clicked_button)

        self.delete_chapter_shortcut = QShortcut(QKeySequence("Delete"), self.chapter_tab)
        self.delete_chapter_shortcut.activated.connect(self.delete_chapter_button.clicked_button)

    def refresh_chapter_table(self):
        self.refresh_chapter_table_signal.emit()

    def change_selected_chapter_row(self, new_selected_index):
        new_selected_index = min(new_selected_index, len(GlobalSetting.CHAPTER_FILES_LIST) - 1)
        self.selected_chapter_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_chapter_up_button.setEnabled(False)
        self.move_chapter_top_button.setEnabled(False)
        self.move_chapter_down_button.setEnabled(False)
        self.move_chapter_bottom_button.setEnabled(False)
        self.move_chapter_to_button.setEnabled(False)
        self.delete_chapter_button.setEnabled(False)

        self.move_chapter_up_shortcut.setEnabled(False)
        self.move_chapter_top_shortcut.setEnabled(False)
        self.move_chapter_down_shortcut.setEnabled(False)
        self.move_chapter_bottom_shortcut.setEnabled(False)
        self.move_chapter_to_shortcut.setEnabled(False)
        self.delete_chapter_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_chapter_up_button.setEnabled(True)
        self.move_chapter_top_button.setEnabled(True)
        self.move_chapter_down_button.setEnabled(True)
        self.move_chapter_bottom_button.setEnabled(True)
        self.move_chapter_to_button.setEnabled(True)
        self.delete_chapter_button.setEnabled(True)

        self.move_chapter_up_shortcut.setEnabled(True)
        self.move_chapter_top_shortcut.setEnabled(True)
        self.move_chapter_down_shortcut.setEnabled(True)
        self.move_chapter_bottom_shortcut.setEnabled(True)
        self.move_chapter_to_shortcut.setEnabled(True)
        self.delete_chapter_shortcut.setEnabled(True)

    def update_global_chapter_files_list_order_deleting(self, index_to_delete):
        del GlobalSetting.CHAPTER_FILES_LIST[index_to_delete]
        del GlobalSetting.CHAPTER_FILES_ABSOLUTE_PATH_LIST[index_to_delete]
        self.refresh_chapter_table()
