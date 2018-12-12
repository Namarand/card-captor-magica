import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from home import Home
from cards import Cards
from sets import Sets

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Card Captor'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = Window(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class Window(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = Home(self)
        self.tab2 = Cards(self)
        self.tab3 = Sets(self)
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Home")
        self.tabs.addTab(self.tab2,"Cards")
        self.tabs.addTab(self.tab3,"Sets")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.layout = QVBoxLayout(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
