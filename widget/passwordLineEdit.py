from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QIcon, QAction
import os
class PasswordLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__()
        root = os.getcwd()
        self.showIcon = QIcon(os.path.join(root,"icon","eye_visible.svg"))
        self.hideIcon = QIcon(os.path.join(root,"icon","eye_hidden.svg"))

        self.showPassAction = QAction(self.showIcon, "Show Password", self)
        self.addAction(self.showPassAction, self.TrailingPosition)
        self.showPassAction.setCheckable(True)
        self.showPassAction.toggled.connect(self.togglePasswordVisibility)
    def togglePasswordVisibility(self, show):
        if show:
            self.setEchoMode(QLineEdit.Normal)
            self.showPassAction.setIcon(self.hideIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.showPassAction.setIcon(self.showIcon)