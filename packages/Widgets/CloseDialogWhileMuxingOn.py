from packages.Widgets.CloseDialog import CloseDialog


class CloseDialogWhileMuxingOn(CloseDialog):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            info_message="¿Estás seguro de que quieres salir?\nEsto detendrá el multiplexado actual",
            close_button_name="Detener multiplexado",
        )