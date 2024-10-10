import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout,QApplication, QLabel,QVBoxLayout, QScrollArea, QPushButton, QProgressBar
from PyQt6.QtGui import QImage,QPixmap,QIcon, QMovie
from PyQt6.QtCore import QSize,Qt

import nibabel
import numpy as np
import cv2
from functools import partial
import urllib3
import json
import base64
import os
import asyncio
import threading
import time
class MriWidget(QWidget):
    def __init__(self, parent=None, patientID=None,size=[1520,1080], patient_name=None):
        super(MriWidget,self).__init__(parent)

        self.setGeometry(400,0,*size)

        
        self.lb = QLabel(parent=self)
        
        self.lb.setText("CT SCAN")
        self.lb.setStyleSheet("color:white;\
                              font-family: Lexend;\
                                            font-size: 48px;\
                                            font-weight: bold;\
                                            ")
        self.lb.move(49,22)
        self.lb.adjustSize()
        self.image_view = QLabel(self)
        
        
        self.icon_lb = QLabel(self)
        self.icon_lb.setGeometry(75,90,200,200)
        self.icon_lb.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon/User.png")))
        
        self.name_lb = QLabel(text=patient_name,parent=self,wordWrap=True)
        self.name_lb.setStyleSheet("font-size:26px; font-weight:bold;color:white;")
        # self.name_lb.adjustSize()
        # self.name_lb.move(75,286)
        self.name_lb.setGeometry(75,286,200,100)

        self.predict_bt = QPushButton("Dự đoán", self)
        self.predict_bt.setStyleSheet("color:#31363F; background-color:#76ABAE;font-size: 30px;color:white;")

        self.predict_bt.setGeometry(95,950,189,55)
        self.predict_bt.clicked.connect(self.predict_event)
        # self.pixmap = QPixmap(512,512)
        
        self.create_predict_widget()
        
        self.img_size = (870,870)
        self.img_idx = 0
        self.image_view.setGeometry(400,109,*self.img_size)
        
        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(400,89,870,20)
        self.prog_bar.setStyleSheet("color:black;")
        self.prog_bar.hide()
        
        
        self.list_img_layout = QVBoxLayout()
        for i in range(1000):
            bt = QPushButton()
            bt.setFixedSize(128,128)
            self.list_img_layout.addWidget(bt)
        
        self.scrol = QScrollArea(self)
        self.scrol.setGeometry(1270,0,200,1080)
        temp_wg = QWidget()
        temp_wg.setLayout(self.list_img_layout)
        temp_wg.setFixedWidth(200)
        self.scrol.setWidget(temp_wg)
        
        self.show()
        
        self.load_widget = Loadwidget(self, text="Đang tải ảnh")
        self.load_widget.setGeometry(400,0,800,400)
        self.load_widget.show()


        self.thr = threading.Thread(target=self.__dislay_when_init,args=(patientID,),daemon=True)

        self.thr.start()
        # self.thr.join()
        


    
    
    def __dislay_when_init(self, mri_file):
        self.imgs, self.max_idx = self.__get_image(mri_file=mri_file)
 
        self.imgs = self.__image_proccessing(self.imgs,*self.img_size)
        
        self.__dislay_img_on_imgview(self.imgs[0],*self.img_size)
        
        self.list_image(self.imgs)
    def __get_image(self,mri_file:str):

        stat, image = self.get_file_from_API(mri_file)
        if stat == True:
            self.load_widget.close()
            imgs= np.asarray(image.get_fdata())
            max_idx = imgs.shape[2]
            return imgs, max_idx
    
    def __dislay_img_on_imgview(self,img,w,h):
        p = w*3
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img,w,h,p,QImage.Format.Format_RGB888)))

    def get_file_from_API(self, imageId):
        http = urllib3.PoolManager()
        param = {"patientID":imageId}
        rs = http.request("POST","103.63.121.200:9012/get_image_with_patientID",body=json.dumps(param), headers={'Content-Type': 'application/json'})
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
            return True, image
            
    
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


        predict_thread = threading.Thread(target=self.predict_process,daemon=True)
        predict_thread.start()
        show_thr = threading.Thread(target=self.show_progress, daemon=True)
        show_thr.start() 
        
    def show_progress(self):
        # self.predict_bt.hide()
        # self.prog_bar.show()
        # for i in range(20):
        #     self.prog_bar.setValue(i*5)
        #     time.sleep(1)
        self.load_widget.predict("Đang dự đoán")
        # self.load_widget.setGeometry(400,0,800,400)
        self.load_widget.show()

        # print(rs.status)
    def predict_process(self):
        print("oke oke")
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
            # self.predict_bt.setText("Predict Volume is : {}".format(volume_data))
            # self.predict_bt.setStyleSheet("color:black; background-color:green;font-size: 30px;")
            self.predict_bt.setDisabled(True)
            # self.volume_label  = QLabel(self)
            # self.volume_label.setText(volume_data)
            # self.volume_label.setGeometry()
            # self.load_widget.close()
            # self.predict_bt.show()
            self.load_widget.hide()
            self.dislay_volume(volume=volume_data)
    def create_predict_widget(self):
        self.volume_lb = QWidget(parent=self)
        self.volume_lb.setGeometry(30,396,340,278)
        self.volume_lb.setStyleSheet("border:3px solid; border-radius:20px; border-color:#FFFFFF;background-color:#222831;")
        self.volume_lb.hide()
        
        self.lb = QLabel(text="Thể tích máu tụ \ndự đoán ",parent=self, alignment=Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop)
        self.lb.setGeometry(85,409,340,110)
        self.lb.setWordWrap(True)
        self.lb.setStyleSheet("color:#76ABAE;border:none;font-size:30px;")
        self.lb.adjustSize()
        self.lb.hide()
        
        self.vlb = QLabel(parent=self)
        # self.vlb.setText(volume)
        self.vlb.setStyleSheet("font-size:64px; font-weight:bold; color:#EA0107; border:none;background-color:#222831;")
        self.vlb.move(115,493)
        self.vlb.hide()
        
        
        self.mmlb = QLabel(parent=self)
        self.mmlb.setGeometry(180,570,82,44)
        self.mmlb.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon/mm.png")))
        self.mmlb.setStyleSheet("background-color:#222831;")
        self.mmlb.hide()
    
    def dislay_volume(self,volume):
        self.volume_lb.show()
        self.lb.show()
        self.vlb.setText(volume)
        self.vlb.adjustSize()
        self.vlb.show()
        self.mmlb.show()        
        
    def process_predict_data(self):
        
        imgs = nibabel.load(os.path.join(os.getcwd(),"data","output.nii.gz"))

        imgs = imgs.get_fdata()

        # imgs = imgs * 255
        imgs = imgs.astype(np.uint8)
        in_imgs = nibabel.load(os.path.join(os.getcwd(),"data","input.nii.gz"))
        in_imgs = in_imgs.get_fdata()
        in_imgs = in_imgs.astype(np.uint8)
        predict_frames = []
        for i in range(128):
            
            img64 = imgs[:,:,i]

            img64 = np.where(img64 == 1, 0, 1)
            in_img = in_imgs[:,:,i]
            # in_img *= 255
            # 
            in_img = np.multiply(in_img,img64)
            in_img = np.clip(in_img,0,255)
            in_img = in_img.astype(np.uint8)
            
            in_img = cv2.cvtColor(in_img, cv2.COLOR_GRAY2RGB)
            
            img64 = imgs[:,:,i]
            img64  = img64.astype(np.uint8)
            img64 = img64*255
            ret, labels = cv2.connectedComponents(img64)
            label_hue = np.uint8(179 * labels / np.max(labels))
            blank_ch = 255 * np.ones_like(label_hue)
            labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
            labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2RGB)
            labeled_img[label_hue == 0] = 0
            labeled_img =  in_img+labeled_img
            labeled_img = cv2.resize(labeled_img, self.img_size)
            predict_frames.append(labeled_img)




        # for i in range(128):
            
        #     frame = cv2.cvtColor(imgs[:,:,i], cv2.COLOR_GRAY2RGB)
        #     frame[np.where((frame!=[0, 0, 0]).all(axis=2))] = [255,0,0]
        #     frame[np.where((frame==[0,0,0]).all(axis=2))] = [1,1,1]

        #     img64 = cv2.cvtColor(in_imgs[:,:,i], cv2.COLOR_GRAY2RGB)

        #     total_img = img64 * frame
            
        #     total_img = np.clip(total_img,0,255)
        #     total_img = cv2.resize(total_img,self.img_size)
        #     predict_frames.append(total_img)
            
        # print(len(predict_frames))
        return predict_frames

    # def dislay_mri_file(self,images,w,h):
        # img1,w,h,p = self.get_image(self.imgs[0],w,h)
    def list_image(self, imgs):
        
        w,h = 128,128
        BPL = w*3
        for ar in range(len(imgs)):
            bt = self.list_img_layout.itemAt(ar).widget()
            img = cv2.resize(imgs[ar],(w,h))
            bt.setIcon(QIcon(QPixmap.fromImage(QImage(img,w,h,BPL,QImage.Format.Format_RGB888))))
            bt.setIconSize(QSize(128,128))
            bt.setStyleSheet("QPushButton { border: none; }")
            
            bt.clicked.connect(partial(self.dislay_image_event,imgs,ar))

            # layout.addWidget(l_lb[ar]) 
        



    
    def dislay_image_event(self,imgs,ar):
        img = imgs[ar]
        
        w,h = self.img_size
        self.img_idx = ar
        self.__dislay_img_on_imgview(img,w,h)

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A: 
            if self.img_idx > 0:
                self.img_idx -= 1
                w,h = self.img_size
                self.__dislay_img_on_imgview(self.imgs[self.img_idx],w,h)
        elif event.key() == Qt.Key.Key_D:
            if self.img_idx < self.max_idx -1:
                self.img_idx += 1
                w,h = self.img_size
                self.__dislay_img_on_imgview(self.imgs[self.img_idx],w,h)
  

class Loadwidget(QWidget):
    def __init__(self, parent=None,text=None):
        super(Loadwidget, self).__init__(parent=parent)
        self.load_icon = QLabel(self)
        self.load_icon.setGeometry(0,0,100,100)
        movie = QMovie(os.path.join(os.getcwd(),"icon","loading.gif"))
        self.load_icon.setMovie(movie)
        movie.start()
        self.text = QLabel(self)
        self.text.setGeometry(110,25,500,50)
        self.text.setText(text)
        self.text.setStyleSheet("font-family: Lexend;\
                                            font-size: 45px;\
                                            font-weight: 700;\
                                            line-height: 56.25px;\
                                            text-align: left;\
                                            color:white;\
                                            ")
    def predict(self, text=None):
        self.text.setText(text)
        self.text.adjustSize()
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MriWidget(mri_file="2400106729.nii.gzMDkvMjAvMjAyNCwgMTg6Mjc6MzM=")
    window.show()
    sys.exit(app.exec())
