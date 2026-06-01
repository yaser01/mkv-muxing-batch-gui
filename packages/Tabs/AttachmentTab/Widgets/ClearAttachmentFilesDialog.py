from packages.Startup import GlobalIcons
from packages.Widgets.YesNoDialog import YesNoDialog


class ClearAttachmentFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText("¿Estás seguro?\nEsto eliminará todos los archivos adjuntos")
        self.setWindowTitle("Limpiar archivos adjuntos")
        self.setWindowIcon(GlobalIcons.NoMarkIcon)

    def execute(self):
        self.exec()