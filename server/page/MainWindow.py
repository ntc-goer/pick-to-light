import os

import serial
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget

# Import your page classes
from page.CreateOrderPage import CreateOrderPage
from page.HomePage import HomePage
from page.OrderManagementPage import OrderManagementPage
from page.PTLPage import PTLPage
from page.ProductLocationPage import ProductLocationPage
from page.ProductManagementPage import ProductManagementPage
from page.widget.SerialReaderThread import SerialReaderThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        port = os.getenv("SERIAL_PORT", "COM3")
        baud_rate = os.getenv("SERIAL_BAUD_RATE", 9600)
        # self.arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=1)
        self.arduino = None
        self.reader = SerialReaderThread(arduino=self.arduino)
        self.start_listening()

        # Config Main Window
        self.setWindowTitle("Warehouse Management")
        self.setWindowIcon(QIcon("images/icon.ico"))
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

        # Define an index map for clarity
        self.PAGE_INDEX = {
            'HOME': 0,
            'PRODUCT_MANAGEMENT': 1,
            'CREATE_ORDER': 2,
            'ORDER_MANAGEMENT': 3,
            'PRODUCT_LOCATION': 4,
            'PTL': 5
        }
        self.current_index = -1  # Track the currently active page index

        # Start on the Home Page
        self.stack_change(self.PAGE_INDEX['HOME'])

    # ----------------------------------------------------------------------
    ## Core Fix: Managing Page Destruction
    # ----------------------------------------------------------------------

    def start_listening(self):
        if self.reader is not None:
            self.reader.data_received.connect(self.update_console)
            self.reader.start()

    def stop_listening(self):
        if self.reader:
            self.reader.stop()
            self.reader.wait()
            self.reader = None

    def update_console(self, text):
        print(text)

    def stack_change(self, target_index):
        # 1. Clean up the existing widget (if any)
        if self.stacked_widget.count() > 0:
            current_widget = self.stacked_widget.currentWidget()

            # This is the crucial part: Remove and delete the old widget
            # Note: The QStackedWidget must be empty before inserting the new widget
            # in a fixed-index system, which is why we're not using target_index here.
            # We simply remove the one widget, then insert the new one at index 0.

            # Get the current widget and remove it from the stack
            self.stacked_widget.removeWidget(current_widget)

            # Manually delete the widget and its children to free resources
            # This implicitly calls the destructors, releasing the camera thread.
            current_widget.deleteLater()

        # 2. Initialize and Insert the new widget at index 0
        new_widget = None
        if target_index == self.PAGE_INDEX['HOME']:
            new_widget = HomePage(
                self.goto_product_manage_page,
                self.goto_create_order_page,
                self.goto_order_manage_page,
                self.go_to_product_location_page,
                self.goto_ptl_page
            )
        elif target_index == self.PAGE_INDEX['PRODUCT_MANAGEMENT']:
            new_widget = ProductManagementPage(self.goto_home_page)
        elif target_index == self.PAGE_INDEX['CREATE_ORDER']:
            new_widget = CreateOrderPage(self.goto_home_page)
        elif target_index == self.PAGE_INDEX['ORDER_MANAGEMENT']:
            new_widget = OrderManagementPage(self.goto_home_page)
        elif target_index == self.PAGE_INDEX['PRODUCT_LOCATION']:
            new_widget = ProductLocationPage(self.goto_home_page, arduino=self.arduino)
        elif target_index == self.PAGE_INDEX['PTL']:
            new_widget = PTLPage(self.goto_home_page, arduino=self.arduino)
        else:
            return  # Don't proceed if widget is None

        # Add the new widget and make it the current one.
        # Since we removed the previous one, the new widget will be at index 0.
        self.stacked_widget.addWidget(new_widget)
        self.stacked_widget.setCurrentWidget(new_widget)
        self.current_index = target_index  # Update the current index tracker
        print(f"Inserted and set new page (index {target_index}).")

    # ----------------------------------------------------------------------
    ## Navigation Methods (Unchanged)
    # ----------------------------------------------------------------------

    def goto_home_page(self):
        self.stack_change(self.PAGE_INDEX['HOME'])

    def goto_product_manage_page(self):
        self.stack_change(self.PAGE_INDEX['PRODUCT_MANAGEMENT'])

    def goto_create_order_page(self):
        self.stack_change(self.PAGE_INDEX['CREATE_ORDER'])

    def goto_order_manage_page(self):
        self.stack_change(self.PAGE_INDEX['ORDER_MANAGEMENT'])

    def go_to_product_location_page(self):
        self.stack_change(self.PAGE_INDEX['PRODUCT_LOCATION'])

    def goto_ptl_page(self):
        self.stack_change(self.PAGE_INDEX['PTL'])