from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QHeaderView, QGridLayout, QScrollArea, QLayoutItem, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap,QImage
from PyQt6.QtCore import QSize
import cv2
import sys
import urllib3
import json
from widget import mriView, patientView
import os
import numpy as np
import asyncio
class InventoryWidget(QScrollArea):
    def __init__(self, parent=None, auth_id= None):
        super(InventoryWidget, self).__init__(parent)
        self.setGeometry(400,0,1520,1050)
        

        self.root = os.getcwd()

        self.auth_id = auth_id
        asyncio.run(self.__load_data_when_init())

    async def __load_data_when_init(self):
        stat, data = await self.get_data()
        if stat ==  True:
            self.load_data(data)
        else:
            self.parent().set_notice(title="error",text="can't load model", icon=QMessageBox.Icon.Warning)
    async def get_data(self):
        auth_id = self.auth_id
        param = json.dumps({"authID":auth_id})
        http = urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9012/patients", body=param,headers={'Content-Type': 'application/json'})
        print(rs.status)
        if rs.status == 200:
            data = rs.data.decode("ascii")
            data = json.loads(data)
            return True, data
        else: 
            return False, None
            
    def load_data(self, data, colume=4):
        gridlayout = QGridLayout()

        inven_wg = QWidget()
        

        datas = data["patients"]

        print(len(datas))
        for idx,d in enumerate(datas):
            icon = gridIcon(self,patient_info=d, mainview=self.parent())
            r, c = idx//colume, idx%colume
            gridlayout.addWidget(icon,r,c)

        inven_wg.setFixedWidth(1520)
        inven_wg.setLayout(gridlayout)
        self.setWidget(inven_wg)

        
class gridIcon(QWidget):
    def __init__(self, parent=None, patient_info=None, mainview=None):
        
        super(gridIcon,self).__init__(parent)
        self.setFixedSize(200,250)
        self.button = QPushButton(self)
        self.button.setGeometry(0,0,200,200)
        
        self.mainview = mainview
        
        icon = cv2.imread(os.path.join(os.getcwd(),"icon/icon.jpg"))
        self.patient_info = patient_info
        # icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB) 
        # icon = cv2.resize(icon,(150,150))
        # icon = plt.imread(os.path.join(os.getcwd(),"icon\\test.jpg"))
        # self.button.setIcon(QIcon(QPixmap.fromImage(QImage(icon,150,150,150*3,QImage.Format.Format_RGB888))))
        self.button.setIcon(QIcon(os.path.join(os.getcwd(),"icon/User.png")))
        self.button.setIconSize(QSize(200,200))
        self.button.setStyleSheet(" QPushButton { border: none; border-color:black;border-radius: 12px; }")
        self.button.clicked.connect(self.click_treeview_event)
        self.patientID = patient_info["patientID"]

        self.label = QLabel(self,wordWrap=True)
        self.label.move(0,180)
        # self.label.sizeHint
        self.label.setStyleSheet("color:white; font-size:20px")

        self.label.setText(self.patient_info["name"])
        self.label.adjustSize()
    def click_treeview_event(self):
        self.parent().close()
        self.mainview.set_mainview(patientView.PatientWidget(parent=self.mainview,patient_info=self.patient_info))
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryWidget(auth_id="Y2hpdGhpZW4yMDI0LTA5LTI1IDE4OjUxOjE4LjQ5ODg4MQ==")
    window.show()
    sys.exit(app.exec())
