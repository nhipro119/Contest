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
        self.create_login_layout()
        self.create_login_button(self.total_layout)
    def create_login_layout(self):
        welcome_lb = QLabel(self)
        welcome_lb.setGeometry(460,197,700,45)
        welcome_lb.setText("WELCOME BACK!")
        welcome_lb.setStyleSheet("font-family: Lexend;\
                                font-size: 45px;\
                                font-weight: 700;\
                                line-height: 56.25px;\
                                text-align: left;\
                                ")
        self.usernameLe = QLineEdit(self)
        self.usernameLe.setStyleSheet("background-color:#D9D9D9; border: 1px solid; border-color:black;border-radius: 30px;")
        self.usernameLe.setGeometry(460,352,520,62)

        self.usernameLe.setPlaceholderText("Username")



        self.passwordLe = QLineEdit(self)
        self.passwordLe.setPlaceholderText("Password")
        self.passwordLe.setStyleSheet("background-color:#D9D9D9; border: 1px solid; border-color:black;border-radius: 30px;")
        self.passwordLe.setGeometry(460,438,520,62)

    
    def create_login_button(self, parent:QLayout):
        loWidget = QWidget()
        # loWidget.setFixedSize(400,400)
        loLayout = QGridLayout()
        loginbt = QPushButton("Login",self)
        loginbt.setGeometry(570,634,300,62)
        loginbt.setStyleSheet("background-color: #48CFCB; border: 1px solid; border-color:black;border-radius: 30px;")
        loginbt.clicked.connect(self.login)
        # loLayout.addWidget(loginbt,0,0,1,1)

        register_bt = QPushButton("Register your account",self)
        register_bt.setGeometry(460,263,300,41)
        register_bt.setStyleSheet("font-family: Lexend;\
                                    font-size: 20px;\
                                    font-weight: 700;\
                                    line-height: 25px;\
                                    text-align: left;\
                                    border: none;\
                                    ")
        register_bt.clicked.connect(self.register_bt_event)
        loLayout.addWidget(register_bt,0,1,1,1)

        self.loginLb = QLabel("oke")
        loLayout.addWidget(self.loginLb,1,0,1,2)

        # loWidget.setLayout(loLayout)

        # parent.addWidget(loWidget)

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
