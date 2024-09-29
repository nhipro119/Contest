from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QHeaderView, QGridLayout, QScrollArea, QLayoutItem, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap,QImage
from PyQt6.QtCore import QSize
import cv2
from PIL import Image
import sys
import urllib3
import json
import matplotlib.pyplot as plt
from widget import mriView
import os
import numpy as np
class InventoryWidget(QScrollArea):
    def __init__(self, parent=None, auth_id= None):
        super(InventoryWidget, self).__init__(parent)
        self.setGeometry(400,0,1520,1080)
        self.gridlayout = QGridLayout(self)
        self.setLayout(self.gridlayout)
        self.root = os.getcwd()
        # self.add_data_in_treeView()
        self.auth_id = auth_id
        self.get_data()

    def get_data(self):
        auth_id = self.auth_id
        param = json.dumps({"authID":auth_id})
        http = urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9012/inventory", body=param,headers={'Content-Type': 'application/json'})
        print(rs.status)
        if rs.status == 200:
            data = rs.data.decode("ascii")
            data = json.loads(data)
            self.load_data(data)
    def load_data(self, data, colume=6):
        datas = data["list file"]
        
        for idx,d in enumerate(datas):
            icon = gridIcon(self,mri_id=d[0], name=d[1])
            r, c = idx//colume, idx%colume
            self.gridlayout.addWidget(icon,r,c)

    

        
class gridIcon(QWidget):
    def __init__(self, parent=None, name=None, mri_id=None):
        
        super(gridIcon,self).__init__(parent)
        self.setFixedSize(150,200)
        self.button = QPushButton(self)
        self.button.setGeometry(0,0,150,150)

        icon = cv2.imread(os.path.join(os.getcwd(),"icon\\icon.jpg"))

        icon = cv2.cvtColor(icon, cv2.COLOR_BGR2RGB) 
        icon = cv2.resize(icon,(150,150))
        # icon = plt.imread(os.path.join(os.getcwd(),"icon\\test.jpg"))
        self.button.setIcon(QIcon(QPixmap.fromImage(QImage(icon,150,150,150*3,QImage.Format.Format_RGB888))))
        self.button.setIconSize(QSize(150,150))
        self.button.clicked.connect(self.click_treeview_event)
        self.mri_id = mri_id

        self.label = QLabel(self)
        self.label.setGeometry(0,160,150,40)
        self.label.setText(name)
    def click_treeview_event(self):
        mri = mriView.MriWidget(parent=self.parent().parent(),mri_file=self.mri_id)
        mri.show()
        self.parent().close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryWidget(auth_id="Y2hpdGhpZW4yMDI0LTA5LTI1IDE4OjUxOjE4LjQ5ODg4MQ==")
    window.show()
    sys.exit(app.exec())
