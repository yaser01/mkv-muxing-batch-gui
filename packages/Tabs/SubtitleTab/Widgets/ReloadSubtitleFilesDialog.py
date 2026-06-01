from packages.Widgets.YesNoDialog import YesNoDialog


class ReloadSubtitleFilesDialog(YesNoDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.message.setText(
            "¿Estás seguro?\nEsto recargará todos los archivos de subtítulos y afectará el emparejamiento actual"
        )
        self.setWindowTitle("Cambiar archivos de subtítulos")

    def execute(self):
        self.exec()