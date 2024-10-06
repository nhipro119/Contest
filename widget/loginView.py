from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout,QFormLayout, QPushButton,QLayout, QApplication, QGridLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QWindow
import urllib3
import json
import sys
import os
# from widget import registerView
class loginWidget(QWidget):
    def __init__(self, parent=None, size=[1420,1000]):
        super(loginWidget,self).__init__(parent=parent)

        self.setGeometry(0,0,1920,1080)
        # .format(
        
        self.setAutoFillBackground(True)
        bglb = QLabel(self)
        bglb.setFixedSize(1920,1080)
        bglb.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon/Login.jpg")))
        # style = "QWidget{background-image: url({})}"
        # self.setStyleSheet(style)
        

        self.create_login_layout()
        self.create_login_button()
    def create_login_layout(self):
        
        welcome_lb = QLabel(self)
        welcome_lb.move(614,146)
        welcome_lb.setText("Xin chào")
        welcome_lb.setStyleSheet("font-family: Lexend;\
                                font-size: 96px;\
                                font-weight: bold;\
                                background-color: transparent;color:white;")
        lyalb = QLabel(parent=self,text="Đăng nhập vào tài khoản của bạn")
        lyalb.setStyleSheet("font-size:40px; color:white;")
        lyalb.setGeometry(628,262,600,48)
        welcome_lb.adjustSize()
        email = QLabel(parent=self,text="Tên đăng nhập")
        email.setStyleSheet("color:white;font-size:40px")
        email.move(628,373)
        email.adjustSize()
        self.usernameLe = QLineEdit(self)
        self.usernameLe.setStyleSheet("color:white; border: 2px solid; border-color:white;border-radius: 10px;background-color: transparent;font-size:30px;")
        self.usernameLe.setGeometry(628,442,677,77)

        self.usernameLe.setPlaceholderText("Nhập tên đăng nhập")


        password = QLabel(parent=self, text="Mật khẩu")
        password.setStyleSheet("color:white;font-size:40px")
        password.move(628,540)
        password.adjustSize()
        
        self.passwordLe = QLineEdit(self)
        self.passwordLe.setPlaceholderText("Nhập mật khẩu")
        self.passwordLe.setStyleSheet("color:white; border: 2px solid; border-color:white;border-radius: 10px;background-color: transparent;font-size:30px;")
        self.passwordLe.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordLe.setGeometry(628,609,677,77)

    
    def create_login_button(self):

        # loWidget.setFixedSize(400,400)
        loLayout = QGridLayout()
        loginbt = QPushButton("Đăng nhập",self)
        loginbt.setGeometry(628,776,677,55)
        loginbt.setStyleSheet("background-color: #76ABAE; border: none; border-color:black;border-radius: 10px;color:#31363F; font-size:25px")
        loginbt.clicked.connect(self.login)
        # loLayout.addWidget(loginbt,0,0,1,1)
        
        
        daclb = QLabel(parent=self,text="Chưa có tài khoản?")
        daclb.setStyleSheet("background-color: transparent; color:white; font-size:24px;")
        daclb.setGeometry(864,865,268,29)

        register_bt = QPushButton("Đăng ký tại đây",self)
        register_bt.setGeometry(1129,865,200,29)
        register_bt.setStyleSheet("font-family: Lexend;\
                                    font-size: 24px;\
                                    text-align: left;\
                                    border: none;\
                                    color:#76ABAE;background-color: transparent;\
                                    ")
        register_bt.clicked.connect(self.register_bt_event)
        loLayout.addWidget(register_bt,0,1,1,1)

        self.loginLb = QLabel("oke")
        loLayout.addWidget(self.loginLb,1,0,1,2)

        # loWidget.setLayout(loLayout)

        # parent.addWidget(loWidget)

    def register_bt_event(self):
        self.hide()
        self.parent().create_register()

    
    def check_empty(self, text: str):
        if text.strip() == "":
            return False
        return True
    def login(self):
        if  not (self.check_empty(self.usernameLe.text()) and self.check_empty(self.passwordLe.text())):
            self.parent().set_notice(title="Error", text="Tên đăng nhập hoặc mật khẩu không được để trống", icon = QMessageBox.Icon.Critical)
        param = {"username":self.usernameLe.text(),
                 "password":self.passwordLe.text()}
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/login", body=json.dumps(param),headers={'Content-Type': 'application/json'})
        if res.status != 200:
            self.parent().set_notice(title="Error", text="Tên đăng nhập hoặc mật khẩu không đúng", icon = QMessageBox.Icon.Critical)
        else:

            info_data = res.data.decode("ascii")
            
            self.parent().set_account(info_data)
            self.close()


        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = loginWidget()
    window.show()
    sys.exit(app.exec())
