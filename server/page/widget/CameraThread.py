import time

import cv2
import imutils
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage


class CameraThread(QThread):
    frame_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.running = False
        self.cap = None

    def run(self):
        print("Start capture", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        self.running = True
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.cap.isOpened() and self.running:
            _, frame = self.cap.read()
            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)
        # cleanup when loop exits
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        print("Camera released", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image,
                       image.shape[1],
                       image.shape[0],
                       QImage.Format.Format_RGB888)
        return image

    def stop(self):
        self.running = False
        self.wait()  # block until thread fully exits
        time.sleep(0.2)
