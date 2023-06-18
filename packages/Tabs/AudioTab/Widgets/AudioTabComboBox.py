from PySide2.QtCore import Signal, Qt, QSize, QEvent
from PySide2.QtWidgets import QComboBox, QStyledItemDelegate

from packages.Startup import GlobalIcons
from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.SetupThems import get_dark_palette, get_light_palette
from packages.Tabs.GlobalSetting import GlobalSetting


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignJustify | Qt.AlignCenter


class AudioTabComboBox(QComboBox):
    create_new_tab_signal = Signal()
    current_tab_changed_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.hint_when_enabled = "Audios Groups"
        self.name = "Audio"
        self.hint_when_enabled = "Clear Files"
        self.closeOnLineEditClick = False
        # delegate = AlignDelegate(self)
        # self.setItemDelegate(delegate)
        self.addItem(self.name + " #1")
        self.addItem(GlobalIcons.PlusIcon, "New")
        self.setIconSize(QSize(13, 13))
        self.setEditable(True)
        self.setStyleSheet("QComboBox::pane {border-radius: 5px;}")
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.lineEdit().setContextMenuPolicy(Qt.PreventContextMenu)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().installEventFilter(self)

        # self.setEditable(False)
        self.setToolTip(self.hint_when_enabled)
        self.setMaximumWidth(screen_size.width() // 12)
        self.setMinimumWidth(screen_size.width() // 14)
        self.currentIndexChanged.connect(self.check_selected)

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)

    def check_selected(self, new_selected):
        if self.itemText(new_selected).find("New") != -1:
            self.create_new_tab_signal.emit()
            self.removeItem(self.count() - 1)
            self.addItem(self.name + " #" + str(self.count() + 1))
            self.addItem(GlobalIcons.PlusIcon, "New")
            self.setCurrentIndex(self.count() - 2)

        else:
            self.current_tab_changed_signal.emit(new_selected)

    def disable_select(self):
        self.lineEdit().deselect()

    def eventFilter(self, object, event):
        if str(event.__class__).find("Event") == -1:
            return False
        if str(event.__class__).find("Event") == -1:
            return False
        try:
            if self.isEnabled():
                if object == self.lineEdit():
                    if event.type() == QEvent.MouseButtonRelease:
                        if self.closeOnLineEditClick:
                            self.hidePopup()
                        else:
                            self.showPopup()
                        return True
                    return False
        except Exception as e:
            return False

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def delete_tab(self, index_to_remove):
        self.setCurrentIndex(index_to_remove - 1)
        self.removeItem(index_to_remove)
        for i in range(self.count() - 1):
            self.setItemText(i, self.name + " #" + str(i + 1))

    def hide_new_tab_option(self):
        if self.itemText(self.count() - 1).find("New") != -1:
            self.removeItem(self.count() - 1)

    def show_new_tab_option(self):
        if self.itemText(self.count() - 1).find("New") == -1:
            self.addItem(GlobalIcons.PlusIcon, "New")

    def update_theme_mode_state(self):
        if Options.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet("QComboBox::pane {border-radius: 5px;}")
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
