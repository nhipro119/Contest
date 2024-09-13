# main_window.py

"""Main window-style application."""

import sys
from screeninfo import get_monitors

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget
)

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        # self.setCentralWidget(QLabel("I'm the Central Widget"))
        mornitor = get_monitors()[0]
        height = mornitor.height
        width = mornitor.width
        self.setMinimumSize(width,height)
        self.showMaximized()
        self.create_main_layout()
        # self._createMenu()
        # self._createToolBar()
        # self._createStatusBar()
        print(self.frameGeometry().size())



    def create_main_layout(self):
        self.total_widget = QWidget(self)
        print(self.total_widget.frameGeometry().size())
        self.total_layout =  QHBoxLayout(self.total_widget)
        self.bt = QPushButton("okela",self.total_widget)
        print(self.bt.frameGeometry().size())
        self.total_layout.addChildWidget(self.bt)
        self.total_widget.setLayout(self.total_layout)
        self.setCentralWidget(self.total_widget)



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

