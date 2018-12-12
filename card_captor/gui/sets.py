import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QListWidget 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from mtgsdk import Set

class Sets(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.list = QListWidget(parent)
        self.add_all_sets()
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)

    def add_all_sets(self):
        sets = Set.all()
        for s in sets:
            self.list.addItem(s.name)
