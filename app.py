import openpyxl
from openpyxl.styles import PatternFill
import subprocess
import sys
import os
import threading
import re
from appgui import open_gui
from tkinter import filedialog
from datetime import datetime

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_valid_hour(value):
    try:
        hour = int(str(value))
        return 1 <= hour <= 12
    except (ValueError, TypeError):
        return False

def highlight_cells(sheet, start_hour, frequency, row, is_medication=False, 
                     has_merged_pair=False, is_13_hour=False, note_text=None):
    """
    Highlights cells based on the given start_hour and frequency.
    If note_text is provided (for Food/Water), then the bottom cell of the first
    highlighted occurrence will be updated with that note and filled with an orange color.
    """
    if not start_hour or not frequency:
        print(f"Missing start_hour or frequency for row {row}")
        return
        
    try:
        start_hour = int(start_hour)
        frequency = int(frequency)
        if not (1 <= start_hour <= 12):
            print(f"Invalid start hour {start_hour} for row {row}")
            return
    except (ValueError, TypeError):
        print(f"Invalid start_hour ({start_hour}) or frequency ({frequency}) for row {row}")
        return

    highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    orange_fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
    
    if is_13_hour:
        # For the 13-hour template, we use a list-based mapping.
        columns = list('CDEFGHIJKLMNOP')
        hours = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7]
        try:
            start_idx = hours.index(start_hour)
        except ValueError:
            print(f"Invalid start hour {start_hour} for 13-hour template")
            return
        first_occurrence = True
        current_idx = start_idx
        while current_idx < len(columns):
            col = columns[current_idx]
            cell = f"{col}{row}"
            sheet[cell].fill = highlight_fill

            if has_merged_pair or is_medication:
                cell_below = f"{col}{row + 1}"
                if first_occurrence and note_text:
                    sheet[cell_below].value = note_text
                    sheet[cell_below].fill = orange_fill
                    first_occurrence = False
                else:
                    sheet[cell_below].fill = highlight_fill

            current_idx += frequency

    else:
        # For the 24-hour template.
        time_columns = []
        hour_mapping = {}
        all_columns = [chr(i) for i in range(ord('D'), ord('Z') + 1)] + ['AA']
        for col in all_columns:
            cell = sheet[f"{col}5"]
            cell_value = cell.value
            if cell_value:
                # Use regex to extract the first integer from the header cell.
                match = re.search(r'\d+', str(cell_value))
                if match:
                    hour = int(match.group())
                    if 1 <= hour <= 12 and col not in hour_mapping.values():
                        hour_mapping[hour] = col
                        time_columns.append(col)
        print("Debug: Detected time_columns in header row:", time_columns)

        start_indices = []
        for i, col in enumerate(time_columns):
            cell_value = sheet[f"{col}5"].value
            if cell_value:
                match = re.search(r'\d+', str(cell_value))
                if match:
                    header_hour = int(match.group())
                    if header_hour == start_hour:
                        start_indices.append(i)
        if not start_indices:
            print(f"Warning: No matching header found for start_hour {start_hour} in the 24-hour template.")
            print("Debug: start_indices =", start_indices)
        else:
            print(f"Debug: For start_hour {start_hour}, found start_indices =", start_indices)

        for start_idx in start_indices:
            first_occurrence = True
            current_idx = start_idx
            while current_idx < len(time_columns):
                col = time_columns[current_idx]
                cell = f"{col}{row}"
                sheet[cell].fill = highlight_fill

                if has_merged_pair:
                    cell_below = f"{col}{row + 1}"
                    if first_occurrence and note_text:
                        sheet[cell_below].value = note_text
                        sheet[cell_below].fill = orange_fill
                        first_occurrence = False
                    else:
                        sheet[cell_below].fill = highlight_fill
                elif is_medication:
                    cell_below = f"{col}{row + 1}"
                    sheet[cell_below].fill = highlight_fill

                current_idx += frequency
                if current_idx >= len(time_columns):
                    break

