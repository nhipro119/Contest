from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,QDateEdit,QApplication, QFormLayout,QFileDialog,QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QDateTime, QSize,QDate
import json
import sys
import urllib3
import os
import base64
import asyncio
from widget import mriView
class PatientWidget(QWidget):
    def __init__(self, parent=None, patient_info= None):
        super(PatientWidget, self).__init__(parent)
        # self.setGeometry(400,0,1520,1080)
        self.setStyleSheet("background-color:#222831")
        self.create_form()
        self.path = ""
        
        self.patient_info = patient_info
        self.view_info(patient_info=patient_info)
    def create_form(self):
        user_icon = QLabel(parent=self)
        user_icon.setPixmap(QPixmap(os.path.join(os.getcwd(),"icon/User.png")))
        user_icon.setGeometry(27,128,200,200)
        patien_lb = QLabel(text="Thông tin bệnh nhân", parent=self)
        patien_lb.setGeometry(49,22,451,58)
        patien_lb.setStyleSheet("font-size:48px; font-weight:bold;color:white;")
        patien_lb.adjustSize()
        # patien_lb.setWordWrap(True)
        self.form = QFormLayout(self)
        
        # self.sex.move(700,10)
        infolabel(text="Họ và Tên", parent=self,h=147)

        self.nameTb = wordedit(parent=self,geometry=[295,199,508,58])


        
        infolabel(text="Giới tính", parent=self,h=285)


        self.sex = QCheckBox(text="",parent=self)
        # self.sex.setFixedSize(100,100)
        self.sex.move(295,345)
        self.sex.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}")

        nam = infolabel(text="Nam", parent=self, w=330,h=335)
        # self.form.addRow(gioitinh, self.sex)
        
        infolabel(text="Số điện thoại",parent=self,h=391)
        
        self.sdtTb = wordedit(parent=self,geometry=[295,443, 508,58])
        # self.form.addRow(sdt, self.sdtTb)
        
        infolabel(text="Ngày tháng năm sinh", parent=self,h=538)
        

        self.dateTb = QDateEdit(parent=self, calendarPopup=True)
        self.dateTb.setDateTime(QDateTime.currentDateTime())
        self.dateTb.setDisplayFormat("dd/MM/yyyy")
        self.dateTb.setStyleSheet("font-size:20px; color:white;")
        self.dateTb.setGeometry(295,590, 508,58)


        infolabel(text="Địa chỉ", parent=self, h=676)

        self.addressTb = wordedit(parent=self,geometry=[295,728,508,58])

        # mri_image_lb = QLabel(parent=self, text="CT Scan File")
        # mri_image_lb.move(855,92)
        # mri_image_lb.adjustSize()
        self.choose_file_bt = QPushButton(parent=self)
        self.choose_file_bt.setGeometry(855,135,513,785)
        self.choose_file_bt.setIcon(QIcon(os.path.join(os.getcwd(),"icon/upload.png")))
        self.choose_file_bt.setIconSize(QSize(513,785))
        self.choose_file_bt.clicked.connect(self.choose_file_event)
        
        self.save_bt = QPushButton(parent=self, text="Tải lên")
        self.save_bt.setStyleSheet(" background-color:#76ABAE; color:#31363F; border-radius:10px;font-size:25px")
        self.save_bt.setGeometry(614,950,189,55)
        self.save_bt.clicked.connect(self.create_event)
        

        
        # self.create_bt = QPushButton(text="create", parent=self)
        # self.create_bt.clicked.connect(self.create_event)
        # self.form.addRow(self.create_bt)
        self.view_bt = QPushButton(parent=self, text="Xem ảnh")
        self.view_bt.setGeometry(1179, 950, 189, 55)
        self.view_bt.setStyleSheet(" background-color:#76ABAE; color:#31363F; border-radius:10px;color:white; font-size:20px;")
        self.view_bt.clicked.connect(self.view_event)
        self.view_bt.hide()
        # self.setLayout(self.form)
        
    def check_empty(self):
        box = [self.nameTb, self.dateTb, self.addressTb, self.sdtTb]
        for b in box:
            if b.text().strip() == "":
                return False
        return True
    
    def create_event(self):
        if self.parent().auth_id == None:
            self.set_notice(title="warning", text="bạn chưa đăng nhập",icon=QMessageBox.Icon.Critical)
            return
        if not self.check_empty():
            self.parent().set_notice(title="warning", text="không được để trống các thông tin",icon=QMessageBox.Icon.Critical)
            return 
        if self.path == "":
            self.parent().set_notice(title="warning", text="bạn chưa chọn tệp CT ",icon=QMessageBox.Icon.Critical)
            return

        
        sex = True if self.sex.isChecked() else False
        datas,names = self.read_file(path=self.path)
        name = self.path.split("/")[-1]
        
        param = json.dumps({"name":self.nameTb.text(),
                 "phone": self.sdtTb.text(),
                 "sex": sex,
                 "birth":str(self.dateTb.date().toPyDate()),
                 "job": None,
                 "address": self.addressTb.text(),
                 "authID":self.parent().auth_id,
                 "image_datas":datas,
                 "dir_name":name,
                 "image_names":names
                 })
        self.upload_file(param)
        



    
        
    def upload_file(self,param):
        http = urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9012/create-patient", body = param,headers={'Content-Type': 'application/json'})
        if rs.status ==  200:
            id = json.loads(rs.data.decode("ascii"))["id"]
            self.parent().notice_label.close()
            self.parent().set_notice(title="success", text="Thêm bệnh nhân thành công", icon=QMessageBox.Icon.Information)
            self.parent().set_mainview(mriView.MriWidget(parent=self.parent(),patientID=id, patient_name=self.nameTb.text()))



            
    def read_file(self, path):
        lfs = os.listdir(self.path)
        datas = []
        names = []
        for lf in lfs:
            with open(os.path.join(self.path,lf),"rb") as f:
                data = f.read()
                data = base64.b64encode(data)
                data = data.decode("ascii")
                datas.append(data)
                names.append(lf)
        print(type(datas[0]))
        print(type(names[0]))
        return json.dumps(datas), json.dumps(names)

    def view_event(self):
        self.parent().set_mainview(mriView.MriWidget(parent=self.parent(),patientID=self.patient_info["patientID"], patient_name=self.patient_info["name"]))
        
    def choose_file_event(self):
        self.path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        print("path is:",self.path)
        # self.path = QFileDialog.getOpenFileName(None, 'Chọn ảnh CT', os.getcwd(),"(*.zip)")
        # print(self.path)
        if self.path != "":
            lf = os.listdir(self.path)
            for l in lf:
                if not l.lower().endswith(".dcm"):
                    self.parent().set_notice(title="warning", text="Thư mục đang chọn chứa tệp tin không phải dicom",icon=QMessageBox.Icon.Critical)
                    self.path = ""
                    return
            
            self.choose_file_bt.setIcon(QIcon(os.path.join(os.getcwd(),"icon/uploaded.png")))
    
    def view_info(self, patient_info:dict):
        if patient_info != None:
            self.nameTb.setText(patient_info["name"])
            self.nameTb.setDisabled(True)
            
            self.sdtTb.setText(patient_info["phone"])
            self.sdtTb.setDisabled(True)
            
            self.addressTb.setText(patient_info["address"])
            self.addressTb.setDisabled(True)
            
            self.sex.setChecked(patient_info["sex"])
            self.sex.setDisabled(True)
            
            self.dateTb.setDate(QDate.fromString(patient_info["birth"],"dd/MM/yyyy"))
            self.dateTb.setDisabled(True)
            
            self.choose_file_bt.setIcon(QIcon(os.path.join(os.getcwd(),"icon/uploaded.png")))
            self.choose_file_bt.setDisabled(True)
            
            self.save_bt.hide()
            
            self.view_bt.show()
    
    
class infolabel(QLabel):
    def __init__(self,parent= None, text="", w=295,h=0):
        super(infolabel,self).__init__(parent=parent)
        
        self.setText(text)
        self.setStyleSheet("font-size:30px; color:#FFFFFF;")
        self.adjustSize()
        self.move(w,h)
class wordedit(QLineEdit):
    def __init__(self, parent=None, geometry=[0,0,0,0]):
        super(wordedit, self).__init__(parent=parent)
        self.setStyleSheet("border: 1px solid; border-radius:7; border-color:#EEEEEE; color:#FFFFFF;font-size:20px;")
        self.setGeometry(*geometry)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    
    window = PatientWidget()
    window.show()
    sys.exit(app.exec())        