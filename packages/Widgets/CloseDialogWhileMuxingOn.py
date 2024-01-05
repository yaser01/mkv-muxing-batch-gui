from packages.Widgets.CloseDialog import CloseDialog


class CloseDialogWhileMuxingOn(CloseDialog):
    def __init__(self, parent=None):
        super().__init__(parent, info_message="Are you sure you want to exit ?\nThis will stop current muxing",
                         close_button_name="Stop Muxing")
