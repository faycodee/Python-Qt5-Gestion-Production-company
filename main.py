from pymongo import MongoClient
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout



def ListerRegion():
 conn = MongoClient(host='localhost', port=27017)
 db = conn.Productions
 region_collection = db.Région.find()
 for region in region_collection:
    reg.addItem(region["nom"])
 conn.close()


app = QApplication([])
window = QWidget()

# إنشاء ComboBox
reg = QComboBox(window)
ListerRegion()
# وضع ComboBox في واجهة المستخدم
layout = QVBoxLayout()
layout.addWidget(reg)
window.setLayout(layout)
window.show()

app.exec_()
