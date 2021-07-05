import json
import subprocess

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


def increase_id_by_one(string):
    return str(int(string) + 1)


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
        self.final_command = ""
        self.json_info = ""
        self.tracks_json_info = ""
        self.videos_track_json_info = []  # type: list[SingleTrackData]
        self.subtitles_track_json_info = []  # type: list[SingleTrackData]
        self.audios_track_json_info = []  # type: list[SingleTrackData]
        self.setup_commands()
        self.generate_mkvpropedit_json_file()

    def setup_commands(self):
        self.generate_info_file()
        self.setup_attachments_options()
        self.setup_chapter_options()
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
            if track["type"] == "audio":
                self.audios_track_json_info.append(new_track_info)
            elif track["type"] == "subtitles":
                self.subtitles_track_json_info.append(new_track_info)
            elif track["type"] == "video":
                self.videos_track_json_info.append(new_track_info)

    def setup_attachments_options(self):
        if GlobalSetting.ATTACHMENT_ENABLED:
            attachments_list_with_attach_command = []
            discard_old_attachments_list_command = []
            if GlobalSetting.ATTACHMENT_DISCARD_OLD:
                for i in range(self.number_of_old_attachments + 2):
                    attachments_list_with_attach_command.append(add_json_line("--delete-attachment"))
                    attachments_list_with_attach_command.append(add_json_line(str(i)))
            for i in range(len(GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST)):
                if GlobalSetting.ATTACHMENT_FILES_CHECKING_LIST[i]:
                    file_to_attach = GlobalSetting.ATTACHMENT_FILES_ABSOLUTE_PATH_LIST[i]
                    attachments_list_with_attach_command.append(add_json_line("--add-attachment"))
                    attachments_list_with_attach_command.append(
                        add_json_line(fix_windows_backslash_path(file_to_attach)))
            self.attachments_attach_command = "".join(attachments_list_with_attach_command)
            self.discard_old_attachments_command = "".join(discard_old_attachments_list_command)

    def setup_chapter_options(self):
        if GlobalSetting.CHAPTER_ENABLED:
            if self.job.chapter_found:
                self.chapter_attach_command = add_json_line("--chapters") + \
                                              add_json_line(fix_windows_backslash_path(self.job.chapter_name_absolute))

    def make_other_subtitle_not_forced(self):
        change_forced_subtitle_commands_list = []
        for track in self.subtitles_track_json_info:
            change_forced_subtitle_commands_list.append(add_json_line("--forced-track"))
            change_forced_subtitle_commands_list.append(add_json_line(track.id + ":no"))
        self.change_default_forced_subtitle_track_setting_source_video_command += "".join(
            change_forced_subtitle_commands_list)

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
                else:
                    subtitle_track_language = ISO_639_2_LANGUAGES[subtitle_track]
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
                else:
                    subtitle_track_language = ISO_639_2_LANGUAGES[subtitle_track]
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
                else:
                    audio_track_language = ISO_639_2_LANGUAGES[audio_track]
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
                else:
                    audio_track_language = ISO_639_2_LANGUAGES[audio_track]
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

    # noinspection PyListCreation
    def setup_ui_language(self):
        ui_language_commands_list = []
        ui_language_commands_list.append(add_double_quotation("--ui-language") + ",")
        ui_language_commands_list.append(add_json_line("en"))
        self.ui_language_command = "".join(ui_language_commands_list)

    # noinspection PyListCreation
    def setup_input_video_command(self):
        input_video_commands_list = []
        input_video_commands_list.append(add_json_line(fix_windows_backslash_path(self.job.video_name_absolute)))
        self.input_video_command = "".join(input_video_commands_list)

    def setup_final_command(self):
        self.final_command = "["
        self.final_command += "\n"
        self.final_command += self.ui_language_command
        self.final_command += self.input_video_command
        self.final_command += self.change_default_forced_subtitle_track_setting_source_video_command
        self.final_command += self.change_default_forced_audio_track_setting_source_video_command
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
