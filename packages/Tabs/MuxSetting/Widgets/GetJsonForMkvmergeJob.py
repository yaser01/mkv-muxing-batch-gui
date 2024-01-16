import json
import operator
import os
import subprocess
import sys
from pathlib import Path
from platform import platform
from sys import platform

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


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def change_file_extension_to_mkv(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[:file_extension_start_index] + ".mkv"
    return new_file_name_with_mkv_extension


def change_file_extension_to_mkv_with_random_suffix(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[
                                       :file_extension_start_index] + "#" + GlobalSetting.RANDOM_OUTPUT_SUFFIX + ".mkv "
    return new_file_name_with_mkv_extension


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


class GetJsonForMkvmergeJob:
    def __init__(self, job: SingleJobData):
        self.job = job
        self.current_track_index = 1
        self.file_info_json = ""
        self.ui_language_command = ""
        self.output_video_command = ""
        self.input_video_command = ""
        self.attachments_attach_command = ""
        self.chapter_attach_command = ""
        self.new_subtitle_append_command = ""
        self.new_audio_append_command = ""
        self.old_video_append_command = ""
        self.old_audio_append_command = ""
        self.old_subtitle_append_command = ""
        self.discard_old_attachments_command = ""
        self.change_default_forced_subtitle_track_setting_source_video_command = ""
        self.change_default_forced_audio_track_setting_source_video_command = ""
        self.specify_video_track_source_video_command = ""
        self.specify_subtitle_track_source_video_command = ""
        self.specify_audio_track_source_video_command = ""
        self.video_default_duration_fps_command = ""
        self.track_order_line = ""
        self.track_order_command = ""
        self.final_command = ""
        self.json_info = ""
        self.tracks_json_info = ""
        self.videos_track_json_info = []  # type: list[SingleTrackData]
        self.subtitles_track_json_info = []  # type: list[SingleTrackData]
        self.audios_track_json_info = []  # type: list[SingleTrackData]
        self.attachments_json_info = []  # type: list[SingleAttachmentData]
        self.setup_commands()
        self.generate_mkvmerge_json_job_file()

    def setup_commands(self):
        self.generate_info_file()
        self.setup_video_track_order()
        self.setup_attachments_options()
        self.setup_chapter_options()
        self.setup_old_video_tracks_options()
        self.setup_new_audio_tracks_options()
        self.setup_old_audio_tracks_options()
        self.setup_audio_track_order()
        self.setup_new_subtitle_tracks_options()
        self.setup_old_subtitle_tracks_options()
        self.setup_subtitle_track_order()
        self.setup_which_old_videos_to_keep()
        self.setup_which_old_subtitles_to_keep()
        self.setup_which_old_audios_to_keep()
        self.make_this_subtitle_default_forced()
        self.make_this_audio_default_forced()
        self.setup_ui_language()
        self.setup_output_video_command()
        self.setup_input_video_command()
        self.setup_video_default_duration_fps_command()
        self.setup_track_order_command()
        self.setup_final_command()

    def generate_info_file(self):
        info_file_path = GlobalFiles.mkvmergeJsonInfoFilePath
        with open(info_file_path, 'w+', encoding="UTF-8") as info_file:
            command = add_double_quotation(GlobalFiles.MKVMERGE_PATH) + " -J " + add_double_quotation(
                self.job.video_name_absolute)
            subprocess.run(command, shell=True, stdout=info_file, env=GlobalFiles.ENVIRONMENT)
        with open(info_file_path, 'r', encoding="UTF-8") as info_file:
            self.json_info = json.load(info_file)
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
        discard_old = self.job.discard_old_attachments
        if discard_old:
            self.discard_old_attachments_command = add_json_line("--no-attachments")
        if len(self.job.attachments_absolute_path) > 0:
            allow_duplicates = self.job.allow_duplicates_attachments
            attachments_list_with_attach_command = []
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
                attachments_list_with_attach_command.append(add_json_line("--attach-file"))
                attachments_list_with_attach_command.append(
                    add_json_line(check_for_system_backslash_path(file_to_attach)))
            self.attachments_attach_command = "".join(attachments_list_with_attach_command)

    def setup_chapter_options(self):
        if GlobalSetting.CHAPTER_ENABLED:
            if self.job.chapter_found:
                self.chapter_attach_command = add_json_line("--chapters") + \
                                              add_json_line(
                                                  check_for_system_backslash_path(self.job.chapter_name_absolute))
            elif GlobalSetting.CHAPTER_DISCARD_OLD:
                self.discard_old_attachments_command = add_json_line("--no-chapters")

    def setup_video_default_duration_fps_command(self):
        if GlobalSetting.VIDEO_DEFAULT_DURATION_FPS not in ["", "Default"]:
            self.video_default_duration_fps_command = add_json_line("--default-duration") + add_json_line(
                "0:" + GlobalSetting.VIDEO_DEFAULT_DURATION_FPS)

    def setup_video_track_order(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_REORDER_ACTIVATED:
            for bulk_track in (
                    sorted(GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING.values(),
                           key=operator.attrgetter('order'))):
                if not bulk_track.is_enabled:
                    continue
                for video_track in self.videos_track_json_info:
                    if video_track.id == bulk_track.id:
                        self.track_order_line += "0:" + str(video_track.id) + ","
                        break
        else:
            for video in self.videos_track_json_info:
                self.track_order_line += "0:" + str(video.id) + ","

    def setup_old_video_tracks_options(self):
        old_video_command_list = []
        if GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_MODIFIED_ACTIVATED:
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING[track_id]
                if not bulk_track.is_enabled:
                    continue
                found = False
                for video_track in self.videos_track_json_info:
                    if video_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                # add video language
                if bulk_track.language != "[Old]":
                    old_video_command_list.append(add_json_line("--language"))
                    old_video_command_list.append(
                        add_json_line(f"{track_id}:" + ISO_639_2_LANGUAGES[bulk_track.language]))
                # add video track name
                if bulk_track.track_name != "[Old]":
                    old_video_command_list.append(add_json_line("--track-name"))
                    old_video_command_list.append(add_json_line(f"{track_id}:" + bulk_track.track_name))
                # add video set default
                if bulk_track.is_default == 2:
                    old_video_command_list.append(add_json_line("--default-track-flag"))
                    old_video_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_default == 0:
                    old_video_command_list.append(add_json_line("--default-track-flag"))
                    old_video_command_list.append(add_json_line(f"{track_id}:no"))
                # add video set forced
                if bulk_track.is_forced == 2:
                    old_video_command_list.append(add_json_line("--forced-display-flag"))
                    old_video_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_forced == 0:
                    old_video_command_list.append(add_json_line("--forced-display-flag"))
                    old_video_command_list.append(add_json_line(f"{track_id}:no"))
            self.old_video_append_command = "".join(old_video_command_list)

    def setup_old_subtitle_tracks_options(self):
        old_subtitle_command_list = []
        if GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_MODIFIED_ACTIVATED:
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING[track_id]
                if not bulk_track.is_enabled:
                    continue
                found = False
                for subtitle_track in self.subtitles_track_json_info:
                    if subtitle_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                # add subtitle language
                if bulk_track.language != "[Old]":
                    old_subtitle_command_list.append(add_json_line("--language"))
                    old_subtitle_command_list.append(
                        add_json_line(f"{track_id}:" + ISO_639_2_LANGUAGES[bulk_track.language]))
                # add subtitle track name
                if bulk_track.track_name != "[Old]":
                    old_subtitle_command_list.append(add_json_line("--track-name"))
                    old_subtitle_command_list.append(add_json_line(f"{track_id}:" + bulk_track.track_name))
                # add subtitle set default
                if bulk_track.is_default == 2:
                    old_subtitle_command_list.append(add_json_line("--default-track-flag"))
                    old_subtitle_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_default == 0:
                    old_subtitle_command_list.append(add_json_line("--default-track-flag"))
                    old_subtitle_command_list.append(add_json_line(f"{track_id}:no"))
                # add subtitle set forced
                if bulk_track.is_forced == 2:
                    old_subtitle_command_list.append(add_json_line("--forced-display-flag"))
                    old_subtitle_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_forced == 0:
                    old_subtitle_command_list.append(add_json_line("--forced-display-flag"))
                    old_subtitle_command_list.append(add_json_line(f"{track_id}:no"))
            self.old_subtitle_append_command = "".join(old_subtitle_command_list)

    def setup_new_subtitle_tracks_options(self):
        if GlobalSetting.SUBTITLE_ENABLED:
            subtitle_command_list = []
            if self.job.subtitle_found:
                for i in range(len(self.job.subtitle_name_absolute)):
                    # add subtitle language
                    subtitle_command_list.append(add_json_line("--language"))
                    subtitle_command_list.append(
                        add_json_line("0:" + ISO_639_2_LANGUAGES[self.job.subtitle_language[i]]))
                    # add subtitle track name
                    if self.job.subtitle_track_name != "":
                        subtitle_command_list.append(add_json_line("--track-name"))
                        subtitle_command_list.append(add_json_line("0:" + self.job.subtitle_track_name[i]))
                    # add subtitle set default
                    if self.job.subtitle_set_default[i]:
                        subtitle_command_list.append(add_json_line("--default-track"))
                        subtitle_command_list.append(add_json_line("0:yes"))
                        self.make_other_subtitle_not_default()
                    else:
                        subtitle_command_list.append(add_json_line("--default-track"))
                        subtitle_command_list.append(add_json_line("0:no"))
                    # add subtitle set forced
                    if self.job.subtitle_set_forced[i]:
                        subtitle_command_list.append(add_json_line("--forced-track"))
                        subtitle_command_list.append(add_json_line("0:yes"))
                        self.make_other_subtitle_not_forced()
                    else:
                        subtitle_command_list.append(add_json_line("--forced-track"))
                        subtitle_command_list.append(add_json_line("0:no"))
                    # add subtitle delay
                    subtitle_delay_in_millisecond = int(1000 * float(self.job.subtitle_delay[i]))
                    subtitle_command_list.append(add_json_line("--sync"))
                    subtitle_command_list.append(add_json_line("0:" + str(subtitle_delay_in_millisecond)))
                    # add subtitle file
                    subtitle_command_list.append(add_json_line("("))
                    subtitle_command_list.append(
                        add_json_line(check_for_system_backslash_path(self.job.subtitle_name_absolute[i])))
                    subtitle_command_list.append(add_json_line(")"))
                self.new_subtitle_append_command = "".join(subtitle_command_list)

    def setup_subtitle_track_order(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_REORDER_ACTIVATED:
            later_subtitle_tracks = ""
            for i in range(len(self.job.subtitle_name_absolute)):
                if self.job.subtitle_set_at_top[i] == 0:
                    self.track_order_line += str(self.current_track_index) + ":0,"
                else:
                    later_subtitle_tracks += str(self.current_track_index) + ":0,"
                self.current_track_index += 1
            for bulk_track in (
                    sorted(GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING.values(),
                           key=operator.attrgetter('order'))):
                if not bulk_track.is_enabled:
                    continue
                for subtitle_track in self.subtitles_track_json_info:
                    if subtitle_track.id == bulk_track.id:
                        self.track_order_line += "0:" + str(subtitle_track.id) + ","
                        break
            self.track_order_line += later_subtitle_tracks
        else:
            tracks_order_list = []
            for i in range(len(self.job.subtitle_name_absolute)):
                if self.job.subtitle_set_at_top[i] != -1:
                    tracks_order_list.append(
                        (self.job.subtitle_set_at_top[i], False, int(i), str(self.current_track_index) + ":0,"))
                else:
                    tracks_order_list.append(
                        (555, True, i, str(self.current_track_index) + ":0,"))
                self.current_track_index += 1
            order_id = 0
            for bulk_track in (
                    sorted(GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING.values(),
                           key=operator.attrgetter('order'))):
                if not bulk_track.is_enabled:
                    continue
                for subtitle_track in self.subtitles_track_json_info:
                    if subtitle_track.id == bulk_track.id:
                        tracks_order_list.append(
                            (order_id, True, int(subtitle_track.id), "0:" + str(subtitle_track.id) + ","))
                        order_id += 1
                        break
            tracks_order_list.sort()
            for track_order in tracks_order_list:
                self.track_order_line += track_order[3]

    def setup_old_audio_tracks_options(self):
        old_audio_command_list = []
        if GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_MODIFIED_ACTIVATED:
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING[track_id]
                if not bulk_track.is_enabled:
                    continue
                found = False
                for audio_track in self.audios_track_json_info:
                    if audio_track.id == bulk_track.id:
                        found = True
                        break
                if not found:
                    continue
                # add audio language
                if bulk_track.language != "[Old]":
                    old_audio_command_list.append(add_json_line("--language"))
                    old_audio_command_list.append(
                        add_json_line(f"{track_id}:" + ISO_639_2_LANGUAGES[bulk_track.language]))
                # add audio track name
                if bulk_track.track_name != "[Old]":
                    old_audio_command_list.append(add_json_line("--track-name"))
                    old_audio_command_list.append(add_json_line(f"{track_id}:" + bulk_track.track_name))
                # add audio set default
                if bulk_track.is_default == 2:
                    old_audio_command_list.append(add_json_line("--default-track-flag"))
                    old_audio_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_default == 0:
                    old_audio_command_list.append(add_json_line("--default-track-flag"))
                    old_audio_command_list.append(add_json_line(f"{track_id}:no"))
                # add audio set forced
                if bulk_track.is_forced == 2:
                    old_audio_command_list.append(add_json_line("--forced-display-flag"))
                    old_audio_command_list.append(add_json_line(f"{track_id}:yes"))
                elif bulk_track.is_forced == 0:
                    old_audio_command_list.append(add_json_line("--forced-display-flag"))
                    old_audio_command_list.append(add_json_line(f"{track_id}:no"))
            self.old_audio_append_command = "".join(old_audio_command_list)

    def setup_new_audio_tracks_options(self):
        if GlobalSetting.AUDIO_ENABLED:
            audio_command_list = []
            if self.job.audio_found:
                for i in range(len(self.job.audio_name_absolute)):
                    # add audio language
                    audio_command_list.append(add_json_line("--language"))
                    audio_command_list.append(
                        add_json_line("0:" + ISO_639_2_LANGUAGES[self.job.audio_language[i]]))
                    # add audio track name
                    if self.job.audio_track_name != "":
                        audio_command_list.append(add_json_line("--track-name"))
                        audio_command_list.append(add_json_line("0:" + self.job.audio_track_name[i]))
                    # add audio set default
                    if self.job.audio_set_default[i]:
                        audio_command_list.append(add_json_line("--default-track"))
                        audio_command_list.append(add_json_line("0:yes"))
                        self.make_other_audio_not_default()
                    else:
                        audio_command_list.append(add_json_line("--default-track"))
                        audio_command_list.append(add_json_line("0:no"))
                    # add audio set forced
                    if self.job.audio_set_forced[i]:
                        audio_command_list.append(add_json_line("--forced-track"))
                        audio_command_list.append(add_json_line("0:yes"))
                        self.make_other_audio_not_forced()
                    else:
                        audio_command_list.append(add_json_line("--forced-track"))
                        audio_command_list.append(add_json_line("0:no"))
                    # add audio delay
                    audio_delay_in_millisecond = int(1000 * float(self.job.audio_delay[i]))
                    audio_command_list.append(add_json_line("--sync"))
                    audio_command_list.append(add_json_line("0:" + str(audio_delay_in_millisecond)))
                    # add audio file
                    audio_command_list.append(add_json_line("("))
                    audio_command_list.append(
                        add_json_line(check_for_system_backslash_path(self.job.audio_name_absolute[i])))
                    audio_command_list.append(add_json_line(")"))
                self.new_audio_append_command = "".join(audio_command_list)

    def setup_audio_track_order(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_REORDER_ACTIVATED:
            later_audio_tracks = ""
            for i in range(len(self.job.audio_name_absolute)):
                if self.job.audio_set_at_top[i] == 0:
                    self.track_order_line += str(self.current_track_index) + ":0,"
                else:
                    later_audio_tracks += str(self.current_track_index) + ":0,"
                self.current_track_index += 1
            for bulk_track in (
                    sorted(GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.values(),
                           key=operator.attrgetter('order'))):
                if not bulk_track.is_enabled:
                    continue
                for audio_track in self.audios_track_json_info:
                    if audio_track.id == bulk_track.id:
                        self.track_order_line += "0:" + str(audio_track.id) + ","
                        break
            self.track_order_line += later_audio_tracks
        else:
            tracks_order_list = []
            for i in range(len(self.job.audio_name_absolute)):
                if self.job.audio_set_at_top[i] != -1:
                    tracks_order_list.append(
                        (self.job.audio_set_at_top[i], False, int(i), str(self.current_track_index) + ":0,"))
                else:
                    tracks_order_list.append(
                        (555, True, i, str(self.current_track_index) + ":0,"))
                self.current_track_index += 1
            order_id = 0
            for bulk_track in (
                    sorted(GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.values(),
                           key=operator.attrgetter('order'))):
                if not bulk_track.is_enabled:
                    continue
                for audio_track in self.audios_track_json_info:
                    if audio_track.id == bulk_track.id:
                        tracks_order_list.append(
                            (order_id, True, int(audio_track.id), "0:" + str(audio_track.id) + ","))
                        order_id += 1
                        break
            tracks_order_list.sort()
            for track_order in tracks_order_list:
                self.track_order_line += track_order[3]

    def make_other_subtitle_not_default(self):
        change_default_subtitle_commands_list = []
        for track in self.subtitles_track_json_info:
            change_default_subtitle_commands_list.append(add_json_line("--default-track"))
            change_default_subtitle_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_subtitle_track_setting_source_video_command += "".join(
            change_default_subtitle_commands_list)

    def make_other_subtitle_not_forced(self):
        change_forced_subtitle_commands_list = []
        for track in self.subtitles_track_json_info:
            change_forced_subtitle_commands_list.append(add_json_line("--forced-track"))
            change_forced_subtitle_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_subtitle_track_setting_source_video_command += "".join(
            change_forced_subtitle_commands_list)

    def make_other_audio_not_forced(self):
        change_forced_audio_commands_list = []
        for track in self.audios_track_json_info:
            change_forced_audio_commands_list.append(add_json_line("--forced-track"))
            change_forced_audio_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_audio_track_setting_source_video_command += "".join(
            change_forced_audio_commands_list)

    def make_other_audio_not_default(self):
        change_default_audio_commands_list = []
        for track in self.audios_track_json_info:
            change_default_audio_commands_list.append(add_json_line("--default-track"))
            change_default_audio_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_audio_track_setting_source_video_command += "".join(
            change_default_audio_commands_list)

    def setup_which_old_videos_to_keep(self):
        if GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_DELETED_ACTIVATED:
            only_keep_those_video_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_VIDEOS_BULK_SETTING[track_id]
                if bulk_track.is_enabled:
                    found = False
                    for video_track in self.videos_track_json_info:
                        if video_track.id == bulk_track.id:
                            found = True
                            break
                    if not found:
                        continue
                    only_keep_those_video_list.append(bulk_track.id)
            if len(only_keep_those_video_list) > 0:
                self.specify_video_track_source_video_command = add_json_line("--video-tracks")
                self.specify_video_track_source_video_command += add_json_line(
                    ",".join(only_keep_those_video_list))
            else:
                self.specify_video_track_source_video_command = add_json_line("--no-video")

    def setup_which_old_subtitles_to_keep(self):
        if GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED:
            if len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES) == 0:
                self.specify_subtitle_track_source_video_command = add_json_line("--no-subtitles")
            else:
                only_keep_those_subtitle_list = GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_IDS.copy()
                for track_name in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_NAMES:
                    for my_subtitle_track in self.subtitles_track_json_info:
                        if my_subtitle_track.track_name == track_name:
                            only_keep_those_subtitle_list.append(my_subtitle_track.id)
                for language in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS_LANGUAGES:
                    only_keep_those_subtitle_list.append(ISO_639_2_LANGUAGES[language])
                only_keep_those_subtitle_list = list(dict.fromkeys(only_keep_those_subtitle_list))
                if len(only_keep_those_subtitle_list) > 0:
                    self.specify_subtitle_track_source_video_command = add_json_line("--subtitle-tracks")
                    self.specify_subtitle_track_source_video_command += add_json_line(
                        ",".join(only_keep_those_subtitle_list))
                else:
                    self.specify_subtitle_track_source_video_command = add_json_line("--no-subtitles")
        elif GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_DELETED_ACTIVATED:
            only_keep_those_subtitle_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_SUBTITLES_BULK_SETTING[track_id]
                if bulk_track.is_enabled:
                    found = False
                    for subtitle_track in self.subtitles_track_json_info:
                        if subtitle_track.id == bulk_track.id:
                            found = True
                            break
                    if not found:
                        continue
                    only_keep_those_subtitle_list.append(bulk_track.id)
            if len(only_keep_those_subtitle_list) > 0:
                self.specify_subtitle_track_source_video_command = add_json_line("--subtitle-tracks")
                self.specify_subtitle_track_source_video_command += add_json_line(
                    ",".join(only_keep_those_subtitle_list))
            else:
                self.specify_subtitle_track_source_video_command = add_json_line("--no-subtitles")

    def setup_which_old_audios_to_keep(self):
        if GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED:
            if len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES) == 0:
                self.specify_audio_track_source_video_command = add_json_line("--no-audio")
            else:
                only_keep_those_audios_list = GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_IDS.copy()
                for track_name in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_NAMES:
                    for my_audio_track in self.audios_track_json_info:
                        if my_audio_track.track_name == track_name:
                            only_keep_those_audios_list.append(my_audio_track.id)
                for audio in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS_LANGUAGES:
                    only_keep_those_audios_list.append(ISO_639_2_LANGUAGES[audio])
                only_keep_those_audios_list = list(dict.fromkeys(only_keep_those_audios_list))
                if len(only_keep_those_audios_list) > 0:
                    self.specify_audio_track_source_video_command = add_json_line("--audio-tracks")
                    self.specify_audio_track_source_video_command += add_json_line(
                        ",".join(only_keep_those_audios_list))
                else:
                    self.specify_audio_track_source_video_command = add_json_line("--no-audio")
        elif GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_DELETED_ACTIVATED:
            only_keep_those_audios_list = []
            for track_id in GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING.keys():
                bulk_track = GlobalSetting.VIDEO_OLD_TRACKS_AUDIOS_BULK_SETTING[track_id]
                if bulk_track.is_enabled:
                    found = False
                    for audio_track in self.audios_track_json_info:
                        if audio_track.id == bulk_track.id:
                            found = True
                            break
                    if not found:
                        continue
                    only_keep_those_audios_list.append(bulk_track.id)
            if len(only_keep_those_audios_list) > 0:
                self.specify_audio_track_source_video_command = add_json_line("--audio-tracks")
                self.specify_audio_track_source_video_command += add_json_line(
                    ",".join(only_keep_those_audios_list))
            else:
                self.specify_audio_track_source_video_command = add_json_line("--no-audio")

    def make_this_subtitle_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_SEMI_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if not subtitle_track.isspace():
                change_default_subtitle_commands_list = []
                if subtitle_track == "":
                    for subtitle in self.subtitles_track_json_info:
                        change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                        change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                    self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                        change_default_subtitle_commands_list)
                else:
                    track_type, track_value = check_type_of_track_chosen(subtitle_track)
                    subtitle_track_id = ""
                    if track_type == "id":
                        subtitle_track_id = delete_trailing_zero_string(track_value)
                        found_subtitle_with_this_id = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.id == subtitle_track_id:
                                found_subtitle_with_this_id = True
                                break
                        if not found_subtitle_with_this_id:
                            subtitle_track_id = ""
                    elif track_type == "lang":
                        subtitle_track_language = ISO_639_2_LANGUAGES[track_value]
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.language == subtitle_track_language:
                                subtitle_track_id = subtitle.id
                                break
                    elif track_type == "name":
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.track_name == track_value:
                                subtitle_track_id = subtitle.id
                                break
                    if subtitle_track_id != "":
                        change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                        change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.id != subtitle_track_id:
                                change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                        self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                            change_default_subtitle_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_FULL_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if not subtitle_track.isspace():
                change_default_subtitle_commands_list = []
                if subtitle_track == "":
                    for subtitle in self.subtitles_track_json_info:
                        change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                        change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                        change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                        change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                    self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                        change_default_subtitle_commands_list)
                else:
                    track_type, track_value = check_type_of_track_chosen(subtitle_track)
                    change_default_subtitle_commands_list = []
                    subtitle_track_id = ""
                    if track_type == "id":
                        subtitle_track_id = delete_trailing_zero_string(track_value)
                        found_subtitle_with_this_id = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.id == subtitle_track_id:
                                found_subtitle_with_this_id = True
                                break
                        if found_subtitle_with_this_id:
                            change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                            change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                            change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                            change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.id != subtitle_track_id:
                                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                                    change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))

                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "lang":
                        subtitle_track_language = ISO_639_2_LANGUAGES[track_value]
                        found_subtitle_with_this_language = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.language == subtitle_track_language:
                                found_subtitle_with_this_language = True
                                break
                        if found_subtitle_with_this_language:
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.language == subtitle_track_language and subtitle_track_id == "":
                                    subtitle_track_id = subtitle.id
                                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line(subtitle_track_id + ":yes"))
                                    change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line(subtitle_track_id + ":yes"))
                                else:
                                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                                    change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)
                    elif track_type == "name":
                        found_subtitle_with_this_track_name = False
                        for subtitle in self.subtitles_track_json_info:
                            if subtitle.track_name == track_value:
                                found_subtitle_with_this_track_name = True
                                break
                        if found_subtitle_with_this_track_name:
                            for subtitle in self.subtitles_track_json_info:
                                if subtitle.track_name == track_value and subtitle_track_id == "":
                                    subtitle_track_id = subtitle.id
                                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line(subtitle_track_id + ":yes"))
                                    change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                    change_default_subtitle_commands_list.append(
                                        add_json_line(subtitle_track_id + ":yes"))
                                else:
                                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                                    change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                    change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                            self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                                change_default_subtitle_commands_list)

    def make_this_audio_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if not audio_track.isspace():
                change_default_audio_commands_list = []
                if audio_track == "":
                    for audio in self.audios_track_json_info:
                        change_default_audio_commands_list.append(add_json_line("--default-track"))
                        change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                    self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                        change_default_audio_commands_list)
                else:
                    track_type, track_value = check_type_of_track_chosen(audio_track)
                    audio_track_id = ""
                    if track_type == "id":
                        audio_track_id = delete_trailing_zero_string(track_value)
                        found_audio_with_this_id = False
                        for audio in self.audios_track_json_info:
                            if audio.id == audio_track_id:
                                found_audio_with_this_id = True
                                break
                        if not found_audio_with_this_id:
                            audio_track_id = ""
                    elif track_type == "lang":
                        audio_track_language = ISO_639_2_LANGUAGES[track_value]
                        for audio in self.audios_track_json_info:
                            if audio.language == audio_track_language:
                                audio_track_id = audio.id
                                break
                    elif track_type == "name":
                        for audio in self.audios_track_json_info:
                            if audio.track_name == track_value:
                                audio_track_id = audio.id
                                break
                    if audio_track_id != "":
                        change_default_audio_commands_list.append(add_json_line("--default-track"))
                        change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                        for audio in self.audios_track_json_info:
                            if audio.id != audio_track_id:
                                change_default_audio_commands_list.append(add_json_line("--default-track"))
                                change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                        self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                            change_default_audio_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if not audio_track.isspace():
                change_default_audio_commands_list = []
                if audio_track == "":
                    for audio in self.audios_track_json_info:
                        change_default_audio_commands_list.append(add_json_line("--default-track"))
                        change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                        change_default_audio_commands_list.append(add_json_line("--forced-track"))
                        change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                    self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                        change_default_audio_commands_list)
                else:
                    track_type, track_value = check_type_of_track_chosen(audio_track)
                    audio_track_id = ""
                    if track_type == "id":
                        audio_track_id = delete_trailing_zero_string(track_value)
                        found_audio_with_this_id = False
                        for audio in self.audios_track_json_info:
                            if audio.id == audio_track_id:
                                found_audio_with_this_id = True
                                break
                        if found_audio_with_this_id:
                            change_default_audio_commands_list.append(add_json_line("--default-track"))
                            change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                            change_default_audio_commands_list.append(add_json_line("--forced-track"))
                            change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                            for audio in self.audios_track_json_info:
                                if audio.id != audio_track_id:
                                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                                    change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))

                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "lang":
                        audio_track_language = ISO_639_2_LANGUAGES[track_value]
                        found_audio_with_this_language = False
                        for audio in self.audios_track_json_info:
                            if audio.language == audio_track_language:
                                found_audio_with_this_language = True
                                break
                        if found_audio_with_this_language:
                            for audio in self.audios_track_json_info:
                                if audio.language == audio_track_language and audio_track_id == "":
                                    audio_track_id = audio.id
                                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                                    change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                                else:
                                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                                    change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)
                    elif track_type == "name":
                        found_audio_with_this_audio = False
                        for audio in self.audios_track_json_info:
                            if audio.track_name == track_value:
                                found_audio_with_this_audio = True
                                break
                        if found_audio_with_this_audio:
                            for audio in self.audios_track_json_info:
                                if audio.track_name == track_value and audio_track_id == "":
                                    audio_track_id = audio.id
                                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                                    change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                                else:
                                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                                    change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                    change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                            self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                                change_default_audio_commands_list)

    # noinspection PyListCreation
    def setup_ui_language(self):
        ui_language_commands_list = []
        ui_language_commands_list.append(add_double_quotation("--ui-language") + ",")
        if platform == "win32":
            ui_language_commands_list.append(add_json_line("en"))
        else:
            ui_language_commands_list.append(add_json_line("en_US"))
        self.ui_language_command = "".join(ui_language_commands_list)

    # noinspection PyListCreation
    def setup_output_video_command(self):
        if GlobalSetting.OVERWRITE_SOURCE_FILES:
            folder_path = os.path.dirname(self.job.video_name_absolute)
            output_video_name = Path(change_file_extension_to_mkv_with_random_suffix(self.job.video_name))
            output_video_name_absolute = os.path.join(folder_path, output_video_name)
        else:
            folder_path = Path(GlobalSetting.DESTINATION_FOLDER_PATH)
            output_video_name = Path(change_file_extension_to_mkv(self.job.video_name))
            output_video_name_absolute = os.path.join(folder_path, output_video_name)

        output_video_commands_list = []
        output_video_commands_list.append(add_json_line("--output"))
        output_video_commands_list.append(add_json_line(check_for_system_backslash_path(output_video_name_absolute)))
        self.output_video_command = "".join(output_video_commands_list)

    # noinspection PyListCreation
    def setup_input_video_command(self):
        input_video_commands_list = []
        input_video_commands_list.append(add_json_line("("))
        input_video_commands_list.append(add_json_line(check_for_system_backslash_path(self.job.video_name_absolute)))
        input_video_commands_list.append(add_json_line(")"))
        self.input_video_command = "".join(input_video_commands_list)

    def setup_final_command(self):
        self.final_command = "["
        self.final_command += "\n"
        self.final_command += self.ui_language_command
        self.final_command += self.output_video_command

        self.final_command += self.discard_old_attachments_command
        self.final_command += self.specify_video_track_source_video_command
        self.final_command += self.specify_subtitle_track_source_video_command
        self.final_command += self.specify_audio_track_source_video_command
        self.final_command += self.old_video_append_command
        self.final_command += self.old_audio_append_command
        self.final_command += self.old_subtitle_append_command
        self.final_command += self.change_default_forced_subtitle_track_setting_source_video_command
        self.final_command += self.change_default_forced_audio_track_setting_source_video_command

        self.final_command += self.video_default_duration_fps_command
        self.final_command += self.input_video_command
        self.final_command += self.new_audio_append_command
        self.final_command += self.new_subtitle_append_command
        self.final_command += self.attachments_attach_command
        self.final_command += self.chapter_attach_command
        self.final_command += self.track_order_command
        self.final_command = self.final_command[:-1]  # delete last ,
        self.final_command += "\n"
        self.final_command += "]"

    def setup_track_order_command(self):
        track_order_command_list = []
        if self.track_order_line != "":
            track_order_line = self.track_order_line[:-1]  # delete last ,
            track_order_command_list.append(add_json_line("--track-order"))
            track_order_command_list.append(add_json_line(track_order_line))
            self.track_order_command = "".join(track_order_command_list)

    def generate_mkvmerge_json_job_file(self):
        job_file_path = GlobalFiles.mkvmergeJsonJobFilePath
        with open(job_file_path, 'w+', encoding="UTF-8") as job_file:
            job_file.write(self.final_command)
