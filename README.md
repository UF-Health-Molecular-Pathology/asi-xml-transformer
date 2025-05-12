# asi-xml-transformer
Translates Epic data into an XML format compatible with ASI

# ASI XML Converter

This Python script automates the transformation of HL7 files from Epic as an XML file so that it can be imported into  the ASI system. It processes files from an input directory, renames specific XML tags, applies custom formatting (e.g., dates), and exports the transformed files to a separate output directory. Once processed, original files are deleted from the input directory.

## Features

- Renames XML elements based on a user-defined mapping.
- Applies formatting for `PatientDateofBirth` and `ReceivedDate`.
- Creates a new XML structure with selected fields.
- Processes all `.xml` files in a given directory.
- Removes original files after successful transformation.

## Requirements

- Python 3.x

## Usage

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/asi-xml-converter.git
cd asi-xml-converter

**### 2. Update the script:**
folder_path = "/your/input/directory"
out_folder_path = "/your/output/directory"

**### 3. Run the script:**

python3 update_xml_info.py

**Rename Mapping**

You can customize the XML element renaming by modifying the rename_mapping dictionary:
rename_mapping = {
    'OBR.2': 'Name',
    'PID.3': 'PatientID',
    'PID.5.1': 'PatientLastName',
    'PID.5.2': 'PatientFirstName',
    'OBR.14': 'ReceivedDate',
    'PID.7': 'PatientDateofBirth',
    'PID.8': 'Sex'
}

**Output Format**
The resulting XML structure will look like this:
<Case>
    <Name>...</Name>
    <PatientID>...</PatientID>
    <PatientLastName>...</PatientLastName>
    <PatientFirstName>...</PatientFirstName>
    <PatientDateofBirth>YYYY-MM-DD</PatientDateofBirth>
    <Sex>...</Sex>
    <ReceivedDate>YYYY-MM-DDTHH:MM:SS</ReceivedDate>
</Case>

**Error Handling**
If a file is malformed and cannot be parsed, it logs the error and continues processing the rest.
If no XML files are found in the input directory, it prints a message and exits.



You can customize the XML element renaming by modifying the rename_mapping dictionary:
