from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette, QBrush
from PySide2.QtWidgets import QTreeWidget, QStyledItemDelegate, QStyle


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.new_palette = self.palette()
        self.new_palette.setColor(QPalette.ColorRole.Highlight, QColor(255, 255, 255, 0))
        self.setPalette(self.new_palette)

        class StyleDelegateForQTreeWidget(QStyledItemDelegate):
            color_default = QColor("#aaedff")  # aaedff: blue Kashef

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
                    if item.background(0) != QBrush():
                        return item.background(0).color()
                    if item.background(1) != QBrush():
                        return item.background(1).color()
                if self.parent().alternatingRowColors():
                    if index.row() % 2 == 1:
                        return option.palette.color(QPalette.AlternateBase)
                return option.palette.color(QPalette.Base)

            @staticmethod
            def combineColors(c1, c2):
                c3 = QColor()
                c3.setRed((c1.red() + c2.red()) // 2)
                c3.setGreen((c1.green() + c2.green()) // 2)
                c3.setBlue((c1.blue() + c2.blue()) // 2)
                return c3

        self.setItemDelegate(StyleDelegateForQTreeWidget(self))
