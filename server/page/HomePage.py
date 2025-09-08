from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class HomePage(QWidget):
    def __init__(self, gotoCreateOrderPage, gotoOrderManagePage):
        super().__init__()

        # Main vertical layout
        layout = QVBoxLayout(self)

        # Add stretch at the top
        layout.addStretch()

        # Two buttons stacked in the center
        button1 = QPushButton("Create Order")
        button1.setStyleSheet("""
                            QPushButton {
                                padding: 10px;
                            }
                        """)
        button1.clicked.connect(gotoCreateOrderPage)

        button2 = QPushButton("Order Management")
        button2.setStyleSheet("""
                            QPushButton {
                                padding: 10px;
                            }
                        """)
        button2.clicked.connect(gotoOrderManagePage)

        button1.setFixedWidth(200)
        button2.setFixedWidth(200)

        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Add stretch at the bottom
        layout.addStretch()