import os
import sys

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QToolTip, QStyleFactory

from packages.Startup.Options import Options, read_option_file
from packages.Startup.GlobalFiles import SettingJsonInfoFilePath, LanguagesFilePath
from packages.Startup.SetupThems import get_light_palette, get_dark_palette


def set_application_style():
    MainApplication.setStyle(QStyleFactory.create("Fusion"))
    if Options.Dark_Mode:
        apply_dark_mode()
    else:
        apply_light_mode()


def keep_screen_resolution_good():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '2'


def apply_light_mode():
    palette = get_light_palette()
    MainApplication.setPalette(palette)
    QToolTip.setPalette(palette)


def apply_dark_mode():
    palette = get_dark_palette()
    MainApplication.setPalette(palette)
    QToolTip.setPalette(palette)


read_option_file(option_file=SettingJsonInfoFilePath, all_languages_file_path=LanguagesFilePath)
keep_screen_resolution_good()
MainApplication = QApplication(sys.argv)
set_application_style()
