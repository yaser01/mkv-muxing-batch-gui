import json
from pathlib import Path

from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QPushButton

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Startup.GlobalFiles import SettingJsonInfoFilePath
from packages.Startup.GlobalIcons import ThemeIcon
from packages.Startup.MainApplication import apply_dark_mode, apply_light_mode


def save_theme_mode_state():
    setting_data = {"Default_Video_Directory": DefaultOptions.Default_Video_Directory,
                    "Default_Video_Extensions": DefaultOptions.Default_Video_Extensions,
                    "Default_Subtitle_Directory": DefaultOptions.Default_Subtitle_Directory,
                    "Default_Subtitle_Extensions": DefaultOptions.Default_Subtitle_Extensions,
                    "Default_Subtitle_Language": DefaultOptions.Default_Subtitle_Language,
                    "Default_Audio_Directory": DefaultOptions.Default_Audio_Directory,
                    "Default_Audio_Extensions": DefaultOptions.Default_Audio_Extensions,
                    "Default_Audio_Language": DefaultOptions.Default_Audio_Language,
                    "Default_Chapter_Directory": DefaultOptions.Default_Chapter_Directory,
                    "Default_Chapter_Extensions": DefaultOptions.Default_Chapter_Extensions,
                    "Default_Attachment_Directory": DefaultOptions.Default_Attachment_Directory,
                    "Default_Destination_Directory": DefaultOptions.Default_Destination_Directory,
                    "Default_Favorite_Subtitle_Languages": DefaultOptions.Default_Favorite_Subtitle_Languages,
                    "Default_Favorite_Audio_Languages": DefaultOptions.Default_Favorite_Audio_Languages,
                    "Dark_Mode": DefaultOptions.Dark_Mode
                    }
    setting_file_path = Path(SettingJsonInfoFilePath)
    with open(setting_file_path, "w+", encoding="UTF-8") as setting_file:
        json.dump(setting_data, setting_file)


class ThemeButton(QPushButton):
    dark_mode_updated_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(ThemeIcon)
        self.setIconSize(QSize(18, 18))
        self.setText("")
        self.clicked.connect(self.open_setting_dialog)

    def open_setting_dialog(self):
        if DefaultOptions.Dark_Mode:
            apply_light_mode()
        else:
            apply_dark_mode()
        DefaultOptions.Dark_Mode = not DefaultOptions.Dark_Mode
        save_theme_mode_state()

        self.dark_mode_updated_signal.emit()
