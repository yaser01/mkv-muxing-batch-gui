from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QFont
from PySide2.QtWidgets import QLabel, \
    QDialog, QPushButton, QHBoxLayout, QVBoxLayout
from packages.Startup.GlobalFiles import AppIconPath, AboutIcon
from packages.Startup.PreDefined import GitHubRepoUrlTag, GPLV2UrlTag, GitHubIssuesUrlTag
from packages.Startup.Version import Version
from packages.Tabs.SettingTab.Widgets.TelegramLabel import TelegramLabel
from packages.Tabs.SettingTab.Widgets.TwitterLabel import TwitterLabel


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About MKV Muxing Batch GUI")
        self.setWindowIcon(AboutIcon)
        self.app_icon_label = QLabel()
        self.app_icon_label.setPixmap(QPixmap(AppIconPath).scaledToHeight(175))
        self.app_name_label = QLabel("MKV Muxing Batch GUI")
        self.app_current_version = QLabel("Version: " + str(Version))
        self.app_link_github_label = QLabel("Check for updates on: " + GitHubRepoUrlTag)
        self.app_link_github_label.setOpenExternalLinks(True)
        self.app_licence_label = QLabel("MKV Muxing Batch GUI is released under the " + GPLV2UrlTag + "+ licence")
        self.app_licence_label.setOpenExternalLinks(True)
        self.app_warranty_label = QLabel()
        self.app_warranty_label.setText("it is provided as is with no warranty of any kind, including the \n"
                                        "warranty of design and fitness for a particular purpose")
        self.app_warranty_label.setAlignment(Qt.AlignCenter)
        self.app_bug_report_label = QLabel(
            "you can report issues on the " + GitHubIssuesUrlTag)
        self.app_bug_report_label.setOpenExternalLinks(True)
        self.app_bug_report_issue_link_label = QLabel("please visit the " + GitHubIssuesUrlTag)
        self.app_bug_report_issue_link_label.setOpenExternalLinks(True)
        self.app_follow_me_label = QLabel("Contact me on:")
        self.app_bug_report_label.setOpenExternalLinks(True)
        self.social_twitter_label = TwitterLabel()
        self.social_telegram_label = TelegramLabel()
        self.ok_button = QPushButton("OK")
        self.social_media_layout = QHBoxLayout()
        self.social_media_layout.addWidget(QLabel(""), stretch=3)
        self.social_media_layout.addWidget(self.social_twitter_label, stretch=0)
        self.social_media_layout.addWidget(QLabel(""), stretch=0)
        self.social_media_layout.addWidget(self.social_telegram_label, stretch=0)
        self.social_media_layout.addWidget(QLabel(""), stretch=3)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.app_icon_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.app_name_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.app_current_version, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.app_link_github_label, alignment=Qt.AlignCenter)
        # self.main_layout.addWidget(self.app_licence_label, alignment=Qt.AlignCenter)
        # self.main_layout.addWidget(self.app_warranty_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.app_bug_report_label, alignment=Qt.AlignCenter)
        # self.main_layout.addWidget(self.app_bug_report_issue_link_label, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.app_follow_me_label, alignment=Qt.AlignCenter)
        self.main_layout.addLayout(self.social_media_layout)
        self.main_layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)
        # self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)
        self.setup_ui()
        self.signal_connect()

    def setup_app_name_label(self):
        app_name_font = self.app_name_label.font()
        app_name_font.setWeight(QFont.DemiBold)
        app_name_font.setPixelSize(self.app_name_label.fontInfo().pixelSize() + 2)
        self.app_name_label.setFont(app_name_font)

    def setup_ui(self):
        self.setup_app_name_label()
        self.disable_question_mark_window()

    def signal_connect(self):
        self.ok_button.clicked.connect(self.click_yes)

    def click_yes(self):
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, on=False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(QSize(self.size().width() + 30, self.size().height()))

    def execute(self):
        self.exec_()
