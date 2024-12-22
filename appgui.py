import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def clear_all_fields():
    # Clear all entry fields
    patient_entry.delete(0, tk.END)
    chart_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    a_entry.delete(0, tk.END)
    owner_entry.delete(0, tk.END)
    problem_entry.delete(0, tk.END)
    dvm_entry.delete(0, tk.END)
    e_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    sex_entry.delete(0, tk.END)
    ivc_entry.delete(0, tk.END)
    techs_entry.delete(0, tk.END)
    initials_entry.delete(0, tk.END)
    apply_start_hour.delete(0, tk.END)
    apply_freq.delete(0, tk.END)
    
    # Reset CPR/DNR to default
    cpr_dnr_var.set("CPR")

    # Clear all treatment fields
    for treatment in treatment_entries:
        treatment["start_hour"].delete(0, tk.END)
        treatment["frequency"].delete(0, tk.END)
        set_placeholder(treatment["start_hour"], "Start Hour")
        set_placeholder(treatment["frequency"], "Frequency")

    # Remove all procedures
    for entry in procedure_entries:
        entry["date"].destroy()
        entry["note"].destroy()
    procedure_entries.clear()

    # Remove all medications
    for entry in medication_entries:
        entry["name"].destroy()
        entry["dosage"].destroy()
        entry["start_hour"].destroy()
        entry["frequency"].destroy()
    medication_entries.clear()

    # Reset placeholders
    set_placeholder(patient_entry, "Enter Patient Name")
    set_placeholder(chart_entry, "Enter Chart Number")
    set_placeholder(date_entry, "Enter Date")
    set_placeholder(a_entry, "Enter A Value")
    set_placeholder(owner_entry, "Enter Owner Name")
    set_placeholder(problem_entry, "Enter Problem")
    set_placeholder(dvm_entry, "Enter DVM")
    set_placeholder(e_entry, "Enter E Value")
    set_placeholder(age_entry, "Enter Age")
    set_placeholder(sex_entry, "Enter Sex")
    set_placeholder(ivc_entry, "Enter IVC Info")
    set_placeholder(techs_entry, "Enter Techs")
    set_placeholder(initials_entry, "Enter Initials")
    set_placeholder(apply_start_hour, "Start Hour")
    set_placeholder(apply_freq, "Frequency")

# Function to collect data and return to the main application
def collect_data():
    data = {
        "cpr_dnr": cpr_dnr_var.get(),
        "patient": patient_entry.get().strip(),
        "chartnum": chart_entry.get().strip(),
        "date": date_entry.get().strip(),
        "a": a_entry.get().strip(),
        "owner": owner_entry.get().strip(),
        "problem": problem_entry.get().strip(),
        "dvm": dvm_entry.get().strip(),
        "e": e_entry.get().strip(),
        "age": age_entry.get().strip(),
        "sex": sex_entry.get().strip(),
        "ivcinfo": ivc_entry.get().strip(),
        "techs": techs_entry.get().strip(),
        "procedures": [],
        "treatments": {},
        "medications": [],
        "initials": initials_entry.get().strip()
    }

    # Clean procedure entries
    for entry in procedure_entries:
        date = entry["date"].get().strip()
        note = entry["note"].get().strip()
        if date or note:
            if date == "Date":
                date = ""
            if note == "Procedure":
                note = ""
            data["procedures"].append({"date": date, "note": note})

    # Process all treatments
    for treatment in treatment_entries:
        name = treatment["name"]
        start_hour = treatment["start_hour"].get().strip()
        frequency = treatment["frequency"].get().strip()
        
        # Remove placeholder text if present
        if start_hour == "Start Hour":
            start_hour = ""
        if frequency == "Frequency":
            frequency = ""
            
        data["treatments"][name] = {
            "start_hour": start_hour,
            "frequency": frequency
        }

    # Clean medication entries
    for med in medication_entries:
        name = med["name"].get().strip()
        dosage = med["dosage"].get().strip()
        start_hour = med["start_hour"].get().strip()
        frequency = med["frequency"].get().strip()
        
        # Remove placeholder text
        if name == "Name":
            name = ""
        if dosage == "Dosage":
            dosage = ""
        if start_hour == "Start Hour":
            start_hour = ""
        if frequency == "Frequency":
            frequency = ""
            
        if name or dosage or start_hour or frequency:
            data["medications"].append({
                "name": name,
                "dosage": dosage,
                "start_hour": start_hour,
                "frequency": frequency
            })

    # Remove placeholder text from all entries
    for key in data:
        if isinstance(data[key], str) and data[key].startswith("Enter "):
            data[key] = ""

    return data

