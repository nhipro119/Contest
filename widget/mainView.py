
import sys
from screeninfo import get_monitors

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,QLayout
)
from widget import mriView, registerView, loginView
import urllib3
import json
from functools import partial
class Main(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        # self.setCentralWidget(QLabel("I'm the Central Widget"))
        mornitor = get_monitors()[0]
        height = mornitor.height
        width = mornitor.width
        self.setMinimumSize(width,height)
        self.showMaximized()
        self.total_widget = QWidget()
        # self.total_layout =  QHBoxLayout()
        # self.total_widget.setLayout(self.total_layout)
        self.setCentralWidget(self.total_widget)
        self.create_menu_widget(self.total_widget)
        # self.view_widget = QWidget(self.total_widget)
        # self.view_widget.setGeometry(400,0,1050,1080)
        self.auth_id = None
        self.info = {"name":None, "mail":None, "phone":None}


    def create_menu_widget(self,parent):
        menu_widget = QWidget(parent)
        menu_widget.setGeometry(0,0,400,1080)
        menu_widget.setFixedWidth(400)
        

        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)
        self.info_lb = QLabel("oke")
        self.info_lb.setFixedSize(100,200)
        menu_layout.addWidget(self.info_lb)
        inventory_bt = QPushButton("INVENTORY")
        menu_layout.addWidget(inventory_bt)


        patient_bt = QPushButton("PATIENT")
        menu_layout.addWidget(patient_bt)
        
        self.login_bt = QPushButton("LOGIN")
        self.login_bt.clicked.connect(self.login_bt_event)

        menu_layout.addWidget(self.login_bt)
        
        # parent.addWidget(menu_widget)

    def login_bt_event(self):
        self.login_widget = loginView.loginWidget(self.total_widget)
        self.login_widget.setGeometry(400,0,800,800)
        self.login_widget.show()
        # self.login_widget.setGeometry(400,0,800,800)
    
    def create_register(self):
        self.regView = registerView.RegisterView(self.total_widget)
        self.regView.setGeometry(400,0,800,800)
        
        self.regView.show()
        
    # def create_main_widget(self,parent:QLayout, widget:QWidget):
    #     parent.addWidget(widget)

    # def login(self):
    #     login = loginView.loginWidget(parent=self)
        
    def set_account(self, info:str):
        print(info)
        info_data = json.loads(info)

        with open("data/account.txt", "w") as f:
            f.write(info)
        
        
        self.auth_id = info_data["auth_id"]

        self.set_info(info_data["info"])
        try:
            self.login_bt.setText("logout")
            self.login_bt.clicked.disconnect()
            self.login_bt.clicked.connect(self.logout_event)
        except:
            print("login button cant disconnect")

    def logout_event(self):
        self.auth_id = None
        self.info_lb.setText("no loggin")
        self.info = {"name":None, "mail":None, "phone":None}
        with open("./data/account.txt", "w") as f:
            f.write("")

    def get_account_from_authid(self):
        param = json.dumps({"authId":self.auth_id})
        http = urllib3.PoolManager()
        rs = http.request("POST", "103.63.121.200:9011/get_info",body=param)
        if rs.status == 200:
            data = rs.data.decode("ascii")
            dict_data = json.loads(data)
            self.set_info(data=dict_data)

    def set_info(self, data:dict):
        self.info_lb.setText(data["name"])    
        self.info["phone"] = data["phone"]
        self.info["mail"] = data["mail"]
        self.info["name"] = data["name"]
# if __name__ == "__main__":
#     app = QApplication([])
#     window = Window()
#     window.show()
#     sys.exit(app.exec())
