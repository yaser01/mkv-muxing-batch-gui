from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout,QShortcut

from packages.Tabs.AttachmentTab.Widgets.DeleteAttachmentButton import DeleteAttachmentButton
from packages.Tabs.AttachmentTab.Widgets.MoveAttachmentBottomButton import MoveAttachmentBottomButton
from packages.Tabs.AttachmentTab.Widgets.MoveAttachmentDownButton import MoveAttachmentDownButton
from packages.Tabs.AttachmentTab.Widgets.MoveAttachmentToButton import MoveAttachmentToButton
from packages.Tabs.AttachmentTab.Widgets.MoveAttachmentTopButton import MoveAttachmentTopButton
from packages.Tabs.AttachmentTab.Widgets.MoveAttachmentUpButton import MoveAttachmentUpButton
from packages.Tabs.GlobalSetting import GlobalSetting


def update_global_attachment_files_list_order_to_top(index_to_move):
    while index_to_move > 0:
        temp_for_swap = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move]
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move] = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[
            index_to_move - 1]
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move - 1] = temp_for_swap
        index_to_move -= 1


def update_global_attachment_files_list_order_to_up(index_to_move):
    temp_for_swap = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move] = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move - 1]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move - 1] = temp_for_swap


def update_global_attachment_files_list_order_to_position(list_of_old_and_new_index):
    old_index = list_of_old_and_new_index[0]
    new_index = list_of_old_and_new_index[1]
    temp_for_swap = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[old_index]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[old_index] = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[new_index]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[new_index] = temp_for_swap


def update_global_attachment_files_list_order_to_down(index_to_move):
    temp_for_swap = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move] = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[
        index_to_move + 1]
    GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move + 1] = temp_for_swap


def update_global_attachment_files_list_order_to_bottom(index_to_move):
    while index_to_move < len(GlobalSetting.ATTACHMENT_PATH_DATA_LIST) - 1:
        temp_for_swap = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move]
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move] = GlobalSetting.ATTACHMENT_PATH_DATA_LIST[
            index_to_move + 1]
        GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_move + 1] = temp_for_swap
        index_to_move += 1


