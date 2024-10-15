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
        self.volume_lb.setGeometry(30,396,340,550)
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
        self.vlb.setStyleSheet("font-size:40px; font-weight:bold; color:#EA0107; border:none;background-color:#222831;")
        self.vlb.move(50,493)
        self.vlb.hide()
        
        self.tong_so_vung_lb = QLabel(self)
        self.tong_so_vung_lb.move(50,545)
        self.tong_so_vung_lb.setStyleSheet("font-size:30px; color:white; ")
        self.tong_so_vung_lb.hide()
        
        # self.mmlb = QLabel(parent=self)
        # self.mmlb.setGeometry(200,493,82,44)
        # self.mmlb.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon/mm.png")))
        # self.mmlb.setStyleSheet("background-color:#222831;")
        # self.mmlb.hide()

        self.svllo = QVBoxLayout()
        self.vllbs = []
        svlwg = QWidget()
        for i in range(100):
            vlwg = VolumeClassWidget(svlwg)
            vlwg.setStyleSheet("border-color: white;")
            self.svllo.addWidget(vlwg)
            self.vllbs.append(vlwg)
        
        svlwg.setLayout(self.svllo)
        self.svla = QScrollArea(self)
        self.svla.setGeometry(35,600,330,300)
        self.svla.setWidget(svlwg)
        self.svla.verticalScrollBar().hide()
        self.svla.horizontalScrollBar().hide()
        self.svla.setStyleSheet("border:None;")
        # self.svla.show()
        

    def dislay_volume(self,volume):
        self.volume_lb.show()
        self.lb.show()
        str_volume = "Tổng: {} ml".format(volume)
        self.vlb.setText(str_volume)
        self.vlb.adjustSize()
        self.vlb.show()
        self.tong_so_vung_lb.show()
        # self.mmlb.show()        
        
    def process_predict_data(self):
        
        out_imgs = nibabel.load(os.path.join(os.getcwd(),"data","output.nii.gz"))

        pixdim = out_imgs.header["pixdim"][1:4]
        self.pixdim = pixdim[0]*pixdim[1]*pixdim[2]

        
        out_imgs = out_imgs.get_fdata()
        out_imgs = out_imgs.astype(np.uint8)
        out_imgs *= 255

        in_imgs = nibabel.load(os.path.join(os.getcwd(),"data","input.nii.gz"))
        in_imgs = in_imgs.get_fdata()
        in_imgs = in_imgs.astype(np.uint8)


        
        areas = []
        num_area = 1
        pi = 3.14156
        labeled_imgs = []
        predict_frames = []
        for i in range(self.max_idx):
        # print("hinh",i,":",end=" ")
            ret, labels = cv2.connectedComponents(out_imgs[:,:,i])
            # new_area = np.where(labels == 1)
            
            # print(new_area)
            
            new_areas = []
            area_each_image = {}
            for dem1 in range(len(areas)):
                areas[dem1].discontinous()
            for r in range(1,ret):
                check_overlap = False
                new_area = np.where(labels == r)
                new_area = new_area[0]+pi*new_area[1]
                new_area = new_area.tolist()
                
                for idx,ar in enumerate(areas):
                    overlap = set(ar.ar).intersection(set(new_area))
                    if len(overlap) > 0:
                        areas[idx].translate_area(new_area)
                        check_overlap = True
                        area_each_image[r] = areas[idx].area_idx

                        break
                    
                        # areas[idx].discontinous()
                    
                if not check_overlap:
                    
                    new_areas.append([new_area,r])

                

            for dem2 in range(len(areas)):
                if not areas[dem2].continous:
                    areas[dem2].ar = []
            for new_area in new_areas:
                areas.append(Area(new_area[0],num_area))
                area_each_image[new_area[1]] = num_area
                num_area += 1
            zero = np.zeros(shape=labels.shape)
            for aai in area_each_image.keys():

                # print("anh co vung ", aai, " thuoc area ",area_each_image[aai])
                temp = np.where(labels == aai, area_each_image[aai],0)
                zero = zero + temp
            labeled_imgs.append(zero)
            # for aai in area_each_image.keys():
            #     labels = np.where(labels == aai, area_each_image[aai],labels)
            # labeled_imgs.append(labels)


        for i in range(len(labeled_imgs)):
            # print(np.max(np.asarray(labeled_imgs)))
            label_hue = np.uint8(179 * labeled_imgs[i] / np.max(np.asarray(labeled_imgs)))
            blank_ch = 255 * np.ones_like(label_hue)
            labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
            
            labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2RGB)
            labeled_img[label_hue == 0] = 0
            img64 = out_imgs[:,:,i]

            img64 = np.where(img64 == 255, 0, 1)
            in_img = in_imgs[:,:,i]
            # in_img *= 255
            # 
            in_img = np.multiply(in_img,img64)
            in_img = in_img.astype(np.uint8)
            
            in_img = cv2.cvtColor(in_img, cv2.COLOR_GRAY2RGB)
            
            # img64 = out_imgs[:,:,i]
            # img64  = img64.astype(np.uint8)
            # img64 = img64*255
            labeled_img =  in_img+labeled_img
            labeled_img = cv2.resize(labeled_img, self.img_size)
            predict_frames.append(labeled_img)
        areas.sort(reverse = True, key = key)
        self.tong_so_vung_lb.setText("Có {} vùng tụ máu".format(len(areas)))
        for i in range(min(len(areas),100)):
            self.vllbs[i].set_value(areas[i].area_idx, areas[i].NOP*self.pixdim/1000, len(areas))



