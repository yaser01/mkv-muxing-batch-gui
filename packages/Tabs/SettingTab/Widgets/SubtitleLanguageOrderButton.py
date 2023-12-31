from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup.GlobalIcons import SettingIcon
from packages.Tabs.SettingTab.Widgets.LanguagePreferenceDialog import LanguagePreferenceDialog


class SubtitleLanguageOrderButton(QPushButton):
    new_language_list_signal = Signal(list)

    def __init__(self, current_language_list):
        super().__init__()
        self.setIcon(SettingIcon)
        self.setIconSize(QSize(20, 20))
        self.setText("")
        self.clicked.connect(self.open_setting_dialog)
        self.current_language_list = current_language_list

    def open_setting_dialog(self):
        language_preference_dialog = LanguagePreferenceDialog(old_favorite=self.current_language_list,
                                                              window_title="Subtitle Language Preference", parent=self)
        language_preference_dialog.execute()
        self.current_language_list = language_preference_dialog.current_favorite.copy()
        self.new_language_list_signal.emit(self.current_language_list.copy())
