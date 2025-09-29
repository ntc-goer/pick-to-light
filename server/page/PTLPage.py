import os

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QSizePolicy, QFrame
from db.db_manager import get_db
from page.widget.BackButton import BackButton
from page.widget.CameraThread import CameraThread
from page.widget.PtlOrderItem import PtlOrderItem


class PTLPage(QWidget):
    def __init__(self, goto_home_page, arduino):
        super().__init__()
        self.scanner_label = None
        self.db = get_db()
        self.arduino = arduino

        # Layout
        layout = QGridLayout(self)
        self.order_id_input = ""

        back_button = BackButton(goto_home_page, after_func=self.stop_camera)

        self.l_container = QWidget()
        self.l_layout = QVBoxLayout(self.l_container)
        self.l_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.l_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)
        self.load_left_layout()

        self.r_container = QWidget()
        self.r_layout = QVBoxLayout(self.r_container)
        self.r_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.r_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)
        self.load_right_layout()
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.set_image)

        layout.addWidget(back_button, 0, 0, 1, 2)  # row=0, col=0, span=1x1
        layout.addWidget(self.l_container, 1, 0, 1, 1)
        layout.addWidget(self.r_container, 1, 1, 1, 1)

        # Stretching: make both columns expand properly
        layout.setColumnStretch(0, 4)  # left column
        layout.setColumnStretch(1, 8)  # right column (wider)
        layout.setRowStretch(1, 1)

    def on_text_changed(self, text):
        self.order_id_input = text

    def submit_order_id(self):
        self.order_id_input = self.order_id_input.strip()
        self.load_right_layout(reload=True)

    def open_camera(self):
        if not hasattr(self, "camera_thread") or not self.camera_thread.isRunning():
            self.camera_thread = CameraThread()
            self.camera_thread.frame_signal.connect(self.set_image)
            self.camera_thread.start()

    def stop_camera(self):
        print("stop camera thread", self.camera_thread)
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread.wait()
            self.camera_thread.deleteLater()
            self.camera_thread = None

    @pyqtSlot(QImage)
    def set_image(self, image):
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(
            self.scanner_label.width(),
            self.scanner_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.scanner_label.setPixmap(pixmap)

    def load_left_layout(self):
        qr_label = QLabel("Scan QR Code")
        self.scanner_label = QLabel()
        self.scanner_label.setFixedSize(300, 200)
        or_label = QLabel("Or Input Order Id:")
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("9c7227ac-9960-46d9-ba40-1036541b61f3")
        line_edit.textChanged.connect(self.on_text_changed)

        submit_button = QPushButton("Find")
        submit_button.setStyleSheet("""
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
        submit_button.clicked.connect(self.submit_order_id)
        self.l_layout.addWidget(qr_label)
        self.l_layout.addWidget(self.scanner_label)

        # addWidget QR
        self.l_layout.addWidget(or_label)
        self.l_layout.addWidget(line_edit)
        self.l_layout.addWidget(submit_button)

        self.open_camera()

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def on_ptl(self, order_id):
        print("order_id", order_id)

    def on_show_direction(self):
        self.load_map()

    def load_right_layout(self, reload=False):
        if self.order_id_input == "":
            return
        order = self.db.get_order_by_id(self.order_id_input)
        if order is None:
            if reload:
                self.show_message("Order not found")
            return

        order_title_label = QLabel(f"Order #{order['id']}")
        order_title_label.setStyleSheet("font-size: 14px; font-weight: bold")
        self.r_layout.addWidget(order_title_label)

        order_items = self.db.get_order_items_by_order_id(order["id"])
        for item in order_items:
            self.r_layout.addWidget(
                PtlOrderItem(
                    product_id=item["product_id"],
                    product_name=item["product_name"],
                    product_image=item["product_image"],
                    quantity=item["quantity"],
                    db=self.db,
                )
            )

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.r_layout.addWidget(line)

    def make_spacer(self):
        spacer = QLabel("")
        spacer.setStyleSheet("""
            QLabel {
                background-color: lightgray;
                min-width: 30px;
                min-height: 30px;
            }
        """)
        return spacer

    def make_gate(self):
        spacer = QLabel("")
        spacer.setStyleSheet("""
            QLabel {
                background-color: blue;
                min-width: 30px;
                min-height: 30px;
            }
        """)
        return spacer

    def get_shelve_positions(self):
        shelve_positions = os.getenv("SHELVE_POSITIONS").split(",")
        result = []
        for position in shelve_positions:
            split_position = [int(x) for x in position.split(":")]
            result.append(split_position)
        return result

    def calculate_map_size(self, shelve_positions, shelve_size, padding_bottom_right_map):
        rows = [p[0] for p in shelve_positions]
        cols = [p[1] for p in shelve_positions]
        return [max(rows) + shelve_size[0] + padding_bottom_right_map,
                max(cols) + shelve_size[1] + padding_bottom_right_map]

    def load_map(self):
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        shelves = os.getenv("SHELVES").split(",")
        shelve_positions = self.get_shelve_positions()

        cols = os.getenv("SHELVE_COLS").split(",")
        rows = os.getenv("SHELVE_ROWS").split(",")

        db = get_db()
        order_items = db.get_order_items_by_order_id(self.order_id_input)
        product_location = {}
        for _, order_item in enumerate(order_items):
            locations = db.get_product_location_by_product_id(order_item["product_id"])
            if len(locations) == 0:
                continue
            # FIX ME: 1 PRODUCT HAVE MANY LOCATIONS , CHECK STOCK
            product_location[
                f"{locations[0]['shelve']}-{locations[0]['row_location']}-{locations[0]['column_location']}"] = order_item

        padding_map = 3

        shelve_size = [len(rows), len(cols)]
        map_size = self.calculate_map_size(shelve_positions, shelve_size, padding_map)

        # Draw map
        for row in range(map_size[0]):
            for col in range(map_size[1]):
                grid.addWidget(self.make_spacer(), row, col, 1, 1)

        # Draw gate
        gate_position = [int(x) for x in os.getenv("GATE_POSITION").split(":")]
        grid.addWidget(
            self.make_gate(),
            gate_position[0],
            gate_position[1],
            1,
            1
        )
        for shelve_i, shelve in enumerate(shelves):
            shelve_split = shelve.split(" ")
            shelve_name = shelve_split[0][0] + shelve_split[1]
            start_shelve_row = shelve_positions[shelve_i][0]
            start_shelve_col = shelve_positions[shelve_i][1]
            for row_i, row in enumerate(rows):
                for col_i, col in enumerate(cols):
                    btn = QPushButton(f"{shelve_name}-{row}{col}")
                    btn.setFlat(True)
                    btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                    default_style = """
                        QPushButton {
                            border: 1px solid #555;
                            background-color: #f9f9f9;
                            min-width: 80px;
                            min-height: 60px;
                            text-align: center;
                        }
                    """

                    occupied_style = """
                        QPushButton {
                            border: 1px solid #555;
                            background-color: #fff59d;
                            min-width: 80px;
                            min-height: 60px;
                            text-align: center;
                            font-weight: bold;
                        }
                    """
                    if f"{shelve}-{row}-{col}" in product_location:
                        btn.setStyleSheet(occupied_style)
                    else:
                        btn.setStyleSheet(default_style)

                    grid.addWidget(
                        btn,
                        start_shelve_row + row_i,
                        start_shelve_col + col_i,
                        1,
                        1
                    )

        self.r_layout.addWidget(grid_container)
