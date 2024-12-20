from pymongo import MongoClient
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout


conn = MongoClient(host='localhost', port=27017)


db = conn.Productions


region_collection = db.region_collection.find()


conn.close()

conn = MongoClient(host='localhost', port=27017)


db = conn.Productions
region_collection = db.region_collection.find()
conn.close()


app = QApplication([])
window = QWidget()

# إنشاء ComboBox
cmb1 = QComboBox(window)
cmb1.addItem("DT")
cmb1.addItem("SM")
cmb1.addItem("TH")

# وضع ComboBox في واجهة المستخدم
layout = QVBoxLayout()
layout.addWidget(cmb1)
window.setLayout(layout)
window.show()

app.exec_()
