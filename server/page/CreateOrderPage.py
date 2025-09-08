import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QScrollArea, QToolButton

from page.widget.ProductCard import ProductCard


class CreateOrderPage(QWidget):
    def __init__(self, gotoHomePage):
        super().__init__()

        # Layout
        layout = QGridLayout(self)

        # === Column 1 ===
        # Back button (row 0, col 0)
        back_button = QToolButton()
        back_button.setIcon(QIcon("page/images/back.jpg"))  # <- your back icon path
        back_button.setIconSize(QSize(32, 32))
        back_button.setToolTip("Go Back")
        back_button.clicked.connect(gotoHomePage)
        back_button.setStyleSheet("border: none; background: transparent")  # remove button border

        # Scroll area for product list
        product_scroll = QScrollArea()
        product_scroll.setWidgetResizable(True)




        # === Column 2 ===
        selected_scroll = QScrollArea()
        selected_scroll.setWidgetResizable(True)

        selected_container = QWidget()
        selected_layout = QVBoxLayout(selected_container)

        self.product_container = QWidget()
        self.container_layout = QVBoxLayout(self.product_container)
        self.showProduct("Shirt", "page/images/shirt1.jpg")
        self.showProduct("Jean", "page/images/jean.jpg")
        product_scroll.setWidget(self.product_container)
        # Example selected products
        for i in range(5):
            selected_layout.addWidget(QLabel(f"Selected Product {i + 1}"))

        selected_scroll.setWidget(selected_container)

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(product_scroll, 1, 0, 1, 1)  # row=1, col=0, span=1x1
        layout.addWidget(selected_scroll, 0, 1, 2, 1)  # spans 2 rows in col=1

        # Stretching: make both columns expand properly
        layout.setColumnStretch(0, 7)  # left column
        layout.setColumnStretch(1, 3)  # right column (wider)
        layout.setRowStretch(1, 1)  # allow product list row to expand

    def showProduct(self, label, imageUrl):
        title_label = QLabel(label)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")

        self.container_layout.addWidget(title_label)

        product_layout = QGridLayout(self.product_container)
        self.container_layout.addLayout(product_layout)

        itemPerRow = 5
        # Example product items
        for i in range(7):
            product_layout.addWidget(
                ProductCard(imageUrl, f"Product {i}"),
                i / itemPerRow,
                i % itemPerRow, 1, 1)
