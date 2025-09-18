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
        self._initialized = {}

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

        # self.homePage = HomePage(
        #     self.goto_create_order_page,
        #     self.goto_order_manage_page,
        #     self.go_to_product_location_page,
        #     self.goto_ptl_page
        # )
        # self.createOrderPage = CreateOrderPage(self.goto_home_page)
        # self.orderManagePage = OrderManagementPage(self.goto_home_page)
        # self.productLocationManagePage = ProductLocationPage(self.goto_home_page)
        # self.ptlPage = PTLPage(self.goto_home_page)

        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QWidget())

        self.stack_change(0)
        self.stacked_widget.currentChanged.connect(self.stack_change)

    def stack_change(self, index):
        if index in self._initialized:
            self.stacked_widget.setCurrentIndex(index)
            return
        if index == 0:
            self.stacked_widget.insertWidget(0, HomePage(
                self.goto_create_order_page,
                self.goto_order_manage_page,
                self.go_to_product_location_page,
                self.goto_ptl_page
            ))
        elif index == 1:
            self.stacked_widget.insertWidget(1, CreateOrderPage(self.goto_home_page))
        elif index == 2:
            self.stacked_widget.insertWidget(2, OrderManagementPage(self.goto_home_page))
        elif index == 3:
            self.stacked_widget.insertWidget(3, ProductLocationPage(self.goto_home_page))
        elif index == 4:
            self.stacked_widget.insertWidget(4, PTLPage(self.goto_home_page))
        self._initialized[index] = True
        self.stacked_widget.setCurrentIndex(index)

    def goto_home_page(self):
        self.stack_change(0)

    def goto_create_order_page(self):
        self.stack_change(1)

    def goto_order_manage_page(self):
        self.stack_change(2)

    def go_to_product_location_page(self):
        self.stack_change(3)

    def goto_ptl_page(self):
        self.stack_change(4)
