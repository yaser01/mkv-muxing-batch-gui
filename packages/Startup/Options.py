import json
from pathlib import Path
from PySide2.QtWidgets import QWidget
from packages.Startup.GlobalFiles import SettingJsonInfoFilePath
from packages.Widgets.SingleDefaultPresetsData import SingleDefaultPresetsData


def get_data_from_json(json_data, attribute, default_value):
    try:
        return json_data[attribute]
    except Exception as e:
        return default_value


def get_names_list_of_presets():
    names_list = []
    for preset in Options.DefaultPresets:
        names_list.append(preset.Preset_Name)
    return names_list


class Options(QWidget):
    DefaultPresets = [SingleDefaultPresetsData()]
    CurrentPreset = SingleDefaultPresetsData()
    FavoritePresetId = 0
    Dark_Mode = False
    Attachment_Expert_Mode_Info_Message_Show = True
    Choose_Preset_On_Startup = False


def save_options():
    default_presets_data = []
    for preset_id in range(len(Options.DefaultPresets)):
        temp_default_preset = {
            "Preset_Name": Options.DefaultPresets[preset_id].Preset_Name,
            "Default_Video_Directory": Options.DefaultPresets[preset_id].Default_Video_Directory,
            "Default_Video_Extensions": Options.DefaultPresets[preset_id].Default_Video_Extensions,
            "Default_Subtitle_Directory": Options.DefaultPresets[preset_id].Default_Subtitle_Directory,
            "Default_Subtitle_Extensions": Options.DefaultPresets[
                preset_id].Default_Subtitle_Extensions,
            "Default_Subtitle_Language": Options.DefaultPresets[preset_id].Default_Subtitle_Language,
            "Default_Audio_Directory": Options.DefaultPresets[preset_id].Default_Audio_Directory,
            "Default_Audio_Extensions": Options.DefaultPresets[preset_id].Default_Audio_Extensions,
            "Default_Audio_Language": Options.DefaultPresets[preset_id].Default_Audio_Language,
            "Default_Chapter_Directory": Options.DefaultPresets[preset_id].Default_Chapter_Directory,
            "Default_Chapter_Extensions": Options.DefaultPresets[preset_id].Default_Chapter_Extensions,
            "Default_Attachment_Directory": Options.DefaultPresets[
                preset_id].Default_Attachment_Directory,
            "Default_Destination_Directory": Options.DefaultPresets[
                preset_id].Default_Destination_Directory,
            "Default_Favorite_Subtitle_Languages": Options.DefaultPresets[
                preset_id].Default_Favorite_Subtitle_Languages,
            "Default_Favorite_Audio_Languages": Options.DefaultPresets[
                preset_id].Default_Favorite_Audio_Languages,
        }
        default_presets_data.append(temp_default_preset)
    options_data = {
        "Presets": default_presets_data,
        "FavoritePresetId": Options.FavoritePresetId,
        "Dark_Mode": Options.Dark_Mode,
        "Attachment_Expert_Mode_Info_Message_Show": Options.Attachment_Expert_Mode_Info_Message_Show,
        "Choose_Preset_On_Startup": Options.Choose_Preset_On_Startup
    }
    options_file_path = Path(SettingJsonInfoFilePath)
    with open(options_file_path, "w+", encoding="UTF-8") as option_file:
        json.dump(options_data, option_file, indent=4)


def read_option_file(option_file):
    option_file_path = Path(option_file)
    if option_file_path.is_file():
        with open(option_file_path, "r+", encoding="UTF-8") as option_file:
            data = json.load(option_file)
            presets = get_data_from_json(json_data=data, attribute="Presets", default_value="Old")
            if presets == "Old":
                preset_number = 1
            else:
                preset_number = len(presets)
            Options.DefaultPresets.clear()
            for preset_id in range(preset_number):
                temp_default_preset = SingleDefaultPresetsData()
                temp_default_preset.Preset_Name = get_data_from_json(json_data=presets[preset_id],
                                                                     attribute="Preset_Name",
                                                                     default_value=f"Preset #{preset_id + 1}")
                temp_default_preset.Default_Video_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                 attribute="Default_Video_Directory",
                                                                                 default_value="")
                temp_default_preset.Default_Video_Extensions = get_data_from_json(json_data=presets[preset_id],
                                                                                  attribute="Default_Video_Extensions",
                                                                                  default_value=["MKV"])
                temp_default_preset.Default_Subtitle_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                    attribute="Default_Subtitle_Directory",
                                                                                    default_value="")
                temp_default_preset.Default_Subtitle_Extensions = get_data_from_json(json_data=presets[preset_id],
                                                                                     attribute="Default_Subtitle_Extensions",
                                                                                     default_value=["ASS"])
                temp_default_preset.Default_Subtitle_Language = get_data_from_json(json_data=presets[preset_id],
                                                                                   attribute="Default_Subtitle_Language",
                                                                                   default_value="English")
                temp_default_preset.Default_Audio_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                 attribute="Default_Audio_Directory",
                                                                                 default_value="")
                temp_default_preset.Default_Audio_Extensions = get_data_from_json(json_data=presets[preset_id],
                                                                                  attribute="Default_Audio_Extensions",
                                                                                  default_value=["AAC"])
                temp_default_preset.Default_Audio_Language = get_data_from_json(json_data=presets[preset_id],
                                                                                attribute="Default_Audio_Language",
                                                                                default_value="English")
                temp_default_preset.Default_Chapter_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                   attribute="Default_Chapter_Directory",
                                                                                   default_value="")
                temp_default_preset.Default_Chapter_Extensions = get_data_from_json(json_data=presets[preset_id],
                                                                                    attribute="Default_Chapter_Extensions",
                                                                                    default_value=["XML"])
                temp_default_preset.Default_Attachment_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                      attribute="Default_Attachment_Directory",
                                                                                      default_value="")
                temp_default_preset.Default_Destination_Directory = get_data_from_json(json_data=presets[preset_id],
                                                                                       attribute="Default_Destination_Directory",
                                                                                       default_value="")
                temp_default_preset.Default_Favorite_Subtitle_Languages = get_data_from_json(
                    json_data=presets[preset_id],
                    attribute="Default_Favorite_Subtitle_Languages",
                    default_value=['English',
                                   'Arabic'])
                temp_default_preset.Default_Favorite_Audio_Languages = get_data_from_json(json_data=presets[preset_id],
                                                                                          attribute="Default_Favorite_Audio_Languages",
                                                                                          default_value=['English',
                                                                                                         'Arabic'])
                Options.DefaultPresets.append(temp_default_preset)
            Options.FavoritePresetId = get_data_from_json(json_data=data, attribute="FavoritePresetId", default_value=0)
            Options.Dark_Mode = get_data_from_json(json_data=data, attribute="Dark_Mode", default_value=False)
            Options.Attachment_Expert_Mode_Info_Message_Show = get_data_from_json(json_data=data,
                                                                                  attribute="Attachment_Expert_Mode_Info_Message_Show",
                                                                                  default_value=True)
            Options.Choose_Preset_On_Startup = get_data_from_json(json_data=data,
                                                                  attribute="Choose_Preset_On_Startup",
                                                                  default_value=False)
    save_options()