def fill_template(data):
    try:
        print("Starting to process the template...")
        flow_sheet_type = data.get("flow_sheet_type", "24 Hour Flow Sheet")
        print(f"Flow sheet type: {flow_sheet_type}")
        template_filename = "24template.xlsx" if flow_sheet_type == "24 Hour Flow Sheet" else "13template.xlsx"
        print(f"Using template file: {template_filename}")
        template_path = resource_path(template_filename)
        print(f"Template path: {template_path}")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file '{template_path}' not found.")

        workbook = openpyxl.load_workbook(template_path)
        sheet = workbook.active

        yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        # Process medications: build replacements (with initials appended if provided)
        medications = data.get("medications", [])
        med_replacements = {}
        for i, medication in enumerate(medications, start=1):
            if i <= 8:
                name = medication.get("name", "").strip()
                dosage = medication.get("dosage", "").strip()
                initials = medication.get("initials", "").strip()
                combined_med = f"{name} {dosage}".strip()
                if initials:
                    combined_med += f" ({initials})"
                med_replacements[f"{{med{i}}}"] = combined_med

        # Build the replacements dictionary for standard placeholders.
        replacements = {
            "{cpr_dnr}": data.get("cpr_dnr", ""),
            "{patient}": data.get("patient", ""),
            "{chartnum}": data.get("chartnum", ""),
            "{date}": data.get("date", ""),
            "{owner}": data.get("owner", ""),
            "{problem}": data.get("problem", ""),
            "{dvm}": data.get("dvm", ""),
            "{age}": data.get("age", ""),
            "{sex}": data.get("sex", ""),
            "{ivcinfo}": data.get("ivcinfo", ""),
            "{techs}": data.get("techs", ""),
            "{initials}": data.get("initials", ""),
            "{weight}": data.get("weight", ""),
            "{wt_kg}": data.get("wt_kg", "")
        }
        # For Food/Water note, we now insert the note dynamically via highlight_cells.
        # Therefore, no dedicated {food_note} placeholder is needed.

        # If the flow sheet type is "24 Hour Flow Sheet", process procedures.
        if flow_sheet_type == "24 Hour Flow Sheet":
            procedures = data.get("procedures", [])
            for i in range(6):
                num = i + 2
                date_placeholder = f"{{date{num}}}"
                note_placeholder = f"{{noted{num}}}"
                if i < len(procedures):
                    proc = procedures[i]
                    replacements[date_placeholder] = proc.get("date", "")
                    replacements[note_placeholder] = proc.get("note", "")
                else:
                    replacements[date_placeholder] = ""
                    replacements[note_placeholder] = ""

        # Process all placeholders in the template.
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and isinstance(cell.value, str):
                    cell_value = cell.value
                    if cell_value == "{cpr_dnr}":
                        cpr_dnr_value = data.get("cpr_dnr", "")
                        cell.value = cpr_dnr_value
                        if cpr_dnr_value == "CPR":
                            cell.fill = yellow_fill
                        elif cpr_dnr_value == "DNR":
                            cell.fill = red_fill
                    elif cell_value in med_replacements:
                        cell.value = med_replacements[cell_value]
                    elif "{a}" in cell_value:
                        cell.value = cell_value.replace("{a}", data.get("a", ""))
                    elif "{e}" in cell_value:
                        cell.value = cell_value.replace("{e}", data.get("e", ""))
                    elif cell_value in replacements:
                        cell.value = replacements[cell_value]
                    elif cell_value.startswith("{") and cell_value.endswith("}"):
                        cell.value = ""

        # Define treatment rows for each template type.
        if flow_sheet_type == "13 Hour Flow Sheet":
            treatment_rows = {
                "Temperature": {"row": 9, "merged": False},
                "Pulse": {"row": 10, "merged": False},
                "Respiratory Rate": {"row": 11, "merged": False},
                # MMCRT will be handled separately.
                "IV Fluids / Rate": {"row": 14, "merged": True},
                "Additives": {"row": 16, "merged": True},
                "Check IVC": {"row": 18, "merged": False},
                "Walk/Litter": {"row": 19, "merged": False},
                "Urine (+/-)": {"row": 20, "merged": False},
                "Stool (+/-)": {"row": 21, "merged": False},
                "Vomit (+/-)": {"row": 22, "merged": False},
                "Food / Water": {"row": 23, "merged": True}
            }
        else:
            treatment_rows = {
                "Temperature": {"row": 6, "merged": False},
                "Pulse": {"row": 7, "merged": False},
                "Respiratory Rate": {"row": 8, "merged": False},
                # MMCRT handled separately.
                "IV Fluids / Rate": {"row": 11, "merged": True},
                "Additives": {"row": 13, "merged": True},
                "Check IVC": {"row": 15, "merged": False},
                "Walk/Litter": {"row": 16, "merged": False},
                "Urine (+/-)": {"row": 17, "merged": False},
                "Stool (+/-)": {"row": 18, "merged": False},
                "Vomit (+/-)": {"row": 19, "merged": False},
                "Food / Water": {"row": 20, "merged": True}
            }

        # Process treatments (except MMCRT).
        for treatment_name, info in treatment_rows.items():
            if treatment_name in data.get("treatments", {}):
                details = data["treatments"][treatment_name]
                frequency = details.get("frequency", "").strip()
                # For Temperature, Pulse, and Respiratory Rate, use the "initial" field if provided.
                if treatment_name in ["Temperature", "Pulse", "Respiratory Rate"]:
                    start_val = details.get("initial", "").strip() or details.get("start_hour", "").strip()
                else:
                    start_val = details.get("start_hour", "").strip()
                
                # For Food / Water, retrieve the note text.
                note_text = details.get("note", "").strip() if treatment_name == "Food / Water" else None

                if start_val and frequency and start_val not in ["Start Hour", "Initial Start"]:
                    try:
                        highlight_cells(sheet, start_val, frequency, info["row"],
                                          has_merged_pair=info["merged"],
                                          is_13_hour=(flow_sheet_type == "13 Hour Flow Sheet"),
                                          note_text=note_text)
                    except Exception as e:
                        print(f"Error highlighting treatment {treatment_name}: {str(e)}")

        # Process MMCRT separately using two fields: mm_start and crt_start.
        if "MMCRT" in data.get("treatments", {}):
            details = data["treatments"]["MMCRT"]
            frequency = details.get("frequency", "").strip()
            mm_start = details.get("mm_start", "").strip()
            crt_start = details.get("crt_start", "").strip()
            if flow_sheet_type == "24 Hour Flow Sheet":
                mm_row = 9
                crt_row = 10
            else:
                mm_row = 12
                crt_row = 13
            if mm_start and frequency and mm_start not in ["MM Start"]:
                try:
                    highlight_cells(sheet, mm_start, frequency, mm_row,
                                      has_merged_pair=True,
                                      is_13_hour=(flow_sheet_type == "13 Hour Flow Sheet"))
                except Exception as e:
                    print(f"Error highlighting MM start in MMCRT: {str(e)}")
            if crt_start and frequency and crt_start not in ["CRT Start"]:
                try:
                    highlight_cells(sheet, crt_start, frequency, crt_row,
                                      has_merged_pair=True,
                                      is_13_hour=(flow_sheet_type == "13 Hour Flow Sheet"))
                except Exception as e:
                    print(f"Error highlighting CRT start in MMCRT: {str(e)}")

        # Process medications: highlight cells for each medication.
        for i, medication in enumerate(medications, start=1):
            if i <= 8:
                if flow_sheet_type == "13 Hour Flow Sheet":
                    row_num = 25 + ((i - 1) * 2)  # Adjusted for 13-hour template (rows 25/26, 27/28, etc.)
                else:
                    row_num = 21 + (i * 2 - 1)
                start_hour = medication.get("start_hour", "")
                frequency = medication.get("frequency", "")
                if start_hour and frequency and start_hour not in ["Start Hour"] and frequency not in ["Frequency"]:
                    try:
                        highlight_cells(sheet, start_hour, frequency, row_num,
                                          is_medication=True,
                                          is_13_hour=(flow_sheet_type == "13 Hour Flow Sheet"))
                    except Exception as e:
                        print(f"Error highlighting medication {i}: {str(e)}")

        patient_name = data.get("patient", "").strip()
        if patient_name.startswith("Enter "):
            patient_name = ""
        today = datetime.now().strftime("%Y.%m.%d")
        default_filename = f"{today}-{patient_name}-Flow-Chart.xlsx"

        documents_path = os.path.expanduser("~/Documents")
        output_path = filedialog.asksaveasfilename(
            initialdir=documents_path,
            initialfile=default_filename,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not output_path:
            print("Save cancelled by user")
            return

        workbook.save(output_path)
        print("Template processing completed. Saving the file.")

        if os.name == "nt":
            os.startfile(output_path)
        elif os.name == "posix":
            subprocess.call(["open" if "darwin" in os.sys.platform else "xdg-open", output_path])

        print("Flow sheet generated successfully and opened.")

    except Exception as e:
        print(f"Error generating flow sheet: {str(e)}")
        raise

def start_processing(data):
    try:
        fill_template(data)
    except Exception as e:
        print(f"Error in processing thread: {str(e)}")

if __name__ == "__main__":
    def handle_submit(data):
        print(f"Main received flow sheet type: {data.get('flow_sheet_type')}")
        print("Data received from GUI:", data)
        thread = threading.Thread(target=start_processing, args=(data,))
        thread.daemon = True
        thread.start()

    open_gui(handle_submit)