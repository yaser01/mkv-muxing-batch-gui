import hashlib
import json
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Widgets.SingleTrackData import SingleTrackData
from packages.Widgets.TreeWidget import TreeWidget


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def add_row(parent, name):
    item = QTreeWidgetItem(parent)
    item.setText(0, name)
    return item


def add_child(parent: QTreeWidgetItem, name):
    item = QTreeWidgetItem(parent)
    item.setText(0, name)


class MediaInfoTreeWidget(TreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(1)
        self.setup_info()
        self.setHeaderHidden(True)
        self.clearFocus()
        self.setFocusPolicy(Qt.ClickFocus)

    def setup_info(self):
        videos = GlobalSetting.VIDEO_FILES_ABSOLUTE_PATH_LIST.copy()
        for video_name in videos:
            audios_track_info = []
            subtitles_track_info = []
            videos_track_info = []
            attachments_info = []
            chapter_num_entries = ""
            string_name_hash = hashlib.sha1((str(video_name)).encode('utf-8')).hexdigest()
            media_info_file_path = os.path.join(GlobalFiles.MediaInfoFolderPath, string_name_hash + ".json")
            # if() not found
            with open(media_info_file_path, 'r', encoding="UTF-8") as media_info_file:
                json_info = json.load(media_info_file)
            tracks_json_info = json_info["tracks"]
            attachments_json_info = json_info["attachments"]
            chapters_json_info = json_info["chapters"]
            for track in tracks_json_info:
                new_track_info = SingleTrackData()
                new_track_info.codec = str(track["codec"])
                new_track_info.id = str(track["id"])
                new_track_info.is_default = str(
                    get_attribute(data=track["properties"], attribute="default_track", default_value="no"))
                new_track_info.is_forced = str(
                    get_attribute(data=track["properties"], attribute="forced_track", default_value="no"))
                new_track_info.language = str(
                    get_attribute(data=track["properties"], attribute="language", default_value="UND"))
                new_track_info.track_name = str(
                    get_attribute(data=track["properties"], attribute="track_name", default_value="Unnamed"))
                if track["type"] == "audio":
                    audios_track_info.append(new_track_info)
                elif track["type"] == "subtitles":
                    subtitles_track_info.append(new_track_info)
                elif track["type"] == "video":
                    videos_track_info.append(new_track_info)
            for chapter in chapters_json_info:
                chapter_num_entries = chapter["num_entries"]
            for attachment in attachments_json_info:
                attachments_info.append(attachment["file_name"])
            file_name = os.path.basename(video_name)
            file_row = add_row(parent=self, name=file_name)
            if len(videos_track_info) > 0:
                video_main_string = "Videos " + "(" + str(len(videos_track_info)) + ")"
                video_main_row = add_row(parent=file_row, name=video_main_string)
                for video_track in videos_track_info:
                    video_track_string = "Track Id: " + str(video_track.id) + " | " + "Name: " + str(
                        video_track.track_name) + " | " + "Language: " + str(
                        video_track.language).upper() + " | " + "Codec: " + str(video_track.codec)
                    video_track_row = add_row(parent=video_main_row, name=video_track_string)

            if len(audios_track_info) > 0:
                audio_main_string = "Audios " + "(" + str(len(audios_track_info)) + ")"
                audio_main_row = add_row(parent=file_row, name=audio_main_string)
                for audio_track in audios_track_info:
                    audio_track_string = "Track Id: " + str(audio_track.id) + " | " + "Name: " + str(
                        audio_track.track_name) + " | " + "Language: " + str(
                        audio_track.language).upper() + " | " + "Codec: " + str(audio_track.codec)
                    audio_track_row = add_row(parent=audio_main_row, name=audio_track_string)

            if len(subtitles_track_info) > 0:
                subtitle_main_string = "Subtitles " + "(" + str(len(subtitles_track_info)) + ")"
                subtitle_main_row = add_row(parent=file_row, name=subtitle_main_string)
                for subtitle_track in subtitles_track_info:
                    subtitle_track_string = "Track Id: " + str(subtitle_track.id) + " | " + "Name: " + str(
                        subtitle_track.track_name) + " | " + "Language: " + str(
                        subtitle_track.language).upper() + " | " + "Codec: " + str(subtitle_track.codec)
                    subtitle_track_row = add_row(parent=subtitle_main_row, name=subtitle_track_string)
            if len(attachments_info) > 0:
                attachment_main_string = "Attachments " + "(" + str(len(attachments_info)) + ")"
                attachment_main_row = add_row(parent=file_row, name=attachment_main_string)
                for attachment_name in attachments_info:
                    attachment_file_row = add_row(parent=attachment_main_row, name=attachment_name)
            if chapter_num_entries != "":
                chapter_main_string = "Chapters - Number of Entries: " + str(chapter_num_entries)
                chapter_main_row = add_row(parent=file_row, name=chapter_main_string)
