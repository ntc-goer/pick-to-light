from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout


class CartItem(QWidget):
    def __init__(self, product_id,title, product_image, price, quantity):
        super().__init__()

        self.product_id = product_id
        self.product_image = product_image
        self.price = price
        self.title = title
        self.quantity = quantity

        layout = QGridLayout(self)

        # Product image
        image_label = QLabel()
        pixmap = QPixmap(product_image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Product Data
        product_data_container = QWidget()
        product_data_layout = QVBoxLayout(product_data_container)
        ## Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold;")
        product_data_layout.addWidget(title_label)
        ## Price
        price_label = QLabel(str(price))
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        product_data_layout.addWidget(price_label)

        # Product Quantity
        quantity_label = QLabel("x" + str(quantity))
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quantity_label.setStyleSheet("font-weight: bold;")

        layout.addWidget(image_label, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(product_data_container, 0, 1, 1, 1)
        layout.addWidget(quantity_label, 0, 2, 1, 1)

        # Stretching
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)