import os
import sys

from PySide2 import QtCore
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QApplication, QToolTip, QStyleFactory


def setup_tool_tip_style():
    tool_tip_palette = QToolTip.palette()
    tool_tip_palette.setColor(QPalette.ToolTipBase, QColor("#FFFFFF"))
    tool_tip_palette.setColor(QPalette.ToolTipText, QColor("#505050"))
    QToolTip.setPalette(tool_tip_palette)


def set_application_style():
    MainApplication.setStyle(QStyleFactory.create("Fusion"))


def keep_screen_resolution_good():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '2'


keep_screen_resolution_good()
MainApplication = QApplication(sys.argv)
setup_tool_tip_style()
set_application_style()
