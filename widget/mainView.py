
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

from widget import mriView, registerView, loginView, inventoryView
import urllib3
import json
from functools import partial
import os
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
        self.info = {"name":None, "mail":None, "phone":None}
        self.__login_when_init()


    def create_menu_widget(self,parent):
        menu_widget = QWidget(parent)
        menu_widget.setStyleSheet("border: 1px solid;border-radius: 5px; border-color:black;")
        menu_widget.setGeometry(0,0,400,1080)
        menu_widget.setFixedWidth(400)
        

        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)
        self.info_lb = QLabel("oke")
        self.info_lb.setFixedSize(100,200)
        menu_layout.addWidget(self.info_lb)
        inventory_bt = QPushButton("INVENTORY")
        inventory_bt.setFixedSize(350,100)
        inventory_bt.setStyleSheet("border: 1px solid; border-color:black;border-radius: 5px; background-color:green;")
        inventory_bt.clicked.connect(self.open_inventory_event)
        menu_layout.addWidget(inventory_bt)


        upload_bt = QPushButton("UPLOAD")
        upload_bt.setStyleSheet("  background-color: #04AA6D;\
                                        color: white;\
                                        padding: 14px 20px;\
                                        margin: 8px 0;\
                                        border: none;\
                                        cursor: pointer;\
                                        width: 100%;")
        upload_bt.clicked.connect(self.upload_file)
        menu_layout.addWidget(upload_bt)
        
        self.login_bt = QPushButton("LOGIN")
        self.login_bt.setStyleSheet("  background-color: #04AA6D;\
                                        color: white;\
                                        padding: 14px 20px;\
                                        margin: 8px 0;\
                                        border: none;\
                                        cursor: pointer;\
                                        width: 100%;")
        self.login_bt.clicked.connect(self.login_bt_event)

        menu_layout.addWidget(self.login_bt)
        
        # parent.addWidget(menu_widget)
    def set_notice(self,title=None,text=None, icon=None):
        print("oke")
        self.notice_label.setWindowTitle(title)
        self.notice_label.setText(text)
        self.notice_label.setIcon(icon)
        bt = self.notice_label.exec()
        if bt == QMessageBox.StandardButton.Ok:
            self.notice_label.hide()
        


    def upload_file(self):
        # self.notice_label.setText(" not login yet")
        if self.auth_id == None:
            self.set_notice(title="warning", text="not login yet",icon=QMessageBox.Icon.Critical)
            return
        root = os.getcwd()
        path = QFileDialog.getOpenFileName(None, 'Select nii file', root,"(*.nii.gz)")
        path = path[0]
        if ".nii.gz" not in path.split("/")[-1]:
            self.set_notice(title="warning", text="this file isn't ni.gz file",icon=QMessageBox.Icon.Critical)
        http = urllib3.PoolManager()
        http.request("POST","103.63.121.200:9012/upload")
    def open_inventory_event(self):
        inventoryWidget = inventoryView.InventoryWidget(parent=self,auth_id=self.auth_id)
        inventoryWidget.show()
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
        self.auth_id = data["auth_id"]
        account_info = data["info"]
        self.info["name"] = account_info["name"]
        self.info["mail"] = account_info["mail"]
        self.info["phone"] = account_info["phone"]
        self.info_lb.setText(account_info["name"])
        self.set_logout()
        return True
        

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
