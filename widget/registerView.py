from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,QFormLayout, QApplication, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QTime
from PyQt6.QtGui import QPixmap
import sys
from functools import partial
import urllib3
import json
import os
# import passwordLineEdit
class RegisterView(QWidget):
    def  __init__(self, parent=None, size=[1920,1080]):
        super(RegisterView,self).__init__(parent)
        self.total_layout = QVBoxLayout()
        bglb = QLabel(self)
        bglb.setFixedSize(1920,1080)
        bglb.setPixmap(QPixmap(os.path.join(os.getcwd(), "icon/Signup.jpg")))
        self.setFixedSize(*size)
        self.setAutoFillBackground(True)
        self.create_form_layout()
        
        self.create_create_register_button(self.total_layout)
        
    def create_form_layout(self):
        
        create_account_label = QLabel("Tạo tài khoản",parent=self)
        create_account_label.move(611,102)
        create_account_label.setStyleSheet("font-family: Lexend;\
                                            font-size: 96px;\
                                            font-weight: bold;\
                                            text-align: left;\
                                                color:white;\
                                            ")
        create_account_label.adjustSize()
        
        name = QLabel(text="Họ và Tên", parent=self)
        name.move(191,218)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        
        self.Namele = QLineEdit(self)
        self.Namele.setGeometry(191,287,677,77)
        self.Namele.setPlaceholderText("Nhập họ và tên")
        self.Namele.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        # self.formLayout.addRow(Namelb,self.Namele)
        self.Namele.textChanged.connect(partial(self.__warning,self.Namele))


        name = QLabel(text="Số điện thoại", parent=self)
        name.move(191,387)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        self.PhoneLe = QLineEdit(self)
        self.PhoneLe.setGeometry(191,456,677,77)
        self.PhoneLe.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        self.PhoneLe.setPlaceholderText("Nhập số điện thoại")
        self.PhoneLe.textChanged.connect(partial(self.__warning,self.PhoneLe))

        name = QLabel(text="Email", parent=self)
        name.move(191,554)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        
        self.MailLe = QLineEdit(self)
        self.MailLe.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        self.MailLe.setGeometry(191,623,677,77)
        self.MailLe.setPlaceholderText("Nhập email")
        self.MailLe.textChanged.connect(partial(self.__warning,self.MailLe))

        name = QLabel(text="Tên Đăng Nhập", parent=self)
        name.move(1088,218)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        
        self.usernamele = QLineEdit(self)
        self.usernamele.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        self.usernamele.setGeometry(1088,287,677,77)
        self.usernamele.setPlaceholderText("Nhập tên đăng nhập")
        self.usernamele.textChanged.connect(partial(self.__warning,self.usernamele))
        
        name = QLabel(text="Mật khẩu", parent=self)
        name.move(1088,387)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        self.passwordle = QLineEdit(self)
        self.passwordle.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        self.passwordle.setGeometry(1088,456,677,77)
        self.passwordle.setPlaceholderText("Nhập mật khẩu")
        # self.formLayout.addRow(passwordlb, self.passwordle)
        self.passwordle.setEchoMode(QLineEdit.EchoMode.Password)

        name = QLabel(text="Xác nhận mật khẩu", parent=self)
        name.move(1088,554)
        name.setStyleSheet("color:white; font-size:40px;background-color: transparent;")
        name.adjustSize()
        self.Cble = QLineEdit(self)
        self.Cble.setStyleSheet("background-color: transparent; color:white;   border: 1px solid; border-color:white;border-radius: 12px;font-size:30px;")
        self.Cble.setPlaceholderText("Xác nhận mật khẩu")
        self.Cble.setGeometry(1088,623, 677,77)
        self.Cble.setEchoMode(QLineEdit.EchoMode.Password)
        


        # self.formWidget.setLayout(self.formLayout)
        # parent.addWidget(self.formWidget)
    def create_create_register_button(self,parent):

        regbutton = QPushButton("Đăng ký",parent=self)
        regbutton.setStyleSheet("background-color: #76ABAE; border: none;border-radius: 10px;color:#31363F; font-size:25px")
        regbutton.setGeometry(629,796,677,55)
        regbutton.clicked.connect(self._create_account)





    def check_phone(self):
        if len(self.PhoneLe.text()) != 10:
            return False
        if not self.PhoneLe.text().isdecimal():
            return False
        return True
    def check_email(self):
        if len(self.MailLe.text()) <=2:
            return False
        if "@" not in self.MailLe.text():
            return False
        return True
    def __check_password(self):
        """check password enough lenght"""
        if len(self.passwordle.text().strip()) < 6:
            return False
        
        return True
    def __check_cple(self):
        """check comfirm password is same with password"""
        if self.Cble.text() != self.passwordle.text():
            return False
        return True
    def __warning(self, le):
        """warning when type content under 2 character"""
        # if len(le.text()) <=2:
        #     le.setStyleSheet("background-color:#D9D9D9;   border-radius: 12px; border-color: red;")
        # else:
        #     le.setStyleSheet("background-color:#D9D9D9;   border-radius: 12px;")    
    
    def __get_info(self):
        info = {"username":self.usernamele.text(),
                "password":self.passwordle.text(),
                "name":self.Namele.text(),
                "phone":self.PhoneLe.text(),
                "mail":self.MailLe.text()}
        return info
    def check_empty(self):
        box = [self.MailLe, self.PhoneLe, self.Namele, self.usernamele, self.passwordle]
        for b in box:
            if b.text().strip() == "":
                return False
        return True
    

    
    def _create_account(self):
        if  not self.check_empty():
            self.parent().set_notice(title="Error",text="Bạn phải nhập đủ hết thông tin", icon=QMessageBox.Icon.Warning)
            return False
        info = self.__get_info()
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/register",body=json.dumps(info),headers={'Content-Type': 'application/json'})
        if res.status == 400:
            self.parent().set_notice(title="Error",text="Tên đăng nhập đã có", icon=QMessageBox.Icon.Warning)
            return False
        elif res.status == 500:
            self.parent().set_notice(title="Error",text="Lỗi", icon=QMessageBox.Icon.Warning)
        elif res.status == 200:
            self.login()
            self.close()
    
    def login(self):
        param = {"username":self.usernamele.text(),
                 "password":self.passwordle.text()}
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/login", body=json.dumps(param),headers={'Content-Type': 'application/json'})
        if res.status != 200:
            self.loginLb.setText("username or password is not correct")
        else:

            info_data = res.data.decode("ascii")

            self.parent().set_account(info_data)
if __name__ =="__main__":
    app = QApplication(sys.argv)
    rv = RegisterView()
    rv.show()
    sys.exit(app.exec())
