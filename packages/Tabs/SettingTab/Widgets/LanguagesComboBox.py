from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox

from packages.Startup.InitializeScreenResolution import screen_size


class LanguagesComboBox(QComboBox):
    def __init__(self, items_list, default_item):
        super().__init__()
        self.setMinimumWidth(screen_size.width() // 10)
        self.addItems(items_list)
        self.setCurrentIndex(items_list.index(default_item))
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")

    def addItems(self, texts):
        super().addItems(texts)
        for i in range(len(texts)):
            self.setItemData(i, texts[i], Qt.ToolTipRole)
