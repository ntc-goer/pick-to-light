from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFileDialog, QLineEdit, \
    QMessageBox

from db.db_manager import get_db
from page.widget.BackButton import BackButton
from page.widget.ProductItem import ProductItem


class ProductManagementPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()

        self.upload_product_stock = 0
        self.upload_product_name = ""
        self.upload_file_name = None
        self.image_label = None
        self.is_add_product = True

        self.edit_product_id = None
        self.edit_product_name = ""
        self.edit_product_image = None
        self.edit_product_stock = None
        self.edit_product_price = None

        self.db = get_db()

        # Layout
        layout = QGridLayout(self)

        # Back button (row 0, col 0)
        back_button = BackButton(goto_home_page)

        # Product scroll
        self.product_scroll = QScrollArea()
        self.product_scroll.setWidgetResizable(True)

        self.product_container = QWidget()
        self.product_layout = QVBoxLayout(self.product_container)
        self.product_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.product_scroll.setWidget(self.product_container)

        self.load_products()

        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        add_product_button = QPushButton("Add Product")
        add_product_button.setStyleSheet("""
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
        add_product_button.clicked.connect(self.add_product)

        self.edit_container = QWidget()
        self.edit_layout = QVBoxLayout(self.edit_container)
        self.edit_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.edit_container.setStyleSheet("""
           QWidget {
               background-color: #ffffff;
           }
        """)

        self.right_layout.addWidget(add_product_button)
        self.right_layout.addWidget(self.edit_container)
        self.right_layout.setStretchFactor(self.edit_container, 1)

        self.load_right_part()

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(self.product_scroll, 1, 0, 1, 1)  # row=1, col=0, span=1x1
        layout.addWidget(self.right_container, 1, 1, 1, 1)  # row=1, col=1, span=1x1

        layout.setColumnStretch(0, 7)  # left column
        layout.setColumnStretch(1, 3)  # right column (wider)
        layout.setRowStretch(1, 1)  # allow product list row to expand

    def edit_product(self, product_id):
        self.edit_product_id = product_id
        self.is_add_product = False
        self.load_right_part()

    def load_products(self):
        while self.product_layout.count():
            item = self.product_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        products = self.db.get_products()
        for product in products:
            self.product_layout.addWidget(
                ProductItem(
                    product_id=product["id"],
                    product_name=product["product_name"],
                    product_image=product["product_image"],
                    stock=product["stock"],
                    price=product["price"],
                    edit_product_cb=self.edit_product
                ))

    def load_right_part(self):
        while self.edit_layout.count():
            item = self.edit_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if self.is_add_product:
            self.load_add_product()
        else:
            self.load_edit_product()

    def load_add_product(self):
        add_product_label = QLabel("Add Product")
        add_product_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        add_product_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.edit_layout.addWidget(add_product_label)

        self.image_label = QLabel("No Image")
        self.image_label.setFixedSize(100, 100)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_layout.addWidget(self.image_label)

        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)
        upload_button.setStyleSheet("""
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
        self.edit_layout.addWidget(upload_button)

        upload_product_name_label = QLabel(f"Product Name:")
        upload_product_name_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.edit_layout.addWidget(upload_product_name_label)

        upload_product_name = QLineEdit()
        upload_product_name.setPlaceholderText("Shirt")
        upload_product_name.textChanged.connect(self.on_upload_product_name_changed)
        self.edit_layout.addWidget(upload_product_name)

        upload_product_stock_label = QLabel(f"Product Stock:")
        upload_product_stock_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.edit_layout.addWidget(upload_product_stock_label)

        upload_product_stock = QLineEdit()
        upload_product_stock.setPlaceholderText("10")
        upload_product_stock.textChanged.connect(self.on_upload_product_stock_changed)
        upload_product_stock.setValidator(QIntValidator(1,99999))
        self.edit_layout.addWidget(upload_product_stock)

        add_product_button = QPushButton("Add Product")
        add_product_button.clicked.connect(self.submit_add_product)
        add_product_button.setStyleSheet("""
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
        self.edit_layout.addWidget(add_product_button)


    def load_edit_product(self):
        edit_product_label = QLabel("Edit Product")
        edit_product_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        edit_product_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.edit_layout.addWidget(edit_product_label)
        product = self.db.get_product_by_id(self.edit_product_id)
        if product is None:
            return self.show_message("Product not found")

        self.edit_product_name = product["product_name"]
        self.edit_product_image = product["product_image"]
        self.edit_product_stock = int(product["stock"])
        self.edit_product_price = product["price"]

        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_layout.addWidget(self.image_label)
        pixmap = QPixmap(self.edit_product_image)

        scaled_pixmap = pixmap.scaled(
            self.image_label.width(),
            self.image_label.height(),
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        edit_image_button = QPushButton("Upload Image")
        edit_image_button.clicked.connect(self.upload_edit_image)
        edit_image_button.setStyleSheet("""
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
        self.edit_layout.addWidget(edit_image_button)

        edit_product_name_label = QLabel(f"Product Name:")
        edit_product_name_label.setStyleSheet("font-size: 12px; margin-top: 10px;")

        self.edit_layout.addWidget(edit_product_name_label)

        edit_product_name = QLineEdit()
        edit_product_name.setPlaceholderText("Shirt")
        edit_product_name.setText(self.edit_product_name)
        edit_product_name.textChanged.connect(self.on_edit_product_name_changed)
        self.edit_layout.addWidget(edit_product_name)

        edit_product_stock_label = QLabel(f"Product Stock:")
        edit_product_stock_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.edit_layout.addWidget(edit_product_stock_label)

        print(self.edit_product_stock)
        edit_product_stock = QLineEdit()
        edit_product_stock.setPlaceholderText("10")
        edit_product_stock.setText(str(int(self.edit_product_stock)))
        edit_product_stock.textChanged.connect(self.on_edit_product_stock_changed)
        edit_product_stock.setValidator(QIntValidator(1, 99999))
        self.edit_layout.addWidget(edit_product_stock)

        edit_product_button = QPushButton("Edit Product")
        edit_product_button.clicked.connect(self.submit_edit_product)
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
        self.edit_layout.addWidget(edit_product_button)
        return None

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def submit_add_product(self):
        self.db.insert_product(
            product_name=self.upload_product_name,
            product_image=self.upload_file_name,
            price=1000,
            stock=int(self.upload_product_stock),
        )
        self.load_products()
        self.show_message("Insert Product Successful")
        self.load_right_part()

    def submit_edit_product(self):
        self.db.update_product_by_id(
            product_id=self.edit_product_id,
            product_name=self.edit_product_name,
            product_image=self.edit_product_image,
            price=1000,
            stock=self.edit_product_stock,
        )
        self.load_products()
        self.show_message("Update Product Successful")
        self.load_right_part()

    def on_upload_product_name_changed(self, text):
        self.upload_product_name = text

    def on_edit_product_name_changed(self, text):
        self.edit_product_name = text

    def on_upload_product_stock_changed(self, text):
        self.upload_product_stock = text

    def on_edit_product_stock_changed(self, text):
        self.edit_product_stock = text

    def upload_image(self):
        self.upload_file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if self.upload_file_name:
            pixmap = QPixmap(self.upload_file_name)

            scaled_pixmap = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def upload_edit_image(self):
        self.edit_product_image, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        if self.edit_product_image:
            pixmap = QPixmap(self.edit_product_image)

            scaled_pixmap = pixmap.scaled(
                self.image_label.width(),
                self.image_label.height(),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def add_product(self):
        self.is_add_product = True
        self.load_right_part()
