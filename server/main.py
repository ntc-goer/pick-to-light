import sys

from PyQt6.QtWidgets import QApplication
from page.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.showFullScreen()

    sys.exit(app.exec())
