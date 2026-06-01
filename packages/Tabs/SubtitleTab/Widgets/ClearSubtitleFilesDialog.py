from packages.Startup import GlobalIcons
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearSubtitleFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText("¿Estás seguro?\nEsto eliminará todos los archivos de subtítulos")
        self.setWindowTitle("Limpiar archivos de subtítulos")
        self.setWindowIcon(GlobalIcons.NoMarkIcon)

    def execute(self):
        self.exec()