from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox
)
from pymongo import MongoClient


def fetch_regions():
    conn = MongoClient(host='localhost', port=27017)
    db = conn.Productions
    region_collection = db.Région.find()
    regions = [region["nom"] for region in region_collection]
    conn.close()
    return regions





def fetch_productions(selected_region=None):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Productions"]
    production_collection = db["Productions"]

    if selected_region:
        productions = production_collection.find({"nomRégion": selected_region})
    else:
        productions = production_collection.find()
    
    return list(productions)


class ProductionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Productions")
        self.resize(800, 600)

        self.layout = QVBoxLayout()
        self.filter_layout = QHBoxLayout()
        self.table_layout = QVBoxLayout()
        self.form_layout = QVBoxLayout()
        self.control_layout = QHBoxLayout()

        # Filter by region
        self.region_label = QLabel("Sélectionnez une région:")
        self.selectInput = QComboBox()
        self.selectInput.addItems(fetch_regions())
        self.selectInput.currentTextChanged.connect(self.update_table)

        self.filter_layout.addWidget(self.region_label)
        self.filter_layout.addWidget(self.selectInput)

        # Table for displaying production data
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["CodeEntreprise", "nomRégion", "nombreEmployé", "Production", "EmployéPerformance"]
        )
        self.update_table()
        self.table_layout.addWidget(self.table)

        # Input form for new production
        self.code_label = QLabel("Code Entreprise:")
        self.code_input = QLineEdit()

        self.region_label_form = QLabel("Région:")
        self.region_input = QLineEdit()

        self.employees_label = QLabel("Nombre Employé:")
        self.employees_input = QLineEdit()

        self.production_label = QLabel("Production:")
        self.production_input = QLineEdit()

        self.EmployéPerformance_label = QLabel("EmployéPerformance:")
        self.EmployéPerformance_input = QLineEdit()

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

        # Buttons
        self.add_button = QPushButton("Ajouter")
        self.add_button.clicked.connect(self.add_entry)

        self.delete_button = QPushButton("Supprimer")
        self.delete_button.clicked.connect(self.delete_entry)

        self.quit_button = QPushButton("Quitter")
        self.quit_button.clicked.connect(self.close)

        self.control_layout.addWidget(self.add_button)
        self.control_layout.addWidget(self.delete_button)
        self.control_layout.addWidget(self.quit_button)

        # Combine layouts
        self.layout.addLayout(self.filter_layout)
        self.layout.addLayout(self.table_layout)
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.control_layout)
        self.setLayout(self.layout)

    def update_table(self):
        selected_region = self.selectInput.currentText()
        productions = fetch_productions(selected_region)

        self.table.setRowCount(0)
        for row, prod in enumerate(productions):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(prod["CodeEntreprise"])))
            self.table.setItem(row, 1, QTableWidgetItem(prod["nomRégion"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(prod["nombreEmployé"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(prod["Production"])))
            self.table.setItem(row, 4, QTableWidgetItem(prod["EmployéPerformance"]))

    def add_entry(self):
        # Validate and collect input
        try:
            code = int(self.code_input.text())
            region = self.region_input.text().strip()
            emp_count = int(self.employees_input.text())
            production = int(self.production_input.text())
            EmployéPerformance = self.EmployéPerformance_input.text().strip()

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
            self.update_table()

            # Clear inputs after insertion
            self.code_input.clear()
            self.region_input.clear()
            self.employees_input.clear()
            self.production_input.clear()
            self.EmployéPerformance_input.clear()

            QMessageBox.information(self, "Succès", "Entrée ajoutée avec succès.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Une erreur est survenue: {e}")

    def delete_entry(self):
        # Delete the selected entry
        selected_row = self.table.currentRow()
        if selected_row != -1:
            code = self.table.item(selected_row, 0).text()
            client = MongoClient("mongodb://localhost:27017/")
            db = client["Productions"]
            production_collection = db["Productions"]
            production_collection.delete_one({"CodeEntreprise": int(code)})
            self.update_table()
            QMessageBox.information(self, "Succès", "Entrée supprimée avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une ligne à supprimer.")


if __name__ == "__main__":
    app = QApplication([])
    window = ProductionApp()
    window.show()
    app.exec_()
