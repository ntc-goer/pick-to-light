from pyzbar import pyzbar
import time

import cv2
import imutils
import winsound
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage


class CameraThread(QThread):
    frame_signal = pyqtSignal(QImage)
    qr_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._running = False
        self.detector = cv2.QRCodeDetector()
        self.cap = None
        self.last_data = None
        self.last_time = 0
        self.cooldown = 2

    def run(self):
        # Set running flag
        self._running = True

        # Initialize capture *inside* the thread
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not (self.cap and self.cap.isOpened()):
            # Clear flag if camera failed to open
            self._running = False
            # Exit the run method early
            return

        while self._running:
            ret, frame = self.cap.read()

            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                data = barcode.data.decode("utf-8")

                now = time.time()
                if data != self.last_data or (now - self.last_time) > self.cooldown:
                    self.last_data = data
                    self.last_time = now
                    print("data", data)
                    self.qr_signal.emit(data)

                    winsound.Beep(1000, 1000)

            # Check the running flag again right after read() returns
            if not self._running or not ret:
                break

            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)

            # Add a small delay to yield control and allow the stop() call to be processed
            time.sleep(0.01)

        # cleanup
        if self.cap:
            self.cap.release()
            self.cap = None

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return QImage(
            image,
            image.shape[1],
            image.shape[0],
            QImage.Format.Format_RGB888,
        )

    def stop(self):
        # 1. Clear the running flag (essential for a clean exit)
        self._running = False

        # 2. Force the blocking 'cap.read()' call to return
        #    by releasing the camera resource.
        if self.cap and self.cap.isOpened():
            self.cap.release()

        # NOTE: You don't need to explicitly call self.quit() or self.wait()
        # inside the thread class itself; that's done by the caller (main application).
