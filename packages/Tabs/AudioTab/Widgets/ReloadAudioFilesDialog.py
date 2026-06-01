from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadAudioFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "¿Estás seguro?\nEsto recargará todos los archivos de audio y afectará el emparejamiento actual"
        )
        self.setWindowTitle("Cambiar archivos de audio")

    def execute(self):
        self.exec()