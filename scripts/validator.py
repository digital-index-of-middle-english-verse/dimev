#!/usr/bin/env python3

# Run from the root directory.

# To validate a single file against its schema, supply the path on the command
# line. Else the script validates all files in the data directory.

# TODO: validate textcarrier refs against textcarrier ids
# TODO: validate bibl refs against bibl ids
# TODO: check uniqueness of bibl ids

import xmlschema
import sys
import glob
import re
from lxml import etree

data_dir = 'data/'
schema_dir = 'schemas/'
namespace = '{http://www.w3.org/XML/1998/namespace}'

def main():
    file_list = glob.glob(data_dir + '*.xml')
    validate_files(file_list)
    record_ids = validate_xml_ids(scope='texts')
    textcarrier_ids = validate_xml_ids(scope='textcarriers')
    verify_id_uniqueness([record_ids, textcarrier_ids])

def validate_xml_ids(scope):
    # Select files for scope
    if scope == 'texts':
        file_list = ['Records.xml']
    elif scope == 'textcarriers':
        file_list = ['Manuscripts.xml', 'PrintedBooks.xml', 'Inscriptions.xml']

    # Define container and counters
    id_registry = set()
    error_count = 0
    item_checks = 0
    for filename in file_list:
        print(f'Validating xml:ids in {filename}...')
        path = data_dir + filename
        tree = etree.parse(path)
        root = tree.getroot()
        if scope == 'textcarriers':
            pattern = r'[A-Za-z0-9_\-\.]+'
            child = 'item'
            if filename == 'PrintedBooks.xml':
                # reset child tag
                child = 'bibl'
            for item in root.findall(child):
                item_id = item.get(namespace + 'id')
                id_registry, error_count = validate_id(item_id, pattern, filename, id_registry, error_count)
                item_checks += 1
            print('Done')

        else: # Records.xml
            for item in root.findall('record'):
                # Check the xml:id on the record element
                record_id = item.get(namespace + 'id')
                pattern = r'record-\d+(\.\d{1,2})?'
                if record_id is not None: # NOTE: not all items have an xml:id
                    id_registry, error_count = validate_id(record_id, pattern, filename, id_registry, error_count)
                    item_checks += 1

                    # Check the xml:ids on witness elements, if present
                    witnesses = item.find('witnesses')
                    if witnesses is not None:
                        for witness in witnesses.findall('witness'):
                            wit_id = witness.get(namespace + 'id')
                            dimev_number = re.sub('record-', '', record_id)
                            pattern = 'wit-' + dimev_number + r'-\d{1,3}'
                            id_registry, error_count = validate_id(wit_id, pattern, filename, id_registry, error_count)
                            item_checks += 1

    # Report results
    print(f'Checks of xml:ids in {scope} completed with {item_checks} checks and {error_count} errors.\n')
    return id_registry

def validate_id(item_id, pattern, filename, id_registry, error_count):
    if not re.fullmatch(pattern, item_id):
        print(f'WARNING: found malformed id "{item_id}" in {filename}')
        error_count += 1
    if item_id in id_registry:
        print(f"Duplicate xml:id found: {xml_id}")
        error_count += 1
    else:
        id_registry.add(item_id)
    return id_registry, error_count

def validate_files(file_list):
    # Validate a single file, if its path is given on the command line
    if len(sys.argv) > 1:
        file_list = [sys.argv[1]]
    file_count = 1
    error_count = 0
    for xml_file in file_list:
        xml_file = re.sub(data_dir, '', xml_file) # strip directory, if present
        print(f'Validating "{xml_file}" against schema ({file_count} of {len(file_list)})...')
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
    if error_count == 0:
        print('\nValidation completed with no failures.')
    else:
        print(f'\n{error_count} file(s) failed validation.')

def get_schema(xml_file):
    file_pairs = {
            ('Glossary.xml', 'glossary.xsd'),
            ('Inscriptions.xml', 'inscriptions.xsd'),
            ('Manuscripts.xml', 'manuscripts.xsd'),
            ('PrintedBooks.xml', 'printedbooks.xsd'),
            ('Records.xml', 'records.xsd')
            }
    for pair in file_pairs:
        if pair[0] == xml_file:
            schema_file = pair[1]
            break
    # Load the XSD schema
    return xmlschema.XMLSchema(schema_dir + schema_file)

def verify_id_uniqueness(list_of_sets):
    print('Checking for duplicate ids across all sets of ids...')
    duplicate = False
    check_count = 0
    id_registry = set()
    for id_set in list_of_sets:
        for item in id_set:
            if item in id_registry:
                print(f"Duplicate xml:id found: {item}")
                duplicate = True
            else:
                id_registry.add(item)
            check_count += 1
    print(f"Completed with {check_count} checks.")
    if duplicate == False:
        print('No duplicate ids found.')

if __name__ == "__main__":
    main()
