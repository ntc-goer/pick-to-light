from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class OrderManagementPage(QWidget):
    def __init__(self, gotoHomePage):
        super().__init__()
        self.setWindowTitle("Simple Page")
        self.setGeometry(200, 200, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # Label
        label = QLabel("Hello, Warehouse Management!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        self.setLayout(layout)