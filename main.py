from PyQt5.QtWidgets import (  # استيراد المكونات الأساسية من مكتبة PyQt5 لإنشاء الواجهة الرسومية
    QApplication, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox
)
from pymongo import MongoClient  # استيراد مكتبة MongoClient للتعامل مع قاعدة بيانات MongoDB


# وظيفة لاختبار الاتصال بخادم MongoDB والتأكد من أنه يعمل بشكل صحيح
def test_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")  # إنشاء اتصال مع MongoDB
        client.admin.command('ping')  # إرسال أمر لاختبار الاتصال
        print("MongoDB connection successful.")  # طباعة رسالة نجاح
    except Exception as e:
        print(f"Connection failed: {e}")  # طباعة رسالة فشل إذا حدث خطأ
        QMessageBox.critical(None, "Erreur", "Échec de connexion à MongoDB. Assurez-vous que le serveur est en marche.")


# وظيفة لجلب قائمة المناطق من قاعدة البيانات
def fetch_regions():
    try:
        conn = MongoClient(host='localhost', port=27017)  # إنشاء اتصال مع خادم MongoDB
        db = conn.Productions  # تحديد قاعدة البيانات
        region_collection = db.Région.find()  # استعلام للحصول على قائمة المناطق
        regions = [region["nom"] for region in region_collection]  # استخراج أسماء المناطق فقط
        conn.close()  # إغلاق الاتصال
        return regions if regions else ["Aucune région disponible"]  # إذا لم توجد مناطق، عرض رسالة
    except Exception as e:
        print(f"Error fetching regions: {e}")  # طباعة رسالة الخطأ
        return ["Erreur de connexion"]  # إذا حدث خطأ، إعادة رسالة خطأ


# وظيفة لجلب قائمة الإنتاجات بناءً على المنطقة المحددة
def fetch_productions(selected_region=None):
    try:
        client = MongoClient("mongodb://localhost:27017/")  # إنشاء اتصال مع MongoDB
        db = client["Productions"]  # تحديد قاعدة البيانات
        production_collection = db["Productions"]  # تحديد مجموعة البيانات (collection)

        # إذا تم اختيار منطقة معينة، تصفية النتائج بناءً عليها
        if selected_region and selected_region != "Toutes":
            productions = production_collection.find({"nomRégion": selected_region})
        else:
            productions = production_collection.find()  # جلب جميع البيانات في حالة عدم التصفية

        return list(productions)  # إعادة قائمة بالإنتاجات
    except Exception as e:
        print(f"Error fetching productions: {e}")  # طباعة الخطأ إذا حدث
        return []  # إعادة قائمة فارغة إذا حدث خطأ


