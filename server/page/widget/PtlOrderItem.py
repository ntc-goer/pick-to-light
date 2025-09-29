from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame

from db.db_manager import get_db


class PtlOrderItem(QWidget):
    def __init__(self, product_id, product_name, product_image, quantity, db):
        super().__init__()

        self.db = get_db()

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setHorizontalSpacing(15)
        self.layout.setVerticalSpacing(5)

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
        self.layout.addWidget(image_label, 0, 0, 1, 1)

        # --- Column 2: Product name + quantity ---
        product_data_layout = QVBoxLayout()
        product_data_layout.setSpacing(2)

        title_label = QLabel(product_name)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        product_data_layout.addWidget(title_label)

        quantity_label = QLabel(f"Quantity:  {quantity}")
        quantity_label.setStyleSheet("font-size: 12px; color: #333;")
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        product_data_layout.addWidget(quantity_label)

        self.layout.addLayout(product_data_layout, 0, 1, 1, 1)

        # --- Column 3: Light feature
        self.load_light_indicator()

        # Stretch ratios
        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 6)
        self.layout.setColumnStretch(2, 2)

    def load_light_indicator(self):
        # Load all cell have product id
        row_layout = QHBoxLayout()
        circle = self.create_circle(Qt.GlobalColor.yellow)  # yellow circle
        title = QLabel(f"Pick up <b>{2}</b> at <b>{2}</b>")
        title.setTextFormat(Qt.TextFormat.RichText)
        title.setStyleSheet("font-size: 14px; margin-right: 5px;")
        row_layout.addWidget(title)
        row_layout.addWidget(circle)

        self.layout.addLayout(row_layout, 0, 2, 1, 1)

    def create_circle(self, color):
        pixmap = QPixmap(14, 14)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 14, 14)
        painter.end()

        circle = QLabel()
        circle.setPixmap(pixmap)
        return circle

    def on_ptl_btn_clicked(self):
        print("here")

    def on_show_direction_clicked(self):
        print("on_show_direction_clicked")
