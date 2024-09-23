import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout,QApplication, QLabel,QVBoxLayout, QScrollArea, QPushButton
from PyQt6.QtGui import QImage,QPixmap,QIcon
from PyQt6.QtCore import QSize,Qt
import nibabel
import numpy as np
import cv2
from functools import partial
import urllib3
import json
import base64
import os
class MriWidget(QWidget):
    def __init__(self, parent=None, mri_file=None,size=[1520,1080]):
        super(MriWidget,self).__init__(parent)
        # self.setFixedSize(*size)
        self.setGeometry(400,0,*size)
        # self.total_layout = QVBoxLayout(self)
        self.imgL = QLabel()
        
        b = QPushButton("predict", self)
        b.setGeometry(0,0,100,100)
        # self.pixmap = QPixmap(512,512)
        image = self.get_file_from_API(mri_file)
        
        self.img_idx = 0

        self.imgs= np.asarray(image.get_fdata())
        self.max_idx = self.imgs.shape[2]
        self.image_view = QLabel(self)
        self.image_view.setGeometry(100,50,768,768)
        img1,w,h,p = self.get_image(self.imgs[:,:,0],768,768)
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img1,w,h,p,QImage.Format.Format_RGB888)))
        # self.total_layout.addWidget(self.image_view)
        
        # self.imgL.setPixmap(QPixmap.fromImage(qimage))
        # self.total_layout.addChildWidget(self.imgL)
        self.list_image()
        # self.setLayout(self.total_layout)

    
    def get_file_from_API(self, imageId):
        http = urllib3.PoolManager()
        param = {"imageID":imageId}
        rs = http.request("POST","103.63.121.200:9012/get_image",body=json.dumps(param), headers={'Content-Type': 'application/json'})
        if rs.status == 200:
            print("oke")
            data = rs.data.decode("ascii")
            data = json.loads(data)["img_data"]
            data = data.encode("ascii")
            data = base64.b64decode(data)
            with open(os.path.join(os.getcwd(),"data","input.nii.gz"), "wb") as f:
                f.write(data)
            image = nibabel.load(os.path.join(os.getcwd(),"data","input.nii.gz"))
            return image
            
    
    def get_image(self,img, w=1024,h=1024):
        cv_img = img.astype(np.uint8)
        frame = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        frame = cv2.resize(frame,(w,h))
        bytesPerLine = 3 * w
        return frame, w,h,bytesPerLine
        
    def process_data(self,predict:str):
        img, w,h,p = self.get_image(self.imgs,512,512)
        out_pre = nibabel.load(predict)
        out_pre_img = out_pre.get_fdata()
        for c in range(128):
            img = out_pre_img[:,:,c]
            for r in img:
                pass

    def dislay_mri_file(self):
        pass

    def list_image(self):
        qvbox = QVBoxLayout()
        l_lb = []
        for ar in range(self.imgs.shape[2]):
            l_lb.append(QPushButton())

            # l_lb[ar].set_id(ar)
            img,w,h,BPL = self.get_image(self.imgs[:,:,ar],128,128)
            l_lb[ar].setIcon(QIcon(QPixmap.fromImage(QImage(img,w,h,BPL,QImage.Format.Format_RGB888))))
            l_lb[ar].setIconSize(QSize(128,128))
            l_lb[ar].setStyleSheet("QPushButton { border: none; }")

            
            # l_lb[ar].setFixedSize(128,128)
            l_lb[ar].clicked.connect(partial(self.dislay_image_event,ar))
            # a = QLabel()
            # a.obj
            qvbox.addWidget(l_lb[ar])   
        
        self.lqwidget = QWidget()
        # self.lqwidget.setFixedSize(200,1080)  
        self.lqwidget.setLayout(qvbox)

        scroll = QScrollArea(self)
        scroll.setGeometry(1300,0,200,1080)
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(170)
        # scroll.setFixedWidth(780)
        scroll.setWidget(self.lqwidget)
        # self.total_layout.addWidget(scroll)
    
    def dislay_image_event(self,ar):
        img,w,h,pb = self.get_image(self.imgs[:,:,ar])
        self.img_idx = ar
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img,w,h,pb,QImage.Format.Format_BGR888)))

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A: 
            if self.img_idx > 0:
                self.img_idx -= 1
        elif event.key() == Qt.Key.Key_D:
            if self.img_idx < self.max_idx -1:
                self.img_idx += 1
        img, w,h,pb = self.get_image(self.imgs[:,:,self.img_idx])
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img,w,h,pb,QImage.Format.Format_BGR888)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MriWidget(mri_file="2400106729.nii.gzMDkvMjAvMjAyNCwgMTg6Mjc6MzM=")
    window.show()
    sys.exit(app.exec())
