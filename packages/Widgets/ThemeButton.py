import json
from pathlib import Path

from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QPushButton
from packages.Startup.Options import Options, save_options
from packages.Startup.GlobalIcons import ThemeIcon
from packages.Startup.MainApplication import apply_dark_mode, apply_light_mode


class ThemeButton(QPushButton):
    dark_mode_updated_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(ThemeIcon)
        self.setIconSize(QSize(18, 18))
        self.setText("")
        self.clicked.connect(self.theme_button_clicked)
        if Options.Dark_Mode:
            self.set_tool_tip_when_dark()
        else:
            self.set_tool_tip_when_light()

    def theme_button_clicked(self):
        if Options.Dark_Mode:
            apply_light_mode()
            self.set_tool_tip_when_light()
        else:
            apply_dark_mode()
            self.set_tool_tip_when_dark()
        Options.Dark_Mode = not Options.Dark_Mode
        save_options()
        self.dark_mode_updated_signal.emit()

    def set_tool_tip_when_dark(self):
        self.setToolTip("Switch To Light Mode")
        self.setToolTipDuration(1500)

    def set_tool_tip_when_light(self):
        self.setToolTip("Switch To Dark Mode")
        self.setToolTipDuration(1500)
