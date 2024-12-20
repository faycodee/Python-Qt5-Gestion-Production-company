from pymongo import MongoClient


conn = MongoClient(host='localhost', port=27017)


db = conn.Productions


region_collection = db.region_collection.find()


conn.close()


from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout

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
