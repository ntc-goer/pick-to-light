from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class CartItem(QWidget):
    def __init__(self, id, product_id, product_name, product_image, price, quantity):
        super().__init__()

        self.product_id = product_id
        self.product_image = product_image
        self.price = price
        self.product_name = product_name
        self.quantity = quantity

        layout = QGridLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(5)

        # --- Column 1: Product image ---
        image_label = QLabel()
        image_label.setFixedSize(64, 64)
        pixmap = QPixmap(product_image).scaled(
            64, 64,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label, 0, 0, 2, 1)

        # --- Column 2: Product name + price ---
        product_data_layout = QVBoxLayout()
        product_data_layout.setSpacing(2)

        title_label = QLabel(product_name)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        price_label = QLabel(f"${price:.2f}")
        price_label.setStyleSheet("color: gray; font-size: 12px;")
        price_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        product_data_layout.addWidget(title_label)
        product_data_layout.addWidget(price_label)

        layout.addLayout(product_data_layout, 0, 1, 2, 1)

        # --- Column 3: Quantity ---
        quantity_label = QLabel(f"x {quantity}")
        quantity_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(quantity_label, 0, 2, 2, 1)

        # Stretch ratios: Image small, text large, qty narrow
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 2)