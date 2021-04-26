from PySide2 import QtCore
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalFiles


class ControlQueueButton(QPushButton):
    add_to_queue_clicked_signal = QtCore.Signal()
    start_multiplexing_clicked_signal = QtCore.Signal()
    pause_multiplexing_clicked_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.state = ""
        self.set_state_add_to_queue()
        self.clicked.connect(self.button_clicked)

    def set_state_add_to_queue(self):
        self.state = "ADD"
        self.setText(" Add To Queue")
        self.setIcon(GlobalFiles.AddToQueueIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_start_multiplexing(self):
        self.state = "START"
        self.setText(" Start Multiplexing")
        self.setIcon(GlobalFiles.StartMultiplexingIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_pause_multiplexing(self):
        self.state = "PAUSE"
        self.setText(" Pause Multiplexing")
        self.setIcon(GlobalFiles.PauseMultiplexingIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_pausing_multiplexing(self):
        self.state = "PAUSING"
        self.setText(" Waiting Current Job")
        self.setIcon(GlobalFiles.PauseMultiplexingIcon)
        self.setToolTip("will pause muxing after current job finished")
        self.setDisabled(True)

    def set_state_resume_multiplexing(self):
        self.state = "RESUME"
        self.setText(" Resume Multiplexing")
        self.setIcon(GlobalFiles.StartMultiplexingIcon)
        self.setToolTip("")

    def button_clicked(self):
        if self.state == "ADD":
            self.add_to_queue_clicked_signal.emit()
        elif self.state == "START" or self.state == "RESUME":
            self.start_multiplexing_clicked_signal.emit()
        elif self.state == "PAUSE":
            self.pause_multiplexing_clicked_signal.emit()
