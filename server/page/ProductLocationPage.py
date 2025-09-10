import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea, QLabel, QVBoxLayout, QComboBox, QStackedWidget

from page.widget.BackButton import BackButton


class ProductLocationPage(QWidget):
    def __init__(self, goto_home_page):
        super().__init__()
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
        combo_box.currentIndexChanged.connect(self.changeShelveIndex)

        v_layout.addWidget(self.page_scroll)

        layout.addWidget(back_button, 0, 0, 1, 1)  # row=0, col=0, span=1x1
        layout.addWidget(v_container, 1, 0, 1, 1)  # row=0, col=0, span=1x1

    def changeShelveIndex(self, index):
        self.page_stack.setCurrentIndex(index)

    def load_shelve(self, shelve):
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(5)

        cols = os.getenv("SHELVE_COLS").split(",")
        rows = os.getenv("SHELVE_ROWS").split(",")

        for ir, r in enumerate(rows):
            for ic, c in enumerate(cols):
                cell = QLabel(f"{shelve}-{r}{str(c)}")
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setStyleSheet("""
                    QLabel {
                        border: 1px solid #555;
                        background-color: #f9f9f9;
                        min-width: 80px;
                        min-height: 60px;
                    }
                    QLabel:hover {
                        background-color: #d0ebff;  /* màu khi hover */
                    }
                """)
                cell.setCursor(Qt.CursorShape.PointingHandCursor)
                grid.addWidget(cell, ir, ic)
        return grid_container

