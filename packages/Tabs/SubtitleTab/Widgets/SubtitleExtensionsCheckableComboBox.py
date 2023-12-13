import os

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox

from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllSubtitlesExtensions
from packages.Tabs.GlobalSetting import GlobalSetting, get_files_names_absolute_list, sort_names_like_windows
from packages.Tabs.SubtitleTab.Widgets.ReloadSubtitleFilesDialog import ReloadSubtitleFilesDialog


class SubtitleExtensionsCheckableComboBox(QComboBox):
    # Subclass Delegate to increase item height
    close_list = QtCore.Signal(list)

    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            s = size.height() * 4 // 3
            size.setHeight(int(s))
            return size

    def __init__(self):
        super().__init__()
        # Make the combo editable to set a custom text, but readonly
        self.hint = ""
        self.hint_when_enabled = ""
        self.current_folder_path = ""
        self.current_files_list = ""
        self.current_extensions = []
        self.current_extensions = Options.CurrentPreset.Default_Subtitle_Extensions
        self.is_there_old_files = False
        self.closeOnLineEditClick = False
        # Use custom delegate
        self.setItemDelegate(SubtitleExtensionsCheckableComboBox.Delegate())
        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)
        # Hide and show popup when clicking the line edit

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)
        self.setup_ui()

    def set_current_extensions(self):
        self.clear()
        self.current_extensions = Options.CurrentPreset.Default_Subtitle_Extensions
        self.addItems(AllSubtitlesExtensions)
        self.make_default_extensions_checked()

    def setup_ui(self):
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.lineEdit().installEventFilter(self)
        self.setMinimumWidth(screen_size.width() // 14)
        self.addItems(AllSubtitlesExtensions)
        self.make_default_extensions_checked()

    def make_default_extensions_checked(self):
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() in Options.CurrentPreset.Default_Subtitle_Extensions:
                self.model().item(i).setCheckState(Qt.CheckState.Checked)
        self.updateText()

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def set_current_folder_path(self, new_path):
        self.current_folder_path = new_path

    def set_current_files_list(self, new_list):
        self.current_files_list = new_list

    def disable_select(self):
        self.lineEdit().deselect()

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

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

                if object == self.view().viewport():
                    if event.type() == QEvent.MouseButtonRelease:
                        index = self.view().indexAt(event.pos())
                        item = self.model().item(index.row())
                        if item.checkState() == Qt.CheckState.Checked:
                            item.setCheckState(Qt.CheckState.Unchecked)
                        else:
                            item.setCheckState(Qt.CheckState.Checked)
                        return True
                return False
            else:
                return False
        except Exception as e:
            return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()
        self.check_if_nothing_selected()
        self.check_extensions_changes()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        extensions_text = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                extensions_text.append(self.model().item(i).text())

        text = ', '.join(extensions_text)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(text, Qt.TextElideMode.ElideRight, self.lineEdit().width())
        if elided_text != "":
            non_italic_font = self.lineEdit().font()
            non_italic_font.setItalic(False)
            self.lineEdit().setFont(non_italic_font)
            self.lineEdit().setText(elided_text)
            self.hint = "<nobr>Extensions: [" + text + "]"
        self.setToolTip(self.hint)

    def addItem(self, text, data=None):
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                res.append(self.model().item(i).data())
        return res

    def setData(self, texts):
        for i in range(self.model().rowCount()):
            if self.model().item(i).data() in texts:
                self.model().item(i).setCheckState(Qt.CheckState.Checked)
            else:
                self.model().item(i).setCheckState(Qt.CheckState.Unchecked)

    def check_if_nothing_selected(self):
        count = 0
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.CheckState.Checked:
                count += 1
        if count == 0:
            for i in range(self.model().rowCount()):
                if self.model().item(i).text() in Options.CurrentPreset.Default_Subtitle_Extensions:
                    self.model().item(i).setCheckState(Qt.CheckState.Checked)
        self.updateText()

    def get_files_list(self, new_extensions):
        temp_files_names = sort_names_like_windows(names_list=os.listdir(self.current_folder_path))
        temp_files_names_absolute = get_files_names_absolute_list(temp_files_names, self.current_folder_path)
        result = []
        for i in range(len(temp_files_names)):
            if os.path.isdir(temp_files_names_absolute[i]):
                continue
            for j in range(len(new_extensions)):
                temp_file_extension_start_index = temp_files_names[i].rfind(".")
                if temp_file_extension_start_index == -1:
                    continue
                temp_file_extension = temp_files_names[i][temp_file_extension_start_index + 1:]
                if temp_file_extension.lower() == new_extensions[j].lower():
                    result.append(temp_files_names[i])
                    break
        return result

    def check_extensions_changes(self):
        new_extensions = self.currentData()
        if self.current_extensions == new_extensions:
            return
        if self.current_folder_path != "" and not self.current_folder_path.isspace():
            new_files_list = self.get_files_list(new_extensions=new_extensions)
            new_files_list_sorted = sort_names_like_windows(new_files_list)
            old_files_list_sorted = sort_names_like_windows(self.current_files_list)
            if new_files_list_sorted != old_files_list_sorted:
                if self.is_there_old_files:
                    reload_dialog = ReloadSubtitleFilesDialog()
                    reload_dialog.execute()
                    if reload_dialog.result == "No":
                        new_extensions = self.current_extensions
        self.setData(new_extensions)
        self.current_extensions = new_extensions
        self.close_list.emit(new_extensions)

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
