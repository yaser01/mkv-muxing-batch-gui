from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from packages.Startup.GlobalFiles import (
    AppIconPath,
    MKVMERGE_VERSION,
    MKVPROPEDIT_VERSION,
)
from packages.Startup.GlobalIcons import AboutIcon
from packages.Startup.PreDefined import GitHubRepoUrlTag, GPLV2UrlTag, GitHubIssuesUrlTag
from packages.Startup.Version import VERSION, RELEASE_SUFFIX
from packages.Widgets.MyDialog import MyDialog


class AboutDialog(MyDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de MKV Muxing Batch GUI")
        self.setWindowIcon(AboutIcon)
        self.app_icon_label = QLabel()
        self.app_icon_label.setPixmap(QPixmap(AppIconPath).scaledToHeight(175))
        self.app_name_label = QLabel("MKV Muxing Batch GUI")
        self.app_current_version = QLabel(
            "Versión: " + str(VERSION) + str(RELEASE_SUFFIX)
        )
        self.app_mkvmerge_current_version = QLabel(str(MKVMERGE_VERSION))
        self.app_mkvpropedit_current_version = QLabel(str(MKVPROPEDIT_VERSION))
        self.app_link_github_label = QLabel("Buscar actualizaciones en: " + GitHubRepoUrlTag)
        self.app_link_github_label.setOpenExternalLinks(True)
        self.app_licence_label = QLabel(
            "MKV Muxing Batch GUI se distribuye bajo la licencia " + GPLV2UrlTag + "+"
        )
        self.app_licence_label.setOpenExternalLinks(True)
        self.app_warranty_label = QLabel()
        self.app_warranty_label.setText(
            "se proporciona tal cual, sin garantía de ningún tipo, incluyendo la\n"
            "garantía de diseño e idoneidad para un propósito particular"
        )
        self.app_warranty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_bug_report_label = QLabel(
            "Puedes reportar problemas en la " + GitHubIssuesUrlTag
        )
        self.app_bug_report_label.setOpenExternalLinks(True)
        self.app_bug_report_issue_link_label = QLabel(
            "por favor visita la " + GitHubIssuesUrlTag
        )
        self.app_bug_report_issue_link_label.setOpenExternalLinks(True)
        # self.app_follow_me_label = QLabel("Contact me on:")
        self.app_bug_report_label.setOpenExternalLinks(True)
        # self.social_twitter_label = TwitterLabel()
        # self.social_telegram_label = TelegramLabel()
        self.ok_button = QPushButton("Aceptar")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(0)
        # self.buttons_layout.addWidget(self.donate_button)
        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addStretch(0)
        # self.social_media_layout = QHBoxLayout()
        # self.social_media_layout.addStretch(stretch=3)
        # self.social_media_layout.addWidget(self.social_twitter_label, stretch=0)
        # self.social_media_layout.addStretch(stretch=0)
        # self.social_media_layout.addWidget(self.social_telegram_label, stretch=0)
        # self.social_media_layout.addStretch(stretch=3)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(
            self.app_icon_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.app_name_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.app_current_version, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.app_mkvmerge_current_version, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.app_mkvpropedit_current_version, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addWidget(
            self.app_link_github_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # self.main_layout.addWidget(self.app_licence_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.main_layout.addWidget(self.app_warranty_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(
            self.app_bug_report_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # self.main_layout.addWidget(self.app_bug_report_issue_link_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.main_layout.addWidget(self.app_follow_me_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.main_layout.addLayout(self.social_media_layout)
        self.main_layout.addLayout(self.buttons_layout)
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
        self.setWindowFlag(QtCore.Qt.WindowType.WindowContextHelpButtonHint, on=False)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(QSize(self.size().width() + 30, self.size().height()))

    def execute(self):
        self.exec()