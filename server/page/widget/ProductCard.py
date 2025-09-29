from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ProductCard(QWidget):
    def __init__(self, id, title, image_path, add_to_cart):
        super().__init__()
        self.id = id
        self.image_path = image_path
        self.title = title
        self.add_to_cart = add_to_cart

        # Layout for the card
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Product image
        image_label = QLabel()
        pixmap = QPixmap(image_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Product title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold;")

        # Add to cart button
        add_button = QPushButton("Add to Cart")
        add_button.setStyleSheet("""
               QPushButton {
                   background-color: #4CAF50;
                   color: white;
                   padding: 5px;
                   border-radius: 5px;
               }
               QPushButton:hover {
                   background-color: #45a049;
               }
           """)
        add_button.clicked.connect(self.on_add_to_cart)

        # Add widgets to layout
        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(add_button)

    def on_add_to_cart(self):
        self.add_to_cart(self.id)