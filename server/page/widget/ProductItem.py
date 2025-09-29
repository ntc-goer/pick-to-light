from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QFrame, QSizePolicy, QPushButton


class ProductItem(QWidget):
    def __init__(self, product_id, product_name, product_image, price, stock, edit_product_cb):
        super().__init__()
        self.product_id = product_id
        self.product_name = product_name
        self.product_image = product_image
        self.price = price
        self.stock = int(stock)

        self.edit_product_cb = edit_product_cb

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        content_layout = QGridLayout(content_widget)
        content_layout.setContentsMargins(10, 5, 10, 5)
        content_layout.setHorizontalSpacing(15)
        content_layout.setVerticalSpacing(5)

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
        content_layout.addWidget(image_label, 0, 0, 1, 1)

        # --- Column 2: Product name + stock ---
        product_data_layout = QVBoxLayout()
        product_data_layout.setSpacing(2)

        title_label = QLabel(self.product_name)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        product_data_layout.addWidget(title_label)

        stock_label = QLabel(f"Stock:  {self.stock}")
        stock_label.setStyleSheet("font-size: 12px; color: #333;")
        stock_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        product_data_layout.addWidget(stock_label)

        content_layout.addLayout(product_data_layout, 0, 1, 1, 1)
        # --- Column 3: Edit
        edit_product_button = QPushButton("Edit")
        edit_product_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        edit_product_button.clicked.connect(self.edit_product)
        content_layout.addWidget(edit_product_button, 0, 2, 1, 1)

        # Stretch ratios
        content_layout.setColumnStretch(0, 2)
        content_layout.setColumnStretch(1, 6)
        content_layout.setColumnStretch(2, 2)

        # --- Add content + separator line ---
        main_layout.addWidget(content_widget)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

    def edit_product(self):
        self.edit_product_cb(self.product_id)
