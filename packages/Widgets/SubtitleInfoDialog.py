from PySide2 import QtGui
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, \
     QPushButton, QHBoxLayout, QDoubleSpinBox, QComboBox, QLineEdit, QCheckBox, \
    QFormLayout

from packages.Startup import GlobalFiles
from packages.Startup import GlobalIcons
from packages.Startup.Options import Options
from packages.Widgets.InfoCellDialogTabComboBox import InfoCellDialogTabComboBox
from packages.Widgets.MyDialog import MyDialog


class SubtitleInfoDialog(MyDialog):
    def __init__(self, subtitles_name,
                 subtitles_delay, subtitles_language, subtitles_track_name,
                 subtitles_set_default, subtitles_set_forced
                 , subtitles_default_value_delay, subtitles_default_value_language,
                 subtitles_default_value_track_name, subtitles_default_value_set_default,
                 subtitles_default_value_set_forced, subtitle_set_default_disabled=False,
                 subtitle_set_forced_disabled=False, disable_edit=False, parent=None):
        super().__init__(parent)
        self.window_title = "Subtitle Info"
        self.state = "no"
        self.subtitles_count = len(subtitles_delay)

        self.messageIcon = QLabel()
        self.subtitle_tab_comboBox = InfoCellDialogTabComboBox(hint="Subtitles Groups")
        for i in range(self.subtitles_count):
            self.subtitle_tab_comboBox.addItem("Subtitle #" + str(i + 1))
        self.subtitle_tab_comboBox.setCurrentIndex(0)
        self.subtitle_tab_comboBox.currentIndexChanged.connect(self.update_current_subtitle_index)
        self.current_subtitle_index = 0

        self.disable_edit = disable_edit
        self.current_subtitle_name = subtitles_name
        self.current_subtitle_language = subtitles_language
        self.current_subtitle_delay = subtitles_delay
        self.current_subtitle_track_name = subtitles_track_name
        self.current_subtitle_set_default = subtitles_set_default
        self.current_subtitle_set_forced = subtitles_set_forced

        self.default_subtitle_language = subtitles_default_value_language
        self.default_subtitle_delay = subtitles_default_value_delay
        self.default_subtitle_track_name = subtitles_default_value_track_name
        self.default_subtitle_set_default = subtitles_default_value_set_default
        self.default_subtitle_set_forced = subtitles_default_value_set_forced

        self.subtitle_set_default_disabled = subtitle_set_default_disabled
        self.subtitle_set_forced_disabled = subtitle_set_forced_disabled

        self.subtitle_name_label = QLabel("Subtitle Name:")
        self.subtitle_name_value = QLabel(str(self.current_subtitle_name[self.current_subtitle_index]))
        width_to_be_fixed = 0
        for i in range(len(self.current_subtitle_name)):
            width_to_be_fixed = max(width_to_be_fixed, self.subtitle_name_value.fontMetrics().boundingRect(
                self.current_subtitle_name[i]).width())
        self.subtitle_name_value.setFixedWidth(width_to_be_fixed + 10)
        self.subtitle_delay_label = QLabel("Subtitle Delay:")
        self.subtitle_delay_spin = QDoubleSpinBox()
        self.setup_subtitle_delay_spin()

        self.subtitle_language_label = QLabel("Subtitle Language:")
        self.subtitle_language_comboBox = QComboBox()
        self.setup_subtitle_language_comboBox()

        self.subtitle_track_name_label = QLabel("Subtitle Track Name:")
        self.subtitle_track_name_lineEdit = QLineEdit()
        self.setup_subtitle_track_name_lineEdit()

        self.subtitle_set_forced_label = QLabel("Subtitle Forced State:")
        self.subtitle_set_forced_checkBox = QCheckBox()
        self.setup_subtitle_set_forced_checkBox()

        self.subtitle_set_default_label = QLabel("Subtitle Default State:")
        self.subtitle_set_default_checkBox = QCheckBox()
        self.setup_subtitle_set_default_checkBox()

        self.yes_button = QPushButton("OK")
        self.no_button = QPushButton("Cancel")
        self.reset_button = QPushButton("Reset To Default")

        self.buttons_layout = QHBoxLayout()
        self.subtitle_delay_layout = QHBoxLayout()
        self.subtitle_language_layout = QHBoxLayout()
        self.subtitle_track_name_layout = QHBoxLayout()
        self.subtitle_set_default_layout = QHBoxLayout()
        self.subtitle_set_forced_layout = QHBoxLayout()
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.buttons_layout.addWidget(self.reset_button, stretch=2)
        self.buttons_layout.addWidget(self.yes_button, stretch=2)
        self.buttons_layout.addWidget(self.no_button, stretch=2)
        self.buttons_layout.addWidget(QLabel(""), stretch=3)
        self.subtitle_setting_layout = QGridLayout()
        self.subtitle_editable_setting_layout = QFormLayout()
        self.subtitle_editable_setting_layout.addRow(self.subtitle_name_label, self.subtitle_name_value)
        self.subtitle_editable_setting_layout.addRow(self.subtitle_track_name_label,
                                                     self.subtitle_track_name_lineEdit)
        self.subtitle_editable_setting_layout.addRow(self.subtitle_language_label,
                                                     self.subtitle_language_comboBox)
        self.subtitle_editable_setting_layout.addRow(self.subtitle_delay_label, self.subtitle_delay_spin)
        self.subtitle_editable_setting_layout.addRow(self.subtitle_set_default_label,
                                                     self.subtitle_set_default_checkBox)
        self.subtitle_editable_setting_layout.addRow(self.subtitle_set_forced_label,
                                                     self.subtitle_set_forced_checkBox)
        self.subtitle_setting_layout.addWidget(self.subtitle_tab_comboBox, 0, 0)
        self.subtitle_setting_layout.addLayout(self.subtitle_editable_setting_layout, 1, 0, 5, 2)
        self.subtitle_setting_layout.addWidget(self.messageIcon, 1, 3, 5, -1)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.subtitle_setting_layout, 0, 0, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 0, 1, -1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        if Options.Dark_Mode:
            subtitle_icon_path = GlobalFiles.SubtitleDarkIconPath
        else:
            subtitle_icon_path = GlobalFiles.SubtitleLightIconPath
        self.messageIcon.setPixmap(QtGui.QPixmap(subtitle_icon_path).scaledToHeight(100))
        self.set_dialog_values()
        self.set_default_buttons()
        if self.subtitle_set_default_disabled:
            self.subtitle_set_default_disable()
        if self.subtitle_set_forced_disabled:
            self.subtitle_set_forced_disable()
        if self.disable_edit:
            self.subtitle_track_name_lineEdit.setEnabled(False)
            self.subtitle_language_comboBox.setEnabled(False)
            self.subtitle_delay_spin.setEnabled(False)
            self.subtitle_set_default_checkBox.setEnabled(False)
            self.subtitle_set_forced_checkBox.setEnabled(False)
            self.reset_button.setEnabled(False)

        self.setup_tool_tip_hint_subtitle_set_default()
        self.setup_tool_tip_hint_subtitle_set_forced()

    def signal_connect(self):
        self.subtitle_track_name_lineEdit.textEdited.connect(self.update_current_subtitle_track_name)
        self.subtitle_delay_spin.editingFinished.connect(self.update_current_subtitle_delay)
        self.subtitle_language_comboBox.currentTextChanged.connect(self.update_current_subtitle_language)
        self.subtitle_set_default_checkBox.stateChanged.connect(self.update_current_subtitle_set_default)
        self.subtitle_set_forced_checkBox.stateChanged.connect(self.update_current_subtitle_set_forced)
        self.yes_button.clicked.connect(self.click_yes)
        self.no_button.clicked.connect(self.click_no)
        self.reset_button.clicked.connect(self.reset_subtitle_setting)

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

    def setup_subtitle_track_name_lineEdit(self):
        self.subtitle_track_name_lineEdit.setClearButtonEnabled(True)
        self.subtitle_track_name_lineEdit.setText(self.current_subtitle_track_name[self.current_subtitle_index])

    def setup_subtitle_language_comboBox(self):
        self.subtitle_language_comboBox.addItems(Options.Default_Favorite_Subtitle_Languages)
        self.subtitle_language_comboBox.setCurrentIndex(
            Options.Default_Favorite_Subtitle_Languages.index(
                self.current_subtitle_language[self.current_subtitle_index]))
        self.subtitle_language_comboBox.setMaxVisibleItems(8)
        self.subtitle_language_comboBox.setStyleSheet("QComboBox { combobox-popup: 0; }")

    def setup_subtitle_delay_spin(self):
        # self.subtitle_delay_spin.setMaximumWidth(screen_size.width() // 16)
        self.subtitle_delay_spin.setDecimals(3)
        self.subtitle_delay_spin.setMinimum(-9999.0)
        self.subtitle_delay_spin.setMaximum(9999.0)
        self.subtitle_delay_spin.setSingleStep(0.5)
        self.subtitle_delay_spin.setValue(float(self.current_subtitle_delay[self.current_subtitle_index]))

    def setup_subtitle_set_default_checkBox(self):
        self.subtitle_set_default_checkBox.setText("Set Default")
        self.subtitle_set_default_checkBox.setChecked(
            bool(self.current_subtitle_set_default[self.current_subtitle_index]))

    def setup_subtitle_set_forced_checkBox(self):
        self.subtitle_set_forced_checkBox.setText("Set Forced")
        self.subtitle_set_forced_checkBox.setChecked(
            bool(self.current_subtitle_set_forced[self.current_subtitle_index]))

    def update_current_subtitle_track_name(self):
        self.current_subtitle_track_name[self.current_subtitle_index] = str(self.subtitle_track_name_lineEdit.text())

    def update_current_subtitle_delay(self):
        self.current_subtitle_delay[self.current_subtitle_index] = round(self.subtitle_delay_spin.value(), 5)

    def update_current_subtitle_language(self):
        self.current_subtitle_language[self.current_subtitle_index] = str(self.subtitle_language_comboBox.currentText())

    def update_current_subtitle_set_default(self):
        new_state = self.subtitle_set_default_checkBox.checkState() == Qt.Checked
        self.current_subtitle_set_default[self.current_subtitle_index] = new_state
        if new_state:
            for i in range(len(self.current_subtitle_set_default)):
                if i != self.current_subtitle_index:
                    self.current_subtitle_set_default[i] = False

    def update_current_subtitle_set_forced(self):
        new_state = self.subtitle_set_forced_checkBox.checkState() == Qt.Checked
        self.current_subtitle_set_forced[self.current_subtitle_index] = new_state
        if new_state:
            for i in range(len(self.current_subtitle_set_forced)):
                if i != self.current_subtitle_index:
                    self.current_subtitle_set_forced[i] = False

    def reset_subtitle_setting(self):
        self.current_subtitle_language[self.current_subtitle_index] = self.default_subtitle_language[
            self.current_subtitle_index]
        self.current_subtitle_delay[self.current_subtitle_index] = self.default_subtitle_delay[
            self.current_subtitle_index]
        self.current_subtitle_track_name[self.current_subtitle_index] = self.default_subtitle_track_name[
            self.current_subtitle_index]
        self.current_subtitle_set_default[self.current_subtitle_index] = self.default_subtitle_set_default[
            self.current_subtitle_index]
        self.current_subtitle_set_forced[self.current_subtitle_index] = self.default_subtitle_set_forced[
            self.current_subtitle_index]

        self.subtitle_language_comboBox.setCurrentIndex(
            Options.Default_Favorite_Subtitle_Languages.index(
                self.current_subtitle_language[self.current_subtitle_index]))
        self.subtitle_delay_spin.setValue(float(self.current_subtitle_delay[self.current_subtitle_index]))
        self.subtitle_track_name_lineEdit.setText(self.current_subtitle_track_name[self.current_subtitle_index])
        self.subtitle_set_default_checkBox.setChecked(
            bool(self.current_subtitle_set_default[self.current_subtitle_index]))
        self.subtitle_set_forced_checkBox.setChecked(
            bool(self.current_subtitle_set_forced[self.current_subtitle_index]))

    def subtitle_set_default_disable(self):
        self.subtitle_set_default_checkBox.setDisabled(True)

    def subtitle_set_forced_disable(self):
        self.subtitle_set_forced_checkBox.setDisabled(True)

    def setup_tool_tip_hint_subtitle_set_default(self):
        if self.subtitle_set_default_checkBox.isEnabled():
            self.subtitle_set_default_checkBox.setToolTip("<nobr>set this subtitle to be the default subtitle track "
                                                          "when play")
            self.subtitle_set_default_checkBox.setToolTipDuration(12000)
        else:
            self.subtitle_set_default_checkBox.setToolTip(
                "<nobr>set this subtitle to be the default subtitle track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this subtitle default</b> is enabled on mux setting tab ")
            self.subtitle_set_default_checkBox.setToolTipDuration(12000)

    def setup_tool_tip_hint_subtitle_set_forced(self):
        if self.subtitle_set_forced_checkBox.isEnabled():
            self.subtitle_set_forced_checkBox.setToolTip("<nobr>set this subtitle to be the forced subtitle track when "
                                                         "play")
            self.subtitle_set_forced_checkBox.setToolTipDuration(12000)
        else:
            self.subtitle_set_forced_checkBox.setToolTip(
                "<nobr>set this subtitle to be the forced subtitle track when play<br><b>Disabled</b> because "
                "option "
                "<b>make this subtitle default and forced</b> is enabled on mux setting tab ")
            self.subtitle_set_forced_checkBox.setToolTipDuration(12000)

    def update_current_subtitle_index(self, new_index):
        self.current_subtitle_index = new_index
        self.subtitle_delay_spin.setValue(float(self.current_subtitle_delay[self.current_subtitle_index]))
        self.subtitle_set_default_checkBox.setChecked(
            bool(self.current_subtitle_set_default[self.current_subtitle_index]))
        self.subtitle_set_forced_checkBox.setChecked(
            bool(self.current_subtitle_set_forced[self.current_subtitle_index]))
        self.subtitle_language_comboBox.setCurrentIndex(
            Options.Default_Favorite_Subtitle_Languages.index(
                self.current_subtitle_language[self.current_subtitle_index]))
        self.subtitle_track_name_lineEdit.setText(self.current_subtitle_track_name[self.current_subtitle_index])
        self.subtitle_name_value.setText(str(self.current_subtitle_name[self.current_subtitle_index]))

    def execute(self):
        self.exec_()
