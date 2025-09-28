import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea, QLabel, QVBoxLayout, QComboBox, QStackedWidget, \
    QPushButton, QListView, QMessageBox, QLineEdit, QRadioButton, QButtonGroup

from db.db_manager import get_db
from page.widget.BackButton import BackButton


class ProductLocationPage(QWidget):
    def __init__(self, goto_home_page, arduino = None):
        super().__init__()
        self.check_all_mode = False
        self.test_radio_2 = None
        self.test_radio_1 = None
        self.test_radio_3 = None
        self.test_radio_group = None
        self.test_quantity_text = None
        self.product_combo_box = None
        self.selected_column = None
        self.selected_row = None
        self.selected_shelve = None
        self.setWindowTitle("Product Location Management")
        self.setGeometry(200, 200, 400, 200)
        self.cell_module_text = ""
        self.db = get_db()
        self.arduino = arduino

        # Layout
        layout = QGridLayout(self)

        # Back button (row 0, col 0)
        back_button = BackButton(goto_home_page)

        v_container = QWidget()
        v_layout = QVBoxLayout(v_container)

        shelves = os.getenv("SHELVES").split(",")
        combo_box = QComboBox()
        for shelve in shelves:
            combo_box.addItem(shelve)
        combo_box.setFixedWidth(150)

        v_layout.addWidget(combo_box)

        # Location View
        self.page_scroll = QScrollArea()
        self.page_scroll.setWidgetResizable(True)
        self.page_stack = QStackedWidget()
        self.page_scroll.setWidget(self.page_stack)

        for shelve in shelves:
            self.page_stack.addWidget(self.load_shelve(shelve))

        self.page_stack.setCurrentIndex(0)
        combo_box.currentIndexChanged.connect(self.change_shelve_index)

        v_layout.addWidget(self.page_scroll)

        self.l_edit_container = QWidget()
        self.l_edit_v_layout = QVBoxLayout(self.l_edit_container)
        self.l_edit_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.l_edit_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)
        self.load_update_cell()

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(v_container, 1, 0, 1, 1)  # row=1, col=0, span=1x1
        layout.addWidget(self.l_edit_container, 1, 1, 1, 1)  # row=1, col=0, span=1x1

        # Stretching: make both columns expand properly
        layout.setColumnStretch(0, 8)  # left column
        layout.setColumnStretch(1, 2)  # right column (wider)
        layout.setRowStretch(1, 1)  # allow product list row to expand
    
    def on_test_quantity_text_changed(self, text):
        self.test_quantity_text = text
        
    def update_cell_location(self):
        product_id = self.product_combo_box.currentData()
        self.db.upsert_product_location(product_id, self.selected_shelve, self.selected_row, self.selected_column, self.cell_module_text)
        self.show_message("Update successfully")

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def on_module_text_changed(self, text):
        self.cell_module_text = text

    def load_update_cell(self):
        if self.selected_shelve is None:
            return

        while self.l_edit_v_layout.count():
            item = self.l_edit_v_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        test_check_all_button = QPushButton("Test All ON/OFF")
        test_check_all_button.setStyleSheet("""
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
        test_check_all_button.clicked.connect(self.test_check_all)
        self.l_edit_v_layout.addWidget(test_check_all_button)

        title_label = QLabel(f"Update Cell: {self.selected_shelve}-{self.selected_row}{self.selected_column}")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold")
        self.l_edit_v_layout.addWidget(title_label)

        location = self.db.get_product_location(self.selected_shelve, self.selected_row, self.selected_column)

        products = self.db.get_products()
        self.product_combo_box = QComboBox()

        list_view = QListView()
        self.product_combo_box.setView(list_view)

        self.product_combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        select_product_label = QLabel(f"Select product:")
        select_product_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.l_edit_v_layout.addWidget(select_product_label)

        for _, product in enumerate(products):
            self.product_combo_box.addItem(product["product_name"], product["id"])

        self.l_edit_v_layout.addWidget(self.product_combo_box)

        input_module_label = QLabel(f"Input module Id:")
        input_module_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.l_edit_v_layout.addWidget(input_module_label)

        input_module_edit = QLineEdit()
        input_module_edit.setPlaceholderText("MD112")
        input_module_edit.textChanged.connect(self.on_module_text_changed)
        self.l_edit_v_layout.addWidget(input_module_edit)

        if location is not None:
            self.cell_module_text = location["module_id"]
            input_module_edit.setText(self.cell_module_text)

            index = self.product_combo_box.findData(location["product_id"])
            if index != -1:
                self.product_combo_box.setCurrentIndex(index)

        edit_button = QPushButton("Update Cell Location")
        edit_button.setStyleSheet("""
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
        edit_button.clicked.connect(self.update_cell_location)
        self.l_edit_v_layout.addWidget(edit_button)

        or_label = QLabel("Or")
        or_label.setStyleSheet("font-size: 12px; font-weight: bold; text-align: center;")
        self.l_edit_v_layout.addWidget(or_label)

        test_quantity_label = QLabel(f"Quantity:")
        test_quantity_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.l_edit_v_layout.addWidget(test_quantity_label)

        test_quantity_edit = QLineEdit()
        test_quantity_edit.setPlaceholderText("3")
        test_quantity_edit.textChanged.connect(self.on_test_quantity_text_changed)
        self.l_edit_v_layout.addWidget(test_quantity_edit)

        test_mode_label = QLabel(f"Mode:")
        test_mode_label.setStyleSheet("font-size: 12px; margin-top: 10px;")
        self.l_edit_v_layout.addWidget(test_mode_label)

        self.test_radio_1 = QRadioButton("Off")
        self.test_radio_2 = QRadioButton("On")
        self.test_radio_3 = QRadioButton("Blink")

        # nhóm chúng lại -> chỉ chọn được 1
        self.test_radio_group = QButtonGroup(self)
        self.test_radio_group.addButton(self.test_radio_1)
        self.test_radio_group.addButton(self.test_radio_2)
        self.test_radio_group.addButton(self.test_radio_3)

        self.l_edit_v_layout.addWidget(self.test_radio_1)
        self.l_edit_v_layout.addWidget(self.test_radio_2)
        self.l_edit_v_layout.addWidget(self.test_radio_3)

        test_button = QPushButton("Test Light")
        test_button.setStyleSheet("""
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
        test_button.clicked.connect(self.test_light)
        self.l_edit_v_layout.addWidget(test_button)

    def test_check_all(self ):
        self.check_all_mode = not self.check_all_mode
        if self.check_all_mode:
            text = "CheckAll"
        else:
            text = "OffAll"
        self.arduino.write((text + "\n").encode())

    def test_light(self):
        # text = "A002B|4|1"
        text = f"{self.cell_module_text}|{self.test_quantity_text}|{self.get_test_mode()}"
        print(text)
        self.arduino.write((text + "\n").encode())

    def get_test_mode(self):
        if self.test_radio_1.isChecked():
            return 0
        elif self.test_radio_2.isChecked():
            return 1
        elif self.test_radio_3.isChecked():
            return 2
        else:
            return -1

    def change_shelve_index(self, index):
        self.page_stack.setCurrentIndex(index)

    def on_click_cell(self, shelve, row, column):
        self.selected_shelve = shelve
        self.selected_row = row
        self.selected_column = column
        self.load_update_cell()

    def load_shelve(self, shelve):
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(5)

        cols = os.getenv("SHELVE_COLS").split(",")
        rows = os.getenv("SHELVE_ROWS").split(",")

        for ir, r in enumerate(rows):
            for ic, c in enumerate(cols):
                cell = QPushButton(f"{shelve}-{r}{str(c)}")
                cell.setFlat(True)
                cell.setStyleSheet("QPushButton { text-align: center; }")
                # Check Have Product
                location = self.db.get_product_location(
                    shelve,
                    r,
                    c
                )
                default_style = """
                    QPushButton {
                        border: 1px solid #555;
                        background-color: #f9f9f9;
                        min-width: 80px;
                        min-height: 60px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background-color: #d0ebff;
                    }
                    QPushButton:pressed {
                        background-color: #90caf9;
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
                    QPushButton:hover {
                        background-color: #ffe082;
                    }
                    QPushButton:pressed {
                        background-color: #ffca28;
                    }
                """

                if location is not None:
                    cell.setStyleSheet(occupied_style)
                else:
                    cell.setStyleSheet(default_style)

                cell.setCursor(Qt.CursorShape.PointingHandCursor)
                cell.clicked.connect(lambda isChecked=False, ts=shelve, tr=r, tc=c: self.on_click_cell(ts, tr, tc))
                grid.addWidget(cell, ir, ic)
        return grid_container
