import os
import subprocess
import sys
from os import listdir
from pathlib import Path
from PySide2.QtGui import QPixmap, QIcon
import struct
from PySide2.QtWidgets import QStyleFactory

from packages.Startup.ReadSettingFile import read_setting_file
from packages.Widgets.MissingFilesMessage import MissingFilesMessage
# noinspection PyUnresolvedReferences
import packages.Startup.MainApplication


def create_app_data_folder():
    """
        Returns a parent directory path
        where persistent application data can be stored.

        # linux: ~/.local/share
        # macOS: ~/Library/Application Support
        # windows: C:/Users/<USER>/AppData/Roaming
        """
    home = Path.home()
    app_data = ""
    if sys.platform == "win32":
        app_data = home / "AppData/Roaming"
    elif sys.platform == "linux":
        app_data = home / ".local/share"
    elif sys.platform == "darwin":
        app_data = home / "Library/Application Support"
    my_app_data_folder = app_data / "MKV Muxing Batch GUI"
    try:
        os.makedirs(my_app_data_folder, exist_ok=True)
    except Exception as e:
        pass
    return my_app_data_folder


def add_double_quotation(string):
    return "\"" + str(string) + "\""


def get_file_name_absolute_path(file_name, folder_path):
    return os.path.join(Path(folder_path), file_name)


def get_files_names_absolute_list(files_names, folder_path):
    result = []
    for i in range(len(files_names)):
        result.append(get_file_name_absolute_path(file_name=files_names[i], folder_path=folder_path))
    return result


def delete_old_media_files():
    only_media_info_files = get_files_names_absolute_list(files_names=listdir(MediaInfoFolderPath),
                                                          folder_path=MediaInfoFolderPath)
    for file_name in only_media_info_files:
        try:
            os.remove(file_name)
        except Exception as e:
            pass


script_path = sys.argv[0]  # get path of the this file
script_folder = os.path.dirname(script_path)
resources_folder = os.path.join(os.path.abspath(script_folder), Path('Resources'))
FontFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Fonts'))
IconFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Icons'))
GlobalToolsFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Tools'))
ToolsFolderPath = os.path.join(os.path.abspath(GlobalToolsFolderPath), Path('Windowsx64'))
LanguagesFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Languages'))
if sys.platform=="win32":
    if struct.calcsize("P") * 8 == 32:
        ToolsFolderPath = os.path.join(os.path.abspath(GlobalToolsFolderPath), Path('Windows32'))
    else:
        ToolsFolderPath = os.path.join(os.path.abspath(GlobalToolsFolderPath), Path('Windows64'))
elif sys.platform == "linux" or sys.platform == "linux2":
    ToolsFolderPath = os.path.join(os.path.abspath(GlobalToolsFolderPath), Path('Linux'))
else:
    ToolsFolderPath = os.path.join(os.path.abspath(GlobalToolsFolderPath), Path('Other Systems'))
AppDataFolderPath = create_app_data_folder()
MergeLogsFolderPath = os.path.join(os.path.abspath(AppDataFolderPath), Path('Logs'))
MediaInfoFolderPath = os.path.join(os.path.abspath(AppDataFolderPath), Path('MediaInfo'))
os.makedirs(MergeLogsFolderPath, exist_ok=True)
os.makedirs(MediaInfoFolderPath, exist_ok=True)
delete_old_media_files()


def get_mkvmerge_version():
    with open(TestMkvmergeFilePath, "w+", encoding="UTF-8") as test_file:
        command = add_double_quotation(MKVMERGE_PATH) + " -V"
        mux_process = subprocess.run(command, shell=True, stdout=test_file)
    with open(TestMkvmergeFilePath, "r+", encoding="UTF-8") as test_file:
        return test_file.readline().rstrip()


def get_mkvpropedit_version():
    with open(TestMkvpropeditFilePath, "w+", encoding="UTF-8") as test_file:
        command = add_double_quotation(MKVPROPEDIT_PATH) + " -V"
        mux_process = subprocess.run(command, shell=True, stdout=test_file)
    with open(TestMkvpropeditFilePath, "r+", encoding="UTF-8") as test_file:
        return test_file.readline().rstrip()


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
    LeftArrowIconPath = os.path.join(os.path.abspath(IconFolderPath), 'LeftArrow.png')
    RightArrowIconPath = os.path.join(os.path.abspath(IconFolderPath), 'RightArrow.png')
    ErrorBigIconPath = os.path.join(os.path.abspath(IconFolderPath), 'ErrorBig.png')
    DonationsIconPath = os.path.join(os.path.abspath(IconFolderPath), 'Donations.png')
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
    LeftArrowIcon = QIcon(QPixmap(LeftArrowIconPath))
    RightArrowIcon = QIcon(QPixmap(RightArrowIconPath))
    DonationsIcon = QIcon(QPixmap(DonationsIconPath))
    AppIcon = QIcon(QPixmap(AppIconPath))
    LanguagesFilePath = os.path.join(os.path.abspath(LanguagesFolderPath), "iso639_language_list.json")
    AppLogFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "app_log.txt")
    MuxingLogFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "muxing_log_file.txt")
    TestMkvmergeFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "test_mkvmerge.txt")
    TestMkvpropeditFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "test_mkvpropedit.txt")
    mkvpropeditJsonJobFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "mkvpropeditJob.json")
    mkvmergeJsonJobFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "MkvmergeJob.json")
    mkvmergeJsonInfoFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "MkvmergeInfo.json")
    SettingJsonInfoFilePath = os.path.join(os.path.abspath(AppDataFolderPath), "setting.json")
    MKVPROPEDIT_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvpropedit")
    MKVMERGE_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvmerge")
    MKVPROPEDIT_VERSION = get_mkvpropedit_version()
    MKVMERGE_VERSION = get_mkvmerge_version()
    if MKVMERGE_VERSION.find("mkvmerge") == -1:
        MKVMERGE_VERSION="mkvmerge: not found!"
        raise Exception("mkvmerge file! ")
    if MKVPROPEDIT_VERSION.find("mkvpropedit") == -1:
        MKVPROPEDIT_VERSION = "mkvpropedit: not found!"
        raise Exception("mkvpropedit file! ")
    read_setting_file(setting_json_info_file_path=SettingJsonInfoFilePath, all_languages_file_path=LanguagesFilePath)
except Exception as e:
    missing_files_message = MissingFilesMessage(error_message=str(e))
    missing_files_message.execute()
