
import sys
from widget import mainView
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os

"""Main window-style application."""



if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Round)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(),"icon\icon.jpg")))
    # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    window = mainView.Main()
    window.setWindowTitle('CT Scan');
    window.show()
    sys.exit(app.exec())
    