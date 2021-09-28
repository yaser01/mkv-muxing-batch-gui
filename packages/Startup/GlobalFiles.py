import os
import sys
from pathlib import Path
from PySide2.QtGui import QPixmap, QIcon
import tempfile

from packages.Widgets.MissingFilesMessage import MissingFilesMessage
# noinspection PyUnresolvedReferences
import packages.Startup.MainApplication


def get_temp_folder_path():
    temp_folder_path = tempfile.gettempdir()
    my_temp_folder_path = os.path.join(os.path.abspath(temp_folder_path), Path('MKV Muxing Batch GUI'))
    os.makedirs(my_temp_folder_path, exist_ok=True)
    return my_temp_folder_path


script_path = sys.argv[0]  # get path of the this file
script_folder = os.path.dirname(script_path)
resources_folder = os.path.join(os.path.abspath(script_folder), Path('Resources'))
FontFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Fonts'))
IconFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Icons'))
ToolsFolderPath = os.path.join(os.path.abspath(resources_folder), Path('Tools'))
TempFolderPath = get_temp_folder_path()
MergeLogsFolderPath = os.path.join(os.path.abspath(TempFolderPath), Path('Logs'))
os.makedirs(MergeLogsFolderPath, exist_ok=True)
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
    AppIcon = QIcon(QPixmap(AppIconPath))

    AppLogFilePath = os.path.join(os.path.abspath(TempFolderPath), "app_log.txt")
    MuxingLogFilePath = os.path.join(os.path.abspath(TempFolderPath), "muxing_log_file.txt")
    mkvpropeditJsonJobFilePath = os.path.join(os.path.abspath(TempFolderPath), "mkvpropeditJob.json")
    mkvmergeJsonJobFilePath = os.path.join(os.path.abspath(TempFolderPath), "MkvmergeJob.json")
    mkvmergeJsonInfoFilePath = os.path.join(os.path.abspath(TempFolderPath), "MkvmergeInfo.json")
    MKVPROPEDIT_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvpropedit")
    MKVMERGE_PATH = os.path.join(os.path.abspath(ToolsFolderPath), "mkvmerge")
except Exception as e:
    missing_files_message = MissingFilesMessage(error_message=str(e))
    missing_files_message.execute()
