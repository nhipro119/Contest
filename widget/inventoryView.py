from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QHeaderView

import sys
import urllib3
import json
import mriView
class InventoryWidget(QWidget):
    def __init__(self, parent=None, auth_id= None):
        super(InventoryWidget, self).__init__(parent)
        self.table = QTreeWidget(self)
        self.table.setGeometry(200,0,400,400)
        self.table = self.add_table_field(self.table)
        # self.add_data_in_treeView()
        self.auth_id = auth_id
        self.get_data()
        self.table.doubleClicked.connect(self.click_treeview_event)
    def add_table_field(self, tb:QTreeWidget):
        self.table.setHeaderLabels(["STT","Tên hình ảnh","Tên bệnh nhân","Ngày tạo"])
        return tb
    def get_data(self):
        auth_id = self.auth_id
        param = json.dumps({"authID":auth_id})
        http = urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9012/inventory", body=param,headers={'Content-Type': 'application/json'})
        if rs.status == 200:
            data = rs.data.decode("ascii")
            data = json.loads(data)
            self.load_data_to_table(data)
    def load_data_to_table(self, data):
        datas = data["list file"]
        print(datas)
        for i,d in enumerate(datas):
            item = TreeItem(id=d[0])
            item.setText(0,str(i))
            item.setText(1,d[1])
            item.setText(2,d[3])
            item.setText(3,d[2])
            self.table.addTopLevelItem(item)
    
    def click_treeview_event(self):
        print(self.table.currentItem().IdName)
        
class TreeItem(QTreeWidgetItem):
    def __init__(self, id=None):
        super(TreeItem,self).__init__()
        self.IdName = id
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryWidget(auth_id="Y2hpdGhpZW4yMDI0LTA5LTIwIDE2OjE4OjAyLjg3ODE5OQ==")
    window.show()
    sys.exit(app.exec())
