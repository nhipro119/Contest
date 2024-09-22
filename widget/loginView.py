from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout,QFormLayout, QPushButton,QLayout, QApplication, QGridLayout
import urllib3
import json
import sys
# from widget import registerView
class loginWidget(QWidget):
    def __init__(self, parent=None, size=[1420,1000]):
        super(loginWidget,self).__init__(parent=parent)
        self.setFixedSize(*size)
        self.total_layout = QVBoxLayout()
        self.setLayout(self.total_layout)
        self.create_login_layout(self.total_layout)
        self.create_login_button(self.total_layout)
    def create_login_layout(self, parent:QLayout):
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
        # loWidget.setFixedSize(400,400)
        loLayout = QGridLayout()
        loginbt = QPushButton(text="Login")
        loginbt.clicked.connect(self.login)
        loLayout.addWidget(loginbt,0,0,1,1)

        register_bt = QPushButton(text="Register")
        register_bt.setGeometry(300,0,200,50)
        register_bt.clicked.connect(self.register_bt_event)
        loLayout.addWidget(register_bt,0,1,1,1)

        self.loginLb = QLabel("oke")
        loLayout.addWidget(self.loginLb,1,0,1,2)

        loWidget.setLayout(loLayout)

        parent.addWidget(loWidget)

    def register_bt_event(self):
        self.hide()
        self.parent().parent().create_register()

    
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
        res = http.request("POST","103.63.121.200:9011/login", body=json.dumps(param),headers={'Content-Type': 'application/json'})
        if res.status != 200:
            self.loginLb.setText("username or password is not correct")
        else:

            info_data = res.data.decode("ascii")
            
            self.parent().parent().set_account(info_data)
            self.close()


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loginWidget()
    window.show()
    sys.exit(app.exec())
