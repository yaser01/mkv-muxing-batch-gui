import webbrowser
from PySide2.QtWidgets import QPushButton
from packages.Startup import GlobalFiles
from packages.Startup.PreDefined import DonationsUrl


def open_donations_page():
    webbrowser.open(DonationsUrl)


class DonateButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(GlobalFiles.DonationsIcon)
        self.setText(" Donate")
        self.hint_when_enabled = ":D"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(open_donations_page)
