from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QToolButton


class BackButton(QToolButton):
    def __init__(self, goto_home_page):
        super().__init__()

        self.setIcon(QIcon("page/images/back.jpg"))
        self.setIconSize(QSize(32, 32))
        self.setToolTip("Go Back")
        self.clicked.connect(goto_home_page)
        self.setStyleSheet("border: none; background: transparent")