import os
import sys
import json
from pathlib import Path
from PySide2.QtGui import QPixmap, QIcon
import tempfile

from packages.Startup.DefaultOptions import DefaultOptions
from packages.Widgets.MissingFilesMessage import MissingFilesMessage
# noinspection PyUnresolvedReferences
import packages.Startup.MainApplication


def create_temp_folder_path():
    temp_folder_path = tempfile.gettempdir()
    my_temp_folder_path = os.path.join(os.path.abspath(temp_folder_path), Path('MKV Muxing Batch GUI'))
    os.makedirs(my_temp_folder_path, exist_ok=True)
    return my_temp_folder_path


def read_setting_file():
    setting_file_path = Path(SettingJsonInfoFilePath)
    if setting_file_path.is_file():
        with open(setting_file_path, "r+", encoding="UTF-8") as setting_file:
            data = json.load(setting_file)
            DefaultOptions.Default_Video_Directory = data["Default_Video_Directory"]
            DefaultOptions.Default_Video_Extensions = data["Default_Video_Extensions"]
            DefaultOptions.Default_Subtitle_Directory = data["Default_Subtitle_Directory"]
            DefaultOptions.Default_Subtitle_Extensions = data["Default_Subtitle_Extensions"]
            DefaultOptions.Default_Subtitle_Language = data["Default_Subtitle_Language"]
            DefaultOptions.Default_Audio_Directory = data["Default_Audio_Directory"]
            DefaultOptions.Default_Audio_Extensions = data["Default_Audio_Extensions"]
            DefaultOptions.Default_Audio_Language = data["Default_Audio_Language"]
            DefaultOptions.Default_Chapter_Directory = data["Default_Chapter_Directory"]
            DefaultOptions.Default_Chapter_Extensions = data["Default_Chapter_Extensions"]
            DefaultOptions.Default_Attachment_Directory = data["Default_Attachment_Directory"]
            DefaultOptions.Default_Destination_Directory = data["Default_Destination_Directory"]

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
                        "Default_Destination_Directory": DefaultOptions.Default_Destination_Directory
                        }
        with open(setting_file_path, "w+", encoding="UTF-8") as setting_file:
            json.dump(setting_data, setting_file)


