from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QListWidget, QStyledItemDelegate, QStyle


class ListWidget(QListWidget):
    def __init__(self):
        super().__init__()

        class StyleDelegateForQTableWidget(QStyledItemDelegate):
            color_default = QtGui.QColor("#aaedff")  # aaedff: blue Kashef

            def paint(self, painter, option, index):
                if option.state & QStyle.StateFlag.State_Selected:
                    item_color = index.data(role=Qt.ItemDataRole.DecorationRole.ForegroundRole)
                    if item_color is None:
                        item_color = Qt.GlobalColor.black
                    else:
                        item_color = item_color.color()
                    option.palette.setColor(QPalette.ColorRole.HighlightedText, item_color)
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
