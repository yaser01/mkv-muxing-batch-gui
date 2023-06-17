import json
import os
import subprocess
import sys

from packages.Startup import GlobalFiles
from packages.Startup.PreDefined import ISO_639_2_LANGUAGES
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.SingleJobData import SingleJobData
from packages.Widgets.SingleAttachmentData import SingleAttachmentData
from packages.Widgets.SingleTrackData import SingleTrackData


def add_two_spaces():
    return "  "


def add_double_quotation(string):
    return add_two_spaces() + "\"" + str(string) + "\""


def add_json_line(string):
    return "\n" + add_double_quotation(string) + ","


def delete_trailing_zero_string(string):
    return str(int(str(string)))


def check_for_system_backslash_path(string):
    if sys.platform == "win32":  # Windows
        return string.replace('\\', '\\\\')
    else:
        return string


def increase_id_by_one(string):
    return str(int(string) + 1)


def check_type_of_track_chosen(track):
    value = ""
    left_bracket_index = track.find("[")
    right_bracket_index = track.rfind("]")
    value = track[left_bracket_index + 1:right_bracket_index]
    if track.find("Track Id: [") == 0:
        return "id", value
    elif track.find("Language: [") == 0:
        return "lang", value
    elif track.find("Track Name: [") == 0:
        return "name", value


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


