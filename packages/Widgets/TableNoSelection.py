import typing

from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QStyledItemDelegate, QTableWidget, QStyle


class TableWidgetNoSelection(QTableWidget):
    def __init__(self, *args, **kwargs):
        QTableWidget.__init__(self, *args, **kwargs)
        self.preventSelect = True

        class StyleDelegateForQTableWidget(QStyledItemDelegate):
            color_default = QtGui.QColor("#aaedff")  # aaedff: blue Kashef

            def paint(self, painter, option, index):
                if option.state & QStyle.StateFlag.State_Selected:
                    option.palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
                    color = self.combineColors(self.color_default, self.background(option, index))
                    option.palette.setColor(QPalette.ColorRole.Highlight, color)
                QStyledItemDelegate.paint(self, painter, option, index)

            def background(self, option, index):
                item = self.parent().itemFromIndex(index)
                if item:
                    if item.background() != QtGui.QBrush():
                        return item.background().color()
                if self.parent().alternatingRowColors():
                    if index.row() % 2 == 1:
                        return option.palette.color(QPalette.AlternateBase)
                return option.palette.color(QPalette.Base)

            @staticmethod
            def combineColors(c1, c2):
                c3 = QtGui.QColor()
                c3.setRed((c1.red() + c2.red()) // 2)
                c3.setGreen((c1.green() + c2.green()) // 2)
                c3.setBlue((c1.blue() + c2.blue()) // 2)
                return c3

        self.setItemDelegate(StyleDelegateForQTableWidget(self))

    def selectionCommand(self, index: QtCore.QModelIndex,
                         event: typing.Optional[QtCore.QEvent] = ...) -> QtCore.QItemSelectionModel.SelectionFlag:
        if self.preventSelect == False:
            return super().selectionCommand(index, event)
        if event is None:  # when selecting programmatically or press on header
            return QtCore.QItemSelectionModel.SelectionFlag.NoUpdate
        else:
            return super().selectionCommand(index, event)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        return
