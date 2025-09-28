import serial
from PyQt6.QtCore import QThread, pyqtSignal


class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, arduino = None):
        super().__init__()
        self.ser = arduino
        self._running = True

    def run(self):
        while self._running:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode(errors="ignore").strip()
                if line:
                    self.data_received.emit(line)

    def stop(self):
        self._running = False
        if self.ser.is_open:
            self.ser.close()