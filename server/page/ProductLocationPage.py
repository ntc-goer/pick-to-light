import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea, QLabel, QVBoxLayout, QComboBox, QStackedWidget, \
    QPushButton, QListView, QMessageBox

from db.db_manager import get_db
from page.widget.BackButton import BackButton


class ProductLocationPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()
        self.product_combo_box = None
        self.selected_column = None
        self.selected_row = None
        self.selected_shelve = None
        self.setWindowTitle("Product Location Management")
        self.setGeometry(200, 200, 400, 200)

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

    def update_cell_location(self):
        db = get_db()
        product_id = self.product_combo_box.currentData()
        db.upsert_product_location(product_id, self.selected_shelve, self.selected_row, self.selected_column)
        self.show_message("Cập nhật vị trí thành công")

    def show_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def load_update_cell(self):
        if self.selected_shelve is None:
            return

        while self.l_edit_v_layout.count():
            item = self.l_edit_v_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        title_label = QLabel(f"Update Cell: {self.selected_shelve}-{self.selected_row}{self.selected_column}")
        title_label.setStyleSheet("font-size: 12px; font-weight: bold")
        self.l_edit_v_layout.addWidget(title_label)

        products = get_db().get_products()
        self.product_combo_box = QComboBox()

        list_view = QListView()
        self.product_combo_box.setView(list_view)

        self.product_combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        for _, product in enumerate(products):
            self.product_combo_box.addItem(product["product_name"], product["id"])
        self.l_edit_v_layout.addWidget(self.product_combo_box)

        edit_button = QPushButton("Update Cell Location")
        edit_button.setStyleSheet("""
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
        edit_button.clicked.connect(self.update_cell_location)
        self.l_edit_v_layout.addWidget(edit_button)

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
                location = get_db().get_product_location(
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
