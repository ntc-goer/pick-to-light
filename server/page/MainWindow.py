from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget

from page.CreateOrderPage import CreateOrderPage
from page.HomePage import HomePage
from page.OrderManagementPage import OrderManagementPage
from page.PTLPage import PTLPage
from page.ProductLocationPage import ProductLocationPage


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

        self.homePage = HomePage(
            self.goto_create_order_page,
            self.goto_order_manage_page,
            self.go_to_product_location_page,
            self.goto_ptl_page
        )
        self.createOrderPage = CreateOrderPage(self.goto_home_page)
        self.orderManagePage = OrderManagementPage(self.goto_home_page)
        self.productLocationManagePage = ProductLocationPage(self.goto_home_page)
        self.ptlPage = PTLPage(self.goto_home_page)

        self.stacked_widget.addWidget(self.homePage)
        self.stacked_widget.addWidget(self.createOrderPage)
        self.stacked_widget.addWidget(self.orderManagePage)
        self.stacked_widget.addWidget(self.productLocationManagePage)
        self.stacked_widget.addWidget(self.ptlPage)

        self.stacked_widget.setCurrentIndex(0)

    def goto_home_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def goto_create_order_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def goto_order_manage_page(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_product_location_page(self):
        self.stacked_widget.setCurrentIndex(3)

    def goto_ptl_page(self):
        self.stacked_widget.setCurrentIndex(4)