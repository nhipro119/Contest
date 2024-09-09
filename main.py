# main_window.py

"""Main window-style application."""

import sys

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
        self.showMaximized()
        self.create_main_layout()
        # self._createMenu()
        # self._createToolBar()
        # self._createStatusBar()



    def create_main_layout(self):
        self.total_widget = QWidget(self)
        
        self.total_layout =  QHBoxLayout(self.total_widget)
        self.bt = QPushButton("okela",self.total_widget)
        self.total_layout.addChildWidget(self.bt)
        self.total_widget.setLayout(self.total_layout)
        self.setCentralWidget(self.total_widget)



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())