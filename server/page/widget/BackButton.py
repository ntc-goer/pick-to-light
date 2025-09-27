from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QToolButton


class BackButton(QToolButton):
    def connect_f(self, goto_home_page, pre_func, after_func):
        if pre_func is not None:
            pre_func()
        goto_home_page()
        if after_func is not None:
            after_func()

    def __init__(self, goto_home_page, pre_func = None, after_func = None):
        super().__init__()

        self.setIcon(QIcon("page/images/back.jpg"))
        self.setIconSize(QSize(32, 32))
        self.setToolTip("Go Back")
        self.clicked.connect(lambda: self.connect_f(goto_home_page, pre_func, after_func))
        self.setStyleSheet("border: none; background: transparent")