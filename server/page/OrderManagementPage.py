import time

import qrcode
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea

from db.db_manager import get_db
from page.widget.BackButton import BackButton
from page.widget.OrderCard import OrderCard


class OrderManagementPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()
        self.show_qr_order_id = None
        self.setWindowTitle("Simple Page")
        self.setGeometry(200, 200, 400, 200)

        # Layout
        layout = QGridLayout(self)

        # === Column 1 ===
        # Back button (row 0, col 0)
        back_button = BackButton(goto_home_page)

        # Order scroll
        self.order_scroll = QScrollArea()
        self.order_scroll.setWidgetResizable(True)

        self.order_container = QWidget()
        self.order_layout = QVBoxLayout(self.order_container)
        self.order_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.order_scroll.setWidget(self.order_container)

        self.r_container = QWidget()
        self.r_layout = QVBoxLayout(self.r_container)
        self.r_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.r_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)

        self.load_orders()
        self.load_right_layout()

        layout.addWidget(back_button, 0, 0, 1, 2)  # row=0, col=0, span=1x1
        layout.addWidget(self.order_scroll, 1, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(self.r_container, 1, 1, 1, 1)

        layout.setColumnStretch(0, 7)  # left column
        layout.setColumnStretch(1, 3)  # right column (wider)
        layout.setRowStretch(1, 1)

    def show_qr(self, order_id):
        self.show_qr_order_id = order_id
        self.load_right_layout()

    def load_right_layout(self):
        if not self.show_qr_order_id:
            return

        # Clear layout
        while self.r_layout.count():
            item = self.r_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.show_qr_order_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Convert PIL -> QImage -> QPixmap (copy to avoid GC issue)
        qimg = ImageQt(img).copy()
        pixmap = QPixmap.fromImage(qimg)

        # Add to layout
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(False)
        max_size = 300
        label.setMaximumSize(max_size, max_size)

        label.setPixmap(pixmap.scaled(
            max_size, max_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.r_layout.addWidget(label)

        # Keep reference only to label
        self.qr_label = label

    def load_orders(self):
        while self.order_layout.count():
            item = self.order_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        db = get_db()
        orders = db.get_orders()
        for _, order in enumerate(orders):
            self.order_layout.addWidget(OrderCard
                (
                    order["id"],
                    order["created_at"],
                    show_qr = self.show_qr
                )
            )
