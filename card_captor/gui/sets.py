import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QListWidget, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from mtgsdk import Set

class Sets(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self._create_layout()

    def _create_layout(self):
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self._create_activated_list())
        self.layout.addLayout(self._create_middle_interface())
        self.layout.addWidget(self._create_other_list())
        self.setLayout(self.layout)

    def _create_activated_list(self):
        list_w = QListWidget(self)
        list_w.setSortingEnabled(True)
        self.activated = list_w
        return list_w

    def _create_other_list(self):
        list_w = QListWidget(self)
        list_w.setSortingEnabled(True)
        sets = Set.all()
        for s in sets:
            list_w.addItem(s.name)
        self.unactivated = list_w
        return list_w

    def _create_middle_interface(self):
        list_w = QVBoxLayout(self)
        b0 = QPushButton('<')
        b0.clicked.connect(self._add_to_activated)
        list_w.addWidget(b0)
        b1 = QPushButton('>')
        b1.clicked.connect(self._remove_from_activated)
        list_w.addWidget(b1)
        b2 = QPushButton('<<')
        b2.clicked.connect(self._clear_unactivated)
        list_w.addWidget(b2)
        b3 = QPushButton('>>')
        b3.clicked.connect(self._clear_activated)
        list_w.addWidget(b3)
        list_w.addWidget(QPushButton('Update database'))
        return list_w

    def _add_to_activated(self):
        value = self.unactivated.takeItem(self.unactivated.currentRow())
        self.activated.addItem(value)

    def _remove_from_activated(self):
        value = self.activated.takeItem(self.activated.currentRow())
        self.unactivated.addItem(value)

    def _clear_unactivated(self):
        while self.unactivated.count() > 0:
            item = self.unactivated.takeItem(0)
            self.activated.addItem(item)
        
    def _clear_activated(self):
        while self.activated.count() > 0:
            item = self.activated.takeItem(0)
            self.unactivated.addItem(item)
