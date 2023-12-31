# import faulthandler
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QHBoxLayout, \
    QGridLayout, QLabel, QPushButton, QCheckBox
from packages.Startup.Options import Options, save_options, get_names_list_of_presets
from packages.Startup.GlobalFiles import InfoIconPath
from packages.Startup.GlobalIcons import SettingIcon
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.SettingTab.Widgets.AboutButton import AboutButton
from packages.Tabs.SettingTab.Widgets.DonateButton import DonateButton
from packages.Tabs.SettingTab.Widgets.PresetTabComboBox import PresetTabComboBox
from packages.Tabs.SettingTab.Widgets.PresetTabDeleteButton import PresetTabDeleteButton
from packages.Tabs.SettingTab.Widgets.PresetTabRenameButton import PresetTabRenameButton
from packages.Tabs.SettingTab.Widgets.PresetTabSetDeafultButton import PresetTabSetDefaultButton
from packages.Tabs.SettingTab.Widgets.PresetTabWidget import PresetTabWidget
from packages.Widgets.MyDialog import MyDialog
from packages.Widgets.SingleDefaultPresetsData import SingleDefaultPresetsData


# faulthandler.enable()


class SettingDialog(MyDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(SettingIcon)
        self.setWindowTitle("Options")
        self.setMinimumWidth(screen_size.width() // 1.9)
        self.message = QLabel()
        self.extra_message = QLabel()
        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")
        self.setting_info_text_icon_label = QLabel()
        self.setting_info_text_icon_pixmap = QPixmap(InfoIconPath)
        self.setting_info_text_icon_label.setPixmap(self.setting_info_text_icon_pixmap)
        self.setting_info_text_label = QLabel("Changes will take effect on next launch")
        self.setting_about_button = AboutButton()
        self.setting_donate_button = DonateButton()

        self.preset_tabs = []
        self.preset_counter = 0
        self.preset_tab_label = QLabel("Presets: ")
        self.preset_tab_comboBox = PresetTabComboBox(items=get_names_list_of_presets(),
                                                     activated_preset_id=Options.FavoritePresetId)
        self.preset_tab_delete_button = PresetTabDeleteButton()
        self.preset_tab_rename_button = PresetTabRenameButton()
        self.preset_tab_set_default_button = PresetTabSetDefaultButton()
        self.preset_tab_ask_on_start_check_box = QCheckBox("Ask for preset on startup")
        self.preset_tab_setting_layout = QHBoxLayout()
        self.current_tab_index = 0
        self.current_preset_tab = None
        self.setup_presets()
        self.preset_tab_setting_layout.addWidget(self.preset_tab_label)
        self.preset_tab_setting_layout.addWidget(self.preset_tab_comboBox)
        self.preset_tab_setting_layout.addWidget(self.preset_tab_rename_button)
        self.preset_tab_setting_layout.addWidget(self.preset_tab_delete_button)
        self.preset_tab_setting_layout.addWidget(self.preset_tab_set_default_button)
        self.preset_tab_setting_layout.addStretch(200)
        self.preset_tab_setting_layout.addWidget(self.preset_tab_ask_on_start_check_box)
        self.preset_tab_setting_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(stretch=3)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addStretch(stretch=3)

        self.setting_info_layout = QHBoxLayout()
        self.setting_info_layout.addWidget(self.setting_info_text_icon_label, stretch=0)
        self.setting_info_layout.addWidget(self.setting_info_text_label, stretch=1)
        self.setting_info_layout.addWidget(self.setting_donate_button, stretch=0, alignment=Qt.AlignmentFlag.AlignRight)
        self.setting_info_layout.addWidget(self.setting_about_button, stretch=0, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.preset_tab_setting_layout, 0, 0, 1, 1)
        self.main_layout.addWidget(self.current_preset_tab, 1, 0, 1, 1)
        self.main_layout.addLayout(self.setting_info_layout, 2, 0, 1, 1)
        self.main_layout.addLayout(self.buttons_layout, 3, 0, 1, 1)

        self.main_layout.setRowStretch(1, 0)
        self.main_layout.setRowStretch(2, 0)
        self.main_layout.setRowStretch(3, 0)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_presets(self):
        self.preset_tab_comboBox.setCurrentIndex(Options.FavoritePresetId)
        self.preset_tab_comboBox.updateText(self.preset_tab_comboBox.currentText())
        for preset_id in range(len(Options.DefaultPresets)):
            self.preset_tabs.append(PresetTabWidget(Options.DefaultPresets[preset_id]))
            self.preset_counter += 1
        self.current_tab_index = Options.FavoritePresetId
        self.current_preset_tab = self.preset_tabs[self.current_tab_index]
        self.preset_tab_ask_on_start_check_box.setChecked(Options.Choose_Preset_On_Startup)
        self.update_rename_button_current_tab_name()

    def setup_ui(self):
        self.disable_question_mark_window()

    def signal_connect(self):
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        self.preset_tab_comboBox.current_tab_changed_signal.connect(self.change_current_preset_tab)
        self.preset_tab_comboBox.create_new_tab_signal.connect(self.create_new_preset_tab)
        self.preset_tab_delete_button.remove_tab_signal.connect(self.delete_current_tab)
        self.preset_tab_rename_button.rename_tab_signal.connect(self.update_current_preset_name)
        self.preset_tab_set_default_button.set_active_preset_signal.connect(self.update_default_preset)

    def click_yes(self):
        self.result = "Yes"
        self.save_new_settings()
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def save_new_settings(self):
        default_options = []
        for preset_id in range(self.preset_counter):
            temp_default_options = self.preset_tabs[preset_id].get_current_options_as_option_data()
            temp_default_options.Preset_Name = self.preset_tab_comboBox.itemText(preset_id)
            default_options.append(temp_default_options)
        Options.DefaultPresets = default_options.copy()
        Options.Choose_Preset_On_Startup = self.preset_tab_ask_on_start_check_box.isChecked()
        Options.FavoritePresetId = self.preset_tab_comboBox.activated_preset_id
        save_options()

    def change_current_preset_tab(self, tab_index):
        self.main_layout.replaceWidget(self.current_preset_tab, self.preset_tabs[tab_index])
        self.current_preset_tab.hide()
        self.preset_tabs[tab_index].show()
        self.current_preset_tab = self.preset_tabs[tab_index]
        # if tab_index == 0:
        #     self.preset_tab_delete_button.hide()
        # else:
        #     self.preset_tab_delete_button.show()
        self.current_tab_index = tab_index
        self.update_rename_button_current_tab_name()
        if tab_index != self.preset_tab_comboBox.activated_preset_id:
            self.preset_tab_set_default_button.set_activated()
        else:
            self.preset_tab_set_default_button.set_disabled()

    def update_rename_button_current_tab_name(self):
        self.preset_tab_rename_button.current_preset_name = self.preset_tab_comboBox.currentText()

    def create_new_preset_tab(self):
        self.preset_tabs.append(PresetTabWidget(SingleDefaultPresetsData()))
        self.main_layout.replaceWidget(self.current_preset_tab, self.preset_tabs[-1])
        self.current_preset_tab.hide()
        self.preset_tabs[-1].show()
        self.current_preset_tab = self.preset_tabs[-1]
        self.preset_counter += 1
        self.current_tab_index = self.preset_counter - 1
        self.update_rename_button_current_tab_name()
        if self.preset_counter >= 2:
            self.preset_tab_delete_button.show()
        self.preset_tab_set_default_button.set_activated()

    def delete_current_tab(self):
        self.preset_counter -= 1
        index_to_delete = self.current_tab_index
        if index_to_delete != 0:
            to_switch_tab_index = index_to_delete - 1
            self.current_tab_index = to_switch_tab_index
        else:
            to_switch_tab_index = index_to_delete + 1
            self.current_tab_index = index_to_delete
        self.main_layout.replaceWidget(self.preset_tabs[index_to_delete], self.preset_tabs[to_switch_tab_index])
        self.preset_tab_comboBox.delete_tab(index_to_remove=index_to_delete, new_selected_index=self.current_tab_index)
        self.preset_tabs[index_to_delete].hide()
        self.preset_tabs[index_to_delete].deleteLater()
        del self.preset_tabs[index_to_delete]
        self.current_preset_tab = self.preset_tabs[self.current_tab_index]
        self.current_preset_tab.show()
        self.update_rename_button_current_tab_name()
        if self.preset_counter >= 2:
            self.preset_tab_delete_button.show()
        else:
            self.preset_tab_delete_button.hide()

    def update_current_preset_name(self, new_name):
        self.preset_tab_comboBox.setItemText(self.current_tab_index, new_name)
        self.preset_tab_comboBox.updateText(new_name)
        self.update_rename_button_current_tab_name()

    def update_default_preset(self):
        new_default_preset_id = self.preset_tab_comboBox.currentIndex()
        self.preset_tab_set_default_button.set_disabled()
        self.preset_tab_comboBox.set_activated_preset_id(new_default_preset_id)
        self.preset_tab_comboBox.updateText(self.preset_tab_comboBox.currentText())

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedHeight(self.size().height())

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def execute(self):
        if self.preset_counter >= 2:
            self.preset_tab_delete_button.show()
        else:
            self.preset_tab_delete_button.hide()
        self.exec()
