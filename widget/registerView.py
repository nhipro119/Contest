from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,QFormLayout, QApplication, QVBoxLayout
from PyQt6.QtCore import QTime

import sys
from functools import partial
import urllib3
import json
import passwordLineEdit
class RegisterView(QWidget):
    def  __init__(self, parent=None, size=[1520,1000]):
        super(RegisterView,self).__init__(parent)
        self.total_layout = QVBoxLayout()

        self.setFixedSize(*size)

        self.create_form_layout()
        
        self.create_create_register_button(self.total_layout)
        
    def create_form_layout(self):
        
        create_account_label = QLabel("Create account",parent=self)
        create_account_label.setGeometry(460,197,360,66)
        create_account_label.setStyleSheet("font-family: Lexend;\
                                            font-size: 45px;\
                                            font-weight: 700;\
                                            line-height: 56.25px;\
                                            text-align: left;\
                                            ")
        

        self.Namele = QLineEdit(self)
        self.Namele.setGeometry(483,375,485,40)
        self.Namele.setPlaceholderText("Name")
        self.Namele.setStyleSheet("background-color:#D9D9D9;   border: 1px solid; border-color:black;border-radius: 12px;")
        # self.formLayout.addRow(Namelb,self.Namele)
        self.Namele.textChanged.connect(partial(self.__warning,self.Namele))

        self.PhoneLe = QLineEdit(self)
        self.PhoneLe.setGeometry(483,449,485,40)
        self.PhoneLe.setStyleSheet("background-color:#D9D9D9;   border: 1px solid; border-color:black;border-radius: 12px;")
        self.PhoneLe.setPlaceholderText("Phone")
        self.PhoneLe.textChanged.connect(partial(self.__warning,self.PhoneLe))


        self.MailLe = QLineEdit(self)
        self.MailLe.setStyleSheet("background-color:#D9D9D9;   border: 1px solid; border-color:black;border-radius: 12px;")
        self.MailLe.setGeometry(483,527,485,40)
        self.PhoneLe.setPlaceholderText("Mail")
        self.MailLe.textChanged.connect(partial(self.__warning,self.MailLe))


        self.usernamele = QLineEdit(self)
        self.usernamele.setStyleSheet("background-color:#D9D9D9; border: 1px solid; border-color:black; border-radius: 12px;")
        self.usernamele.setGeometry(483,605,485,40)
        self.usernamele.setPlaceholderText("Username")
        self.usernamele.textChanged.connect(partial(self.__warning,self.usernamele))
        
        
        self.passwordle = QLineEdit(self)
        self.passwordle.setStyleSheet("background-color:#D9D9D9; border: 1px solid; border-color:black; border-radius: 12px;")
        self.passwordle.setGeometry(483,690,485,40)
        self.passwordle.setPlaceholderText("Password")
        # self.formLayout.addRow(passwordlb, self.passwordle)
        self.passwordle.setEchoMode(QLineEdit.EchoMode.Password)

        Cblb = QLabel("Confirm Password")
        self.Cble = QLineEdit(self)
        self.Cble.setStyleSheet("background-color:#D9D9D9; border: 1px solid; border-color:black; border-radius: 12px;")
        self.Cble.setPlaceholderText("Confirm Password")
        self.Cble.setGeometry(483,775, 485,40)
        self.Cble.setEchoMode(QLineEdit.EchoMode.Password)
        


        # self.formWidget.setLayout(self.formLayout)
        # parent.addWidget(self.formWidget)
    def create_create_register_button(self,parent):
        rbwidget = QWidget()
        rblayout = QVBoxLayout()
        regbutton = QPushButton("Register",parent=self)
        regbutton.setStyleSheet("background-color: #48CFCB; border: 1px solid; border-color:black;border-radius: 30px;")
        regbutton.setGeometry(569,860,300,62)
        regbutton.clicked.connect(self._create_account)
        self.warninglb = QLabel()
        # rblayout.addWidget(regbutton)
        # rblayout.addWidget(self.warninglb)

        parent.addWidget(regbutton)
        parent.addWidget(self.warninglb)

    def __check_is_empty(self, text):
        """check a text is empty"""
        if text.strip() == "":
            return True
        return False
    
    def __check_username(self):
        if len(self.usernamele.text()) <=2:
            self.usernamele.setStyleSheet("border: 1px solid red;")
        else:
            self.usernamele.setStyleSheet("border: 1px solid black;")

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
        if len(le.text()) <=2:
            le.setStyleSheet("background-color:#D9D9D9;   border-radius: 12px; border-color: red;")
        else:
            le.setStyleSheet("background-color:#D9D9D9;   border-radius: 12px;")    
    
    def __get_info(self):
        info = {"username":self.usernamele.text(),
                "password":self.passwordle.text(),
                "name":self.Namele.text(),
                "phone":self.PhoneLe.text(),
                "mail":self.MailLe.text()}
        return info
    
    def __check__valid_info(self):
        if self.__check_is_empty(self.Namele.text()) and self.check_email() and self.check_phone() and self.__check_username() and self.__check_password and self.__check_cple():
            return True
        else:
            return False
    
    def _create_account(self):
        if  self.__check__valid_info():
            self.warninglb.setText("your infomation is not correct")
            return False
        info = self.__get_info()
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/register",body=json.dumps(info),headers={'Content-Type': 'application/json'})
        if res.status == 400:
            self.warninglb.setText("account already exists")
            return False
        elif res.status == 500:
            self.warninglb.setText("system error")
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

            self.parent().parent().set_account(info_data)
if __name__ =="__main__":
    app = QApplication(sys.argv)
    rv = RegisterView()
    rv.show()
    sys.exit(app.exec())
