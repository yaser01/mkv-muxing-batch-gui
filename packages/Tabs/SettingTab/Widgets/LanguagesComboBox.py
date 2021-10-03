from PySide2.QtWidgets import QComboBox
from packages.Startup.InitializeScreenResolution import screen_size


class LanguagesComboBox(QComboBox):
    def __init__(self, items_list, default_item):
        super().__init__()
        self.setMinimumWidth(screen_size.width() // 13)
        self.addItems(items_list)
        self.setCurrentIndex(items_list.index(default_item))
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
