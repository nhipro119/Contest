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

        self.image_view = QLabel(self)
        self.image_view.setGeometry(100,50,768,768)

        predict_bt = QPushButton("predict", self)

        predict_bt.setGeometry(0,0,100,100)
        predict_bt.clicked.connect(self.predict_event)
        # self.pixmap = QPixmap(512,512)
        
        self.img_size = (768,768)
        self.img_idx = 0

        self.imgs, self.max_idx = self.__get_image(mri_file=mri_file)
        
        self.imgs = self.__image_proccessing(self.imgs,*self.img_size)
        
        self.__dislay_img_on_imgview(self.imgs[0],*self.img_size)
        
        self.scrol = QScrollArea(self)
        self.scrol.setGeometry(1300,0,200,1080)
        
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(170)
        # scroll.setFixedWidth(780)
        
        # self.total_layout.addWidget(self.image_view)
        
        # self.imgL.setPixmap(QPixmap.fromImage(qimage))
        # self.total_layout.addChildWidget(self.imgL)
        self.list_image(self.imgs)
        # self.setLayout(self.total_layout)

    def __get_image(self,mri_file:str):
        image = self.get_file_from_API(mri_file)
        imgs= np.asarray(image.get_fdata())
        max_idx = imgs.shape[2]
        return imgs, max_idx
    
    def __dislay_img_on_imgview(self,img,w,h):
        p = w*3
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img,w,h,p,QImage.Format.Format_RGB888)))

    def get_file_from_API(self, imageId):
        http = urllib3.PoolManager()
        param = {"imageID":imageId}
        rs = http.request("POST","103.63.121.200:9012/get_image",body=json.dumps(param), headers={'Content-Type': 'application/json'})
        print(rs.status)
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
            
    
    def __image_proccessing(self,imgs, w=1024,h=1024):
        proccessed_img = []
        imgs = imgs.astype(np.uint8)
        for idx in range(imgs.shape[2]):
            cv_img = imgs[:,:,idx]
            frame = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
            frame = cv2.resize(frame,(w,h))
            proccessed_img.append(frame)
        return proccessed_img
    
    def predict_event(self):
        mri_data = open(os.path.join(os.getcwd(),"data","input.nii.gz"), "rb").read()
        file_data = ("input.nii.gz",mri_data)
        http =urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9010/predict",fields={"file":file_data})
        if rs.status == 200:
            print("predict")
            rs_data = rs.data.decode("ascii")
            dict_data = json.loads(rs_data)
            file_data = dict_data["file"]
            volume_data = dict_data["volume"]
            file_data = file_data.encode("ascii")
            file_data = base64.b64decode(file_data)
            with open(os.path.join(os.getcwd(),"data","output.nii.gz"),"wb") as f:
                f.write(file_data)
            self.imgs = self.process_predict_data()
            
            self.__dislay_img_on_imgview(self.imgs[0],*self.img_size)
            self.list_image(self.imgs)
        #     print(volume_data)
        # print(rs.status)
        
    def process_predict_data(self):
        
        imgs = nibabel.load(os.path.join(os.getcwd(),"data","output.nii.gz"))
        # imgs = nibabel.load("240010729.nii.gz")
        img = imgs.get_fdata()
        # for i in range(128):
        img = img * 255
        img = img.astype(np.uint8)
        in_imgs = nibabel.load(os.path.join(os.getcwd(),"data","input.nii.gz"))
        in_img = in_imgs.get_fdata()
        in_img = in_img.astype(np.uint8)
        predict_frames = []
        for i in range(128):
            
            frame = cv2.cvtColor(img[:,:,i], cv2.COLOR_GRAY2RGB)
            frame[np.where((frame!=[0, 0, 0]).all(axis=2))] = [255,0,0]
            frame[np.where((frame==[0,0,0]).all(axis=2))] = [1,1,1]

            img64 = cv2.cvtColor(in_img[:,:,i], cv2.COLOR_GRAY2RGB)

            total_img = img64 * frame
            
            total_img = np.clip(total_img,0,255)
            total_img = cv2.resize(total_img,self.img_size)
            predict_frames.append(total_img)
            
        print(len(predict_frames))
        return predict_frames

    # def dislay_mri_file(self,images,w,h):
        # img1,w,h,p = self.get_image(self.imgs[0],w,h)
    def list_image(self, imgs):


        
        
        # self.lqwidget.setLayout(layout)
        
        
        
        # layout = self.lqwidget.layout()
        # layout = self.remove_widget(layout)
        layout = QVBoxLayout()

        l_lb = []
        w,h = 128,128
        BPL = w*3
        for ar in range(len(imgs)):
            l_lb.append(QPushButton())
            img = cv2.resize(imgs[ar],(w,h))
            l_lb[ar].setIcon(QIcon(QPixmap.fromImage(QImage(img,w,h,BPL,QImage.Format.Format_RGB888))))
            l_lb[ar].setIconSize(QSize(128,128))
            l_lb[ar].setStyleSheet("QPushButton { border: none; }")
            
            l_lb[ar].clicked.connect(partial(self.dislay_image_event,imgs,ar))

            layout.addWidget(l_lb[ar]) 
        
        lqwidget = QWidget()
        lqwidget.setLayout(layout)

        
        self.scrol.setWidget(lqwidget)


    
    def dislay_image_event(self,imgs,ar):
        img = imgs[ar]
        
        w,h = self.img_size
        self.img_idx = ar
        self.__dislay_img_on_imgview(img,w,h)

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A: 
            if self.img_idx > 0:
                self.img_idx -= 1
        elif event.key() == Qt.Key.Key_D:
            if self.img_idx < self.max_idx -1:
                self.img_idx += 1
        w,h = self.img_size
        self.__dislay_img_on_imgview(self.imgs[self.img_idx],w,h)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MriWidget(mri_file="2400106729.nii.gzMDkvMjAvMjAyNCwgMTg6Mjc6MzM=")
    window.show()
    sys.exit(app.exec())
