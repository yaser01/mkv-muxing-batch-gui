from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QFontMetrics
from PySide2.QtWidgets import QStyledItemDelegate, QComboBox

from packages.Startup.PreDefined import *
# noinspection SpellCheckingInspection
from packages.Tabs.GlobalSetting import GlobalSetting


class TracksCheckableComboBox(QComboBox):
    # Subclass Delegate to increase item height
    closeList = QtCore.Signal()

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
        self.current_list = []
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().setContextMenuPolicy(Qt.PreventContextMenu)
        self.hint_when_enabled = ""
        self.empty_selection_string = "Discard All"
        self.empty_selection_hint_string = ""
        self.tracks = []
        self.languages = []

        # Use custom delegate
        self.setItemDelegate(TracksCheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)
        # self.check_if_nothing_selected()

    def disable_select(self):
        self.lineEdit().deselect()

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):
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
                    if item.text().find("Tracks") == -1 and item.text().find("Languages") == -1:
                        if item.checkState() == Qt.Checked:
                            item.setCheckState(Qt.Unchecked)
                        else:
                            item.setCheckState(Qt.Checked)
                        return True
                    else:
                        return False
            return False
        else:
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
        # self.check_if_nothing_selected()
        self.closeList.emit()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        count_tracks = 0
        count_languages = 0
        tracks = []
        languages = []
        tracks_text = []
        languages_text = []
        text = ""
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                if self.model().item(i).text().find("Track") != -1:
                    count_tracks += 1
                    tracks.append(self.model().item(i).text())
                    tracks_text.append(self.model().item(i).text().split(" ")[1])

                elif self.model().item(i).text() in AllSubtitlesLanguages:
                    count_languages += 1
                    languages.append(self.model().item(i).text())
                    languages_text.append(self.model().item(i).text())
        self.tracks = tracks_text
        self.languages = languages_text
        if count_tracks > 0:
            tracks_text = "Tracks: [" + ", ".join(tracks_text) + "]"
            text = tracks_text
        if count_languages > 0:
            languages_text = "Languages: [" + ", ".join(languages_text) + "]"
            if text != "":
                text = text + "," + languages_text
            else:
                text = languages_text

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        if elided_text != "":
            non_italic_font = self.lineEdit().font()
            non_italic_font.setItalic(False)
            self.lineEdit().setFont(non_italic_font)
            self.lineEdit().setText(elided_text)
            if count_tracks > 0:
                self.hint = tracks_text
                if count_languages > 0:
                    self.hint = self.hint + "<br>" + languages_text
            elif count_languages > 0:
                self.hint = languages_text
        else:
            italic_font = self.lineEdit().font()
            italic_font.setItalic(True)
            self.lineEdit().setFont(italic_font)
            self.lineEdit().setText(self.empty_selection_string)
            self.hint = self.empty_selection_hint_string
        self.setToolTip(self.hint)

    def addItem(self, text, data=None):
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        if text.find("Tracks") == -1 and text.find("Languages") == -1:
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model().appendRow(item)
        else:
            # bigger_font=self.lineEdit().font()
            # bigger_font.setPointSize(bigger_font.pointSize()+1)
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            # item.setFont(bigger_font)
            item.setData(Qt.Unchecked)
            self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        self.clear()
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)
        self.current_list = texts.copy()
        self.lineEdit().setText(self.empty_selection_string)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res

    def setData(self, texts):
        for i in range(self.model().rowCount()):
            if self.model().item(i).data() in texts:
                self.model().item(i).setCheckState(Qt.Checked)
            else:
                self.model().item(i).setCheckState(Qt.Unchecked)

    def set_tool_tip_hint(self):
        self.setToolTip(self.hint)
        self.setToolTipDuration(12000)

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
