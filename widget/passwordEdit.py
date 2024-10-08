# from PyQt6.QtWidgets import QLineEdit
# class PasswordEdit(QLineEdit):
#     """
#     A LineEdit with icons to show/hide password entries
#     """
#     CSS = '''QLineEdit {
#         border-radius: 0px;
#         height: 30px;
#         margin: 0px 0px 0px 0px;
#     }
#     '''

#     def __init__(self, parent):
#         self.parent = parent
#         super().__init__(self.parent)

#         # Set styles
#         self.setStyleSheet(self.CSS)

#         self.visibleIcon = load_icon("eye_visible.svg")
#         self.hiddenIcon = load_icon("eye_hidden.svg")

#         self.setEchoMode(QLineEdit.Password)
#         self.togglepasswordAction = self.addAction(self.visibleIcon, QLineEdit.TrailingPosition)
#         self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
#         self.password_shown = False

#     def on_toggle_password_Action(self):
#         if not self.password_shown:
#             self.setEchoMode(QLineEdit.Normal)
#             self.password_shown = True
#             self.togglepasswordAction.setIcon(self.hiddenIcon)
#         else:
#             self.setEchoMode(QLineEdit.Password)
#             self.password_shown = False
#             self.togglepasswordAction.setIcon(self.visibleIcon)