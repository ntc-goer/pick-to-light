from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class HomePage(QWidget):
    def __init__(self, gotoCreateOrderPage, gotoOrderManagePage, goToProductLocationPage):
        super().__init__()

        # Main vertical layout
        layout = QVBoxLayout(self)

        # Add stretch at the top
        layout.addStretch()

        # Two buttons stacked in the center
        button1 = QPushButton("Create Order")
        button1.setStyleSheet("""
                            QPushButton {
                                padding: 20px;
                            }
                        """)
        button1.clicked.connect(gotoCreateOrderPage)

        button2 = QPushButton("Order Management")
        button2.setStyleSheet("""
                            QPushButton {
                                padding: 20px;
                            }
                        """)
        button2.clicked.connect(gotoOrderManagePage)

        button3 = QPushButton("Product Location Management")
        button3.setStyleSheet("""
                                    QPushButton {
                                        padding: 20px;
                                    }
                                """)
        button3.clicked.connect(goToProductLocationPage)

        button1.setFixedWidth(400)
        button2.setFixedWidth(400)
        button3.setFixedWidth(400)

        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button3, alignment=Qt.AlignmentFlag.AlignHCenter)


        # Add stretch at the bottom
        layout.addStretch()