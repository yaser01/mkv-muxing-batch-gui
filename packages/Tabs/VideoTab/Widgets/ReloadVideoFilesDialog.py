from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadVideoFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "¿Estás seguro?\nEsto recargará todos los archivos de video y afectará el emparejamiento en otras pestañas"
        )
        self.setWindowTitle("Cambiar archivos de video")

    def execute(self):
        self.exec()