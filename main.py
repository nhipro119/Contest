# main_window.py
import sys
from widget import mainView
from PyQt6.QtWidgets import QApplication
"""Main window-style application."""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainView.Main()
    window.show()
    sys.exit(app.exec())
    