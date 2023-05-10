from PySide2 import QtCore
from PySide2.QtGui import QPaintEvent
from PySide2.QtWidgets import QPushButton

from packages.Startup import GlobalIcons


class ControlQueueButton(QPushButton):
    add_to_queue_clicked_signal = QtCore.Signal()
    start_multiplexing_clicked_signal = QtCore.Signal()
    pause_multiplexing_clicked_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.state = ""
        self.set_state_add_to_queue()
        self.clicked.connect(self.button_clicked)
        self.states = [" Add To Queue", " Start Multiplexing", " Pause Multiplexing", " Waiting Current Job", " Resume "
                                                                                                              "Multiplexing"]

    def set_state_add_to_queue(self):
        self.state = "ADD"
        self.setText(" Add To Queue")
        self.setIcon(GlobalIcons.AddToQueueIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_start_multiplexing(self):
        self.state = "START"
        self.setText(" Start Multiplexing")
        self.setIcon(GlobalIcons.StartMultiplexingIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_pause_multiplexing(self):
        self.state = "PAUSE"
        self.setText(" Pause Multiplexing")
        self.setIcon(GlobalIcons.PauseMultiplexingIcon)
        self.setToolTip("")
        self.setDisabled(False)

    def set_state_pausing_multiplexing(self):
        self.state = "PAUSING"
        self.setText(" Waiting Current Job")
        self.setIcon(GlobalIcons.PauseMultiplexingIcon)
        self.setToolTip("will pause muxing after current job finished")
        self.setDisabled(True)

    def set_state_resume_multiplexing(self):
        self.state = "RESUME"
        self.setText(" Resume Multiplexing")
        self.setIcon(GlobalIcons.StartMultiplexingIcon)
        self.setToolTip("")

    def paintEvent(self, event: QPaintEvent):
        width = 0
        for text in self.states:
            width = max(width, self.fontMetrics().boundingRect(text).width())
        width += 25
        self.setMinimumWidth(width)
        super().paintEvent(event)

    def button_clicked(self):
        if self.state == "ADD":
            self.add_to_queue_clicked_signal.emit()
        elif self.state == "START" or self.state == "RESUME":
            self.start_multiplexing_clicked_signal.emit()
        elif self.state == "PAUSE":
            self.pause_multiplexing_clicked_signal.emit()
