from PySide2 import QtGui
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QFontMetrics
from PySide2.QtWidgets import QStyledItemDelegate, QComboBox

from packages.Startup.InitializeScreenResolution import screen_size


class ExtensionsCheckableComboBox(QComboBox):
    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            s = size.height() * 4 // 3
            size.setHeight(int(s))
            return size

    def __init__(self, items_list, default_items_list):
        super().__init__()
        self.current_model = QtGui.QStandardItemModel(self)
        self.setModel(self.current_model)
        self.hint = ""
        self.hint_when_enabled = ""
        self.items_list = items_list
        self.default_items_list = default_items_list
        self.closeOnLineEditClick = False
        # Use custom delegate
        self.setItemDelegate(ExtensionsCheckableComboBox.Delegate())
        # Update the text when an item is toggled
        # Hide and show popup when clicking the line edit
        # Prevent popup from closing when clicking on an item

        self.current_model.clear()
        self.view().viewport().installEventFilter(self)
        self.setup_ui()
        self.current_model.dataChanged.connect(self.updateText)

    def setup_ui(self):
        self.addItems(self.items_list)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.lineEdit().installEventFilter(self)
        self.setMinimumWidth(screen_size.width() // 9)
        self.setMaxVisibleItems(6)
        self.make_default_extensions_checked()
        self.lineEdit().selectionChanged.connect(self.disable_select)

    def make_default_extensions_checked(self):
        for i in range(self.current_model.rowCount()):
            if self.current_model.item(i).text() in self.default_items_list:
                self.current_model.item(i).setCheckState(Qt.CheckState.Checked)
        self.updateText()

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
                        item = self.current_model.item(index.row())
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
        for i in range(self.current_model.rowCount()):
            if self.current_model.item(i).checkState() == Qt.CheckState.Checked:
                extensions_text.append(self.current_model.item(i).text())

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
        self.current_model.appendRow(item)

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
        for i in range(self.current_model.rowCount()):
            if self.current_model.item(i).checkState() == Qt.CheckState.Checked:
                res.append(self.current_model.item(i).data())
        return res

    def setData(self, texts):
        for i in range(self.current_model.rowCount()):
            if self.current_model.item(i).data() in texts:
                self.current_model.item(i).setCheckState(Qt.CheckState.Checked)
            else:
                self.current_model.item(i).setCheckState(Qt.CheckState.Unchecked)

    def check_if_nothing_selected(self):
        count = 0
        for i in range(self.current_model.rowCount()):
            if self.current_model.item(i).checkState() == Qt.CheckState.Checked:
                count += 1
        if count == 0:
            for i in range(self.current_model.rowCount()):
                if self.current_model.item(i).text() in self.default_items_list:
                    self.current_model.item(i).setCheckState(Qt.CheckState.Checked)
        self.updateText()

    def check_extensions_changes(self):
        new_extensions = self.currentData()
        self.setData(new_extensions)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled():
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
