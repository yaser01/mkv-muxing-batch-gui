import json
from pathlib import Path

from PySide2.QtWidgets import QWidget

from packages.Startup.GlobalFiles import SettingJsonInfoFilePath


def get_data_from_json(json_data, attribute, default_value):
    try:
        return json_data[attribute]
    except Exception as e:
        return default_value


class Options(QWidget):
    Default_Video_Extensions = ["MKV"]
    Default_Subtitle_Extensions = ["ASS"]
    Default_Subtitle_Language = "English"
    Default_Chapter_Extensions = ["XML"]
    Default_Audio_Extensions = ["AAC"]
    Default_Audio_Language = "English"
    Default_Video_Directory = ""
    Default_Subtitle_Directory = ""
    Default_Chapter_Directory = ""
    Default_Audio_Directory = ""
    Default_Attachment_Directory = ""
    Default_Destination_Directory = ""
    Default_Favorite_Subtitle_Languages = ['English', 'Arabic']
    Default_Favorite_Audio_Languages = ['English', 'Arabic']
    Dark_Mode = False
    Attachment_Expert_Mode_Info_Message_Show = True


def save_options():
    options_data = {"Default_Video_Directory": Options.Default_Video_Directory,
                    "Default_Video_Extensions": Options.Default_Video_Extensions,
                    "Default_Subtitle_Directory": Options.Default_Subtitle_Directory,
                    "Default_Subtitle_Extensions": Options.Default_Subtitle_Extensions,
                    "Default_Subtitle_Language": Options.Default_Subtitle_Language,
                    "Default_Audio_Directory": Options.Default_Audio_Directory,
                    "Default_Audio_Extensions": Options.Default_Audio_Extensions,
                    "Default_Audio_Language": Options.Default_Audio_Language,
                    "Default_Chapter_Directory": Options.Default_Chapter_Directory,
                    "Default_Chapter_Extensions": Options.Default_Chapter_Extensions,
                    "Default_Attachment_Directory": Options.Default_Attachment_Directory,
                    "Default_Destination_Directory": Options.Default_Destination_Directory,
                    "Default_Favorite_Subtitle_Languages": Options.Default_Favorite_Subtitle_Languages,
                    "Default_Favorite_Audio_Languages": Options.Default_Favorite_Audio_Languages,
                    "Dark_Mode": Options.Dark_Mode,
                    "Attachment_Expert_Mode_Info_Message_Show": Options.Attachment_Expert_Mode_Info_Message_Show
                    }
    options_file_path = Path(SettingJsonInfoFilePath)
    with open(options_file_path, "w+", encoding="UTF-8") as option_file:
        json.dump(options_data, option_file)


def read_option_file(option_file, all_languages_file_path):
    with open(all_languages_file_path, "r", encoding="UTF-8") as language_file:
        all_languages = json.load(language_file)
    all_languages = list(all_languages.keys())
    option_file_path = Path(option_file)
    if option_file_path.is_file():
        with open(option_file_path, "r+", encoding="UTF-8") as option_file:
            data = json.load(option_file)
            Options.Default_Video_Directory = get_data_from_json(json_data=data, attribute="Default_Video_Directory",
                                                                 default_value="")
            Options.Default_Video_Extensions = get_data_from_json(json_data=data,
                                                                  attribute="Default_Video_Extensions",
                                                                  default_value=["MKV"])
            Options.Default_Subtitle_Directory = get_data_from_json(json_data=data,
                                                                    attribute="Default_Subtitle_Directory",
                                                                    default_value="")
            Options.Default_Subtitle_Extensions = get_data_from_json(json_data=data,
                                                                     attribute="Default_Subtitle_Extensions",
                                                                     default_value=["ASS"])
            Options.Default_Subtitle_Language = get_data_from_json(json_data=data,
                                                                   attribute="Default_Subtitle_Language",
                                                                   default_value="English")
            Options.Default_Audio_Directory = get_data_from_json(json_data=data, attribute="Default_Audio_Directory",
                                                                 default_value="")
            Options.Default_Audio_Extensions = get_data_from_json(json_data=data,
                                                                  attribute="Default_Audio_Extensions",
                                                                  default_value=["AAC"])
            Options.Default_Audio_Language = get_data_from_json(json_data=data, attribute="Default_Audio_Language",
                                                                default_value="English")
            Options.Default_Chapter_Directory = get_data_from_json(json_data=data,
                                                                   attribute="Default_Chapter_Directory",
                                                                   default_value="")
            Options.Default_Chapter_Extensions = get_data_from_json(json_data=data,
                                                                    attribute="Default_Chapter_Extensions",
                                                                    default_value=["XML"])
            Options.Default_Attachment_Directory = get_data_from_json(json_data=data,
                                                                      attribute="Default_Attachment_Directory",
                                                                      default_value="")
            Options.Default_Destination_Directory = get_data_from_json(json_data=data,
                                                                       attribute="Default_Destination_Directory",
                                                                       default_value="")
            Options.Default_Favorite_Subtitle_Languages = get_data_from_json(json_data=data,
                                                                             attribute="Default_Favorite_Subtitle_Languages",
                                                                             default_value=['English', 'Arabic'])
            Options.Default_Favorite_Audio_Languages = get_data_from_json(json_data=data,
                                                                          attribute="Default_Favorite_Audio_Languages",
                                                                          default_value=['English', 'Arabic'])
            Options.Dark_Mode = get_data_from_json(json_data=data, attribute="Dark_Mode", default_value=False)
            Options.Attachment_Expert_Mode_Info_Message_Show = get_data_from_json(json_data=data,
                                                                                  attribute="Attachment_Expert_Mode_Info_Message_Show",
                                                                                  default_value=True)
    save_options()
