from PySide2 import QtGui
from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QAbstractItemView

from packages.Startup.GlobalIcons import LeftArrowIcon, RightArrowIcon
from packages.Startup.PreDefined import AllSubtitlesLanguages
from packages.Widgets.ListWidget import ListWidget
from packages.Widgets.MyDialog import MyDialog


class LanguagePreferenceDialog(MyDialog):
    def __init__(self, old_favorite, window_title, parent=None):
        super().__init__(parent)
        self.old_favorite = old_favorite
        self.current_favorite = self.old_favorite.copy()
        self.setWindowTitle(window_title)
        self.selected_language_layout = QVBoxLayout()
        self.available_language_layout = QVBoxLayout()
        self.selected_language_list = ListWidget()
        self.available_language_list = ListWidget()
        self.selected_language_label = QLabel("Favorite Languages:")
        self.available_language_label = QLabel("Available Languages:")
        self.selected_language_list.addItems(self.old_favorite)
        self.available_language_list.addItems(AllSubtitlesLanguages)
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.selected_items_from_selected_language = []
        self.selected_items_from_available_language = []
        self.tools_layout = QVBoxLayout()
        self.dialog_buttons_layout = QHBoxLayout()
        self.add_language_button = QPushButton()
        self.add_language_button.setIcon(LeftArrowIcon)
        self.remove_language_button = QPushButton()
        self.remove_language_button.setIcon(RightArrowIcon)
        self.language_preference_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.setup_selected_language_layout()
        self.setup_available_language_layout()
        self.setup_tools_layout()
        self.setup_dialog_buttons_layout()
        self.setup_language_preference_layout()
        self.setup_main_layout()
        self.disable_question_mark_window()
        self.signal_connect()

    def setup_tools_layout(self):
        self.tools_layout.addStretch()
        self.tools_layout.addWidget(self.add_language_button)
        self.tools_layout.addWidget(self.remove_language_button)
        self.tools_layout.addStretch()
        self.add_language_button.setEnabled(False)
        self.remove_language_button.setEnabled(False)

    def setup_selected_language_layout(self):
        self.selected_language_layout.addWidget(self.selected_language_label)
        self.selected_language_layout.addWidget(self.selected_language_list)
        self.selected_language_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def setup_available_language_layout(self):
        self.available_language_layout.addWidget(self.available_language_label)
        self.available_language_layout.addWidget(self.available_language_list)
        self.available_language_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def setup_language_preference_layout(self):
        self.language_preference_layout.addLayout(self.selected_language_layout)
        self.language_preference_layout.addLayout(self.tools_layout)
        self.language_preference_layout.addLayout(self.available_language_layout)

    def setup_dialog_buttons_layout(self):
        self.dialog_buttons_layout.addStretch()
        self.dialog_buttons_layout.addWidget(self.ok_button)
        self.dialog_buttons_layout.addWidget(self.cancel_button)
        self.dialog_buttons_layout.addStretch()

    def setup_main_layout(self):
        self.main_layout.addLayout(self.language_preference_layout)
        self.main_layout.addLayout(self.dialog_buttons_layout)
        self.setLayout(self.main_layout)
        self.selected_language_list.clearSelection()
        self.available_language_list.clearSelection()

    def signal_connect(self):
        self.ok_button.clicked.connect(self.click_yes)
        self.cancel_button.clicked.connect(self.click_no)
        self.selected_language_list.itemSelectionChanged.connect(self.update_selected_languages_selected)
        self.available_language_list.itemSelectionChanged.connect(self.update_available_languages_selected)
        self.add_language_button.clicked.connect(self.add_language_button_clicked)
        self.remove_language_button.clicked.connect(self.remove_language_button_clicked)

    def update_selected_languages_selected(self):
        self.available_language_list.clearSelection()
        self.selected_items_from_selected_language = [item.text() for item in
                                                      self.selected_language_list.selectedItems()]
        if len(self.selected_items_from_selected_language) > 0:
            self.remove_language_button.setEnabled(True)
        else:
            self.remove_language_button.setEnabled(False)

    def update_available_languages_selected(self):
        self.selected_language_list.clearSelection()
        self.selected_items_from_available_language = [item.text() for item in
                                                       self.available_language_list.selectedItems()]
        if len(self.selected_items_from_available_language) > 0:
            self.add_language_button.setEnabled(True)
        else:
            self.add_language_button.setEnabled(False)

    def add_language_button_clicked(self):
        current_selected_language_list = []
        for i in range(self.selected_language_list.count()):
            current_selected_language_list.append(self.selected_language_list.item(i).text())
        for language in self.selected_items_from_available_language:
            if language not in current_selected_language_list:
                self.selected_language_list.addItem(language)
        self.selected_items_from_available_language = []
        self.available_language_list.clearSelection()

    def remove_language_button_clicked(self):
        new_selected_language_list = []
        for i in range(self.selected_language_list.count()):
            if self.selected_language_list.item(i).text() not in self.selected_items_from_selected_language:
                new_selected_language_list.append(self.selected_language_list.item(i).text())
        self.selected_language_list.clear()
        self.selected_language_list.addItems(new_selected_language_list)
        self.selected_items_from_selected_language = []
        self.selected_language_list.clearSelection()

    def click_yes(self):
        self.current_favorite = []
        for i in range(self.selected_language_list.count()):
            self.current_favorite.append(self.selected_language_list.item(i).text())
        if len(self.current_favorite) == 0:
            self.current_favorite.append("English")
        self.close()

    def click_no(self):
        self.current_favorite = self.old_favorite.copy()
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(QSize(self.size().width() + 30, self.size().height()))

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def execute(self):
        self.exec()
