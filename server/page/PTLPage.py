import os

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QSizePolicy, QFrame, QHBoxLayout, QScrollArea

from constants import LIGHT_MODE
from db.db_manager import get_db
from helper.arduino import send_cell_signal
from page.widget.BackButton import BackButton
from page.widget.CameraThread import CameraThread
from page.widget.PtlOrderItem import PtlOrderItem
from page.widget.SerialReaderThread import SerialReaderThread


class PTLPage(QWidget):
    def __init__(self, goto_home_page, arduino):
        super().__init__()
        self.scanner_label = None
        self.db = get_db()
        self.arduino = arduino
        self.reader = SerialReaderThread(arduino=self.arduino)
        self.arduino_start_listening()
        self.order_item_light_state = {}
        self.order_item_cell_state = {}

        # Layout
        layout = QGridLayout(self)
        self.order_id_input = "7a697555-e11e-4b26-b355-6672f0f843e2"

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
        self.r_scroll = QScrollArea()
        self.r_scroll.setWidgetResizable(True)
        self.r_scroll.setWidget(self.r_container)

        self.load_right_layout()
        self.camera_thread = CameraThread()
        self.camera_thread.qr_signal.connect(self.on_qr_detect)
        self.camera_thread.frame_signal.connect(self.set_image)

        layout.addWidget(back_button, 0, 0, 1, 2)  # row=0, col=0, span=1x1
        layout.addWidget(self.l_container, 1, 0, 1, 1)
        layout.addWidget(self.r_scroll, 1, 1, 1, 1)

        # Stretching: make both columns expand properly
        layout.setColumnStretch(0, 4)  # left column
        layout.setColumnStretch(1, 8)  # right column (wider)
        layout.setRowStretch(1, 1)

    def arduino_start_listening(self):
        if self.reader is not None:
            self.reader.data_received.connect(self.arduino_received)
            self.reader.start()

    def arduino_stop_listening(self):
        if self.reader:
            self.reader.stop()
            self.reader.wait()
            self.reader = None

    def arduino_received(self, text):
        data = text.split("|")
        if len(data) < 2 or data[0] == "" or data[1] != "Done":
            return
        module_id = data[0]
        send_cell_signal(self.arduino, module_id, quantity=0, mode=LIGHT_MODE['OFF'])

    def send_light_signal(self, locations, quantity):
        send_cell_signal(self.arduino, locations[0]["module_id"], quantity=quantity, mode=LIGHT_MODE['ON'])

    @pyqtSlot(str)
    def on_qr_detect(self, data):
        self.order_id_input = data
        print("data", data)
        if self.order_id_input is None or self.order_id_input == "":
            return None
        self.order_id_input = self.order_id_input.strip()
        self.load_right_layout(reload=True)
        return None

    def on_text_changed(self, text):
        self.order_id_input = text

    def submit_order_id(self):
        if self.order_id_input is None or self.order_id_input == "":
            return self.show_message("Please enter order id")
        self.order_id_input = self.order_id_input.strip()
        self.load_right_layout(reload=True)
        return None

    def open_camera(self):
        if not hasattr(self, "camera_thread") or not self.camera_thread.isRunning():
            self.camera_thread = CameraThread()
            self.camera_thread.qr_signal.connect(self.on_qr_detect)
            self.camera_thread.frame_signal.connect(self.set_image)
            self.camera_thread.start()

    def stop_camera(self):
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

        while self.r_layout.count():
            item = self.r_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        order_title_container = QWidget()
        order_title_layout = QHBoxLayout(order_title_container)

        order_title_label = QLabel(f"Order #{order['id']}")
        order_title_label.setStyleSheet("font-size: 14px; font-weight: bold")

        ptl_btn = QPushButton("PTL")
        ptl_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border-radius: 5px;
                width: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ptl_btn.clicked.connect(self.ptl_function)

        order_title_layout.addWidget(order_title_label)
        order_title_layout.addWidget(ptl_btn)

        self.r_layout.addWidget(order_title_container)

        order_items = self.db.get_order_items_by_order_id(order["id"])
        locations_arr = []
        for item in order_items:
            locations = self.db.get_product_location_by_product_id(item["product_id"])
            # Fix me
            location = locations[0] if locations else None
            if item["id"] not in self.order_item_light_state:
                self.order_item_light_state[item["id"]] = False
            if item["id"] not in self.order_item_cell_state:
                self.order_item_cell_state[item["id"]] = [
                    {
                        "module_id": location["module_id"],
                        "shelve": location["shelve"],
                        "row_location": location["row_location"],
                        "column_location": location["column_location"],
                        "quantity": item["quantity"],
                    }
                ]
            locations_arr.append(f"{location['shelve']}-{location['row_location']}:{location['column_location']}")
            self.r_layout.addWidget(
                PtlOrderItem(
                    product_id=item["product_id"],
                    product_name=item["product_name"],
                    product_image=item["product_image"],
                    quantity=item["quantity"],
                    db=self.db,
                    locations=locations,
                    off_light_manual=self.off_light_manual,
                    is_lighting=self.order_item_light_state[item["id"]]
                )
            )

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.r_layout.addWidget(line)

        # Draw map start
        warehouse_grid = os.getenv("WAREHOUSE_GRID").split(":")
        shelve_cols = os.getenv("SHELVE_COLS").split(",")
        shelve_rows = os.getenv("SHELVE_ROWS").split(",")

        map_container = QWidget()
        map_layout = QGridLayout(map_container)
        map_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        map_layout.setSpacing(0)
        map_layout.setContentsMargins(0, 0, 0, 0)
        map_layout.setHorizontalSpacing(0)
        map_layout.setVerticalSpacing(0)

        shelve_pos = os.getenv("SHELVE_POSITIONS").split("|")
        shelve_places = []
        for pos_i, pos in enumerate(shelve_pos):
            pos_arr = pos.split("-")
            start_post = pos_arr[0].split(":")
            shelve_dir = pos_arr[1]
            if shelve_dir == "Horizontal":
                # Horizontal 0:0 -> 0:3
                shelve_place = [f"Shelve {pos_i + 1}-{start_post[0]}:{int(start_post[1]) + i}-Horizontal" for i in
                                range(len(shelve_cols))]
                shelve_places.extend(shelve_place)
            elif shelve_dir == "Vertical":
                # Vertical 5:0 -> 2:0
                shelve_place = [f"Shelve {pos_i + 1}-{int(start_post[0]) - i}:{start_post[1]}-Vertical" for i in
                                range(len(shelve_cols))]
                shelve_places.extend(shelve_place)

        gate_pos = os.getenv("GATE_POSITION")
        shelves = os.getenv("SHELVES").split(",")
        h_col_tmp = 1
        v_col_tmp = len(shelve_cols)
        for ri in range(int(warehouse_grid[0])):
            for ci in range(int(warehouse_grid[1])):
                is_in_shelve = False
                for shelve in shelves:
                    shelve_hor = f"{shelve}-{ri}:{ci}-Horizontal"
                    shelve_ver = f"{shelve}-{ri}:{ci}-Vertical"
                    if shelve_hor in shelve_places:
                        is_in_shelve = True
                        cell = QWidget()
                        cell_layout = QVBoxLayout(cell)
                        cell_layout.setContentsMargins(0, 0, 0, 0)
                        cell_layout.setSpacing(0)

                        for i, shelve_row in enumerate(shelve_rows):
                            lb = QLabel(f"{shelve_row}{h_col_tmp}")
                            lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            cell_label = f"{shelve}-{shelve_row}:{h_col_tmp}"
                            if cell_label in locations_arr and self.is_lighting_cell(shelve, shelve_row, h_col_tmp):
                                lb.setStyleSheet("background-color: yellow; border: 1px solid black;")
                            else:
                                lb.setStyleSheet("background-color: white; border: 1px solid black;")
                            cell_layout.setStretch(i, 1)
                            cell_layout.addWidget(lb)
                        h_col_tmp += 1
                        cell.setFixedSize(50, 50)
                        map_layout.addWidget(cell, ri, ci)
                    elif shelve_ver in shelve_places:
                        is_in_shelve = True
                        cell = QWidget()
                        cell_layout = QHBoxLayout(cell)
                        cell_layout.setContentsMargins(0, 0, 0, 0)
                        cell_layout.setSpacing(0)

                        for i, shelve_row in enumerate(shelve_rows):
                            lb = QLabel(f"{shelve_row}{v_col_tmp}")
                            lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            cell_label = f"{shelve}-{shelve_row}:{v_col_tmp}"
                            if cell_label in locations_arr and self.is_lighting_cell(shelve, shelve_row, v_col_tmp):
                                lb.setStyleSheet("background-color: yellow; border: 1px solid black;")
                            else:
                                lb.setStyleSheet("background-color: white; border: 1px solid black;")
                            cell_layout.setStretch(i, 1)
                            cell_layout.addWidget(lb)
                        v_col_tmp -= 1

                        cell.setFixedSize(50, 50)
                        map_layout.addWidget(cell, ri, ci)
                if is_in_shelve:
                    continue
                if f"{ri}:{ci}" == gate_pos:
                    cell = QWidget()
                    cell.setStyleSheet("background-color: #89CFF0;")
                    cell.setFixedSize(50, 50)
                    map_layout.addWidget(cell, ri, ci)
                else:
                    cell = QWidget()
                    cell.setStyleSheet("background-color: #D3D3D3;")
                    cell.setFixedSize(50, 50)
                    map_layout.addWidget(cell, ri, ci)

        self.r_layout.addWidget(map_container)
        # Draw map end

    def is_lighting_cell(self, shelve, row , col):
        keys = self.order_item_light_state.keys()
        is_light = False
        for key in keys:
            if self.order_item_cell_state[key][0]["shelve"] == shelve and self.order_item_cell_state[key][0]["row_location"] == row and self.order_item_cell_state[key][0]["column_location"] == col:
                is_light = self.order_item_light_state[key]
        return is_light


    def off_light_manual(self, location):
        keys = self.order_item_light_state.keys()
        for key in keys:
            if self.order_item_cell_state[key][0]["shelve"] == location["shelve"] and self.order_item_cell_state[key][0][
                "row_location"] == location["row_location"] and self.order_item_cell_state[key][0]["column_location"] == location["column_location"]:
                self.order_item_light_state[key] = False
                send_cell_signal(arduino=self.arduino, module= location["module_id"], quantity= 0, mode=LIGHT_MODE["OFF"])
        self.load_right_layout()

    def ptl_function(self):
        order_item_ids = self.order_item_light_state.keys()
        for order_item_id in order_item_ids:
            self.order_item_light_state[order_item_id] = True
            send_cell_signal(
                self.arduino,
                self.order_item_cell_state[order_item_id][0]["module_id"],
                self.order_item_cell_state[order_item_id][0]["quantity"],
                LIGHT_MODE["ON"]
            )
        self.load_right_layout()


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