class GetJsonForMkvpropeditJob:
    def __init__(self, job: SingleJobData):
        self.job = job
        self.file_info_json = ""
        self.ui_language_command = ""
        self.input_video_command = ""
        self.attachments_attach_command = ""
        self.chapter_attach_command = ""
        self.discard_old_attachments_command = ""
        self.number_of_old_attachments = 0
        self.change_default_forced_subtitle_track_setting_source_video_command = ""
        self.change_default_forced_audio_track_setting_source_video_command = ""
        self.modify_old_videos_command = ""
        self.modify_old_audios_command = ""
        self.modify_old_subtitles_command = ""
        self.final_command = ""
        self.json_info = ""
        self.tracks_json_info = ""
        self.videos_track_json_info = []  # type: list[SingleTrackData]
        self.subtitles_track_json_info = []  # type: list[SingleTrackData]
        self.audios_track_json_info = []  # type: list[SingleTrackData]
        self.attachments_json_info = []  # type: list[SingleAttachmentData]
        self.setup_commands()
        self.generate_mkvpropedit_json_file()

    def setup_commands(self):
        self.generate_info_file()
        self.setup_attachments_options()
        self.setup_chapter_options()
        self.modify_old_videos_tracks()
        self.modify_old_subtitles_tracks()
        self.modify_old_audios_tracks()
        self.make_this_subtitle_default_forced()
        self.make_this_audio_default_forced()
        self.setup_ui_language()
        self.setup_input_video_command()
        self.setup_final_command()

    def generate_info_file(self):
        info_file_path = GlobalFiles.mkvmergeJsonInfoFilePath
        with open(info_file_path, 'w+', encoding="UTF-8") as info_file:
            command = add_double_quotation(GlobalFiles.MKVMERGE_PATH) + " -J " + add_double_quotation(
                self.job.video_name_absolute)
            subprocess.run(command, shell=True, stdout=info_file)
        with open(info_file_path, 'r', encoding="UTF-8") as info_file:
            self.json_info = json.load(info_file)
        self.number_of_old_attachments = len(self.json_info["attachments"])
        self.tracks_json_info = self.json_info["tracks"]
        for track in self.tracks_json_info:
            new_track_info = SingleTrackData()
            new_track_info.id = str(track["id"])
            new_track_info.is_default = str(
                get_attribute(data=track["properties"], attribute="default_track", default_value="no"))
            new_track_info.is_forced = str(
                get_attribute(data=track["properties"], attribute="forced_track", default_value="no"))
            new_track_info.language = str(
                get_attribute(data=track["properties"], attribute="language", default_value="eng"))
            new_track_info.track_name = str(
                get_attribute(data=track["properties"], attribute="track_name", default_value="UnNamedTrackBeBo"))
            new_track_info.uid = str(
                get_attribute(data=track["properties"], attribute="uid", default_value="-1"))
            if track["type"] == "audio":
                self.audios_track_json_info.append(new_track_info)
            elif track["type"] == "subtitles":
                self.subtitles_track_json_info.append(new_track_info)
            elif track["type"] == "video":
                self.videos_track_json_info.append(new_track_info)
        for attachment in self.json_info["attachments"]:
            new_attachment_info = SingleAttachmentData()
            new_attachment_info.file_name = str(
                get_attribute(data=attachment, attribute="file_name", default_value="no_name.ttf"))
            new_attachment_info.id = str(get_attribute(data=attachment, attribute="id", default_value="-1"))
            new_attachment_info.size = get_attribute(data=attachment, attribute="size", default_value=0)
            self.attachments_json_info.append(new_attachment_info)

    def setup_attachments_options(self):
        if len(self.job.attachments_absolute_path)>0:
            attachments_list_with_attach_command = []
            discard_old_attachments_list_command = []
            allow_duplicates = self.job.allow_duplicates_attachments
            discard_old = self.job.discard_old_attachments
            if discard_old:
                for i in range(self.number_of_old_attachments + 2):
                    attachments_list_with_attach_command.append(add_json_line("--delete-attachment"))
                    attachments_list_with_attach_command.append(add_json_line(str(i)))
            for file_to_attach in self.job.attachments_absolute_path:
                file_name_to_attach = os.path.basename(file_to_attach)
                if not discard_old and not allow_duplicates:
                    attachment_already_found = False
                    for attachment in self.attachments_json_info:
                        if attachment.file_name == file_name_to_attach:
                            attachment_already_found = True
                            break
                    if attachment_already_found:
                        continue
                attachments_list_with_attach_command.append(add_json_line("--add-attachment"))
                attachments_list_with_attach_command.append(
                    add_json_line(check_for_system_backslash_path(file_to_attach)))
            self.attachments_attach_command = "".join(attachments_list_with_attach_command)
            self.discard_old_attachments_command = "".join(discard_old_attachments_list_command)

    def setup_chapter_options(self):
        if GlobalSetting.CHAPTER_ENABLED:
            if self.job.chapter_found:
                self.chapter_attach_command = add_json_line("--chapters") + \
                                              add_json_line(
                                                  check_for_system_backslash_path(self.job.chapter_name_absolute))
            elif GlobalSetting.CHAPTER_DISCARD_OLD:
                self.chapter_attach_command = add_json_line("--chapters") + add_json_line("")

    def modify_old_videos_tracks(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_MODIFIED_ACTIVATED:
            old_video_command_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING[track_id]
                found = False
                for video_track in self.videos_track_json_info:
                    if video_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                if bulk_track.language != "[Old]":
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(
                        add_json_line(f"language={ISO_639_2_LANGUAGES[bulk_track.language]}"))
                # add video track name
                if bulk_track.track_name != "[Old]":
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(add_json_line(f"name={bulk_track.track_name}"))
                # add video set default
                if bulk_track.is_default == 2:
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(add_json_line("flag-default=1"))
                elif bulk_track.is_default == 0:
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(add_json_line("flag-default=0"))
                # add video set forced
                if bulk_track.is_forced == 2:
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(add_json_line("flag-forced=1"))
                elif bulk_track.is_forced == 0:
                    old_video_command_list.append(add_json_line("--edit"))
                    old_video_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_video_command_list.append(add_json_line("--set"))
                    old_video_command_list.append(add_json_line("flag-forced=0"))
            self.modify_old_videos_command += ''.join(
                old_video_command_list)

    def modify_old_subtitles_tracks(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_MODIFIED_ACTIVATED:
            old_subtitle_command_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING[track_id]
                found = False
                for subtitle_track in self.subtitles_track_json_info:
                    if subtitle_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                if bulk_track.language != "[Old]":
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(
                        add_json_line(f"language={ISO_639_2_LANGUAGES[bulk_track.language]}"))
                # add subtitle track name
                if bulk_track.track_name != "[Old]":
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(add_json_line(f"name={bulk_track.track_name}"))
                # add subtitle set default
                if bulk_track.is_default == 2:
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(add_json_line("flag-default=1"))
                elif bulk_track.is_default == 0:
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(add_json_line("flag-default=0"))
                # add subtitle set forced
                if bulk_track.is_forced == 2:
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(add_json_line("flag-forced=1"))
                elif bulk_track.is_forced == 0:
                    old_subtitle_command_list.append(add_json_line("--edit"))
                    old_subtitle_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_subtitle_command_list.append(add_json_line("--set"))
                    old_subtitle_command_list.append(add_json_line("flag-forced=0"))
            self.modify_old_subtitles_command += ''.join(
                old_subtitle_command_list)

    def modify_old_audios_tracks(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_MODIFIED_ACTIVATED:
            old_audio_command_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING[track_id]
                found = False
                for audio_track in self.audios_track_json_info:
                    if audio_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                if bulk_track.language != "[Old]":
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(
                        add_json_line(f"language={ISO_639_2_LANGUAGES[bulk_track.language]}"))
                # add audio track name
                if bulk_track.track_name != "[Old]":
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(add_json_line(f"name={bulk_track.track_name}"))
                # add audio set default
                if bulk_track.is_default == 2:
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(add_json_line("flag-default=1"))
                elif bulk_track.is_default == 0:
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(add_json_line("flag-default=0"))
                # add audio set forced
                if bulk_track.is_forced == 2:
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(add_json_line("flag-forced=1"))
                elif bulk_track.is_forced == 0:
                    old_audio_command_list.append(add_json_line("--edit"))
                    old_audio_command_list.append(
                        add_json_line("track:" + increase_id_by_one(bulk_track.id)))
                    old_audio_command_list.append(add_json_line("--set"))
                    old_audio_command_list.append(add_json_line("flag-forced=0"))
            self.modify_old_audios_command += ''.join(
                old_audio_command_list)

    def make_this_subtitle_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_SEMI_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if not subtitle_track.isspace():
                change_default_subtitle_commands_list = []
                if subtitle_track == "":
                    for subtitle in self.subtitles_track_json_info:
                        change_default_subtitle_commands_list.append(add_json_line("--edit"))
                        change_default_subtitle_commands_list.append(
                            add_json_line("track:" + increase_id_by_one(subtitle.id)))
                        change_default_subtitle_commands_list.append(add_json_line("--set"))
                        change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                    self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                        change_default_subtitle_commands_list)
                else:
                    subtitle_track_id = ""
                    track_type, track_value = check_type_of_track_chosen(subtitle_track)
                    if track_type == "id":
                        subtitle_track_id = delete_trailing_zero_string(track_value)
                        found_subtitle_with_this_id = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.id == subtitle_track_id:
                                found_subtitle_with_this_id = True
                                break
                        if found_subtitle_with_this_id:
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))

                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "lang":
                        subtitle_track_language = ISO_639_2_LANGUAGES[track_value]
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.language == subtitle_track_language:
                                subtitle_track_id = subtitle.id
                                break
                        if subtitle_track_id != "":
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "name":
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.track_name == track_value:
                                subtitle_track_id = subtitle.id
                                break
                        if subtitle_track_id != "":
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_FULL_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if not subtitle_track.isspace():
                change_default_subtitle_commands_list = []
                if subtitle_track == "":
                    for subtitle in self.subtitles_track_json_info:
                        change_default_subtitle_commands_list.append(add_json_line("--edit"))
                        change_default_subtitle_commands_list.append(
                            add_json_line("track:" + increase_id_by_one(subtitle.id)))
                        change_default_subtitle_commands_list.append(add_json_line("--set"))
                        change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                        change_default_subtitle_commands_list.append(add_json_line("--set"))
                        change_default_subtitle_commands_list.append(add_json_line("flag-forced=0"))
                    self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                        change_default_subtitle_commands_list)
                else:
                    subtitle_track_id = ""
                    track_type, track_value = check_type_of_track_chosen(subtitle_track)
                    if track_type == "id":
                        subtitle_track_id = delete_trailing_zero_string(track_value)
                        found_subtitle_with_this_id = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.id == subtitle_track_id:
                                found_subtitle_with_this_id = True
                                break
                        if found_subtitle_with_this_id:
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-forced=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-forced=0"))

                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "lang":
                        subtitle_track_language = ISO_639_2_LANGUAGES[track_value]
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.language == subtitle_track_language:
                                subtitle_track_id = subtitle.id
                                break
                        if subtitle_track_id != "":
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-forced=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-forced=0"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "name":
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.track_name == track_value:
                                subtitle_track_id = subtitle.id
                                break
                        if subtitle_track_id != "":
                            change_default_subtitle_commands_list.append(add_json_line("--edit"))
                            change_default_subtitle_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(subtitle_track_id)))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-default=1"))
                            change_default_subtitle_commands_list.append(add_json_line("--set"))
                            change_default_subtitle_commands_list.append(add_json_line("flag-forced=1"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--edit"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(subtitle.id)))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_subtitle_commands_list.append(add_json_line("--set"))
                                    change_default_subtitle_commands_list.append(add_json_line("flag-forced=0"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)

    def make_this_audio_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if not audio_track.isspace():
                change_default_audio_commands_list = []
                if audio_track == "":
                    for audio in self.audios_track_json_info:
                        change_default_audio_commands_list.append(add_json_line("--edit"))
                        change_default_audio_commands_list.append(
                            add_json_line("track:" + increase_id_by_one(audio.id)))
                        change_default_audio_commands_list.append(add_json_line("--set"))
                        change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                    self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                        change_default_audio_commands_list)
                else:
                    audio_track_id = ""
                    track_type, track_value = check_type_of_track_chosen(audio_track)
                    if track_type == "id":
                        audio_track_id = delete_trailing_zero_string(track_value)
                        found_audio_with_this_id = False
                        for audio in self.audios_track_json_info:
                            if audio.id == audio_track_id:
                                found_audio_with_this_id = True
                                break
                        if found_audio_with_this_id:
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))

                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "lang":
                        audio_track_language = ISO_639_2_LANGUAGES[track_value]
                        for audio in self.audios_track_json_info:
                            if audio.language == audio_track_language:
                                audio_track_id = audio.id
                                break
                        if audio_track_id != "":
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "name":
                        for audio in self.audios_track_json_info:
                            if audio.track_name == track_value:
                                audio_track_id = audio.id
                                break
                        if audio_track_id != "":
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if not audio_track.isspace():
                change_default_audio_commands_list = []
                if audio_track == "":
                    for audio in self.audios_track_json_info:
                        change_default_audio_commands_list.append(add_json_line("--edit"))
                        change_default_audio_commands_list.append(
                            add_json_line("track:" + increase_id_by_one(audio.id)))
                        change_default_audio_commands_list.append(add_json_line("--set"))
                        change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                        change_default_audio_commands_list.append(add_json_line("--set"))
                        change_default_audio_commands_list.append(add_json_line("flag-forced=0"))
                    self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                        change_default_audio_commands_list)
                else:
                    audio_track_id = ""
                    track_type, track_value = check_type_of_track_chosen(audio_track)
                    if track_type == "id":
                        audio_track_id = delete_trailing_zero_string(track_value)
                        found_audio_with_this_id = False
                        for audio in self.audios_track_json_info:
                            if audio.id == audio_track_id:
                                found_audio_with_this_id = True
                                break
                        if found_audio_with_this_id:
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-forced=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-forced=0"))

                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "lang":
                        audio_track_language = ISO_639_2_LANGUAGES[track_value]
                        for audio in self.audios_track_json_info:
                            if audio.language == audio_track_language:
                                audio_track_id = audio.id
                                break
                        if audio_track_id != "":
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-forced=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-forced=0"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "name":
                        for audio in self.audios_track_json_info:
                            if audio.track_name == track_value:
                                audio_track_id = audio.id
                                break
                        if audio_track_id != "":
                            change_default_audio_commands_list.append(add_json_line("--edit"))
                            change_default_audio_commands_list.append(
                                add_json_line("track:" + increase_id_by_one(audio_track_id)))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-default=1"))
                            change_default_audio_commands_list.append(add_json_line("--set"))
                            change_default_audio_commands_list.append(add_json_line("flag-forced=1"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--edit"))
                                    change_default_audio_commands_list.append(
                                        add_json_line("track:" + increase_id_by_one(audio.id)))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-default=0"))
                                    change_default_audio_commands_list.append(add_json_line("--set"))
                                    change_default_audio_commands_list.append(add_json_line("flag-forced=0"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)

    # noinspection PyListCreation
    def setup_ui_language(self):
        ui_language_commands_list = []
        ui_language_commands_list.append(add_double_quotation("--ui-language") + ",")
        if sys.platform == "win32":
            ui_language_commands_list.append(add_json_line("en"))
        else:
            ui_language_commands_list.append(add_json_line("en_US"))
        self.ui_language_command = "".join(ui_language_commands_list)

    # noinspection PyListCreation
    def setup_input_video_command(self):
        input_video_commands_list = []
        input_video_commands_list.append(add_json_line(check_for_system_backslash_path(self.job.video_name_absolute)))
        self.input_video_command = "".join(input_video_commands_list)

    def setup_final_command(self):
        self.final_command = "["
        self.final_command += "\n"
        self.final_command += self.ui_language_command
        self.final_command += self.input_video_command
        self.final_command += self.change_default_forced_subtitle_track_setting_source_video_command
        self.final_command += self.change_default_forced_audio_track_setting_source_video_command
        self.final_command += self.modify_old_videos_command
        self.final_command += self.modify_old_audios_command
        self.final_command += self.modify_old_subtitles_command
        self.final_command += self.discard_old_attachments_command
        self.final_command += self.attachments_attach_command
        self.final_command += self.chapter_attach_command
        self.final_command = self.final_command[:-1]  # delete last ,
        self.final_command += "\n"
        self.final_command += "]"

    def generate_mkvpropedit_json_file(self):
        job_file_path = GlobalFiles.mkvpropeditJsonJobFilePath
        with open(job_file_path, 'w+', encoding="UTF-8") as job_file:
            job_file.write(self.final_command)
