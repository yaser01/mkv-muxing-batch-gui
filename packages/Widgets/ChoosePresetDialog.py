from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QHBoxLayout,QGridLayout, QLabel, QPushButton, QComboBox, QCheckBox

from packages.Startup import GlobalIcons
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.Options import Options
from packages.Widgets.MyDialog import MyDialog


class ChoosePresetDialog(MyDialog):
    def __init__(self, preset_list, favorite_preset_id, parent=None):
        super().__init__(parent)
        self.message = QLabel()
        self.message.setText("Presets: ")
        self.extra_message = QLabel()
        self.choose_button = QPushButton("Choose Preset")
        self.default_preset_button = QPushButton("Use Default")
        self.favorite_preset_id = favorite_preset_id
        self.buttonLayout = QHBoxLayout()
        # self.buttonLayout.addWidget(self.blank_preset_button)
        self.buttonLayout.addWidget(QLabel(), stretch=1)
        self.buttonLayout.addWidget(self.choose_button, stretch=3)
        self.buttonLayout.addWidget(self.default_preset_button, stretch=3)
        self.buttonLayout.addWidget(QLabel(), stretch=1)

        self.preset_comboBox = QComboBox()
        self.preset_comboBox.setMaximumWidth(screen_size.width() // 9)
        self.preset_comboBox.setMinimumWidth(screen_size.width() // 14)
        self.preset_comboBox_add_items(preset_list)
        self.preset_comboBox.setCurrentIndex(0)
        self.preset_comboBox.setMaxVisibleItems(8)
        self.preset_comboBox.setStyleSheet("QComboBox { combobox-popup: 0; }")

        self.remember_my_choice_checkbox = QCheckBox("Remember this choice")

        self.preset_layout = QHBoxLayout()
        self.preset_layout.addWidget(self.message)
        self.preset_layout.addWidget(self.preset_comboBox, stretch=3)
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.preset_layout, 0, 0, 1, -1)
        self.main_layout.addWidget(self.remember_my_choice_checkbox, 2, 0, 1, -1,
                                   alignment=Qt.AlignmentFlag.AlignCenter)
        # self.main_layout.addWidget(self.extra_message, 1, 0, 1, 2)
        self.main_layout.addLayout(self.buttonLayout, 3, 0, -1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(13, 13, 13, 13)
        self.setLayout(self.main_layout)

        self.result = "Fresh"
        self.remember = False
        self.chosen_index = -1
        self.setup_ui()
        self.signal_connect()

    def preset_comboBox_set_icon_for_non_active_preset(self, item_index):
        if Options.Dark_Mode:
            self.preset_comboBox.setItemIcon(item_index, GlobalIcons.PresetDarkIcon)
        else:
            self.preset_comboBox.setItemIcon(item_index, GlobalIcons.PresetLightIcon)

    def preset_comboBox_add_items(self, items):
        self.preset_comboBox.setIconSize(QSize(16, 16))
        for item_index in range(len(items)):
            if self.favorite_preset_id == item_index:
                self.preset_comboBox.addItem(GlobalIcons.SelectedItemIcon, items[item_index])
            else:
                self.preset_comboBox.addItem(GlobalIcons.UnSelectedItemIcon, items[item_index])

    def setup_ui(self):
        self.disable_question_mark_window()
        self.reset_dialog_values()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.choose_button.clicked.connect(self.click_on_choose_preset)
        self.default_preset_button.clicked.connect(self.click_default_start)
        pass

    def click_on_choose_preset(self):
        self.result = "Preset"
        self.remember = self.remember_my_choice_checkbox.isChecked()
        self.chosen_index = self.preset_comboBox.currentIndex()
        self.close()

    def click_default_start(self):
        self.result = "Default"
        self.remember = self.remember_my_choice_checkbox.isChecked()
        self.chosen_index = -1
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint,on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)
        self.extra_message.setFont(message_font)

    def reset_dialog_values(self):
        self.setWindowTitle("Startup Preset")  # determine when use
        self.extra_message.setText("")  # determine when use

    def set_default_buttons(self):
        self.choose_button.setDefault(True)
        self.default_preset_button.setDefault(False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()