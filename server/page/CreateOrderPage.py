import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QScrollArea, QToolButton, \
    QSpacerItem, QSizePolicy
from db.db_manager import get_db
from page.widget.BackButton import BackButton
from page.widget.CartItem import CartItem
from page.widget.ProductCard import ProductCard

class CreateOrderPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()

        # Layout
        layout = QGridLayout(self)

        # === Column 1 ===
        # Back button (row 0, col 0)
        back_button = BackButton(goto_home_page)

        # Scroll area for product list
        product_scroll = QScrollArea()
        product_scroll.setWidgetResizable(True)

        self.product_container = QWidget()
        self.container_layout = QVBoxLayout(self.product_container)
        self.load_product("Shirt", os.getenv("SHIRT_CATEGORY_ID"))
        self.load_product("Jean", os.getenv("PANT_CATEGORY_ID"))

        product_scroll.setWidget(self.product_container)

        # === Column 2 ===
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)

        cart_container = QWidget()
        self.cart_layout = QVBoxLayout(cart_container)
        self.cart_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.load_cart()

        cart_scroll.setWidget(cart_container)

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(product_scroll, 1, 0, 1, 1)  # row=1, col=0, span=1x1
        layout.addWidget(cart_scroll, 0, 1, 2, 1)  # spans 2 rows in col=1

        # Stretching: make both columns expand properly
        layout.setColumnStretch(0, 7)  # left column
        layout.setColumnStretch(1, 3)  # right column (wider)
        layout.setRowStretch(1, 1)  # allow product list row to expand

    def create_order(self):
        # Create Order
        db = get_db()
        shop_id = os.getenv("SHOP_ID")
        shop_cart_id = os.getenv("SHOP_CART_ID")

        order = db.create_order(shop_id)
        if not order:
            return
        cart_items = db.get_cart_items(shop_cart_id)
        if len(cart_items) == 0:
            return
        for _, cart_item in enumerate(cart_items):
            db.create_order_item(
                order_id=order["id"],
                product_id=cart_item["product_id"],
                quantity=cart_item["quantity"],
                price=cart_item["price"]
            )
        # Remove cart
        db.delete_cart(shop_cart_id)
        self.load_cart()

    def add_to_cart(self, product_id):
        shop_cart_id = os.getenv("SHOP_CART_ID")
        cart_item = get_db().get_cart_item(shop_cart_id, product_id)
        db = get_db()
        if cart_item is None:
            # Create cart item
            db.create_cart_item(shop_cart_id, product_id, quantity=1)
        else:
            # Update quantity
            db.update_cart_item_quantity(cart_item_id=cart_item["id"], quantity=cart_item["quantity"] + 1)
        self.load_cart()

    def load_cart(self):
        while self.cart_layout.count():
            item = self.cart_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        cart_data = get_db().get_cart_items(os.getenv("SHOP_CART_ID"))
        for _, item in enumerate(cart_data):
            self.cart_layout.addWidget(CartItem(
                item["id"],
                item["product_id"],
                item["product_name"],
                item["product_image"],
                item["price"],
                item["quantity"],)
            )

            # Order button
        order_button = QPushButton("Create Order")
        order_button.setStyleSheet("""
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
        order_button.clicked.connect(self.create_order)
        self.cart_layout.addWidget(order_button)

    def load_product(self, label, category_id):
        title_label = QLabel(label)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.container_layout.addWidget(title_label)

        product_layout = QGridLayout()
        self.container_layout.addLayout(product_layout)

        data = get_db().get_products_by_category(category_id)
        item_per_row = 5
        # Example product items
        for i, item in enumerate(data):
            product_layout.addWidget(
                ProductCard(item["id"], item["product_name"], item["product_image"], add_to_cart= self.add_to_cart),
                i / item_per_row,
                i % item_per_row, 1, 1)

        count = len(data)
        if count < item_per_row:
            for j in range(count, item_per_row):
                spacer = QSpacerItem(150, 150, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
                product_layout.addItem(spacer, 0, j)
