from PySide2.QtWidgets import QFrame


class JobDividingLine(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setFrameShape(QFrame.Shape.VLine)
