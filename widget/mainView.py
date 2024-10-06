
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
    QWidget,QLayout,
    QFileDialog,QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import QSize, Qt
import asyncio
from widget import mriView, registerView, loginView, inventoryView,patientView
import urllib3
import json
from functools import partial
import os
import base64
class Main(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.setStyleSheet("background-color:#222831")
        mornitor = get_monitors()[0]
        height = mornitor.height
        width = mornitor.width
        # self.setGeometry(0,0,1920,1080)
        self.setMinimumSize(width,height)
        self.showMaximized()
        self.notice_label = QMessageBox()
        self.total_widget = QWidget()
        # self.mainView = None
        # self.total_layout =  QHBoxLayout()
        # self.total_widget.setLayout(self.total_layout)
        self.setCentralWidget(self.total_widget)
        self.create_menu_widget(self.total_widget)
        # self.view_widget = QWidget(self.total_widget)
        # self.view_widget.setGeometry(400,0,1050,1080)
        self.auth_id = None
        self.mainview = loginView.loginWidget()
        self.info = {"name":None, "mail":None, "phone":None}
        self.thread_daemon = None
        self.__login_when_init()


    def set_mainview(self,widget:QWidget, geometry=[507,0,1420,1080]):
        self.mainview.close()
        self.mainview = widget
        self.mainview.setGeometry(*geometry)
        self.mainview.show()
        
    def create_menu_widget(self,parent):
        menu_widget = QWidget(parent)
        menu_widget.setStyleSheet(" background-color:#31363F")
        menu_widget.setGeometry(0,0,506,1070)

        
        welcome_lb = QLabel(menu_widget)
        welcome_lb.setGeometry(34,27,195,48)
        welcome_lb.setText("Xin chào,")
        welcome_lb.setStyleSheet("font-size:40px;font-weight: bold;background-color:#31363F; color:white;")
        
        self.icon_lb = QLabel(menu_widget)
        self.icon_lb.setGeometry(326,10,130,130)
        
        self.info_lb = QLabel(text="", parent=self,alignment=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.info_lb.setGeometry(34,90,250,100)
        self.info_lb.setWordWrap(True)
        
        self.info_lb.setStyleSheet("font-size:36px; background-color:#31363F; color:white;")
        
        inventory_bt = QPushButton(icon=QIcon(os.path.join(os.getcwd(),"icon/Archive.png")),text="Danh Sách",parent=menu_widget)
        inventory_bt.setIconSize(QSize(70,70))
        inventory_bt.setGeometry(0,253,506,95)
        inventory_bt.setStyleSheet("border: 3px solid; border-color:#222831;\
                                    font-size:48px;\
                                    font-weight:bold; background-color:#5C8085;color:white;")
        inventory_bt.clicked.connect(self.open_inventory_event)



        
        upload_bt = QPushButton(icon=QIcon(os.path.join(os.getcwd(),"icon/UserCirclePlus.png")),text="Thêm Bệnh Nhân",parent=menu_widget)
        upload_bt.setIconSize(QSize(70,70))
        upload_bt.setStyleSheet("  background-color: #31363F;\
                                        color: white;\
                                            border: 3px solid; border-color:#222831;\
                                        font-size:48px;font-weight:bold;\
                                        width: 100%;")
        upload_bt.clicked.connect(self.open_upload_patient_view)
        upload_bt.setGeometry(0,348,506,95)
        # menu_layout.addWidget(upload_bt)
        
        self.login_bt = QPushButton(text="Đăng xuất",parent=menu_widget)
        
        self.login_bt.setStyleSheet("  background-color: #1E1E1E;\
                                        color: white;\
                                        border: none;\
                                        cursor: pointer;\
                                    font-family: Inter;\
                                    font-size: 30px;\
                                    font-style: normal;\
                                    font-weight: 700;\
                                    line-height: normal;\
                                        width: 100%;")
        self.login_bt.clicked.connect(self.login_bt_event)
        self.login_bt.setGeometry(0,950,506,81)
        # menu_layout.addWidget(self.login_bt)
        
        # parent.addWidget(menu_widget)
        
    
    def set_notice(self,title=None,text=None, icon=None):
        self.notice_label.setWindowTitle(title)
        # self.notice_label.move(400,800)
        self.notice_label.setText(text)
        self.notice_label.setIcon(icon)
        bt = self.notice_label.show()
        if bt == QMessageBox.StandardButton.Ok:
            self.notice_label.hide()
        


    

    

            

    
    def open_upload_patient_view(self):
        self.set_mainview(patientView.PatientWidget(parent=self))
        
    def open_inventory_event(self):
        self.set_mainview(inventoryView.InventoryWidget(parent=self,auth_id=self.auth_id))

        
    def __login_when_init(self):
        self.root_path = os.getcwd()
        if(not os.path.exists(os.path.join(self.root_path,"data"))):
            os.mkdir(os.path.join(self.root_path,"data"))
            with open(os.path.join(self.root_path,"data","account.bin"),"wb") as f:
                f.write("")
            self.login_bt_event()
        elif not os.path.exists(os.path.join(self.root_path,"data","account.bin")):
            self.login_bt_event()
        else:
            if self.read_account_txt():
                self.open_inventory_event()
            else:
                self.login_bt_event()
    def read_account_txt(self):
        with open(os.path.join(self.root_path,"data","account.bin"),"rb") as f:
            data = f.read()
        data = data.decode("utf-8")
        try:
            data = json.loads(data)
        except:
            return False
        print(data)
        self.auth_id = data["auth_id"]
        account_info = data["info"]
        self.set_info(account_info)

        self.set_logout()
        return True
        

    def login_bt_event(self):
        self.set_mainview(loginView.loginWidget(self), geometry=[0,0,1920,1080])
        # login_widget = 
        # login_widget.setGeometry(400,0,800,800)
        # login_widget.show()
        # self.login_widget.setGeometry(400,0,800,800)
    
    def create_register(self):
        self.set_mainview(registerView.RegisterView(self),geometry=[0,0,1920,1080])
        # self.regView = 
        # self.regView.setGeometry(400,0,800,800)
        
        # self.regView.show()
        
    # def create_main_widget(self,parent:QLayout, widget:QWidget):
    #     parent.addWidget(widget)

    # def login(self):
    #     login = loginView.loginWidget(parent=self)
        
    def set_account(self, info:str):
        print(info)
        info_data = json.loads(info)
        info_data_encode = info.encode("utf-8")
        with open("data/account.bin", "wb") as f:
            f.write(info_data_encode)
        
        
        self.auth_id = info_data["auth_id"]

        self.set_info(info_data["info"])
        self.open_inventory_event()
    def set_logout(self):
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
        
        with open("./data/account.bin", "wb") as f:
            f.write("".encode("utf-8"))
        # self.icon_lb.clear()
        self.login_bt_event()
        # self.icon_lb.setText()

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
        self.info_lb.show()
        self.info["phone"] = data["phone"]
        self.info["mail"] = data["mail"]
        self.info["name"] = data["name"]
        self.icon_lb.setStyleSheet("background-color:#31363F")
        self.icon_lb.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon","UserCircle.png")))
# if __name__ == "__main__":
#     app = QApplication([])
#     window = Window()
#     window.show()
#     sys.exit(app.exec())
