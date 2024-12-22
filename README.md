# Gregg's Flow Sheet Generator

![Screenshot 2024-12-22 142926](https://github.com/user-attachments/assets/78f470e8-d733-40f3-af94-10fc82304a92)

**Gregg's Flow Sheet Generator** is a desktop application designed to streamline the creation and management of flow sheets for veterinary use. It simplifies data entry, highlights important information, and generates Excel-based flow charts.

---

## Features

- **User-Friendly GUI**: Built with Tkinter for intuitive input and management of patient data.
- **Dynamic Excel Templates**: Highlights treatments and medications based on start time and frequency.
- **Customizable Fields**: Easily add, edit, and clear entries for treatments, procedures, and medications.
- **Save and Share**: Save generated flow sheets in Excel format for easy distribution.
- **Integrated Placeholder Management**: Fields include placeholders for clear guidance during data entry.

---

## Getting Started

### Prerequisites

- Python 3.8+
- The following Python libraries:
  - `openpyxl`
  - `Pillow`

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/greggs-flow-sheet-generator.git
   cd greggs-flow-sheet-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

---

## Compiling the Application

You can package the application as a standalone executable using **PyInstaller**.

### Steps to Compile:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Ensure the `build.spec` file is in the project directory. If not, create one using:
   ```bash
   pyinstaller app.py --name "GreggsFlowSheetGenerator" --onefile --noconsole
   ```

3. Compile the application:
   ```bash
   pyinstaller build.spec
   ```

4. After the build is complete, the executable will be available in the `dist/` directory. The compiled executable will include:
   - `app.py`
   - `appgui.py`
   - Supporting assets (e.g., `template.xlsx`, `icon.ico`)

---

## Using the Application

1. **Launch the Application**:
   Run the executable or `app.py` to open the graphical interface.

2. **Enter Data**:
   Fill in the required fields for patient information, treatments, medications, and procedures.

3. **Generate Flow Sheet**:
   Click **Submit** to process the data and save it as an Excel file.

4. **Save & Open**:
   Choose a file location to save your flow sheet. The application will automatically open the saved file for review.

---

## File Structure

- `app.py`: Main entry point of the application.
- `appgui.py`: GUI implementation using Tkinter.
- `build.spec`: PyInstaller configuration for packaging the application.
- `file_version_info.txt`: Metadata for the application build.

---

## Known Issues

- Ensure the `template.xlsx` file and `icon.ico` file is placed in the same directory as the executable.
- Placeholder text must be cleared before entering actual data to ensure proper flow sheet generation.

---

## Version Information

- **Version**: 0.1.0.0
- **Company**: G&H Dev
- **Description**: Flow sheet generation tool

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **Tkinter** for GUI design.
- **OpenPyXL** for Excel file manipulation.
- **Pillow** for image processing.
