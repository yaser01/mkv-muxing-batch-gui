from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QVBoxLayout, QShortcut

from packages.Tabs.ChapterTab.Widgets.MoveChapterBottomButton import MoveChapterBottomButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterDownButton import MoveChapterDownButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterToButton import MoveChapterToButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterTopButton import MoveChapterTopButton
from packages.Tabs.ChapterTab.Widgets.MoveChapterUpButton import MoveChapterUpButton


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

    def refresh_chapter_table(self):
        self.refresh_chapter_table_signal.emit()

    def change_selected_chapter_row(self, new_selected_index):
        self.selected_chapter_row_signal.emit(new_selected_index)

    def disable_editable_widgets(self):
        self.move_chapter_up_button.setEnabled(False)
        self.move_chapter_top_button.setEnabled(False)
        self.move_chapter_down_button.setEnabled(False)
        self.move_chapter_bottom_button.setEnabled(False)
        self.move_chapter_to_button.setEnabled(False)

        self.move_chapter_up_shortcut.setEnabled(False)
        self.move_chapter_top_shortcut.setEnabled(False)
        self.move_chapter_down_shortcut.setEnabled(False)
        self.move_chapter_bottom_shortcut.setEnabled(False)
        self.move_chapter_to_shortcut.setEnabled(False)

    def enable_editable_widgets(self):
        self.move_chapter_up_button.setEnabled(True)
        self.move_chapter_top_button.setEnabled(True)
        self.move_chapter_down_button.setEnabled(True)
        self.move_chapter_bottom_button.setEnabled(True)
        self.move_chapter_to_button.setEnabled(True)

        self.move_chapter_up_shortcut.setEnabled(True)
        self.move_chapter_top_shortcut.setEnabled(True)
        self.move_chapter_down_shortcut.setEnabled(True)
        self.move_chapter_bottom_shortcut.setEnabled(True)
        self.move_chapter_to_shortcut.setEnabled(True)
