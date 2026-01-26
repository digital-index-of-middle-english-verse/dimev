#!/usr/bin/env python3

# Run from the root directory.

# To validate a single file against its schema, supply the path on the command
# line. Else the script validates all files in the data directory.

import xmlschema
import sys
import glob
import re
from lxml import etree
from rdflib import Graph, Literal
from rdflib.namespace import DC, DCTERMS

data_dir = 'data/'
schema_dir = 'schemas/'
namespace = '{http://www.w3.org/XML/1998/namespace}'

def main():

    # Validate files against schemas
    file_list = glob.glob(data_dir + '*.xml')
    validate_files(file_list)

    # Gather and validate ids
    record_ids = validate_xml_ids(scope='texts')
    textcarrier_ids = validate_xml_ids(scope='textcarriers')
    bibl_ids = validate_bibl_ids()

    # Verify uniqueness of ids within entire namespace
    all_ids = [record_ids, textcarrier_ids, bibl_ids]
    verify_id_uniqueness(all_ids)

    # Check outgoing references in Records.xml against textcarrier and bibl ids
    check_textcarrier_refs(textcarrier_ids, bibl_ids)

    print('\nAll checks complete.')

def validate_bibl_ids():
    filename = 'Bibliography.rdf'
    print(f'Validating citation keys in {filename}...')
    id_registry = set()
    error_count = 0
    item_checks = 0
    CITATION_KEY_LINE = re.compile(r'^\s*Citation Key:\s*(\S+)\s*$')
    pattern = r'[A-Za-z0-9_\-\.]+'
    path = data_dir + filename
    g = Graph()
    g.parse(path)

    # Iterate over all dc:description triples
    for s, p, o in list(g.triples((None, DC.description, None))):
        text = str(o)
        key_found = False
        for line in text.splitlines():
            m = CITATION_KEY_LINE.match(line)
            if m:
                bibkey = m.group(1)
                id_registry, error_count = validate_id(bibkey, pattern, filename, id_registry, error_count)
                key_found = True
                item_checks += 1
        if key_found == False:
            print(f'WARNING: No citation key found!')
            error_count += 1

    # Report results
    print(f'Checks of citation keys in {filename} completed with {item_checks} checks and {error_count} errors.\n')
    return id_registry

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
        print(f'WARNING: malformed id "{item_id}" in {filename}')
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
        print('Validation completed with no failures.\n')
    else:
        print(f'{error_count} file(s) failed validation.\n')

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

def check_textcarrier_refs(textcarrier_ids, bibl_ids):
    filename = 'Records.xml'
    tree = etree.parse(data_dir + filename)
    root = tree.getroot()
    print(f'\nChecking bibliographic and source references in {filename}...')
    error_count = 0
    item_checks = 0
    bibl_ids.add('MECompendium') # NOTE: A special case

    # Check for bad outbound references in Records.xml
    referenced_textcarriers = set()
    referenced_bibl = set()
    undefined_bibl_keys = set()
    target_tags = ['repertory', 'edition', 'facsimile', 'biblio', 'source', 'mss']
    for elem in root.iter():
        if elem.tag in target_tags:
            key = elem.get('key')
            if key is not None:
                if elem.tag == 'source' or elem.tag == 'mss':
                    referenced_textcarriers.add(key)
                    if key not in textcarrier_ids:
                        print(f'WARNING: Source key {key} is referenced in Records.xml but not defined')
                        error_count += 1
                    item_checks += 1
                else: # modern scholarly works
                    referenced_bibl.add(key)
                    if key not in bibl_ids:
                        # print(f'WARNING: Bibliography key {key} is referenced in Records.xml but not defined')
                        # NOTE: large error counts here are due to manuscript keys referenced within the facsimiles block
                        undefined_bibl_keys.add(key)
                        error_count += 1
                    item_checks += 1
    my_list = sorted(undefined_bibl_keys)
    print(f'WARNING: found {len(my_list)} undefined bibliography keys: {", ".join(my_list)}')

    # Check for unreferenced ids and citation keys
    # NOTE: This yields many false negatives, as it misses (e.g.) citation keys referenced only in Manuscripts.xml

    unreferenced_textcarrier_keys = set()
    unreferenced_bibl_keys = set()
    for key in textcarrier_ids:
        if key not in referenced_textcarriers:
            unreferenced_textcarrier_keys.add(key)
    for key in bibl_ids:
        if key not in referenced_bibl:
            unreferenced_bibl_keys.add(key)
    print(f'Checks completed with {item_checks} checks and {error_count} errors')
    print(f'Found {len(unreferenced_textcarrier_keys)} unreferenced textcarrier keys and {len(unreferenced_bibl_keys)} unreferenced keys to modern scholarly works')

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
