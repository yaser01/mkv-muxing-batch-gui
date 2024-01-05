from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

from packages.Startup import GlobalIcons
from packages.Startup.Options import Options
from packages.Tabs.SettingTab.Widgets.RenamePresetDialog import RenamePresetDialog


class PresetTabRenameButton(QPushButton):
    rename_tab_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalIcons.RenameIcon)
        self.hint_when_enabled = "Rename Preset"
        self.current_preset_name = ""
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(self.clicked_button)
        self.dark_mode_applied = False

    def clicked_button(self):
        rename_preset_to_dialog = RenamePresetDialog(old_name=self.current_preset_name,parent=self)
        rename_preset_to_dialog.execute()
        if rename_preset_to_dialog.result == "Yes":
            self.rename_tab_signal.emit(rename_preset_to_dialog.new_name)

    def paintEvent(self, e):
        super().paintEvent(e)
        if Options.Dark_Mode and not self.dark_mode_applied:
            self.setIcon(GlobalIcons.RenameIcon)
            self.dark_mode_applied = True
        if not Options.Dark_Mode and self.dark_mode_applied:
            self.setIcon(GlobalIcons.RenameIcon)
            self.dark_mode_applied = False
