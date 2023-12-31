import PySide2
from PySide2.QtCore import QEvent
from PySide2.QtGui import Qt, QFontMetrics
from PySide2.QtWidgets import QComboBox

from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Startup.PreDefined import AllAudiosTracks
from packages.Startup.SetupThems import get_dark_palette, get_light_palette
from packages.Tabs.GlobalSetting import GlobalSetting


class MakeThisTrackDefaultComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.current_list = []
        self.current_text = ""
        self.empty_selection_string = "None"
        self.empty_selection_hint_string = "The selected flag [default/forced/both] will be removed from all " \
                                           "corresponding tracks"
        self.addItems(AllAudiosTracks)
        self.setMinimumWidth(screen_size.width() // 12)
        self.setMaximumWidth(screen_size.width() // 4)
        self.setMaxVisibleItems(8)
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.setCurrentIndex(-1)
        self.disable_track_id_text_from_being_selected()
        self.disable_track_language_text_from_being_selected()
        self.disable_track_name_text_from_being_selected()
        self.hint_when_enabled = ""
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().selectionChanged.connect(self.disable_select)
        self.lineEdit().setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False
        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)
        self.activated.connect(self.updateText)
        self.setDisabled(True)

    def disable_select(self):
        self.lineEdit().deselect()

    def eventFilter(self, object, event):
        if str(event.__class__).find("Event") == -1:
            return False
        try:
            if self.isEnabled():
                if object == self.lineEdit():
                    if event.type() == QEvent.MouseButtonRelease:
                        if self.closeOnLineEditClick:
                            self.hidePopup()
                        else:
                            self.showPopup()
                        return True
                    return False
            return False
        except Exception as e:
            return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText(self.currentIndex())
        self.update_shown_text()
        # self.check_if_nothing_selected()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def disable_track_id_text_from_being_selected(self):
        for i in range(self.count()):
            if self.itemText(i) == "---Track Id---":
                self.model().item(i).setEnabled(False)
                self.model().item(i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                break

    def disable_track_language_text_from_being_selected(self):
        for i in range(self.count()):
            if self.itemText(i) == "---Language---":
                self.model().item(i).setEnabled(False)
                self.model().item(i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                break

    def disable_track_name_text_from_being_selected(self):
        for i in range(self.count()):
            if self.itemText(i) == "---Track Name---":
                self.model().item(i).setEnabled(False)
                self.model().item(i).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                break

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)

    def addItems(self, texts: list):
        self.clear()
        super().addItems(texts)
        for i in range(len(texts)):
            if texts[i] != "---Track Id---" and texts[i] != "---Language---" and texts[i] != "---Track Name---":
                self.setItemData(i, texts[i], Qt.ItemDataRole.ToolTipRole)
        self.current_list = texts.copy()
        self.setCurrentIndex(-1)
        self.disable_track_id_text_from_being_selected()
        self.disable_track_language_text_from_being_selected()
        self.disable_track_name_text_from_being_selected()

    def resizeEvent(self, e: PySide2.QtGui.QResizeEvent):
        super().resizeEvent(e)
        self.update_shown_text()

    # noinspection PyAttributeOutsideInit
    def updateText(self, new_index):
        count_tracks_id = 0
        count_tracks_languages = 0
        count_tracks_names = 0
        tracks = []
        tracks_id_text = []
        tracks_name_text = []
        tracks_languages_text = []
        text = ""
        current_tracks = "None"
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() == "---Track Id---":
                current_tracks = "id"
                continue
            elif self.model().item(i).text() == "---Language---":
                current_tracks = "lang"
                continue
            elif self.model().item(i).text() == "---Track Name---":
                current_tracks = "name"
                continue
            if self.currentIndex() == i:
                if current_tracks == "id":
                    count_tracks_id += 1
                    tracks.append(self.model().item(i).text())
                    tracks_id_text.append(self.model().item(i).text().split(" ")[1])
                elif current_tracks == "lang":
                    count_tracks_languages += 1
                    tracks_languages_text.append(self.model().item(i).text())
                elif current_tracks == "name":
                    count_tracks_names += 1
                    tracks_name_text.append(self.model().item(i).text())
        self.tracks_id = tracks_id_text
        self.tracks_language = tracks_languages_text
        self.tracks_name = tracks_name_text
        if count_tracks_id > 0:
            tracks_id_text = "Track Id: [" + ", ".join(tracks_id_text) + "]"
            text = tracks_id_text
        if count_tracks_languages > 0:
            tracks_languages_text = "Language: [" + ", ".join(tracks_languages_text) + "]"
            if text != "":
                text = text + "," + tracks_languages_text
            else:
                text = tracks_languages_text
        if count_tracks_names > 0:
            tracks_name_text = "Track Name: [" + ", ".join(tracks_name_text) + "]"
            if text != "":
                text = text + "," + tracks_name_text
            else:
                text = tracks_name_text
        self.current_text = text
        # Compute elided text (with "...")
        if text != "":
            self.update_shown_text()
            if count_tracks_id > 0:
                self.hint = tracks_id_text
                if count_tracks_languages > 0:
                    self.hint = self.hint + "<br>" + tracks_languages_text
                if count_tracks_names > 0:
                    self.hint = self.hint + "<br>" + tracks_name_text
            elif count_tracks_languages > 0:
                self.hint = tracks_languages_text
                if count_tracks_names > 0:
                    self.hint = self.hint + "<br>" + tracks_name_text
            elif count_tracks_names:
                self.hint = tracks_name_text
        else:
            italic_font = self.lineEdit().font()
            italic_font.setItalic(True)
            self.lineEdit().setFont(italic_font)
            self.lineEdit().setText("")
            self.hint = ""
        self.setToolTip(self.hint)

    def update_shown_text(self):
        if self.current_text != "":
            metrics = QFontMetrics(self.lineEdit().font())
            non_italic_font = self.lineEdit().font()
            non_italic_font.setItalic(False)
            self.lineEdit().setFont(non_italic_font)
            elided_text = metrics.elidedText(self.current_text, Qt.TextElideMode.ElideRight, self.lineEdit().width())
            self.lineEdit().setText(elided_text)
        else:
            italic_font = self.lineEdit().font()
            italic_font.setItalic(True)
            self.lineEdit().setFont(italic_font)
            self.lineEdit().setText(self.empty_selection_string)
            self.setToolTip(self.empty_selection_hint_string)

    def update_theme_mode_state(self):
        if Options.Dark_Mode:
            self.setPalette(get_dark_palette())
        else:
            self.setPalette(get_light_palette())
        self.setStyleSheet("QComboBox { combobox-popup: 0; }")

    def refresh_tracks(self, new_list):
        self.addItems(texts=new_list)
        self.current_text = ""
        self.update_shown_text()