#############IMG 2 ####################################
        # imgs = imgs.get_fdata()

        # # imgs = imgs * 255
        # imgs = imgs.astype(np.uint8)
        # in_imgs = nibabel.load(os.path.join(os.getcwd(),"data","input.nii.gz"))
        # in_imgs = in_imgs.get_fdata()
        # in_imgs = in_imgs.astype(np.uint8)
        # predict_frames = []
        # for i in range(128):
            
        #     img64 = imgs[:,:,i]

        #     img64 = np.where(img64 == 1, 0, 1)
        #     in_img = in_imgs[:,:,i]
        #     # in_img *= 255
        #     # 
        #     in_img = np.multiply(in_img,img64)
        #     in_img = np.clip(in_img,0,255)
        #     in_img = in_img.astype(np.uint8)
            
        #     in_img = cv2.cvtColor(in_img, cv2.COLOR_GRAY2RGB)
            
        #     img64 = imgs[:,:,i]
        #     img64  = img64.astype(np.uint8)
        #     img64 = img64*255
        #     ret, labels = cv2.connectedComponents(img64)
        #     label_hue = np.uint8(179 * labels / np.max(labels))
        #     blank_ch = 255 * np.ones_like(label_hue)
        #     labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        #     labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2RGB)
        #     labeled_img[label_hue == 0] = 0
        #     labeled_img =  in_img+labeled_img
        #     labeled_img = cv2.resize(labeled_img, self.img_size)
        #     predict_frames.append(labeled_img)



##################img 1#######################
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

class VolumeClassWidget(QWidget):
    def __init__(self, parent = None):
        super(VolumeClassWidget,self).__init__(parent=parent)
        self.setFixedSize(400,100)
        self.colorlb = QLabel(parent=self)
        self.colorlb.setGeometry(0,0,100,100)
        self.textlb = QLabel(self)
        self.textlb.move(110,0)
        self.textlb.setStyleSheet("color:white; font-size:30px;")

        
    def set_value(self, color, volumevalue, max_color):
        self.colorlb.setPixmap(self.convert_cv_to_qt(color=color, max_color=max_color))
        str_volume = "{price:.3f} ml".format(price= volumevalue)
        self.textlb.setText(str_volume)
        self.textlb.adjustSize()
    def convert_cv_to_qt(self, color, max_color):
        print("widget_color:",max_color)
        array = np.full(shape=(100,100),fill_value=color)
        label_hue = np.uint8(179 * array / np.max(np.asarray(max_color)))
        blank_ch = 255 * np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2RGB)
        labeled_img[label_hue == 0] = 0
        
        w,h,ch = labeled_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(labeled_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        # p = convert_to_Qt_format.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(convert_to_Qt_format)
    
class Area:
    def __init__(self, ar, area_idx):
        self.ar = ar
        self.continous = True
        self.area_idx = area_idx
        self.NOP = len(ar)
    def translate_area(self, new_area):
        self.ar = new_area
        self.NOP += len(new_area)
        self.continous = True
    def discontinous(self):
        self.continous = False
def key(a:Area):
        return a.NOP