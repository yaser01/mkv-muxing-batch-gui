from packages.Widgets.CloseDialog import CloseDialog


class CloseDialogWhileAtLeastOneOptionSelected(CloseDialog):
    def __init__(self, parent=None):
        super().__init__(
            parent,
            info_message="¿Estás seguro de que quieres salir?\nEsto descartará la selección actual",
            close_button_name="Salir",
        )