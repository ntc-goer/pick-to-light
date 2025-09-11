import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame

from db.db_manager import get_db


class PtlOrderCard(QWidget):
    def __init__(self, id, created_at, on_ptl, on_show_direction):
        super().__init__()
        self.id = id
        self.created_at = created_at
        self.on_ptl = on_ptl
        self.on_show_direction = on_show_direction

        self.db = get_db()

        layout = QGridLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(5)

        # Row 1: #Id - created_at
        order_label = QLabel(f"<b>Order</b> #{self.id} - {self.created_at.strftime('%d %b %Y, %I:%M %p')}")
        order_label.setStyleSheet("font-size: 13px;")
        order_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(order_label, 0, 0, 1, 2)  # span 2 columns

        # Row 2, Column 1: Order Items
        order_item_list_layout = QVBoxLayout()
        self.order_item_layout = QHBoxLayout()
        self.load_order_items()
        order_item_list_layout.addLayout(self.order_item_layout)

        layout.addLayout(order_item_list_layout, 1, 0, 1, 1)

        # Row 2, Column 2: Features
        feature_layout = QHBoxLayout()
        ptl_button = QPushButton("PTL")
        ptl_button.clicked.connect(self.on_ptl_btn_clicked)
        show_direction_button = QPushButton("Show Map")
        show_direction_button.clicked.connect(self.on_show_direction_clicked)

        feature_layout.addWidget(ptl_button)
        feature_layout.addWidget(show_direction_button)
        layout.addLayout(feature_layout, 1, 1, 1, 1)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator, 2, 0, 1, 2)

    def on_ptl_btn_clicked(self):
        self.on_ptl(self.id)

    def on_show_direction_clicked(self):
        self.on_show_direction()

    def load_order_items(self):
        order_items = self.db.get_order_items_by_order_id(self.id)
        order_item_data_layout = QVBoxLayout()
        for _, order_item in enumerate(order_items):
            layout = QHBoxLayout()

            image_label = QLabel()
            image_label.setFixedSize(30, 30)
            pixmap = QPixmap(order_item["product_image"]).scaled(
                30, 30,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(image_label)

            order_item_label = QLabel(f"{order_item['product_name']} x {order_item['quantity']} ")
            order_item_label.setStyleSheet("font-size: 12px;")
            order_item_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(order_item_label)
            order_item_data_layout.addLayout(layout)
        self.order_item_layout.addLayout(order_item_data_layout)
