from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,QFormLayout, QApplication, QVBoxLayout
from qtwidgets import PasswordEdit
import sys
from functools import partial
import urllib3
import json
class RegisterView(QWidget):
    def  __init__(self, parent=None):
        super(RegisterView,self).__init__(parent)
        self.total_layout = QVBoxLayout()
        self.setLayout(self.total_layout)
        self.create_form_layout(self.total_layout)

    def create_form_layout(self, parent):
        self.formWidget = QWidget()

        self.formLayout = QFormLayout()
        
        Namelb = QLabel("Name")
        self.Namele = QLineEdit()
        self.formLayout.addRow(Namelb,self.Namele)
        self.Namele.textChanged.connect(partial(self.__warning,self.Namele))

        PhoneLb = QLabel("Phone")
        self.PhoneLe = QLineEdit()
        self.formLayout.addRow(PhoneLb,self.PhoneLe)
        self.PhoneLe.textChanged.connect(partial(self.__warning,self.PhoneLe))

        MailLb = QLabel("Mail")
        self.MailLe = QLineEdit()
        self.formLayout.addRow(MailLb,self.MailLe)
        self.MailLe.textChanged.connect(partial(self.__warning,self.MailLe))

        usernamelb = QLabel("User Name")
        self.usernamele = QLineEdit()
        self.usernamele.textChanged.connect(partial(self.__warning,self.usernamele))
        
        self.formLayout.addRow(usernamelb, self.usernamele)
        
        passwordlb = QLabel("Password")
        self.passwordle = PasswordEdit()
        self.formLayout.addRow(passwordlb, self.passwordle)
        self.passwordle.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        Cblb = QLabel("Confirm Password")
        self.Cble = PasswordEdit()
        self.Cble.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.formLayout.addRow(Cblb, self.Cble)

        self.formWidget.setLayout(self.formLayout)
        parent.addWidget(self.formWidget)
    def create_create_register_button(self,parent):
        rbwidget = QWidget()
        rblayout = QVBoxLayout()
        regbutton = QPushButton("Register")
        regbutton.clicked.connect(self._create_account)
        self.warninglb = QLabel()
        rblayout.addWidget(regbutton)
        rblayout.addWidget(self.warninglb)
        rbwidget.setLayout(rblayout)
        parent.addWidget(rbwidget)

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
            le.setStyleSheet("border: 1px solid red;")
        else:
            le.setStyleSheet("border: 1px solid black;")    
    
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
        if not self.__check__valid_info():
            self.warninglb.setText("your infomation is not correct")
            return False
        info = self.__get_info()
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/register",body=json.dumps(info))
        if res.status != 200:
            self.warninglb.setText("account already exists")
            return False
        else:
            return True
    
    def login(self):
        param = {"username":self.usernamele.text(),
                "password":self.passwordle.text()}
        http = urllib3.PoolManager()
        res = http.request("POST","103.63.121.200:9011/login",body = json.dumps(param))
        if res.status == 200:
            token = res.data.decode("ascii")[1]
            with open("data/account.txt", "w") as f:
                f.write(token)
if __name__ =="__main__":
    app = QApplication(sys.argv)
    rv = RegisterView()
    rv.show()
    sys.exit(app.exec())
