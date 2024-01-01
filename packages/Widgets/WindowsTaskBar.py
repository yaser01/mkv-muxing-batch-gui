import ctypes
from ctypes import wintypes
import comtypes
import comtypes.client as cc
TaskBarGUID = "{56FDF344-FD6D-11d0-958A-006097C9A090}"
comtypes.CoInitializeEx()
from packages.Widgets.WindowsTaskBarLib import ITaskbarList3


def create_icon(icon_path):
    CreateIconFromResourceEx = ctypes.windll.user32.CreateIconFromResourceEx
    CreateIconFromResourceEx.restype = ctypes.wintypes.HICON
    size_x, size_y = 32, 32
    LR_DEFAULTCOLOR = 0
    LR_SHARED = 32768
    with open(icon_path, "rb") as f:
        png = f.read()
    hicon = CreateIconFromResourceEx(png, len(png), 1, 0x30000, size_x, size_y, LR_SHARED)
    return hicon


class WindowsTaskBar:
    def __init__(self, hwnd):
        super().__init__()
        self.window_id = hwnd
        self.taskbar = cc.CreateObject(
            TaskBarGUID,
            interface=ITaskbarList3, clsctx=comtypes.CLSCTX_ALL)
        self.taskbar.HrInit()

    def setState(self, value):
        if value == 'normal':
            self.taskbar.SetProgressState(self.window_id, 0)

        elif value == 'warning':
            self.taskbar.SetProgressState(self.window_id, 10)

        elif value == 'error':
            self.taskbar.SetProgressState(self.window_id, 15)

        elif value == 'loading':
            self.taskbar.SetProgressState(self.window_id, -15)

        elif value == 'done':
            ctypes.windll.user32.FlashWindow(self.window_id, True)

    def setProgress(self, value: int):
        value = min(value, 100)
        value = max(0, value)
        self.taskbar.setProgressValue(self.window_id, value, 100)

    def setOverlayIcon(self, icon_path):
        hicon = create_icon(icon_path=icon_path)
        self.taskbar.SetOverlayIcon(self.window_id, hicon, "some_random_string")

    def clearOverlayIcon(self):
        self.taskbar.SetOverlayIcon(self.window_id, 0, "some_random_string")
