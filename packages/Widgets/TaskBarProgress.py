from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Widgets.WindowsTaskBar import WindowsTaskBar


class TaskBarProgress(WindowsTaskBar):
    def __init__(self, window_id):
        super().__init__(hwnd=window_id)
        self.setState("normal")
        self.setProgress(0)
        self.clearOverlayIcon()

    def start_muxing(self):
        self.setState("normal")
        self.setOverlayIcon(GlobalFiles.StartMultiplexingIconPath)

    def update_progress(self, new_progress):
        if GlobalSetting.MUXING_ON:
            self.setOverlayIcon(GlobalFiles.StartMultiplexingIconPath)
        self.setProgress(new_progress)
        if new_progress == 100:
            self.setProgress(0)
            self.clearOverlayIcon()
            self.setState("done")

    def hide_progress(self):
        self.setProgress(0)
        self.clearOverlayIcon()

    def pause_progress(self):
        self.setState("warning")
        self.setOverlayIcon(GlobalFiles.PauseMultiplexingIconPath)
