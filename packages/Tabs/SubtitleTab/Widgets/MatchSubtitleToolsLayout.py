from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout, QShortcut

from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleBottomButton import MoveSubtitleBottomButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleDownButton import MoveSubtitleDownButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleToButton import MoveSubtitleToButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleTopButton import MoveSubtitleTopButton
from packages.Tabs.SubtitleTab.Widgets.MoveSubtitleUpButton import MoveSubtitleUpButton


class MatchSubtitleToolsLayout(QVBoxLayout):
    refresh_subtitle_table_signal = Signal()
    selected_subtitle_row_signal = Signal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.subtitle_tab = parent
        self.move_subtitle_up_button = MoveSubtitleUpButton()
        self.move_subtitle_top_button = MoveSubtitleTopButton()
        self.move_subtitle_down_button = MoveSubtitleDownButton()
        self.move_subtitle_bottom_button = MoveSubtitleBottomButton()
        self.move_subtitle_to_button = MoveSubtitleToButton()
        self.setup_shortcuts()
        self.setup_layout()
        self.connect_signals()

    def connect_signals(self):
        self.move_subtitle_up_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_up_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_top_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_top_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_down_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_down_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_bottom_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_bottom_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)
        self.move_subtitle_to_button.swap_happened_signal.connect(self.refresh_subtitle_table)
        self.move_subtitle_to_button.selected_row_after_swap.connect(self.change_selected_subtitle_row)

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
        self.addStretch()

    def set_selected_row(self, selected_row, max_index):
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

    def refresh_subtitle_table(self):
        self.refresh_subtitle_table_signal.emit()

    def change_selected_subtitle_row(self, new_selected_index):
        self.selected_subtitle_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_subtitle_up_button.setEnabled(False)
        self.move_subtitle_top_button.setEnabled(False)
        self.move_subtitle_down_button.setEnabled(False)
        self.move_subtitle_bottom_button.setEnabled(False)
        self.move_subtitle_to_button.setEnabled(False)

        self.move_subtitle_up_shortcut.setEnabled(False)
        self.move_subtitle_top_shortcut.setEnabled(False)
        self.move_subtitle_down_shortcut.setEnabled(False)
        self.move_subtitle_bottom_shortcut.setEnabled(False)
        self.move_subtitle_to_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_subtitle_up_button.setEnabled(True)
        self.move_subtitle_top_button.setEnabled(True)
        self.move_subtitle_down_button.setEnabled(True)
        self.move_subtitle_bottom_button.setEnabled(True)
        self.move_subtitle_to_button.setEnabled(True)

        self.move_subtitle_up_shortcut.setEnabled(True)
        self.move_subtitle_top_shortcut.setEnabled(True)
        self.move_subtitle_down_shortcut.setEnabled(True)
        self.move_subtitle_bottom_shortcut.setEnabled(True)
        self.move_subtitle_to_shortcut.setEnabled(True)
