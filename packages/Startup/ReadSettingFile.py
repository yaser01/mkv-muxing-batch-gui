import json
from pathlib import Path

from packages.Startup.DefaultOptions import DefaultOptions


def get_data_from_json(json, attribute):
    try:
        return json[attribute]
    except Exception as e:
        return ""


def read_setting_file(setting_json_info_file_path, all_languages_file_path):
    with open(all_languages_file_path, "r", encoding="UTF-8") as language_file:
        all_languages = json.load(language_file)
    all_languages = list(all_languages.keys())
    setting_file_path = Path(setting_json_info_file_path)
    if setting_file_path.is_file():
        with open(setting_file_path, "r+", encoding="UTF-8") as setting_file:
            data = json.load(setting_file)
            DefaultOptions.Default_Video_Directory = get_data_from_json(json=data, attribute="Default_Video_Directory")
            DefaultOptions.Default_Video_Extensions = get_data_from_json(json=data,
                                                                         attribute="Default_Video_Extensions")
            DefaultOptions.Default_Subtitle_Directory = get_data_from_json(json=data,
                                                                           attribute="Default_Subtitle_Directory")
            DefaultOptions.Default_Subtitle_Extensions = get_data_from_json(json=data,
                                                                            attribute="Default_Subtitle_Extensions")
            DefaultOptions.Default_Subtitle_Language = get_data_from_json(json=data,
                                                                          attribute="Default_Subtitle_Language")
            DefaultOptions.Default_Audio_Directory = get_data_from_json(json=data, attribute="Default_Audio_Directory")
            DefaultOptions.Default_Audio_Extensions = get_data_from_json(json=data,
                                                                         attribute="Default_Audio_Extensions")
            DefaultOptions.Default_Audio_Language = get_data_from_json(json=data, attribute="Default_Audio_Language")
            DefaultOptions.Default_Chapter_Directory = get_data_from_json(json=data,
                                                                          attribute="Default_Chapter_Directory")
            DefaultOptions.Default_Chapter_Extensions = get_data_from_json(json=data,
                                                                           attribute="Default_Chapter_Extensions")
            DefaultOptions.Default_Attachment_Directory = get_data_from_json(json=data,
                                                                             attribute="Default_Attachment_Directory")
            DefaultOptions.Default_Destination_Directory = get_data_from_json(json=data,
                                                                              attribute="Default_Destination_Directory")
            DefaultOptions.Default_Favorite_Subtitle_Languages = get_data_from_json(json=data,
                                                                                    attribute="Default_Favorite_Subtitle_Languages")
            DefaultOptions.Default_Favorite_Audio_Languages = get_data_from_json(json=data,
                                                                                 attribute="Default_Favorite_Audio_Languages")
            if not DefaultOptions.Default_Favorite_Audio_Languages:
                DefaultOptions.Default_Favorite_Audio_Languages = all_languages
            if not DefaultOptions.Default_Favorite_Subtitle_Languages:
                DefaultOptions.Default_Favorite_Subtitle_Languages = all_languages

    else:
        setting_data = {"Default_Video_Directory": DefaultOptions.Default_Video_Directory,
                        "Default_Video_Extensions": DefaultOptions.Default_Video_Extensions,
                        "Default_Subtitle_Directory": DefaultOptions.Default_Subtitle_Directory,
                        "Default_Subtitle_Extensions": DefaultOptions.Default_Subtitle_Extensions,
                        "Default_Subtitle_Language": DefaultOptions.Default_Subtitle_Language,
                        "Default_Audio_Directory": DefaultOptions.Default_Audio_Directory,
                        "Default_Audio_Extensions": DefaultOptions.Default_Audio_Extensions,
                        "Default_Audio_Language": DefaultOptions.Default_Audio_Language,
                        "Default_Chapter_Directory": DefaultOptions.Default_Chapter_Directory,
                        "Default_Chapter_Extensions": DefaultOptions.Default_Chapter_Extensions,
                        "Default_Attachment_Directory": DefaultOptions.Default_Attachment_Directory,
                        "Default_Destination_Directory": DefaultOptions.Default_Destination_Directory,
                        "Default_Favorite_Subtitle_Languages": DefaultOptions.Default_Favorite_Subtitle_Languages,
                        "Default_Favorite_Audio_Languages": DefaultOptions.Default_Favorite_Audio_Languages
                        }
        with open(setting_file_path, "w+", encoding="UTF-8") as setting_file:
            json.dump(setting_data, setting_file)
