#!/usr/bin/env python3

# This script validates XML files against their XSD schema. Run from the root
# directory. To validate a single file, supply the path on the commend line.
# Else the script validates all files in the data directory.

import xmlschema
import sys
import glob
import re

data_dir = 'data/'
schema_dir = 'schemas/'

def main():
    file_list = get_file_list()
    error_count = validate_files(file_list)
    if error_count == 0:
        print('\nValidation completed with no failures.')
    else:
        print(f'\n{error_count} file(s) failed validation.')

def get_file_list():
    file_list = []
    if len(sys.argv) > 1:
        file_list.append(sys.argv[1])
    else:
        file_list = glob.glob(data_dir + '*.xml')
    return file_list

def validate_files(file_list):
    file_count = 1
    error_count = 0
    for xml_file in file_list:
        xml_file = re.sub(data_dir, '', xml_file) # strip directory, if present
        print(f'Validating "{xml_file}" ({file_count} of {len(file_list)})...')
        schema = get_schema(xml_file)
        # Validate the XML file
        try:
            schema.validate(data_dir + xml_file)
            print("XML is valid")
            file_count += 1
        except xmlschema.XMLSchemaValidationError as e:
            print("XML validation failed:")
            print(e)
            error_count += 1
    return error_count

def get_schema(xml_file):
    file_pairs = {
            ('Bibliography.xml', 'bibliography.xsd'),
            ('Glossary.xml', 'glossary.xsd'),
            ('Inscriptions.xml', 'inscriptions.xsd'),
            ('Manuscripts.xml', 'manuscripts.xsd'),
            ('MSSIndex.xml', 'mssindex.xsd'),
            ('PrintedBooks.xml', 'printedbooks.xsd'),
            ('Records.xml', 'records.xsd')
            }
    for pair in file_pairs:
        if pair[0] == xml_file:
            schema_file = pair[1]
            break
    # Load the XSD schema
    return xmlschema.XMLSchema(schema_dir + schema_file)


if __name__ == "__main__":
    main()
