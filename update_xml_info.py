#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os


def rename_elements(xml_content, rename_mapping):
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Iterate through the elements and rename based on the mapping
    for old_name, new_name in rename_mapping.items():
        for element in root.iter(old_name):
            if new_name == 'Name':  # Special handling for the 'Name' element
                element.tag = new_name
                # Strip the trailing 'A' from the text
                element.text = element.text.rstrip(' A')
            else:
                element.tag = new_name

    # Convert the updated XML to a string
    updated_xml_content = ET.tostring(root).decode()

    return updated_xml_content

def update_xml_files_in_folder(folder_path, out_folder_path, rename_mapping):
    # Check if there are no XML files in the folder
    xml_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.xml')]
    if not xml_files:
        print(f"No XML files found in the folder {folder_path}. Exiting the script.")
        return
    #process the files if they exist
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            out_file_path = os.path.join(out_folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    xml_content = file.read()

                updated_xml_content = rename_elements(xml_content, rename_mapping)
                # Apply the transformation to the updated XML content
                transformed_xml = transform_xml(updated_xml_content)

                with open(out_file_path, 'w', encoding='utf-8') as file:
                    file.write(transformed_xml)

                # Remove the processed file from the "/ext/dinn09a/ASI Initial Export" folder
                os.remove(file_path)

            except ET.ParseError as e:
                print(f"Error: Unable to parse the XML content in {file_path}.")
                print(e)

            except FileNotFoundError:
                print(f"Error: File not found at the specified path: {file_path}.")

def transform_xml(updated_xml_content):
    # Parse the updated XML content
    root = ET.fromstring(updated_xml_content)

    # Create a new root element for the desired XML
    new_root = ET.Element("Case")

    # Extract and transform the elements
    new_root.append(ET.Element("Name"))
    new_root.find("Name").text = root.find(".//Name").text

    elements_to_copy = ["PatientID", "PatientLastName", "PatientFirstName", "PatientDateofBirth", "Sex", "ReceivedDate"]
    for element_name in elements_to_copy:
        element_value = root.find(f".//{element_name}").text

        # Special handling for PatientDateofBirth
        if element_name == "PatientDateofBirth":
            if element_value is not None:
                # The input format is YYYYMMDD
                formatted_date = f"{element_value[0:4]}-{element_value[4:6]}-{element_value[6:8]}"
                element_value = formatted_date
            else:
                continue  # Skip this element if it doesn't exist

        # Special handling for ReceivedDate
        if element_name == "ReceivedDate":
            # The input format is YYYYMMDDHHMMSS
            formatted_datetime = f"{element_value[0:4]}-{element_value[4:6]}-{element_value[6:8]}" \
                                 f"T{element_value[8:10]}:{element_value[10:12]}:{element_value[12:14]}"
            element_value = formatted_datetime

        new_root.append(ET.Element(element_name))
        new_root.find(element_name).text = element_value

    # Convert the new XML to a string
    new_xml_content = ET.tostring(new_root).decode()

    return new_xml_content


if __name__ == '__main__':
    # Specify the folder path containing the XML files -DEV
    #folder_path = "/ext/dinn09a/ASI Initial Export"
    #out_folder_path = "/ext/dinn09a/ASI Orders Export"

    # Specify the folder path containing the XML files -PROD
    folder_path = "/ext/dinn03/ASI Initial Export"
    out_folder_path = "/ext/dinn03/ASI Orders Export"

    # Define the rename mapping (old_element_name: new_element_name)
    rename_mapping = {
        'OBR.2':'Name',
        'PID.3':'PatientID',
        'PID.5.1':'PatientLastName',
        'PID.5.2':'PatientFirstName',
        'OBR.14':'ReceivedDate',
        'PID.7':'PatientDateofBirth',
        'PID.8':'Sex'
    }

    # Update XML files in the specified folder
    update_xml_files_in_folder(folder_path, out_folder_path, rename_mapping)

