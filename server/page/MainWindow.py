from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget

from page.CreateOrderPage import CreateOrderPage
from page.HomePage import HomePage
from page.OrderManagementPage import OrderManagementPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Config Main Window
        self.setWindowTitle("Warehouse Management")
        self.setWindowIcon(QIcon("images/icon.ico"))
        # self.setGeometry(0, 0, 900, 900)
        self.setWindowIcon(QIcon("page/images/warehouse.png"))
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(page/images/bg_home.jpeg);
                background-position: center;
            }
        """)

        # Stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.homePage = HomePage(self.gotoCreateOrderPage, self.gotoOrderManagePage)
        self.createOrderPage = CreateOrderPage(self.gotoHomePage)
        self.orderManagePage = OrderManagementPage(self.gotoHomePage)

        self.stacked_widget.addWidget(self.homePage)
        self.stacked_widget.addWidget(self.createOrderPage)
        self.stacked_widget.addWidget(self.orderManagePage)

        self.stacked_widget.setCurrentIndex(0)

    def gotoHomePage(self):
        self.stacked_widget.setCurrentIndex(0)

    def gotoCreateOrderPage(self):
        self.stacked_widget.setCurrentIndex(1)

    def gotoOrderManagePage(self):
        self.stacked_widget.setCurrentIndex(2)
