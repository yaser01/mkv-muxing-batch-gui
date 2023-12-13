import platform
import sys

from PySide6.QtWidgets import QMainWindow

if sys.platform == "win32":
    from ctypes import byref, c_bool, sizeof, windll
    from ctypes.wintypes import BOOL


class MyMainWindow(QMainWindow):
    def __init__(self, args, parent=None):
        super().__init__()
        self.is_dark_mode_supported = False
        self.is_os_windows = (sys.platform == "win32")
        if self.is_os_windows:
            dwm_api = windll.LoadLibrary("dwmapi")
            try:
                windows_version = int(platform.version().split('.')[2])
            except Exception as e:
                windows_version = 1
            if windows_version < 19041:
                self.dwnwa_use_immersive_dark_mode = 19
            else:
                self.dwnwa_use_immersive_dark_mode = 20
            self.dwmSetWindowAttribute = dwm_api.DwmSetWindowAttribute

    def set_dark_mode(self, on):
        if self.is_os_windows:
            self.dwmSetWindowAttribute(int(self.winId()), self.dwnwa_use_immersive_dark_mode,
                                       byref(c_bool(on)), sizeof(BOOL))
            # to force redraw of title bar
            self.resize(self.width(), self.height() + 1)
            self.resize(self.width(), self.height() - 1)
