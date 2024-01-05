from PySide6.QtCore import Signal, Qt, QSize, QEvent
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate

from packages.Startup import GlobalIcons
from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.SetupThems import get_dark_palette, get_light_palette


class PresetTabComboBox(QComboBox):
    create_new_tab_signal = Signal()
    current_tab_changed_signal = Signal(int)

    def __init__(self, items, activated_preset_id):
        super().__init__()
        self.hint_when_enabled = "Preset Groups"
        self.name = "Preset"
        self.hint_when_enabled = "Preset Name"
        self.closeOnLineEditClick = False
        self.activated_preset_id = activated_preset_id
        self.setup_items(items=items)
        self.setIconSize(QSize(16, 16))
        self.setEditable(True)
        self.setStyleSheet("QComboBox::pane {border-radius: 5px;}")
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.lineEdit().setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().installEventFilter(self)
        self.setToolTip(self.hint_when_enabled)
        self.setMaximumWidth(screen_size.width() // 7)
        self.setMinimumWidth(screen_size.width() // 14)
        self.activated.connect(self.check_selected)

    def set_activated_preset_id(self, new_activated_preset_id):
        self.activated_preset_id = new_activated_preset_id

    def setup_items(self, items):
        for item_index in range(len(items)):
            if self.activated_preset_id == item_index:
                self.addItem(GlobalIcons.SelectedItemIcon, items[item_index])
            else:
                self.addItem(GlobalIcons.UnSelectedItemIcon, items[item_index])
        self.addItem(GlobalIcons.PlusIcon, "New Preset")

    def check_selected(self, new_selected):
        new_text = self.itemText(new_selected)
        if new_selected == self.count() - 1:
            self.create_new_tab_signal.emit()
            self.removeItem(self.count() - 1)
            self.addItem(self.name + " #" + str(self.count() + 1))
            new_text = self.name + " #" + str(self.count() + 1)
            self.addItem(GlobalIcons.PlusIcon, "New Preset")
            self.setCurrentIndex(self.count() - 2)
        self.current_tab_changed_signal.emit(new_selected)

        self.updateText(new_text)

    def disable_select(self):
        self.lineEdit().deselect()

    def eventFilter(self, object, event):
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
        for item_index in range(self.count() - 1):
            if self.activated_preset_id == item_index:
                self.setItemIcon(item_index, GlobalIcons.SelectedItemIcon)
            else:
                self.setItemIcon(item_index, GlobalIcons.UnSelectedItemIcon)
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it

        self.closeOnLineEditClick = True

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def delete_tab(self, index_to_remove, new_selected_index):
        self.setCurrentIndex(new_selected_index)
        self.removeItem(index_to_remove)
        if self.activated_preset_id >= index_to_remove:
            self.activated_preset_id -= 1

    def hide_new_tab_option(self):
        if self.itemText(self.count() - 1).find("New") != -1:
            self.removeItem(self.count() - 1)

    def show_new_tab_option(self):
        if self.itemText(self.count() - 1).find("New") == -1:
            self.addItem(GlobalIcons.PlusIcon, "New Preset")

    def update_theme_mode_state(self):
        if Options.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet("QComboBox::pane {border-radius: 5px;}")
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")

    def updateText(self, new_text):
        text = new_text
        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.lineEdit().width())
        if elided_text != "":
            self.lineEdit().setText(elided_text)
            if self.activated_preset_id == self.currentIndex():
                self.setItemIcon(self.currentIndex(), GlobalIcons.SelectedItemIcon)
            else:
                self.setItemIcon(self.currentIndex(), GlobalIcons.UnSelectedItemIcon)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateText(self.currentText())
