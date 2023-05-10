from PySide2 import QtGui
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, \
    QDialog, QPushButton, QHBoxLayout, QDoubleSpinBox, QComboBox, QLineEdit, QCheckBox, \
    QFormLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Startup.DefaultOptions import DefaultOptions
from packages.Widgets.InfoCellDialogTabComboBox import InfoCellDialogTabComboBox


class AudioInfoDialog(QDialog):
    def __init__(self, audios_name,
                 audios_delay, audios_language, audios_track_name,
                 audios_set_default, audios_set_forced
                 , audios_default_value_delay, audios_default_value_language,
                 audios_default_value_track_name, audios_default_value_set_default,
                 audios_default_value_set_forced, audio_set_default_disabled=False,
                 audio_set_forced_disabled=False, disable_edit=False, parent=None):
        super().__init__(parent)
        self.window_title = "Audio Info"
        self.state = "no"
        self.audios_count = len(audios_delay)

        self.messageIcon = QLabel()
        self.audio_tab_comboBox = InfoCellDialogTabComboBox(hint="Audios Groups")
        for i in range(self.audios_count):
            self.audio_tab_comboBox.addItem("Audio #" + str(i + 1))
        self.audio_tab_comboBox.setCurrentIndex(0)
        self.audio_tab_comboBox.currentIndexChanged.connect(self.update_current_audio_index)
        self.current_audio_index = 0

        self.disable_edit = disable_edit
        self.current_audio_name = audios_name
        self.current_audio_language = audios_language
        self.current_audio_delay = audios_delay
        self.current_audio_track_name = audios_track_name
        self.current_audio_set_default = audios_set_default
        self.current_audio_set_forced = audios_set_forced

        self.default_audio_language = audios_default_value_language
        self.default_audio_delay = audios_default_value_delay
        self.default_audio_track_name = audios_default_value_track_name
        self.default_audio_set_default = audios_default_value_set_default
        self.default_audio_set_forced = audios_default_value_set_forced

        self.audio_set_default_disabled = audio_set_default_disabled
        self.audio_set_forced_disabled = audio_set_forced_disabled

        self.audio_name_label = QLabel("Audio Name:")
        self.audio_name_value = QLabel(str(self.current_audio_name[self.current_audio_index]))
        width_to_be_fixed = 0
        for i in range(len(self.current_audio_name)):
            width_to_be_fixed = max(width_to_be_fixed, self.audio_name_value.fontMetrics().boundingRect(
                self.current_audio_name[i]).width())
        self.audio_name_value.setFixedWidth(width_to_be_fixed + 10)
        self.audio_delay_label = QLabel("Audio Delay:")
        self.audio_delay_spin = QDoubleSpinBox()
        self.setup_audio_delay_spin()

        self.audio_language_label = QLabel("Audio Language:")
        self.audio_language_comboBox = QComboBox()
        self.setup_audio_language_comboBox()

        self.audio_track_name_label = QLabel("Audio Track Name:")
        self.audio_track_name_lineEdit = QLineEdit()
        self.setup_audio_track_name_lineEdit()

        self.audio_set_forced_label = QLabel("Audio Forced State:")
        self.audio_set_forced_checkBox = QCheckBox()
        self.setup_audio_set_forced_checkBox()

        self.audio_set_default_label = QLabel("Audio Default State:")
        self.audio_set_default_checkBox = QCheckBox()
        self.setup_audio_set_default_checkBox()

        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")
        self.reset_button = QPushButton("Reset To Default")

        self.buttons_layout = QHBoxLayout()
        self.audio_delay_layout = QHBoxLayout()
        self.audio_language_layout = QHBoxLayout()
        self.audio_track_name_layout = QHBoxLayout()
        self.audio_set_default_layout = QHBoxLayout()
        self.audio_set_forced_layout = QHBoxLayout()
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.buttons_layout.addWidget(self.reset_button, stretch=2)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.audio_setting_layout = QGridLayout()
        self.audio_editable_setting_layout = QFormLayout()
        self.audio_editable_setting_layout.addRow(self.audio_name_label, self.audio_name_value)
        self.audio_editable_setting_layout.addRow(self.audio_track_name_label,
                                                  self.audio_track_name_lineEdit)
        self.audio_editable_setting_layout.addRow(self.audio_language_label,
                                                  self.audio_language_comboBox)
        self.audio_editable_setting_layout.addRow(self.audio_delay_label, self.audio_delay_spin)
        self.audio_editable_setting_layout.addRow(self.audio_set_default_label,
                                                  self.audio_set_default_checkBox)
        self.audio_editable_setting_layout.addRow(self.audio_set_forced_label,
                                                  self.audio_set_forced_checkBox)
        self.audio_setting_layout.addWidget(self.audio_tab_comboBox, 0, 0)
        self.audio_setting_layout.addLayout(self.audio_editable_setting_layout, 1, 0, 5, 2)
        self.audio_setting_layout.addWidget(self.messageIcon, 1, 3, 5, -1)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.audio_setting_layout, 0, 0, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.AudioIconPath).scaledToHeight(100))
        self.set_dialog_values()
        self.set_default_buttons()
        if self.audio_set_default_disabled:
            self.audio_set_default_disable()
        if self.audio_set_forced_disabled:
            self.audio_set_forced_disable()
        if self.disable_edit:
            self.audio_track_name_lineEdit.setEnabled(False)
            self.audio_language_comboBox.setEnabled(False)
            self.audio_delay_spin.setEnabled(False)
            self.audio_set_default_checkBox.setEnabled(False)
            self.audio_set_forced_checkBox.setEnabled(False)
            self.reset_button.setEnabled(False)

        self.setup_tool_tip_hint_audio_set_default()
        self.setup_tool_tip_hint_audio_set_forced()

    def signal_connect(self):
        self.audio_track_name_lineEdit.textEdited.connect(self.update_current_audio_track_name)
        self.audio_delay_spin.editingFinished.connect(self.update_current_audio_delay)
        self.audio_language_comboBox.currentTextChanged.connect(self.update_current_audio_language)
        self.audio_set_default_checkBox.stateChanged.connect(self.update_current_audio_set_default)
        self.audio_set_forced_checkBox.stateChanged.connect(self.update_current_audio_set_forced)
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        self.reset_button.clicked.connect(self.reset_audio_setting)

    def click_yes(self):
        self.state = "yes"
        self.close()

    def click_no(self):
        self.state = "no"
        self.close()

    def set_dialog_values(self):
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(GlobalIcons.InfoSettingIcon)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_default_buttons(self):
        self.yes_button.setDefault(True)
        self.yes_button.setFocus()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def setup_audio_track_name_lineEdit(self):
        self.audio_track_name_lineEdit.setClearButtonEnabled(True)
        self.audio_track_name_lineEdit.setText(self.current_audio_track_name[self.current_audio_index])

    def setup_audio_language_comboBox(self):
        self.audio_language_comboBox.addItems(DefaultOptions.Default_Favorite_Audio_Languages)
        self.audio_language_comboBox.setCurrentIndex(
            DefaultOptions.Default_Favorite_Audio_Languages.index(
                self.current_audio_language[self.current_audio_index]))
        self.audio_language_comboBox.setMaxVisibleItems(8)
        self.audio_language_comboBox.setStyleSheet("QComboBox { combobox-popup: 0; }")

    def setup_audio_delay_spin(self):
        # self.audio_delay_spin.setMaximumWidth(screen_size.width() // 16)
        self.audio_delay_spin.setDecimals(3)
        self.audio_delay_spin.setMinimum(-9999.0)
        self.audio_delay_spin.setMaximum(9999.0)
        self.audio_delay_spin.setSingleStep(0.5)
        self.audio_delay_spin.setValue(float(self.current_audio_delay[self.current_audio_index]))

    def setup_audio_set_default_checkBox(self):
        self.audio_set_default_checkBox.setText("Set Default")
        self.audio_set_default_checkBox.setChecked(
            bool(self.current_audio_set_default[self.current_audio_index]))

    def setup_audio_set_forced_checkBox(self):
        self.audio_set_forced_checkBox.setText("Set Forced")
        self.audio_set_forced_checkBox.setChecked(
            bool(self.current_audio_set_forced[self.current_audio_index]))

    def update_current_audio_track_name(self):
        self.current_audio_track_name[self.current_audio_index] = str(self.audio_track_name_lineEdit.text())

    def update_current_audio_delay(self):
        self.current_audio_delay[self.current_audio_index] = round(self.audio_delay_spin.value(), 5)

    def update_current_audio_language(self):
        self.current_audio_language[self.current_audio_index] = str(self.audio_language_comboBox.currentText())

    def update_current_audio_set_default(self):
        new_state = self.audio_set_default_checkBox.checkState() == Qt.Checked
        self.current_audio_set_default[self.current_audio_index] = new_state
        if new_state:
            for i in range(len(self.current_audio_set_default)):
                if i != self.current_audio_index:
                    self.current_audio_set_default[i] = False

    def update_current_audio_set_forced(self):
        new_state = self.audio_set_forced_checkBox.checkState() == Qt.Checked
        self.current_audio_set_forced[self.current_audio_index] = new_state
        if new_state:
            for i in range(len(self.current_audio_set_forced)):
                if i != self.current_audio_index:
                    self.current_audio_set_forced[i] = False

    def reset_audio_setting(self):
        self.current_audio_language[self.current_audio_index] = self.default_audio_language[
            self.current_audio_index]
        self.current_audio_delay[self.current_audio_index] = self.default_audio_delay[
            self.current_audio_index]
        self.current_audio_track_name[self.current_audio_index] = self.default_audio_track_name[
            self.current_audio_index]
        self.current_audio_set_default[self.current_audio_index] = self.default_audio_set_default[
            self.current_audio_index]
        self.current_audio_set_forced[self.current_audio_index] = self.default_audio_set_forced[
            self.current_audio_index]

        self.audio_language_comboBox.setCurrentIndex(
            DefaultOptions.Default_Favorite_Audio_Languages.index(
                self.current_audio_language[self.current_audio_index]))
        self.audio_delay_spin.setValue(float(self.current_audio_delay[self.current_audio_index]))
        self.audio_track_name_lineEdit.setText(self.current_audio_track_name[self.current_audio_index])
        self.audio_set_default_checkBox.setChecked(
            bool(self.current_audio_set_default[self.current_audio_index]))
        self.audio_set_forced_checkBox.setChecked(
            bool(self.current_audio_set_forced[self.current_audio_index]))

    def audio_set_default_disable(self):
        self.audio_set_default_checkBox.setDisabled(True)

    def audio_set_forced_disable(self):
        self.audio_set_forced_checkBox.setDisabled(True)

    def setup_tool_tip_hint_audio_set_default(self):
        if self.audio_set_default_checkBox.isEnabled():
            self.audio_set_default_checkBox.setToolTip("<nobr>set this audio to be the default audio track "
                                                       "when play")
            self.audio_set_default_checkBox.setToolTipDuration(12000)
        else:
            self.audio_set_default_checkBox.setToolTip(
                "<nobr>set this audio to be the default audio track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this audio default</b> is enabled on mux setting tab ")
            self.audio_set_default_checkBox.setToolTipDuration(12000)

    def setup_tool_tip_hint_audio_set_forced(self):
        if self.audio_set_forced_checkBox.isEnabled():
            self.audio_set_forced_checkBox.setToolTip("<nobr>set this audio to be the forced audio track when "
                                                      "play")
            self.audio_set_forced_checkBox.setToolTipDuration(12000)
        else:
            self.audio_set_forced_checkBox.setToolTip(
                "<nobr>set this audio to be the forced audio track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this audio default and forced</b> is enabled on mux setting tab ")
            self.audio_set_forced_checkBox.setToolTipDuration(12000)

    def update_current_audio_index(self, new_index):
        self.current_audio_index = new_index
        self.audio_delay_spin.setValue(float(self.current_audio_delay[self.current_audio_index]))
        self.audio_set_default_checkBox.setChecked(
            bool(self.current_audio_set_default[self.current_audio_index]))
        self.audio_set_forced_checkBox.setChecked(
            bool(self.current_audio_set_forced[self.current_audio_index]))
        self.audio_language_comboBox.setCurrentIndex(
            DefaultOptions.Default_Favorite_Audio_Languages.index(
                self.current_audio_language[self.current_audio_index]))
        self.audio_track_name_lineEdit.setText(self.current_audio_track_name[self.current_audio_index])
        self.audio_name_value.setText(str(self.current_audio_name[self.current_audio_index]))

    def execute(self):
        self.exec_()
