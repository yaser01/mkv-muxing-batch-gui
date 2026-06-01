from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QResizeEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QLabel

from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.TrackInfoTableColumnsID import (
    TrackInfoTableColumnsID,
)
from packages.Widgets.GreenTikCell import GreenTikCell
from packages.Widgets.RedCrossCell import RedCrossCell
from packages.Widgets.SingleOldTrackData import SingleOldTrackData
from packages.Widgets.TableWidget import TableWidget


class TrackInfoTable(TableWidget):
    def __init__(self):
        super().__init__()
        self.column_ids = TrackInfoTableColumnsID()
        self.setColumnCount(len(self.column_ids.columns_name))
        self.horizontal_header = None
        self.tracks_info: list[list[SingleOldTrackData]] = [[]]
        self.video_names = []
        self.setRowCount(0)
        self.force_no_selection()
        self.create_horizontal_header()
        self.setup_horizontal_header()
        self.setup_columns()
        self.connect_signals()
        self.adjust_column_widths()

    def adjust_column_widths(self):
        header = self.horizontalHeader()
        # Ajustar todas las columnas al contenido
        for col in range(self.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        # La columna de Idioma de pista puede estirarse si hay espacio
        header.setSectionResizeMode(self.column_ids.Track_Language, QHeaderView.ResizeMode.Stretch)
        # También aseguramos un ancho mínimo para los nombres de video y pista
        self.setColumnWidth(self.column_ids.Video_Name, max(200, self.columnWidth(self.column_ids.Video_Name)))
        self.setColumnWidth(self.column_ids.Track_Name, max(150, self.columnWidth(self.column_ids.Track_Name)))

    def connect_signals(self):
        self.horizontalHeader().sectionResized.connect(self.on_section_resized)

    def on_section_resized(self, logicalIndex, oldSize, newSize):
        pass  # Opcional, se puede dejar vacío

    def setup_columns(self):
        for column_id in range(len(self.column_ids.columns_name)):
            self.set_column_name(
                column_index=column_id, name=self.column_ids.columns_name[column_id]
            )

    def set_column_name(self, column_index, name):
        column = QTableWidgetItem(name)
        column.setTextAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.setHorizontalHeaderItem(column_index, column)

    def force_no_selection(self):
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def create_horizontal_header(self):
        self.horizontal_header = self.horizontalHeader()

    def setup_horizontal_header(self):
        # Configuración inicial (se sobrescribirá al ajustar anchos)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Video_Name, QHeaderView.ResizeMode.Interactive)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Found, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Is_Default, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Is_Forced, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Name, QHeaderView.ResizeMode.Interactive)
        self.horizontal_header.setSectionResizeMode(self.column_ids.Track_Language, QHeaderView.ResizeMode.Stretch)

    def set_row_value_video_name(self, row_id: int, video_name: Path):
        item = QTableWidgetItem(str(video_name))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_id, self.column_ids.Video_Name, item)

    def set_row_value_empty_cell(self, row_id: int, column_id: int):
        self.setCellWidget(row_id, column_id, QLabel())

    def set_row_value_empty_item(self, row_id, column_id):
        item = QTableWidgetItem(" ")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_id, column_id, item)

    def set_row_value_found_track(self, row_id, found):
        if found:
            self.setCellWidget(row_id, self.column_ids.Found, GreenTikCell(tool_tip="Pista encontrada"))
        else:
            self.setCellWidget(row_id, self.column_ids.Found, RedCrossCell(tool_tip="Pista no encontrada"))

    def set_row_value_is_default_track(self, row_id, is_default):
        if is_default:
            self.setCellWidget(row_id, self.column_ids.Is_Default, GreenTikCell(tool_tip="La pista es predeterminada"))
        else:
            self.setCellWidget(row_id, self.column_ids.Is_Default, RedCrossCell(tool_tip="La pista no es predeterminada"))

    def set_row_value_is_forced_track(self, row_id, is_forced):
        if is_forced:
            self.setCellWidget(row_id, self.column_ids.Is_Forced, GreenTikCell(tool_tip="La pista es forzada"))
        else:
            self.setCellWidget(row_id, self.column_ids.Is_Forced, RedCrossCell(tool_tip="La pista no es forzada"))

    def set_row_value_track_name(self, new_row_id, track_name):
        item = QTableWidgetItem(track_name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(new_row_id, self.column_ids.Track_Name, item)

    def set_row_value_track_language(self, new_row_id, track_language):
        item = QTableWidgetItem(track_language)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(new_row_id, self.column_ids.Track_Language, item)

    def setup_video_names(self):
        self.setRowCount(len(self.video_names))
        for new_row_id in range(len(self.video_names)):
            self.set_row_value_video_name(new_row_id, self.video_names[new_row_id])

    def setup_info(self, track_id):
        for new_row_id in range(len(self.video_names)):
            found_track = False
            for track in self.tracks_info[new_row_id]:
                if int(track.id) == int(track_id):
                    self.set_row_value_found_track(new_row_id, True)
                    self.set_row_value_is_default_track(new_row_id, track.is_default)
                    self.set_row_value_is_forced_track(new_row_id, track.is_forced)
                    self.set_row_value_track_name(new_row_id, track.track_name)
                    self.set_row_value_track_language(new_row_id, track.language)
                    found_track = True
                    break
            if not found_track:
                self.set_row_value_found_track(new_row_id, False)
                self.set_row_value_empty_cell(new_row_id, self.column_ids.Is_Default)
                self.set_row_value_empty_cell(new_row_id, self.column_ids.Is_Forced)
                self.set_row_value_empty_item(new_row_id, self.column_ids.Track_Name)
                self.set_row_value_empty_item(new_row_id, self.column_ids.Track_Language)

        self.adjust_column_widths()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.adjust_column_widths()

    def update_video_name(self, new_video_names_list: list[Path]):
        self.video_names = new_video_names_list.copy()
        self.setup_video_names()

    def update_tracks_info(self, new_tracks_info_list):
        self.tracks_info = new_tracks_info_list.copy()