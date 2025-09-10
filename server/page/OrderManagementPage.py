from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QToolButton, QScrollArea

from db.db_manager import get_db
from page.widget.BackButton import BackButton
from page.widget.OrderCard import OrderCard


class OrderManagementPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()
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

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        self.load_orders()
        layout.addWidget(self.order_scroll, 1, 0, 1, 1)  # row=0, col=0, span=1x1

    def load_orders(self):
        while self.order_layout.count():
            item = self.order_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        db = get_db()
        orders = db.get_orders()
        for _, order in enumerate(orders):
            self.order_layout.addWidget(OrderCard(order["id"], order["created_at"]))
