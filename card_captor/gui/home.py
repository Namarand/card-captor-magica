from tempfile import mkdtemp
import cv2
import sys

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QHBoxLayout, QLabel

from output_handler import Output
from trie import Trie
from loop import process_frame

class Home(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self._create_layout()

    def _create_layout(self):
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self._create_camera())
        self.layout.addWidget(self._create_cards_list())
        self.setLayout(self.layout)

    def _create_camera(self):
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = CameraThread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        return self.label

    def _create_cards_list(self):
        return QPushButton()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        database = Trie()
        folder = mkdtemp()
        output = Output()
        while True:
            ret, frame = cap.read()
            if ret:
                frame = process_frame(frame, database, folder, output)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
