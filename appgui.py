import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
    QDateEdit, QGridLayout, QMessageBox, QScrollArea, QGroupBox, QSizePolicy, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, Qt

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FlowSheetGenerator(QWidget):
    def __init__(self, on_submit):
        super().__init__()
        self.on_submit = on_submit
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gregg's Flow Sheet Generator | v0.2")
        self.setWindowIcon(QIcon(resource_path('icon.ico')))
        self.setMinimumSize(1200, 800)  # Set minimum size for the window

        main_layout = QVBoxLayout()

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Flow Sheet Type Selection
        flow_sheet_type_layout = QHBoxLayout()
        flow_sheet_type_layout.addWidget(QLabel("Select Flow Sheet Type:"))
        self.flow_sheet_type_combo = QComboBox()
        self.flow_sheet_type_combo.addItems(["24 Hour Flow Sheet", "13 Hour Flow Sheet"])
        self.flow_sheet_type_combo.currentIndexChanged.connect(self.update_form_for_flow_sheet_type)
        flow_sheet_type_layout.addWidget(self.flow_sheet_type_combo)
        scroll_layout.addLayout(flow_sheet_type_layout)

        # Patient Info Section
        patient_info_group = QGroupBox()
        patient_info_layout = QGridLayout()
        self.cpr_dnr_combo = QComboBox()
        self.cpr_dnr_combo.addItems(["CPR", "DNR"])
        patient_info_layout.addWidget(QLabel("CPR/DNR"), 0, 0)
        patient_info_layout.addWidget(self.cpr_dnr_combo, 0, 1)

        self.patient_entry = QLineEdit()
        self.patient_entry.setPlaceholderText("Enter Patient Name")
        patient_info_layout.addWidget(QLabel("Patient:"), 0, 2)
        patient_info_layout.addWidget(self.patient_entry, 0, 3)

        self.chart_entry = QLineEdit()
        self.chart_entry.setPlaceholderText("Enter Chart Number")
        patient_info_layout.addWidget(QLabel("Chart #:"), 0, 4)
        patient_info_layout.addWidget(self.chart_entry, 0, 5)

        self.date_entry = QDateEdit()
        self.date_entry.setDate(QDate.currentDate())
        self.date_entry.setCalendarPopup(True)
        patient_info_layout.addWidget(QLabel("Date:"), 0, 6)
        patient_info_layout.addWidget(self.date_entry, 0, 7)

        self.a_entry = QLineEdit()
        self.a_entry.setPlaceholderText("Enter A Value")
        patient_info_layout.addWidget(QLabel("A:"), 1, 0)
        patient_info_layout.addWidget(self.a_entry, 1, 1)

        self.owner_entry = QLineEdit()
        self.owner_entry.setPlaceholderText("Enter Owner Name")
        patient_info_layout.addWidget(QLabel("Owner:"), 1, 2)
        patient_info_layout.addWidget(self.owner_entry, 1, 3)

        self.problem_entry = QLineEdit()
        self.problem_entry.setPlaceholderText("Enter Problem")
        patient_info_layout.addWidget(QLabel("Problem:"), 1, 4)
        patient_info_layout.addWidget(self.problem_entry, 1, 5, 1, 2)

        self.dvm_entry = QLineEdit()
        self.dvm_entry.setPlaceholderText("Enter DVM")
        patient_info_layout.addWidget(QLabel("DVM:"), 1, 7)
        patient_info_layout.addWidget(self.dvm_entry, 1, 8)

        self.e_entry = QLineEdit()
        self.e_entry.setPlaceholderText("Enter E Value")
        patient_info_layout.addWidget(QLabel("E:"), 2, 0)
        patient_info_layout.addWidget(self.e_entry, 2, 1)

        self.age_entry = QLineEdit()
        self.age_entry.setPlaceholderText("Enter Age")
        patient_info_layout.addWidget(QLabel("Age:"), 2, 2)
        patient_info_layout.addWidget(self.age_entry, 2, 3)

        self.sex_entry = QLineEdit()
        self.sex_entry.setPlaceholderText("Enter Sex")
        patient_info_layout.addWidget(QLabel("Sex:"), 2, 4)
        patient_info_layout.addWidget(self.sex_entry, 2, 5)

        self.weight_entry = QLineEdit()
        self.weight_entry.setPlaceholderText("Enter Weight (lbs)")
        self.weight_entry.textChanged.connect(self.update_kg_from_lbs)
        patient_info_layout.addWidget(QLabel("Weight (lbs):"), 2, 6)
        patient_info_layout.addWidget(self.weight_entry, 2, 7)

        self.wt_kg_entry = QLineEdit()
        self.wt_kg_entry.setPlaceholderText("Enter Weight (kg)")
        self.wt_kg_entry.textChanged.connect(self.update_lbs_from_kg)
        patient_info_layout.addWidget(QLabel("Weight (kg):"), 2, 8)
        patient_info_layout.addWidget(self.wt_kg_entry, 2, 9)

        self.ivc_entry = QLineEdit()
        self.ivc_entry.setPlaceholderText("Enter IVC Info")
        patient_info_layout.addWidget(QLabel("IVC Size/Site/Date:"), 3, 0)
        patient_info_layout.addWidget(self.ivc_entry, 3, 1)

        self.techs_entry = QLineEdit()
        self.techs_entry.setPlaceholderText("Enter Techs")
        patient_info_layout.addWidget(QLabel("Techs:"), 3, 2)
        patient_info_layout.addWidget(self.techs_entry, 3, 3)

        patient_info_group.setLayout(patient_info_layout)
        scroll_layout.addWidget(patient_info_group)

        # Procedures and Treatments Section
        self.procedures_treatments_layout = QHBoxLayout()

        # Procedures Section
        self.procedures_group = QGroupBox("Procedures")
        self.procedures_layout = QVBoxLayout()
        self.procedure_entries = []

        self.add_procedure_btn = QPushButton("Add Procedure")
        self.add_procedure_btn.setFixedWidth(150)
        self.add_procedure_btn.setFixedHeight(40)
        self.add_procedure_btn.clicked.connect(self.add_procedure)
        self.procedures_layout.addWidget(self.add_procedure_btn, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.procedures_group.setLayout(self.procedures_layout)
        self.procedures_treatments_layout.addWidget(self.procedures_group, 1)

        # Treatments Section
        treatments_group = QGroupBox("Treatments")
        self.treatments_layout = QVBoxLayout()
        self.treatment_entries = []

        quick_add_layout = QHBoxLayout()
        self.apply_start_hour = QLineEdit()
        self.apply_start_hour.setPlaceholderText("Start Hour")
        quick_add_layout.addWidget(QLabel("Quick Add - Start Hour:"))
        quick_add_layout.addWidget(self.apply_start_hour)

        self.apply_freq = QLineEdit()
        self.apply_freq.setPlaceholderText("Frequency")
        quick_add_layout.addWidget(QLabel("Frequency:"))
        quick_add_layout.addWidget(self.apply_freq)

        apply_to_all_btn = QPushButton("Apply to All")
        apply_to_all_btn.setFixedWidth(150)
        apply_to_all_btn.setFixedHeight(40)
        apply_to_all_btn.clicked.connect(self.apply_to_all_treatments)
        quick_add_layout.addWidget(apply_to_all_btn)

        self.treatments_layout.addLayout(quick_add_layout)

        # Define treatments – note that our updated code handles special treatments
        treatments = [
            "Temperature", "Pulse", "Respiratory Rate", "MMCRT", "IV Fluids / Rate", "Additives",
            "Check IVC", "Walk/Litter", "Urine (+/-)", "Stool (+/-)", "Vomit (+/-)", "Food / Water"
        ]

        for treatment in treatments:
            self.add_treatment(treatment)

        treatments_group.setLayout(self.treatments_layout)
        self.procedures_treatments_layout.addWidget(treatments_group, 1)

        scroll_layout.addLayout(self.procedures_treatments_layout)

        # Medications Section
        medications_group = QGroupBox("Medications")
        self.medications_layout = QVBoxLayout()
        self.medication_entries = []

        add_medication_btn = QPushButton("Add Medication")
        add_medication_btn.setFixedWidth(150)
        add_medication_btn.setFixedHeight(40)
        add_medication_btn.clicked.connect(self.add_medication)
        self.medications_layout.addWidget(add_medication_btn, alignment=Qt.AlignTop | Qt.AlignLeft)

        medications_group.setLayout(self.medications_layout)
        scroll_layout.addWidget(medications_group)

        # Bottom Section
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)  # Add stretch to push the elements to the right

        self.initials_entry = QLineEdit()
        self.initials_entry.setPlaceholderText("Enter Initials")
        self.initials_entry.setFixedWidth(150)
        bottom_layout.addWidget(QLabel("Initials:"))
        bottom_layout.addWidget(self.initials_entry)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit)
        bottom_layout.addWidget(submit_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_all_fields)
        bottom_layout.addWidget(clear_btn)

        scroll_layout.addLayout(bottom_layout)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def update_form_for_flow_sheet_type(self):
        selected_type = self.flow_sheet_type_combo.currentText()
        if selected_type == "13 Hour Flow Sheet":
            self.procedures_group.hide()
        else:
            self.procedures_group.show()

    def update_kg_from_lbs(self):
        try:
            lbs = float(self.weight_entry.text())
            kg = lbs * 0.453592
            self.wt_kg_entry.blockSignals(True)
            self.wt_kg_entry.setText(f"{kg:.2f}")
            self.wt_kg_entry.blockSignals(False)
        except ValueError:
            pass

    def update_lbs_from_kg(self):
        try:
            kg = float(self.wt_kg_entry.text())
            lbs = kg / 0.453592
            self.weight_entry.blockSignals(True)
            self.weight_entry.setText(f"{lbs:.2f}")
            self.weight_entry.blockSignals(False)
        except ValueError:
            pass

    def add_procedure(self):
        if len(self.procedure_entries) >= 6:
            QMessageBox.critical(self, "Error", "You can only add up to 6 procedures.")
            return

        procedure_layout = QHBoxLayout()
        date_entry = QDateEdit()
        date_entry.setDate(QDate.currentDate())
        date_entry.setCalendarPopup(True)
        note_entry = QLineEdit()
        note_entry.setPlaceholderText("Procedure")

        date_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        note_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        procedure_layout.addWidget(date_entry)
        procedure_layout.addWidget(note_entry)

        self.procedures_layout.addLayout(procedure_layout)
        self.procedure_entries.append({"date": date_entry, "note": note_entry})

    # -------------------------------------------------------------------------
    # Updated add_treatment to handle special cases per client directives.
    def add_treatment(self, treatment):
        treatment_layout = QHBoxLayout()
        treatment_label = QLabel(treatment)
        treatment_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        if treatment == "MMCRT":
            # For MM/CRT, split the start field into two vertical boxes.
            mmcrt_layout = QVBoxLayout()
            mm_start_entry = QLineEdit()
            mm_start_entry.setPlaceholderText("MM Start")
            crt_start_entry = QLineEdit()
            crt_start_entry.setPlaceholderText("CRT Start")
            mmcrt_layout.addWidget(mm_start_entry)
            mmcrt_layout.addWidget(crt_start_entry)
            frequency_entry = QLineEdit()
            frequency_entry.setPlaceholderText("Frequency")
            frequency_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            treatment_layout.addWidget(treatment_label)
            treatment_layout.addLayout(mmcrt_layout)
            treatment_layout.addWidget(frequency_entry)
            self.treatments_layout.addLayout(treatment_layout)
            self.treatment_entries.append({
                "name": treatment,
                "mm_start": mm_start_entry,
                "crt_start": crt_start_entry,
                "frequency": frequency_entry
            })
        elif treatment in ["Temperature", "Pulse", "Respiratory Rate"]:
            # For these treatments, add an extra "Initial Start" field.
            initial_entry = QLineEdit()
            initial_entry.setPlaceholderText("Initial Start")
            start_hour_entry = QLineEdit()
            start_hour_entry.setPlaceholderText("Start Hour")
            frequency_entry = QLineEdit()
            frequency_entry.setPlaceholderText("Frequency")
            initial_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            start_hour_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            frequency_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            treatment_layout.addWidget(treatment_label)
            treatment_layout.addWidget(initial_entry)
            treatment_layout.addWidget(start_hour_entry)
            treatment_layout.addWidget(frequency_entry)
            self.treatments_layout.addLayout(treatment_layout)
            self.treatment_entries.append({
                "name": treatment,
                "initial": initial_entry,
                "start_hour": start_hour_entry,
                "frequency": frequency_entry
            })
        elif treatment == "Food / Water":
            # For Food/Water, add an optional note field that highlights orange if filled.
            start_hour_entry = QLineEdit()
            start_hour_entry.setPlaceholderText("Start Hour")
            frequency_entry = QLineEdit()
            frequency_entry.setPlaceholderText("Frequency")
            note_entry = QLineEdit()
            note_entry.setPlaceholderText("Food/Water Note (optional)")
            note_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # Change background color to orange if text is entered.
            note_entry.textChanged.connect(lambda text, widget=note_entry: widget.setStyleSheet(
                "background-color: orange;" if text.strip() != "" else ""
            ))
            start_hour_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            frequency_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            treatment_layout.addWidget(treatment_label)
            treatment_layout.addWidget(start_hour_entry)
            treatment_layout.addWidget(frequency_entry)
            treatment_layout.addWidget(note_entry)
            self.treatments_layout.addLayout(treatment_layout)
            self.treatment_entries.append({
                "name": treatment,
                "start_hour": start_hour_entry,
                "frequency": frequency_entry,
                "note": note_entry
            })
        else:
            # For all other treatments use the default layout.
            start_hour_entry = QLineEdit()
            start_hour_entry.setPlaceholderText("Start Hour")
            frequency_entry = QLineEdit()
            frequency_entry.setPlaceholderText("Frequency")
            start_hour_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            frequency_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            treatment_layout.addWidget(treatment_label)
            treatment_layout.addWidget(start_hour_entry)
            treatment_layout.addWidget(frequency_entry)
            self.treatments_layout.addLayout(treatment_layout)
            self.treatment_entries.append({
                "name": treatment,
                "start_hour": start_hour_entry,
                "frequency": frequency_entry
            })

    # -------------------------------------------------------------------------
    # Updated add_medication to include an initials field for the first dose.
    def add_medication(self):
        if len(self.medication_entries) >= 8:
            QMessageBox.critical(self, "Error", "You can only add up to 8 medications.")
            return

        medication_layout = QHBoxLayout()
        name_entry = QLineEdit()
        name_entry.setPlaceholderText("Name")
        dosage_entry = QLineEdit()
        dosage_entry.setPlaceholderText("Dosage")
        start_hour_entry = QLineEdit()
        start_hour_entry.setPlaceholderText("Start Hour")
        frequency_entry = QLineEdit()
        frequency_entry.setPlaceholderText("Frequency")
        initials_entry = QLineEdit()
        initials_entry.setPlaceholderText("Initials (1st dose)")

        name_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dosage_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        start_hour_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        frequency_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        initials_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        medication_layout.addWidget(name_entry)
        medication_layout.addWidget(dosage_entry)
        medication_layout.addWidget(start_hour_entry)
        medication_layout.addWidget(frequency_entry)
        medication_layout.addWidget(initials_entry)

        self.medications_layout.addLayout(medication_layout)
        self.medication_entries.append({
            "name": name_entry,
            "dosage": dosage_entry,
            "start_hour": start_hour_entry,
            "frequency": frequency_entry,
            "initials": initials_entry
        })

    def apply_to_all_treatments(self):
        start_hour = self.apply_start_hour.text()
        freq = self.apply_freq.text()

        if start_hour == "Start Hour" or freq == "Frequency":
            return

        for treatment in self.treatment_entries:
            # Only update treatments that have the generic start_hour field.
            if "start_hour" in treatment and treatment["start_hour"] is not None:
                treatment["start_hour"].setText(start_hour)
            if "frequency" in treatment and treatment["frequency"] is not None:
                treatment["frequency"].setText(freq)

    def clear_all_fields(self):
        self.cpr_dnr_combo.setCurrentIndex(0)
        self.patient_entry.clear()
        self.chart_entry.clear()
        self.date_entry.setDate(QDate.currentDate())
        self.a_entry.clear()
        self.owner_entry.clear()
        self.problem_entry.clear()
        self.dvm_entry.clear()
        self.e_entry.clear()
        self.age_entry.clear()
        self.sex_entry.clear()
        self.weight_entry.clear()
        self.wt_kg_entry.clear()
        self.ivc_entry.clear()
        self.techs_entry.clear()
        self.initials_entry.clear()

        for entry in self.procedure_entries:
            entry["date"].deleteLater()
            entry["note"].deleteLater()
        self.procedure_entries.clear()

        for treatment in self.treatment_entries:
            if "start_hour" in treatment and treatment["start_hour"]:
                treatment["start_hour"].clear()
            if "frequency" in treatment and treatment["frequency"]:
                treatment["frequency"].clear()
            # Clear additional fields if they exist.
            if "initial" in treatment and treatment["initial"]:
                treatment["initial"].clear()
            if "mm_start" in treatment and treatment["mm_start"]:
                treatment["mm_start"].clear()
            if "crt_start" in treatment and treatment["crt_start"]:
                treatment["crt_start"].clear()
            if "note" in treatment and treatment["note"]:
                treatment["note"].clear()

        for entry in self.medication_entries:
            entry["name"].deleteLater()
            entry["dosage"].deleteLater()
            entry["start_hour"].deleteLater()
            entry["frequency"].deleteLater()
            entry["initials"].deleteLater()
        self.medication_entries.clear()

    def submit(self):
        if not self.initials_entry.text().strip():
            self.show_initials_dialog()
            return

        data = {
            "flow_sheet_type": self.flow_sheet_type_combo.currentText(),  # must stay first
            "cpr_dnr": self.cpr_dnr_combo.currentText(),
            "patient": self.patient_entry.text().strip(),
            "chartnum": self.chart_entry.text().strip(),
            "date": self.date_entry.date().toString("yyyy-MM-dd"),
            "a": self.a_entry.text().strip(),
            "owner": self.owner_entry.text().strip(),
            "problem": self.problem_entry.text().strip(),
            "dvm": self.dvm_entry.text().strip(),
            "e": self.e_entry.text().strip(),
            "age": self.age_entry.text().strip(),
            "sex": self.sex_entry.text().strip(),
            "weight": self.weight_entry.text().strip(),
            "wt_kg": self.wt_kg_entry.text().strip(),
            "ivcinfo": self.ivc_entry.text().strip(),
            "techs": self.techs_entry.text().strip(),
            "procedures": [],
            "treatments": {},
            "medications": [],
            "initials": self.initials_entry.text().strip()
        }
        print(f"Data being submitted with flow sheet type: {data['flow_sheet_type']}")  # Debug print

        for entry in self.procedure_entries:
            date = entry["date"].date().toString("yyyy-MM-dd")
            note = entry["note"].text().strip()
            if date or note:
                data["procedures"].append({"date": date, "note": note})

        # Updated: capture extra treatment fields based on treatment type.
        for treatment in self.treatment_entries:
            name = treatment["name"]
            if name in ["Temperature", "Pulse", "Respiratory Rate"]:
                initial = treatment["initial"].text().strip()
                start_hour = treatment["start_hour"].text().strip()
                frequency = treatment["frequency"].text().strip()
                data["treatments"][name] = {
                    "initial": initial,
                    "start_hour": start_hour,
                    "frequency": frequency
                }
            elif name == "MMCRT":
                mm_start = treatment["mm_start"].text().strip()
                crt_start = treatment["crt_start"].text().strip()
                frequency = treatment["frequency"].text().strip()
                data["treatments"][name] = {
                    "mm_start": mm_start,
                    "crt_start": crt_start,
                    "frequency": frequency
                }
            elif name == "Food / Water":
                start_hour = treatment["start_hour"].text().strip()
                frequency = treatment["frequency"].text().strip()
                note = treatment["note"].text().strip()
                data["treatments"][name] = {
                    "start_hour": start_hour,
                    "frequency": frequency,
                    "note": note
                }
            else:
                start_hour = treatment["start_hour"].text().strip()
                frequency = treatment["frequency"].text().strip()
                data["treatments"][name] = {
                    "start_hour": start_hour,
                    "frequency": frequency
                }

        # Updated: include medication initials.
        for med in self.medication_entries:
            name = med["name"].text().strip()
            dosage = med["dosage"].text().strip()
            start_hour = med["start_hour"].text().strip()
            frequency = med["frequency"].text().strip()
            initials = med["initials"].text().strip()
            if name or dosage or start_hour or frequency or initials:
                data["medications"].append({
                    "name": name,
                    "dosage": dosage,
                    "start_hour": start_hour,
                    "frequency": frequency,
                    "initials": initials
                })

        self.on_submit(data)

    def show_initials_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Initials Required")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Please enter your initials:"))

        initials_input = QLineEdit()
        layout.addWidget(initials_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.set_initials(dialog, initials_input))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def set_initials(self, dialog, initials_input):
        initials = initials_input.text().strip()
        if initials:
            self.initials_entry.setText(initials)
            dialog.accept()
            self.submit()
        else:
            QMessageBox.warning(self, "Warning", "Initials cannot be empty.")

def open_gui(on_submit):
    app = QApplication(sys.argv)
    ex = FlowSheetGenerator(on_submit)
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    def dummy_submit(data):
        print("Collected Data:", data)
    open_gui(dummy_submit)
