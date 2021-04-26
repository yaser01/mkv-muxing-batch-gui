import json
import os
import subprocess
from pathlib import Path

from packages.Startup import GlobalFiles
from packages.Startup.PreDefined import ISO_639_2_LANGUAGES
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.MuxSetting.Widgets.SingleJobData import SingleJobData
from packages.Tabs.MuxSetting.Widgets.SingleTrackData import SingleTrackData


def add_two_spaces():
    return "  "


def add_double_quotation(string):
    return add_two_spaces() + "\"" + str(string) + "\""


def add_json_line(string):
    return "\n" + add_double_quotation(string) + ","


def delete_trailing_zero_string(string):
    return str(int(str(string)))


def fix_windows_backslash_path(string):
    return string.replace('\\', '\\\\')


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


def change_file_extension_to_mkv(file_name):
    file_extension_start_index = file_name.rfind(".")
    new_file_name_with_mkv_extension = file_name[:file_extension_start_index] + ".mkv"
    return new_file_name_with_mkv_extension


class GetJsonForMkvmergeJob:
    def __init__(self, job: SingleJobData):
        self.job = job
        self.file_info_json = ""
        self.ui_language_command = ""
        self.output_video_command = ""
        self.input_video_command = ""
        self.attachments_attach_command = ""
        self.chapter_attach_command = ""
        self.subtitle_append_command = ""
        self.discard_old_attachments_command = ""
        self.change_default_forced_subtitle_track_setting_source_video_command = ""
        self.change_default_forced_audio_track_setting_source_video_command = ""
        self.specify_subtitle_track_source_video_command = ""
        self.specify_audio_track_source_video_command = ""
        self.final_command = ""
        self.json_info = ""
        self.tracks_json_info = ""
        self.videos_track_json_info = []  # type: list[SingleTrackData]
        self.subtitles_track_json_info = []  # type: list[SingleTrackData]
        self.audios_track_json_info = []  # type: list[SingleTrackData]
        self.setup_commands()
        self.generate_mkvmerge_json_job_file()

    def setup_commands(self):
        self.generate_info_file()
        self.setup_attachments_options()
        self.setup_chapter_options()
        self.setup_subtitle_options()
        self.setup_only_keep_those_subtitles()
        self.setup_only_keep_those_audios()
        self.make_this_subtitle_default_forced()
        self.make_this_audio_default_forced()
        self.setup_ui_language()
        self.setup_output_video_command()
        self.setup_input_video_command()
        self.setup_final_command()

    def generate_info_file(self):
        info_file_path = GlobalFiles.mkvmergeJsonInfoFilePath
        with open(info_file_path, 'w+') as info_file:
            command = add_double_quotation(GlobalFiles.MKVMERGE_PATH) + " -J " + add_double_quotation(
                self.job.video_name_absolute)
            subprocess.run(command, shell=True, stdout=info_file)
        with open(info_file_path, 'r') as info_file:
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
            if track["type"] == "audio":
                self.audios_track_json_info.append(new_track_info)
            elif track["type"] == "subtitles":
                self.subtitles_track_json_info.append(new_track_info)
            elif track["type"] == "video":
                self.videos_track_json_info.append(new_track_info)

    def setup_attachments_options(self):
        if GlobalSetting.ATTACHMENT_ENABLED:
            attachments_list_with_attach_command = []
            if GlobalSetting.ATTACHMENT_DISCARD_OLD:
                self.discard_old_attachments_command = add_json_line("--no-attachments")
            for i in range(len(GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST)):
                if GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST[i]:
                    file_to_attach = GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST[i]
                    attachments_list_with_attach_command.append(add_json_line("--attach-file"))
                    attachments_list_with_attach_command.append(
                        add_json_line(fix_windows_backslash_path(file_to_attach)))
            self.attachments_attach_command = "".join(attachments_list_with_attach_command)

    def setup_chapter_options(self):
        if GlobalSetting.CHAPTER_ENABLED:
            if self.job.chapter_found:
                self.chapter_attach_command = add_json_line("--chapters") + \
                                              add_json_line(fix_windows_backslash_path(self.job.chapter_name_absolute))

    def setup_subtitle_options(self):

        if GlobalSetting.SUBTITLE_ENABLED:
            subtitle_command_list = []
            if self.job.subtitle_found:
                # add subtitle language
                subtitle_command_list.append(add_json_line("--language"))
                subtitle_command_list.append(add_json_line("0:" + ISO_639_2_LANGUAGES[self.job.subtitle_language]))
                # add subtitle track name
                if self.job.subtitle_track_name != "":
                    subtitle_command_list.append(add_json_line("--track-name"))
                    subtitle_command_list.append(add_json_line("0:" + self.job.subtitle_track_name))
                # add subtitle set default
                if self.job.subtitle_set_default:
                    subtitle_command_list.append(add_json_line("--default-track"))
                    subtitle_command_list.append(add_json_line("0:yes"))
                # add subtitle set forced
                if self.job.subtitle_set_forced:
                    subtitle_command_list.append(add_json_line("--forced-track"))
                    subtitle_command_list.append(add_json_line("0:yes"))
                    self.make_other_subtitle_not_forced()
                # add subtitle delay
                subtitle_delay_in_millisecond = int(1000 * float(self.job.subtitle_delay))
                subtitle_command_list.append(add_json_line("--sync"))
                subtitle_command_list.append(add_json_line("0:" + str(subtitle_delay_in_millisecond)))
                # add subtitle file
                subtitle_command_list.append(add_json_line("("))
                subtitle_command_list.append(add_json_line(fix_windows_backslash_path(self.job.subtitle_name_absolute)))
                subtitle_command_list.append(add_json_line(")"))
                self.subtitle_append_command = "".join(subtitle_command_list)

    def make_other_subtitle_not_forced(self):
        change_forced_subtitle_commands_list = []
        for track in self.subtitles_track_json_info:
            change_forced_subtitle_commands_list.append(add_json_line("--forced-track"))
            change_forced_subtitle_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_subtitle_track_setting_source_video_command += "".join(
            change_forced_subtitle_commands_list)

    def setup_only_keep_those_subtitles(self):
        if GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_ENABLED:
            if len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS) == 0:
                self.specify_subtitle_track_source_video_command = add_json_line("--no-subtitles")
            else:
                only_keep_those_subtitle_list = GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_TRACKS
                for language in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_SUBTITLES_LANGUAGES:
                    only_keep_those_subtitle_list.append(ISO_639_2_LANGUAGES[language])
                self.specify_subtitle_track_source_video_command = add_json_line("--subtitle-tracks")
                self.specify_subtitle_track_source_video_command += add_json_line(
                    ",".join(only_keep_those_subtitle_list))

    def setup_only_keep_those_audios(self):
        if GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_ENABLED:
            if len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_LANGUAGES) == 0 and \
                    len(GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS) == 0:
                self.specify_audio_track_source_video_command = add_json_line("--no-audio")
            else:
                only_keep_those_audios_list = GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_TRACKS
                for audio in GlobalSetting.MUX_SETTING_ONLY_KEEP_THOSE_AUDIOS_LANGUAGES:
                    only_keep_those_audios_list.append(ISO_639_2_LANGUAGES[audio])
                self.specify_audio_track_source_video_command = add_json_line("--audio-tracks")
                self.specify_audio_track_source_video_command += add_json_line(
                    ",".join(only_keep_those_audios_list))

    def make_this_subtitle_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_SEMI_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if (not subtitle_track.isspace()) and subtitle_track != "":
                change_default_subtitle_commands_list = []
                subtitle_track_id = ""
                if subtitle_track.find("Track") != -1:
                    subtitle_track = subtitle_track.split(" ")[1]
                    subtitle_track_id = delete_trailing_zero_string(subtitle_track)
                    found_subtitle_with_this_id = False
                    for subtitle in self.subtitles_track_json_info:
                        if subtitle.id == subtitle_track_id:
                            found_subtitle_with_this_id = True
                            break
                    if not found_subtitle_with_this_id:
                        subtitle_track_id = ""
                else:
                    subtitle_track_language = ISO_639_2_LANGUAGES[subtitle_track]
                    for subtitle in self.subtitles_track_json_info:
                        if subtitle.language == subtitle_track_language:
                            subtitle_track_id = subtitle.id
                            break
                if subtitle_track_id != "":
                    change_default_subtitle_commands_list.append(add_json_line("--default-track"))
                    change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                    self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                        change_default_subtitle_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_FULL_ENABLED:
            subtitle_track = GlobalSetting.MUX_SETTING_MAKE_THIS_SUBTITLE_DEFAULT_TRACK
            if (not subtitle_track.isspace()) and subtitle_track != "":
                change_default_subtitle_commands_list = []
                subtitle_track_id = ""
                if subtitle_track.find("Track") != -1:
                    subtitle_track = subtitle_track.split(" ")[1]
                    subtitle_track_id = delete_trailing_zero_string(subtitle_track)
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
                                change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))

                        self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                            change_default_subtitle_commands_list)
                else:
                    subtitle_track_language = ISO_639_2_LANGUAGES[subtitle_track]
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
                                change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                                change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                change_default_subtitle_commands_list.append(add_json_line(subtitle_track_id + ":yes"))
                            else:
                                change_default_subtitle_commands_list.append(add_json_line("--forced-track"))
                                change_default_subtitle_commands_list.append(add_json_line(subtitle.id + ":no"))
                        self.change_default_forced_subtitle_track_setting_source_video_command += ''.join(
                            change_default_subtitle_commands_list)

    def make_this_audio_default_forced(self):
        if GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_SEMI_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if (not audio_track.isspace()) and audio_track != "":
                change_default_audio_commands_list = []
                audio_track_id = ""
                if audio_track.find("Track") != -1:
                    audio_track = audio_track.split(" ")[1]
                    audio_track_id = delete_trailing_zero_string(audio_track)
                    found_audio_with_this_id = False
                    for audio in self.audios_track_json_info:
                        if audio.id == audio_track_id:
                            found_audio_with_this_id = True
                            break
                    if not found_audio_with_this_id:
                        audio_track_id = ""
                else:
                    audio_track_language = ISO_639_2_LANGUAGES[audio_track]
                    for audio in self.audios_track_json_info:
                        if audio.language == audio_track_language:
                            audio_track_id = audio.id
                            break
                if audio_track_id != "":
                    change_default_audio_commands_list.append(add_json_line("--default-track"))
                    change_default_audio_commands_list.append(add_json_line(audio_track_id + ":yes"))
                    self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                        change_default_audio_commands_list)

        elif GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_FULL_ENABLED:
            audio_track = GlobalSetting.MUX_SETTING_MAKE_THIS_AUDIO_DEFAULT_TRACK
            if (not audio_track.isspace()) and audio_track != "":
                change_default_audio_commands_list = []
                audio_track_id = ""
                if audio_track.find("Track") != -1:
                    audio_track = audio_track.split(" ")[1]
                    audio_track_id = delete_trailing_zero_string(audio_track)
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
                                change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))

                        self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                            change_default_audio_commands_list)
                else:
                    audio_track_language = ISO_639_2_LANGUAGES[audio_track]
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
                                change_default_audio_commands_list.append(add_json_line("--forced-track"))
                                change_default_audio_commands_list.append(add_json_line(audio.id + ":no"))
                        self.change_default_forced_audio_track_setting_source_video_command += ''.join(
                            change_default_audio_commands_list)

    # noinspection PyListCreation
    def setup_ui_language(self):
        ui_language_commands_list = []
        ui_language_commands_list.append(add_double_quotation("--ui-language") + ",")
        ui_language_commands_list.append(add_json_line("en"))
        self.ui_language_command = "".join(ui_language_commands_list)

    # noinspection PyListCreation
    def setup_output_video_command(self):
        folder_path = Path(GlobalSetting.DESTINATION_FOLDER_PATH)
        output_video_name = Path(change_file_extension_to_mkv(self.job.video_name))
        output_video_name_absolute = os.path.join(folder_path, output_video_name)

        output_video_commands_list = []
        output_video_commands_list.append(add_json_line("--output"))
        output_video_commands_list.append(add_json_line(fix_windows_backslash_path(output_video_name_absolute)))
        self.output_video_command = "".join(output_video_commands_list)

    # noinspection PyListCreation
    def setup_input_video_command(self):
        input_video_commands_list = []
        input_video_commands_list.append(add_json_line("("))
        input_video_commands_list.append(add_json_line(fix_windows_backslash_path(self.job.video_name_absolute)))
        input_video_commands_list.append(add_json_line(")"))
        self.input_video_command = "".join(input_video_commands_list)

    def setup_final_command(self):
        self.final_command = "["
        self.final_command += "\n"
        self.final_command += self.ui_language_command
        self.final_command += self.output_video_command

        self.final_command += self.discard_old_attachments_command
        self.final_command += self.specify_subtitle_track_source_video_command
        self.final_command += self.specify_audio_track_source_video_command

        self.final_command += self.change_default_forced_subtitle_track_setting_source_video_command
        self.final_command += self.change_default_forced_audio_track_setting_source_video_command

        self.final_command += self.input_video_command
        self.final_command += self.subtitle_append_command
        self.final_command += self.attachments_attach_command
        self.final_command += self.chapter_attach_command
        self.final_command = self.final_command[:-1]  # delete last ,
        self.final_command += "\n"
        self.final_command += "]"

    def generate_mkvmerge_json_job_file(self):
        job_file_path = GlobalFiles.mkvmergeJsonJobFilePath
        with open(job_file_path, 'w+', encoding="utf-8") as job_file:
            job_file.write(self.final_command)