script_path = sys.argv[0]  # get path of the this file
script_folder = os.path.dirname(script_path)
resources_folder = os.path.join(os.path.abspath(script_folder), Path('Resources'))
FontFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Fonts'))
IconFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Icons'))
ToolsFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Tools'))
LanguagesFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Languages'))
TempFolderPath = create_temp_folder_path()
MergeLogsFolderPath = os.path.join(os.path.abspath(TempFolderPath), Path('Logs'))
MediaInfoFolderPath = os.path.join(os.path.abspath(TempFolderPath), Path('MediaInfo'))
os.makedirs(MergeLogsFolderPath, exist_ok=True)
os.makedirs(MediaInfoFolderPath, exist_ok=True)
try:
    MyFontPath = os.path.join(os.path.abspath(FontFolderPath), 'OpenSans.ttf')
    WarningCheckBigIconPath = os.path.join(os.path.abspath(IconFolderPath), 'WarningCheckBig.png')
    WarningCheckIconPath = os.path.join(os.path.abspath(IconFolderPath), 'WarningCheck.png')
    TrueCheckIconPath = os.path.join(os.path.abspath(IconFolderPath), 'TrueCheck.png')
    ChapterIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Chapter.svg')
    SubtitleIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Subtitle.svg')
    AudioIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Audio.svg')
    StartMultiplexingIconPath = os.path.join(os.path.abspath(IconFolderPath), 'StartMultiplexing.svg')
    PauseMultiplexingIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Pause.png')
    AddToQueueIconPath = os.path.join(os.path.abspath(IconFolderPath), 'AddToQueue.svg')
    InfoSettingIconPath = os.path.join(os.path.abspath(IconFolderPath), 'InfoSetting.svg')
    InfoIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Info.svg')
    AboutIconPath = os.path.join(os.path.abspath(IconFolderPath), 'About.svg')
    NoMarkIconPath = os.path.join(os.path.abspath(IconFolderPath), 'NoMark.svg')
    RedDashIconPath = os.path.join(os.path.abspath(IconFolderPath), 'RedDash.svg')
    PlusIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Plus.svg')
    TrashIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Trash.svg')
    SwitchIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Switch.svg')
    QuestionIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Question.svg')
    InfoBigIconPath = os.path.join(os.path.abspath(IconFolderPath), 'InfoBig.png')
    OkIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Ok.png')
    ErrorIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Error.png')
    ErrorBigIconPath = os.path.join(os.path.abspath(IconFolderPath), 'ErrorBig.png')
    ClearIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Clear.svg')
    RefreshIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Refresh.svg')
    TopIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Top.svg')
    DownIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Down.svg')
    UpIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Up.svg')
    BottomIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Bottom.svg')
    FolderIconPath = os.path.join(os.path.abspath(IconFolderPath), 'SelectFolder.svg')
    SpinnerIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Spinner.gif')
    GoodJobIconPath = os.path.join(os.path.abspath(IconFolderPath), 'GoodJob.png')
    SettingIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Setting.svg')
    TelegramIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Telegram.svg')
    TwitterIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Twitter.svg')
    AppIconPath = os.path.join(os.path.abspath(IconFolderPath), 'App.ico')
    OkIcon = QIcon(QPixmap(OkIconPath))
    ErrorIcon = QIcon(QPixmap(ErrorIconPath))
    ErrorBigIcon = QIcon(QPixmap(ErrorBigIconPath))
    SubtitleIcon = QIcon(QPixmap(SubtitleIconPath))
    SwitchIcon = QIcon(QPixmap(SwitchIconPath))
    RefreshIcon = QIcon(QPixmap(RefreshIconPath))
    QuestionIcon = QIcon(QPixmap(QuestionIconPath))
    NoMarkIcon = QIcon(QPixmap(NoMarkIconPath))
    PlusIcon = QIcon(QPixmap(PlusIconPath))
    TrashIcon = QIcon(QPixmap(TrashIconPath))
    RedDashIcon = QIcon(QPixmap(RedDashIconPath))
    InfoIcon = QIcon(QPixmap(InfoIconPath))
    AboutIcon = QIcon(QPixmap(AboutIconPath))
    InfoSettingIcon = QIcon(QPixmap(InfoSettingIconPath))
    WarningCheckBigIcon = QIcon(QPixmap(WarningCheckBigIconPath))
    WarningCheckIcon = QIcon(QPixmap(WarningCheckIconPath))
    StartMultiplexingIcon = QIcon(QPixmap(StartMultiplexingIconPath))
    PauseMultiplexingIcon = QIcon(QPixmap(PauseMultiplexingIconPath))
    AddToQueueIcon = QIcon(QPixmap(AddToQueueIconPath))
    CleanIcon = QIcon(QPixmap(ClearIconPath))
    TopIcon = QIcon(QPixmap(TopIconPath))
    DownIcon = QIcon(QPixmap(DownIconPath))
    UpIcon = QIcon(QPixmap(UpIconPath))
    BottomIcon = QIcon(QPixmap(BottomIconPath))
    SelectFolderIcon = QIcon(QPixmap(FolderIconPath))
    SettingIcon = QIcon(QPixmap(SettingIconPath))
    TelegramIcon = QIcon(QPixmap(TelegramIconPath))
    TwitterIcon = QIcon(QPixmap(TwitterIconPath))
    AppIcon = QIcon(QPixmap(AppIconPath))
    LanguagesFilePath = os.path.join(os.path.abspath(LanguagesFolderPath), "iso639_language_list.json")
    AppLogFilePath = os.path.join(os.path.abspath(TempFolderPath), "app_log.txt")
    MuxingLogFilePath = os.path.join(os.path.abspath(TempFolderPath), "muxing_log_file.txt")
    mkvpropeditJsonJobFilePath = os.path.join(os.path.abspath(TempFolderPath), "mkvpropeditJob.json")
    mkvmergeJsonJobFilePath = os.path.join(os.path.abspath(TempFolderPath), "MkvmergeJob.json")
    mkvmergeJsonInfoFilePath = os.path.join(os.path.abspath(TempFolderPath), "MkvmergeInfo.json")
    SettingJsonInfoFilePath = os.path.join(os.path.abspath(TempFolderPath), "setting.json")
    MKVPROPEDIT_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvpropedit")
    MKVMERGE_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvmerge")

    read_setting_file()
except Exception as e:
    missing_files_message = MissingFilesMessage(error_message=str(e))
    missing_files_message.execute()
