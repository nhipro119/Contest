from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout,QFormLayout, QPushButton,QLayout
import urllib3
import json
class loginWidget(QWidget):
    def __init__(self, parent=None):
        super(loginWidget,self).__init__(parent=parent)
        self.total_layout = QVBoxLayout()
    def create_login_layout(self, parent):
        paramWiget = QWidget()
        paramLayout = QFormLayout()
        username = QLabel("Username")
        self.usernameLe = QLineEdit()
        paramLayout.addRow(username,self.usernameLe)

        pwLb = QLabel("Password")
        self.passwordLe = QLineEdit()
        paramLayout.addRow(pwLb, self.passwordLe)
        paramWiget.setLayout(paramLayout)
        parent.addWidget(paramWiget)
    
    def create_login_button(self, parent:QLayout):
        loWidget = QWidget()
        loLayout = QVBoxLayout()
        loginbt = QPushButton(text="Login")
        loLayout.addWidget(loginbt)

        self.loginLb = QLabel()
        loLayout.addWidget(self.loginLb)

        loWidget.setLayout(loLayout)

        parent.addWidget(loWidget)
    
    def check_empty(self, text: str):
        if text.strip() == "":
            return False
        return True
    def login(self):
        if  not (self.check_empty(self.usernameLe.text()) and self.check_empty(self.passwordLe.text())):
            self.loginLb.setText("username or password is empty")
        param = {"username":self.usernameLe.text(),
                 "password":self.passwordLe.text()}
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/login", body=json.dumps(param))
        if res.status != 200:
            self.loginLb.setText("username or password is not correct")
        else:

            token = res.data.decode("ascii")[1]
            with open("data/account.txt", "w") as f:
                f.write(token)


        

