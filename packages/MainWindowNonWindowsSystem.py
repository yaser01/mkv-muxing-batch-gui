import PySide2
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QFrame, QVBoxLayout

from packages.Startup import GlobalIcons
from packages.Startup.InitializeScreenResolution import width_factor, height_factor
from packages.Startup.Options import Options, save_options, get_names_list_of_presets
from packages.Startup.Version import Version
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.TabsManager import TabsManager
from packages.Widgets.ChoosePresetDialog import ChoosePresetDialog
from packages.Widgets.CloseDialogWhileAtLeastOneOptionSelected import CloseDialogWhileAtLeastOneOptionSelected
from packages.Widgets.CloseDialogWhileMuxingOn import CloseDialogWhileMuxingOn
from packages.Widgets.MyMainWindow import MyMainWindow


def check_if_exit_when_muxing_on():
    close_dialog = CloseDialogWhileMuxingOn()
    close_dialog.execute()
    return close_dialog.result == 'Exit'


def check_if_exit_while_selected_one_option():
    close_dialog = CloseDialogWhileAtLeastOneOptionSelected()
    close_dialog.execute()
    return close_dialog.result == 'Exit'


class MainWindowNonWindowsSystem(MyMainWindow):
    def __init__(self, args, parent=None):
        super().__init__(args=args, parent=parent)
        self.resize(int(width_factor * 1100), int(height_factor * 635))
        self.setWindowTitle("MKV Muxing Batch GUI v" + str(Version))
        self.setWindowIcon(GlobalIcons.AppIcon)
        self.tabs = TabsManager()
        self.tabs_frame = QFrame()
        self.tabs_layout = QVBoxLayout()
        self.setup_tabs_layout()
        self.setCentralWidget(self.tabs_frame)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.show_window()
        self.check_if_need_to_show_choose_preset_dialog(parent=self.window())
        self.tabs.set_preset_options()
        self.connect_signals()

    def connect_signals(self):
        self.tabs.currentChanged.connect(self.update_minimum_size)

    def show_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def setup_tabs_layout(self):
        self.tabs_frame.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setContentsMargins(9, 9, 9, 12)
        self.tabs_layout.addWidget(self.tabs)
        self.tabs_frame.setLayout(self.tabs_layout)

    def update_minimum_size(self):
        self.setMinimumSize(self.minimumSizeHint())

    def closeEvent(self, event: PySide2.QtGui.QCloseEvent):
        muxing_on = GlobalSetting.MUXING_ON
        if muxing_on:
            want_to_exit = check_if_exit_when_muxing_on()
            if want_to_exit:
                super().closeEvent(event)
            else:
                event.ignore()
            return
        option_selected = len(GlobalSetting.VIDEO_FILES_LIST) > 0 and not GlobalSetting.JOB_QUEUE_FINISHED
        if option_selected:
            want_to_exit = check_if_exit_while_selected_one_option()
            if want_to_exit:
                super().closeEvent(event)
            else:
                event.ignore()
            return
        super().closeEvent(event)
    @staticmethod
    def check_if_need_to_show_choose_preset_dialog(parent):
        if Options.Choose_Preset_On_Startup:
            choose_preset_dialog = ChoosePresetDialog(preset_list=get_names_list_of_presets(),
                                                      favorite_preset_id=Options.FavoritePresetId,parent=parent)
            choose_preset_dialog.execute()
            selected_preset_id = Options.FavoritePresetId
            if choose_preset_dialog.chosen_index != -1:
                selected_preset_id = choose_preset_dialog.chosen_index
            Options.CurrentPreset = Options.DefaultPresets[selected_preset_id]
            if choose_preset_dialog.remember:
                Options.Choose_Preset_On_Startup = False
                Options.FavoritePresetId = selected_preset_id
                save_options()
            return True
        else:
            Options.CurrentPreset = Options.DefaultPresets[Options.FavoritePresetId]
            return False