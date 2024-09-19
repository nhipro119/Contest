from PyQt6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QHeaderView

import sys
import urllib3
import json
class InventoryWidget(QWidget):
    def __init__(self, parent=None):
        super(InventoryWidget, self).__init__(parent)
        self.table = QTreeWidget(self)
        self.table.setGeometry(200,0,400,400)
        self.table = self.add_table_field(self.table)
        self.add_data_in_treeView()
    def add_table_field(self, tb:QTreeWidget):
        self.table.setHeaderLabels(["STT","Tên hình ảnh","Tên bệnh nhân","Ngày tạo"])
        # tb.setHeader(QHeaderView())
        # tb.setHeaderItem(QTreeWidgetItem("Tên hình ảnh"))
        # tb.setHeaderItem(QTreeWidgetItem("Tên bệnh nhân"))
        # tb.setHeaderItem(QTreeWidgetItem("Ngày tạo"))
        return tb
    def get_data(self):
        auth_id = self.parent().auth_id
        param = json.dumps({"auth_id":auth_id})
        http = urllib3.PoolManager()
        rs = http.request("POST","103.63.121.200:9012/inventory", body=auth_id)
    def add_data_in_treeView(self):
        
        item = QTreeWidgetItem(["A","b"])
        self.table.addTopLevelItem(item)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryWidget()
    window.show()
    sys.exit(app.exec())
