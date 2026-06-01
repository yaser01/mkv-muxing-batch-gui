from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QLabel

from packages.Startup.GlobalIcons import InfoIcon
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import (
    GlobalSetting,
    convert_string_integer_to_two_digit_string,
)
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.ModifyOldTracksTabsManager import (
    ModifyOldTracksTabsManager,
)
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.TrackInfoTable import (
    TrackInfoTable,
)
from packages.Widgets.InfoDialog import InfoDialog
from packages.Widgets.MyDialog import MyDialog


class ModifyOldTracksDialog(MyDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Modificar pistas antiguas")
        self.instructions_label = QLabel()
        self.ok_button = QPushButton("Aceptar")
        self.cancel_button = QPushButton("Cancelar")
        self.reset_button = QPushButton("Restablecer a valores predeterminados")
        self.old_tracks_tabs = ModifyOldTracksTabsManager()
        self.track_info_label = QLabel("Información sobre pistas:")
        self.info_button = QPushButton(text="")
        self.info_button.setIcon(InfoIcon)
        self.track_info_table = TrackInfoTable()
        self.track_info_table.update_video_name(GlobalSetting.VIDEO_FILES_LIST)
        self.main_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.info_layout = QHBoxLayout()
        self.setup_instructions_label()
        self.setup_layouts()
        self.setup_window_dimension()
        self.disable_question_mark_window()
        self.enable_maximize_mark_window()
        self.setLayout(self.main_layout)
        self.connect_signals()
        self.reset_button.setEnabled(GlobalSetting.JOB_QUEUE_EMPTY)
        try:
            self.old_tracks_tabs.setCurrentIndex(1)
            self.update_showed_track_info(
                ("subtitle", GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO[0][0].id)
            )  # ensure subtitle track is shown when open dialog first time
        except IndexError:
            try:
                self.old_tracks_tabs.setCurrentIndex(0)
                self.update_showed_track_info(
                    ("video", GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO[0][0].id)
                )  # ensure video track is shown when open dialog first time if not have subtitle
            except IndexError:
                pass

    def setup_layouts(self):
        self.setup_info_layout()
        self.setup_buttons_layout()
        self.setup_main_layout()

    def setup_info_layout(self):
        self.info_layout.addWidget(self.info_button)
        self.info_layout.addWidget(self.instructions_label, stretch=10)

    def setup_buttons_layout(self):
        self.buttons_layout.addStretch(stretch=3)
        self.buttons_layout.addWidget(self.reset_button, stretch=2)
        self.buttons_layout.addWidget(self.ok_button, stretch=2)
        self.buttons_layout.addWidget(self.cancel_button, stretch=2)
        self.buttons_layout.addStretch(stretch=3)

    def setup_window_dimension(self):
        self.setMinimumWidth(screen_size.width() // 1.5)
        self.setMinimumHeight(screen_size.height() // 2.5)

    def setup_main_layout(self):
        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addWidget(self.old_tracks_tabs)
        self.main_layout.addWidget(self.track_info_label)
        self.main_layout.addWidget(self.track_info_table)
        self.main_layout.addLayout(self.buttons_layout)

    def setup_instructions_label(self):
        self.instructions_label.setTextFormat(Qt.TextFormat.RichText)
        instructions_text = (
            "Aquí puedes modificar/deshabilitar pistas antiguas e incluso reordenarlas usando [Ctrl+Flecha arriba/abajo] "
            "para mover la pista hacia arriba/abajo."
        )

        no_editing_text = (
            "<br>La edición está <b>Deshabilitada</b> porque la cola de trabajos tiene trabajos pendientes."
        )
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            instructions_text += no_editing_text
        self.instructions_label.setText(instructions_text)

    def disable_question_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def enable_maximize_mark_window(self):
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, on=True)

    def connect_signals(self):
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.save_settings)
        self.reset_button.clicked.connect(self.restore_defaults)
        self.old_tracks_tabs.current_selected_track_changed.connect(
            self.update_showed_track_info
        )
        self.old_tracks_tabs.currentChanged.connect(self.update_current_tab)
        self.info_button.clicked.connect(self.show_info_dialog)

    def show_info_dialog(self):
        info_dialog = InfoDialog(
            window_title="Conflicto con otras configuraciones",
            info_message="Usar esta ventana limitará/deshabilitará el uso de las siguientes "
            "opciones:<br> "
            "1- <b>Multiplexar después de pista</b> en pestañas de Subtítulos/Audio.<br>"
            "2- <b>Conservar solo estos subtítulos/audios</b> por [ID de pista, Nombre de pista, "
            "Idioma de pista] en la pestaña de Multiplexado.<br> "
            "3- <b>Hacer este subtítulo/audio predeterminado</b> por [ID de pista, Nombre de pista, "
            "Idioma de pista] en la pestaña de Multiplexado.<br> "
            "Esto es necesario porque las opciones anteriores también [dependen/modifican] la pista "
            "antigua de alguna manera.<br> "
            "Además, agregar nuevos subtítulos/audios con opciones: (establecer como predeterminado/forzado) "
            "anulará las opciones: (establecer como predeterminado/forzado) que se muestran aquí.<br> "
            "<u>En resumen</u> tienes que saber lo que estás haciendo :D</div>",
            parent=self,
        )
        info_dialog.execute()

    def restore_defaults(self):
        self.old_tracks_tabs.restore_defaults()
        # ensure track info show when restore default
        # not sure if there a better way to do this
        if self.old_tracks_tabs.currentIndex() == 1:
            track_type = "subtitle"
            track_id = GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO[0][0].id
        elif self.old_tracks_tabs.currentIndex() == 2:
            track_type = "audio"
            track_id = GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO[0][0].id
        elif self.old_tracks_tabs.currentIndex() == 0:
            track_type = "video"
            track_id = GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO[0][0].id

        self.update_showed_track_info((track_type, track_id))

    def save_settings(self):
        self.old_tracks_tabs.save_settings()
        self.close()

    def update_showed_track_info(self, new_info):
        track_type, track_id = new_info
        if track_type == "subtitle" and self.old_tracks_tabs.currentIndex() == 1:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_INFO.copy()
            )
            self.track_info_label.setText(
                f"Información sobre la pista de subtítulo [{convert_string_integer_to_two_digit_string(track_id)}] entre videos:"
            )
        elif track_type == "audio" and self.old_tracks_tabs.currentIndex() == 2:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_INFO.copy()
            )
            self.track_info_label.setText(
                f"Información sobre la pista de audio [{convert_string_integer_to_two_digit_string(track_id)}] entre videos:"
            )
        elif track_type == "video" and self.old_tracks_tabs.currentIndex() == 0:
            self.track_info_table.update_tracks_info(
                new_tracks_info_list=GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_INFO.copy()
            )
            self.track_info_label.setText(
                f"Información sobre la pista de video [{convert_string_integer_to_two_digit_string(track_id)}] entre videos:"
            )
        self.track_info_table.setup_info(track_id=track_id)

    def update_current_tab(self, tab_id):
        if tab_id == 0:
            self.old_tracks_tabs.video_tab.table_focused()
        elif tab_id == 1:
            self.old_tracks_tabs.subtitle_tab.table_focused()
        elif tab_id == 2:
            self.old_tracks_tabs.audio_tab.table_focused()

    def execute(self):
        self.exec()