def set_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder))
    entry.config(fg="grey")

def clear_placeholder(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)
        entry.config(fg="grey")

def open_gui(on_submit):
    root = tk.Tk()
    root.title("Gregg's Flow Sheet Generator")
    
    # Set window icon
    try:
        root.iconbitmap(resource_path('icon.ico'))
    except tk.TclError:
        print("Warning: icon.ico not found")

    # Declare all global variables
    global cpr_dnr_var, patient_entry, chart_entry, date_entry, a_entry, owner_entry
    global problem_entry, dvm_entry, e_entry, age_entry, sex_entry, ivc_entry, techs_entry
    global initials_entry, procedure_entries, treatment_entries, medication_entries
    global apply_start_hour, apply_freq

    # Initialize entry variables
    cpr_dnr_var = tk.StringVar(value="CPR")
    patient_entry = tk.Entry(root, width=30)
    chart_entry = tk.Entry(root, width=15)
    date_entry = tk.Entry(root, width=15)
    a_entry = tk.Entry(root, width=15)
    owner_entry = tk.Entry(root, width=30)
    problem_entry = tk.Entry(root, width=30)
    dvm_entry = tk.Entry(root, width=30)
    e_entry = tk.Entry(root, width=15)
    age_entry = tk.Entry(root, width=15)
    sex_entry = tk.Entry(root, width=15)
    ivc_entry = tk.Entry(root, width=30)
    techs_entry = tk.Entry(root, width=30)
    initials_entry = tk.Entry(root, width=15)

    procedure_entries = []
    treatment_entries = []
    medication_entries = []

    # First Row - Patient Info
    tk.Label(root, text="CPR/DNR").grid(row=0, column=0, padx=5, pady=5)
    tk.OptionMenu(root, cpr_dnr_var, "CPR", "DNR").grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Patient:").grid(row=0, column=2, padx=5, pady=5)
    patient_entry.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(root, text="Chart #:").grid(row=0, column=4, padx=5, pady=5)
    chart_entry.grid(row=0, column=5, padx=5, pady=5)
    
    tk.Label(root, text="Date:").grid(row=0, column=6, padx=5, pady=5)
    date_entry.grid(row=0, column=7, padx=5, pady=5)

    # Second Row
    tk.Label(root, text="A:").grid(row=1, column=0, padx=5, pady=5)
    a_entry.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Owner:").grid(row=1, column=2, padx=5, pady=5)
    owner_entry.grid(row=1, column=3, padx=5, pady=5)
    
    tk.Label(root, text="Problem:").grid(row=1, column=4, padx=5, pady=5)
    problem_entry.grid(row=1, column=5, columnspan=2, padx=5, pady=5)
    
    tk.Label(root, text="DVM:").grid(row=1, column=7, padx=5, pady=5)
    dvm_entry.grid(row=1, column=8, padx=5, pady=5)

    # Third Row
    tk.Label(root, text="E:").grid(row=2, column=0, padx=5, pady=5)
    e_entry.grid(row=2, column=1, padx=5, pady=5)
    
    tk.Label(root, text="Age:").grid(row=2, column=2, padx=5, pady=5)
    age_entry.grid(row=2, column=3, padx=5, pady=5)
    
    tk.Label(root, text="Sex:").grid(row=2, column=4, padx=5, pady=5)
    sex_entry.grid(row=2, column=5, padx=5, pady=5)
    
    tk.Label(root, text="IVC Size/Site/Date:").grid(row=2, column=6, padx=5, pady=5)
    ivc_entry.grid(row=2, column=7, padx=5, pady=5)
    
    tk.Label(root, text="Techs:").grid(row=2, column=8, padx=5, pady=5)
    techs_entry.grid(row=2, column=9, padx=5, pady=5)

    # Create frames for sections
    procedures_frame = tk.LabelFrame(root, text="Procedures", padx=5, pady=5)
    procedures_frame.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

    treatments_frame = tk.LabelFrame(root, text="Treatments", padx=5, pady=5)
    treatments_frame.grid(row=3, column=5, columnspan=5, padx=10, pady=10, sticky="nsew")

    # Procedures Section
    def add_procedure():
        if len(procedure_entries) >= 6:
            messagebox.showerror("Error", "You can only add up to 6 procedures.")
            return

        row = len(procedure_entries)
        date_entry = tk.Entry(procedures_frame, width=15)
        note_entry = tk.Entry(procedures_frame, width=40)
        
        date_entry.grid(row=row, column=0, padx=2, pady=2)
        note_entry.grid(row=row, column=1, padx=2, pady=2)
        
        set_placeholder(date_entry, "Date")
        set_placeholder(note_entry, "Procedure")
        
        procedure_entries.append({"date": date_entry, "note": note_entry})

    tk.Button(procedures_frame, text="Add Procedure", command=add_procedure).grid(row=6, column=0, columnspan=2, pady=5)

    # Treatments Quick Add Section
    quick_add_frame = tk.Frame(treatments_frame)
    quick_add_frame.grid(row=0, column=0, columnspan=4, pady=5)

    tk.Label(quick_add_frame, text="Quick Add - Start Hour:").grid(row=0, column=0, padx=2)
    apply_start_hour = tk.Entry(quick_add_frame, width=8)
    apply_start_hour.grid(row=0, column=1, padx=2)
    
    tk.Label(quick_add_frame, text="Frequency:").grid(row=0, column=2, padx=2)
    apply_freq = tk.Entry(quick_add_frame, width=8)
    apply_freq.grid(row=0, column=3, padx=2)

    def apply_to_all_treatments():
        start_hour = apply_start_hour.get()
        freq = apply_freq.get()
        
        if start_hour == "Start Hour" or freq == "Frequency":
            return
            
        for treatment in treatment_entries:
            if start_hour:
                treatment["start_hour"].delete(0, tk.END)
                treatment["start_hour"].insert(0, start_hour)
                treatment["start_hour"].config(fg="black")
            if freq:
                treatment["frequency"].delete(0, tk.END)
                treatment["frequency"].insert(0, freq)
                treatment["frequency"].config(fg="black")

    tk.Button(quick_add_frame, text="Apply to All", command=apply_to_all_treatments).grid(row=0, column=4, padx=5)

    # Add treatments
    treatments = [
        "Temperature", "Pulse", "Respiratory Rate", "MMCRT", "IV Fluids / Rate", "Additives",
        "Check IVC", "Walk/Litter", "Urine (+/-)", "Stool (+/-)", "Vomit (+/-)", "Food / Water"
    ]

    for i, treatment in enumerate(treatments):
        tk.Label(treatments_frame, text=treatment, width=15, anchor="w").grid(row=i+1, column=0, padx=2, pady=2)
        start_hour_entry = tk.Entry(treatments_frame, width=8)
        frequency_entry = tk.Entry(treatments_frame, width=8)
        
        start_hour_entry.grid(row=i+1, column=1, padx=2, pady=2)
        frequency_entry.grid(row=i+1, column=2, padx=2, pady=2)
        
        set_placeholder(start_hour_entry, "Start Hour")
        set_placeholder(frequency_entry, "Frequency")
        
        treatment_entries.append({
            "name": treatment,
            "start_hour": start_hour_entry,
            "frequency": frequency_entry
        })

    # Medications Section
    medications_frame = tk.LabelFrame(root, text="Medications", padx=5, pady=5)
    medications_frame.grid(row=4, column=0, columnspan=10, padx=10, pady=10, sticky="ew")

    def add_medication():
        if len(medication_entries) >= 8:
            messagebox.showerror("Error", "You can only add up to 8 medications.")
            return

        row = len(medication_entries)
        name_entry = tk.Entry(medications_frame, width=30)
        dosage_entry = tk.Entry(medications_frame, width=20)
        start_hour_entry = tk.Entry(medications_frame, width=8)
        frequency_entry = tk.Entry(medications_frame, width=8)
        
        name_entry.grid(row=row, column=0, padx=2, pady=2)
        dosage_entry.grid(row=row, column=1, padx=2, pady=2)
        start_hour_entry.grid(row=row, column=2, padx=2, pady=2)
        frequency_entry.grid(row=row, column=3, padx=2, pady=2)
        
        set_placeholder(name_entry, "Name")
        set_placeholder(dosage_entry, "Dosage")
        set_placeholder(start_hour_entry, "Start Hour")
        set_placeholder(frequency_entry, "Frequency")
        
        medication_entries.append({
            "name": name_entry,
            "dosage": dosage_entry,
            "start_hour": start_hour_entry,
            "frequency": frequency_entry
        })

    tk.Button(medications_frame, text="Add Medication", command=add_medication).grid(row=8, column=0, columnspan=4, pady=5)

    # Bottom section with Initials, Submit, and Icon
    bottom_frame = tk.Frame(root)
    bottom_frame.grid(row=5, column=0, columnspan=10, pady=10)

    tk.Label(bottom_frame, text="Initials:").grid(row=0, column=0, padx=5)
    initials_entry = tk.Entry(bottom_frame, width=15) # Make sure entry is created in bottom_frame
    initials_entry.grid(row=0, column=1, padx=5)
    tk.Button(bottom_frame, text="Submit", command=lambda: on_submit(collect_data())).grid(row=0, column=2, padx=5)
    tk.Button(bottom_frame, text="Clear", command=clear_all_fields).grid(row=0, column=3, padx=5)

    # Icon and Version
    try:
        icon_image = Image.open(resource_path('icon.ico'))
        icon_image = icon_image.resize((32, 32)) # Size of kitty kat
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label = tk.Label(bottom_frame, image=icon_photo)
        icon_label.image = icon_photo  # Keep a reference!
        icon_label.grid(row=0, column=4, padx=20) # Adjust column
        
        version_label = tk.Label(bottom_frame, text="v0.1", font=("Arial", 12, "bold"))
        version_label.grid(row=1, column=4) # Adjust column
    except Exception as e:
        print(f"Error loading icon: {e}")

    # Set placeholders for all main entries
    set_placeholder(patient_entry, "Enter Patient Name")
    set_placeholder(chart_entry, "Enter Chart Number")
    set_placeholder(date_entry, "Enter Date")
    set_placeholder(a_entry, "Enter A Value")
    set_placeholder(owner_entry, "Enter Owner Name")
    set_placeholder(problem_entry, "Enter Problem")
    set_placeholder(dvm_entry, "Enter DVM")
    set_placeholder(e_entry, "Enter E Value")
    set_placeholder(age_entry, "Enter Age")
    set_placeholder(sex_entry, "Enter Sex")
    set_placeholder(ivc_entry, "Enter IVC Info")
    set_placeholder(techs_entry, "Enter Techs")
    set_placeholder(initials_entry, "Enter Initials")
    set_placeholder(apply_start_hour, "Start Hour")
    set_placeholder(apply_freq, "Frequency")

    root.mainloop()

if __name__ == "__main__":
    def dummy_submit(data):
        print("Collected Data:", data)

    open_gui(dummy_submit)