# تعريف واجهة التطبيق الرئيسية
class ProductionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Productions")  # إعداد عنوان النافذة
        self.resize(800, 600)  # ضبط حجم النافذة

        # إنشاء تخطيطات مختلفة لتنظيم الواجهة
        self.layout = QVBoxLayout()  # التخطيط الرئيسي
        self.filter_layout = QHBoxLayout()  # تخطيط شريط الفلترة
        self.table_layout = QVBoxLayout()  # تخطيط جدول البيانات
        self.form_layout = QVBoxLayout()  # تخطيط نموذج الإدخال
        self.control_layout = QHBoxLayout()  # تخطيط أزرار التحكم

        # شريط الفلترة حسب المنطقة
        self.region_label = QLabel("Sélectionnez une région:")  # نص للإشارة إلى القائمة المنسدلة
        self.selectInput = QComboBox()  # عنصر القائمة المنسدلة
        self.selectInput.addItems(["Toutes"] + fetch_regions())  # إضافة الخيارات للقائمة
        self.selectInput.currentTextChanged.connect(self.update_table)  # ربط تغيير الخيار بتحديث الجدول

        self.filter_layout.addWidget(self.region_label)
        self.filter_layout.addWidget(self.selectInput)

        # جدول عرض البيانات
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # تحديد عدد الأعمدة
        self.table.setHorizontalHeaderLabels(  # إعداد عناوين الأعمدة
            ["CodeEntreprise", "nomRégion", "nombreEmployé", "Production", "EmployéPerformance"]
        )
        self.update_table()  # استدعاء دالة التحديث لعرض البيانات الأولية
        self.table_layout.addWidget(self.table)

        # نموذج إدخال بيانات جديدة
        self.code_label = QLabel("Code Entreprise:")  # تسمية لحقل إدخال كود الشركة
        self.code_input = QLineEdit()

        self.region_label_form = QLabel("Région:")  # تسمية لحقل إدخال المنطقة
        self.region_input = QLineEdit()

        self.employees_label = QLabel("Nombre Employé:")  # تسمية لحقل عدد الموظفين
        self.employees_input = QLineEdit()

        self.production_label = QLabel("Production:")  # تسمية لحقل الإنتاج
        self.production_input = QLineEdit()

        self.EmployéPerformance_label = QLabel("EmployéPerformance:")  # تسمية لحقل أداء الموظف
        self.EmployéPerformance_input = QLineEdit()

        # إضافة الحقول إلى تخطيط النموذج
        self.form_layout.addWidget(self.code_label)
        self.form_layout.addWidget(self.code_input)
        self.form_layout.addWidget(self.region_label_form)
        self.form_layout.addWidget(self.region_input)
        self.form_layout.addWidget(self.employees_label)
        self.form_layout.addWidget(self.employees_input)
        self.form_layout.addWidget(self.production_label)
        self.form_layout.addWidget(self.production_input)
        self.form_layout.addWidget(self.EmployéPerformance_label)
        self.form_layout.addWidget(self.EmployéPerformance_input)

        # أزرار التحكم
        self.add_button = QPushButton("Ajouter")  # زر لإضافة البيانات
        self.add_button.clicked.connect(self.add_entry)  # ربط الزر بوظيفة الإضافة

        self.delete_button = QPushButton("Supprimer")  # زر لحذف البيانات
        self.delete_button.clicked.connect(self.delete_entry)  # ربط الزر بوظيفة الحذف

        self.quit_button = QPushButton("Quitter")  # زر لإغلاق التطبيق
        self.quit_button.clicked.connect(self.close)

        # إضافة الأزرار إلى تخطيط التحكم
        self.control_layout.addWidget(self.add_button)
        self.control_layout.addWidget(self.delete_button)
        self.control_layout.addWidget(self.quit_button)

        # دمج جميع التخطيطات في التخطيط الرئيسي
        self.layout.addLayout(self.filter_layout)
        self.layout.addLayout(self.table_layout)
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.control_layout)
        self.setLayout(self.layout)

    # تحديث البيانات في الجدول
    def update_table(self):
        selected_region = self.selectInput.currentText()  # الحصول على المنطقة المحددة
        productions = fetch_productions(selected_region)  # جلب البيانات بناءً على المنطقة

        self.table.setRowCount(0)  # إعادة تعيين الصفوف
        for row, prod in enumerate(productions):  # تعبئة الجدول بالبيانات
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(prod["CodeEntreprise"])))
            self.table.setItem(row, 1, QTableWidgetItem(prod["nomRégion"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(prod["nombreEmployé"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(prod["Production"])))
            self.table.setItem(row, 4, QTableWidgetItem(prod["EmployéPerformance"]))

    # وظيفة لإضافة بيانات جديدة إلى قاعدة البيانات
    def add_entry(self):
        try:
            # قراءة البيانات المدخلة من النموذج
            code = int(self.code_input.text())
            region = self.region_input.text().strip()
            emp_count = int(self.employees_input.text())
            production = int(self.production_input.text())
            EmployéPerformance = self.EmployéPerformance_input.text().strip()

            # إدراج البيانات في MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Productions"]
            production_collection = db["Productions"]
            production_collection.insert_one({
                "CodeEntreprise": code,
                "nomRégion": region,
                "nombreEmployé": emp_count,
                "Production": production,
                "EmployéPerformance": EmployéPerformance
            })
            self.update_table()  # تحديث الجدول لعرض البيانات الجديدة

            # تفريغ الحقول بعد الإضافة
            self.code_input.clear()
            self.region_input.clear()
            self.employees_input.clear()
            self.production_input.clear()
            self.EmployéPerformance_input.clear()

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès.")  # رسالة نجاح
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur est survenue: {e}")  # عرض رسالة خطأ

    # وظيفة لحذف البيانات بناءً على السطر المحدد
    def delete_entry(self):
        selected_row = self.table.currentRow()  # الحصول على الصف المحدد
        if selected_row != -1:
            code = self.table.item(selected_row, 0).text()  # استخراج كود الشركة
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Productions"]
            production_collection = db["Productions"]
            production_collection.delete_one({"CodeEntreprise": int(code)})  # حذف البيانات من قاعدة البيانات
            self.update_table()  # تحديث الجدول
            QMessageBox.information(self, "Succès", "Entrée supprimée avec succès.")  # رسالة نجاح
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une ligne à supprimer.")  # رسالة خطأ إذا لم يتم تحديد سطر


# تشغيل التطبيق
if __name__ == "__main__":
    test_connection()  # اختبار الاتصال بقاعدة البيانات
    app = QApplication([])  # إنشاء التطبيق
    window = ProductionApp()  # إنشاء نافذة التطبيق
    window.show()  # عرض النافذة
    app.exec_()  # بدء التطبيق
