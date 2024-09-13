import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout,QApplication, QLabel,QVBoxLayout, QScrollArea, QPushButton
from PyQt6.QtGui import QImage,QPixmap,QIcon
from PyQt6.QtCore import QSize,Qt
import nibabel
import numpy as np
import cv2
from functools import partial
class MriWidget(QWidget):
    def __init__(self, parent=None, mri_file=None):
        super(MriWidget,self).__init__(parent)
        self.setFixedSize(800,800)
        self.total_layout = QVBoxLayout(self)
        self.imgL = QLabel()
        
        b = QPushButton()
        b.setIconSize
        self.pixmap = QPixmap(512,512)
        
        image = nibabel.load(mri_file)
        self.img_idx = 0
    
        self.imgs= np.asarray(image.get_fdata())
        self.max_idx = self.imgs.shape[2]
        self.image_view = QLabel()
        img1,w,h,p = self.get_image(self.imgs[:,:,0])
        self.image_view.setPixmap(QPixmap.fromImage(QImage(img1,w,h,p,QImage.Format.Format_RGB888)))
        self.total_layout.addWidget(self.image_view)
        
        # self.imgL.setPixmap(QPixmap.fromImage(qimage))
        # self.total_layout.addChildWidget(self.imgL)
        self.list_image()
        self.setLayout(self.total_layout)
    
    def get_image(self,img, w=512,h=512):
        cv_img = img.astype(np.uint8)
        frame = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        frame = cv2.resize(frame,(w,h))
        bytesPerLine = 3 * w
        return frame, w,h,bytesPerLine
    def list_image(self):
        qvbox = QHBoxLayout()
        l_lb = []
        for ar in range(self.imgs.shape[2]):
            l_lb.append(QPushButton())

            # l_lb[ar].set_id(ar)
            print(ar)
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
        # lqwidget.setFixedSize(150,500)  
        self.lqwidget.setLayout(qvbox)

        scroll = QScrollArea()
        # scroll.setWidgetResizable(True)
        scroll.setFixedHeight(170)
        scroll.setFixedWidth(780)
        scroll.setWidget(self.lqwidget)
        self.total_layout.addWidget(scroll)
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
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = MriWidget(mri_file="2400106729.nii.gz")
    a.show()
    sys.exit(app.exec())