class MatchAttachmentToolsLayout(QVBoxLayout):
    refresh_attachment_table_signal = Signal()
    selected_attachment_row_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.attachment_tab = parent
        self.move_attachment_up_button = MoveAttachmentUpButton()
        self.move_attachment_top_button = MoveAttachmentTopButton()
        self.move_attachment_down_button = MoveAttachmentDownButton()
        self.move_attachment_bottom_button = MoveAttachmentBottomButton()
        self.move_attachment_to_button = MoveAttachmentToButton()
        self.delete_attachment_button = DeleteAttachmentButton()
        self.setup_shortcuts()
        self.setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.move_attachment_up_button.swap_happened_signal.connect(self.refresh_attachment_table)
        self.move_attachment_up_button.selected_row_after_swap.connect(self.change_selected_attachment_row)
        self.move_attachment_top_button.swap_happened_signal.connect(self.refresh_attachment_table)
        self.move_attachment_top_button.selected_row_after_swap.connect(self.change_selected_attachment_row)
        self.move_attachment_down_button.swap_happened_signal.connect(self.refresh_attachment_table)
        self.move_attachment_down_button.selected_row_after_swap.connect(self.change_selected_attachment_row)
        self.move_attachment_bottom_button.swap_happened_signal.connect(self.refresh_attachment_table)
        self.move_attachment_bottom_button.selected_row_after_swap.connect(self.change_selected_attachment_row)
        self.move_attachment_to_button.swap_happened_signal.connect(self.refresh_attachment_table)
        self.move_attachment_to_button.selected_row_after_swap.connect(self.change_selected_attachment_row)
        self.move_attachment_top_button.move_attachment_to_top_signal.connect(
            update_global_attachment_files_list_order_to_top)
        self.move_attachment_up_button.move_attachment_to_up_signal.connect(
            update_global_attachment_files_list_order_to_up)
        self.move_attachment_to_button.move_attachment_to_position_signal.connect(
            update_global_attachment_files_list_order_to_position)
        self.move_attachment_down_button.move_attachment_to_down_signal.connect(
            update_global_attachment_files_list_order_to_down)
        self.move_attachment_bottom_button.move_attachment_to_bottom_signal.connect(
            update_global_attachment_files_list_order_to_bottom)
        self.delete_attachment_button.delete_happened_signal.connect(
            self.update_global_attachment_files_list_order_deleting)
        self.delete_attachment_button.selected_row_after_delete.connect(self.change_selected_attachment_row)

    def setup_layout(self):
        self.addStretch()
        self.addWidget(self.move_attachment_up_button)
        self.addSpacing(10)
        self.addWidget(self.move_attachment_top_button)
        self.addSpacing(10)
        self.addWidget(self.move_attachment_to_button)
        self.addSpacing(10)
        self.addWidget(self.move_attachment_bottom_button)
        self.addSpacing(10)
        self.addWidget(self.move_attachment_down_button)
        self.addSpacing(10)
        self.addWidget(self.delete_attachment_button)
        self.addStretch()

    def set_selected_row(self, selected_row, max_index):
        self.move_attachment_up_button.current_index = selected_row
        self.move_attachment_up_button.max_index = max_index
        self.move_attachment_top_button.current_index = selected_row
        self.move_attachment_top_button.max_index = max_index
        self.move_attachment_down_button.current_index = selected_row
        self.move_attachment_down_button.max_index = max_index
        self.move_attachment_bottom_button.current_index = selected_row
        self.move_attachment_bottom_button.max_index = max_index
        self.move_attachment_to_button.current_index = selected_row
        self.move_attachment_to_button.max_index = max_index
        self.delete_attachment_button.current_index = selected_row
        self.delete_attachment_button.max_index = max_index

    # noinspection PyAttributeOutsideInit
    def setup_shortcuts(self):
        self.move_attachment_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self.attachment_tab)
        self.move_attachment_up_shortcut.activated.connect(self.move_attachment_up_button.clicked_button)

        self.move_attachment_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self.attachment_tab)
        self.move_attachment_down_shortcut.activated.connect(self.move_attachment_down_button.clicked_button)

        self.move_attachment_top_shortcut = QShortcut(QKeySequence("Ctrl+PgUp"), self.attachment_tab)
        self.move_attachment_top_shortcut.activated.connect(self.move_attachment_top_button.clicked_button)

        self.move_attachment_bottom_shortcut = QShortcut(QKeySequence("Ctrl+PgDown"), self.attachment_tab)
        self.move_attachment_bottom_shortcut.activated.connect(self.move_attachment_bottom_button.clicked_button)

        self.move_attachment_to_shortcut = QShortcut(QKeySequence("Ctrl+M"), self.attachment_tab)
        self.move_attachment_to_shortcut.activated.connect(self.move_attachment_to_button.clicked_button)

        self.delete_attachment_shortcut = QShortcut(QKeySequence("Delete"), self.attachment_tab)
        self.delete_attachment_shortcut.activated.connect(self.delete_attachment_button.clicked_button)

    def refresh_attachment_table(self):
        self.refresh_attachment_table_signal.emit()

    def change_selected_attachment_row(self, new_selected_index):
        new_selected_index = min(new_selected_index, len(GlobalSetting.ATTACHMENT_PATH_DATA_LIST) - 1)
        self.selected_attachment_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_attachment_up_button.setEnabled(False)
        self.move_attachment_top_button.setEnabled(False)
        self.move_attachment_down_button.setEnabled(False)
        self.move_attachment_bottom_button.setEnabled(False)
        self.move_attachment_to_button.setEnabled(False)
        self.delete_attachment_button.setEnabled(False)

        self.move_attachment_up_shortcut.setEnabled(False)
        self.move_attachment_top_shortcut.setEnabled(False)
        self.move_attachment_down_shortcut.setEnabled(False)
        self.move_attachment_bottom_shortcut.setEnabled(False)
        self.move_attachment_to_shortcut.setEnabled(False)
        self.delete_attachment_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_attachment_up_button.setEnabled(True)
        self.move_attachment_top_button.setEnabled(True)
        self.move_attachment_down_button.setEnabled(True)
        self.move_attachment_bottom_button.setEnabled(True)
        self.move_attachment_to_button.setEnabled(True)
        self.delete_attachment_button.setEnabled(True)

        self.move_attachment_up_shortcut.setEnabled(True)
        self.move_attachment_top_shortcut.setEnabled(True)
        self.move_attachment_down_shortcut.setEnabled(True)
        self.move_attachment_bottom_shortcut.setEnabled(True)
        self.move_attachment_to_shortcut.setEnabled(True)
        self.delete_attachment_shortcut.setEnabled(True)

    def update_global_attachment_files_list_order_deleting(self, index_to_delete):
        del GlobalSetting.ATTACHMENT_PATH_DATA_LIST[index_to_delete]
        self.refresh_attachment_table()
