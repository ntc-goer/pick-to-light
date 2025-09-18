import sys

from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

from db.db_manager import init_db
from page.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_dotenv()
    init_db()

    window = MainWindow()

    # window.showFullScreen()
    window.setFixedSize(900, 600)
    window.show()

    sys.exit(app.exec())