from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class HomePage(QWidget):
    def __init__(self,
                 gotoProductManagePage,
                 gotoCreateOrderPage,
                 gotoOrderManagePage,
                 goToProductLocationPage,
                 gotoPtlPage

                 ):
        super().__init__()
        # Main vertical layout
        layout = QVBoxLayout(self)

        # Add stretch at the top
        layout.addStretch()

        # Two buttons stacked in the center

        button0 = QPushButton("Product Management")
        button0.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        button0.setCursor(Qt.CursorShape.PointingHandCursor)
        button0.clicked.connect(gotoProductManagePage)

        button1 = QPushButton("Create Order")
        button1.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        button1.setCursor(Qt.CursorShape.PointingHandCursor)
        button1.clicked.connect(gotoCreateOrderPage)

        button2 = QPushButton("Order Management")
        button2.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;                
                font-size: 14px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        button2.setCursor(Qt.CursorShape.PointingHandCursor)
        button2.clicked.connect(gotoOrderManagePage)

        button3 = QPushButton("Product Location Management")
        button3.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #999;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        button3.setCursor(Qt.CursorShape.PointingHandCursor)
        button3.clicked.connect(goToProductLocationPage)

        button4 = QPushButton("Pick To Light")
        button4.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #42a5f5, stop:1 #1e88e5
                );
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #64b5f6, stop:1 #2196f3
                );
            }
            QPushButton:pressed {
                background-color: #1976d2;
            }
        """)
        button4.setCursor(Qt.CursorShape.PointingHandCursor)
        button4.clicked.connect(gotoPtlPage)

        button0.setFixedWidth(400)
        button1.setFixedWidth(400)
        button2.setFixedWidth(400)
        button3.setFixedWidth(400)
        button4.setFixedWidth(400)

        layout.addWidget(button0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button3, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(button4, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Add stretch at the bottom
        layout.addStretch()
