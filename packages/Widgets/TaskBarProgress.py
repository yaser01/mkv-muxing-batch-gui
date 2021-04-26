from PySide2.QtGui import QIcon
from PySide2.QtWinExtras import QWinTaskbarButton

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting


class TaskBarProgress(QWinTaskbarButton):
    def __init__(self, window_handle):
        super().__init__()
        self.setWindow(window_handle)
        self.progress = self.progress()
        self.progress.setValue(0)
        self.progress.setVisible(True)

    def start_muxing(self):
        self.progress.setVisible(True)
        self.progress.resume()
        self.setOverlayIcon(QIcon(GlobalFiles.StartMultiplexingIconPath))

    def update_progress(self, new_progress):
        self.progress.resume()
        if GlobalSetting.MUXING_ON:
            self.setOverlayIcon(QIcon(GlobalFiles.StartMultiplexingIconPath))
        self.progress.setValue(new_progress)
        if new_progress == 100:
            self.hide_progress()

    def hide_progress(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.clearOverlayIcon()

    def pause_progress(self):
        self.progress.pause()
        self.setOverlayIcon(QIcon(GlobalFiles.PauseMultiplexingIconPath))
