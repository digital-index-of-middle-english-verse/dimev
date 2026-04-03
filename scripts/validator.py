#!/usr/bin/env python3

# To validate a single file against its schema, supply the path on the command
# line. Else the script validates all files in the data directory.

# /// script
# dependencies = [
#   "xmlschema",
#   "lxml",
#   "rdflib"
# ]
# ///

import xmlschema
import sys
import re
from lxml import etree
from pathlib import Path
from rdflib import Graph, Literal, Namespace

root = Path(__file__).parent.parent.resolve()
data_dir = root / 'data'
schema_dir = root / 'schemas'
namespace = '{http://www.w3.org/XML/1998/namespace}'

def main():
    passing = True

    # Validate files against schemas
    passing = validate_by_schema(passing)

    if passing:
        # Validate ids and content
        passing = validate_ids_and_content(passing)

    if passing:
        print('Success! No validation errors.')
        sys.exit(0)
    else:
        print('WARNING: A least one validation failed. Scroll up for details.')
        sys.exit(1)

def validate_ids_and_content(passing):

    ## Gather and validate ids
    passing, record_ids, textcarrier_ids = validate_xml_ids(passing)
    passing, bibl_ids = validate_bibl_ids(passing)

    # Verify uniqueness of ids within entire namespace
    all_ids = [record_ids, textcarrier_ids, bibl_ids]
    passing = verify_id_uniqueness(passing, all_ids)

    # Check outgoing references in Records.xml against textcarrier and bibl ids
    passing = check_bibl_refs(passing, textcarrier_ids, bibl_ids)

    # Check cross-references within Records.xml
    passing = check_crossrefs(passing, record_ids)

    # Validate terms: subjects, verseForms, languages
    passing = validate_terms(passing)

    print('\nAll checks complete.')
    return passing

def validate_terms(passing):
    filename = 'Records.xml'
    tree = etree.parse(data_dir / filename)
    root = tree.getroot()
    item_checks = 0
    error_count = 0
    domains = ['subject', 'form', 'language']
    print(f'\nValidating {", ".join(domains)} terms...')
    for domain in domains:
        valid_terms = get_valid_terms(domain)
        if domain == 'form':
            target_tag = 'verseForms'
        else:
            target_tag = domain + 's'
        for record in root.findall('record'):
            target_element = record.find(target_tag)
            if target_element is not None:
                for term in target_element:
                    if term.text not in valid_terms:
                        print(f'WARNING: unrecognized {domain} term "{term.text}"')
                        passing = False
                        error_count += 1
                item_checks += 1
    print(f'Checked {item_checks} terms. Found {error_count} errors.')
    return passing

def get_valid_terms(domain):
    filename = domain + '-terms.xml'
    tree = etree.parse(data_dir / filename)
    root = tree.getroot()
    valid_terms = []
    for item in root.findall('item'):
        term = item.find('term')
        valid_terms.append(term.text)
    return valid_terms

def check_crossrefs(passing, id_registry):
    filename = 'Records.xml'
    print(f'\nChecking reference targets in {filename}')
    item_checks = 0
    error_count = 0
    tree = etree.parse(data_dir / filename)
    root = tree.getroot()
    for ref in root.iter('ref'):
        target = ref.get('target')
        if target not in id_registry:
            print(f'WARNING: bad target value "{target}"')
            passing = False
            error_count += 1
        item_checks += 1
    print(f'Checked {item_checks} ref elements. Found {error_count} errors.')
    return passing

def validate_bibl_ids(passing):
    filename = 'Bibliography.rdf'
    print(f'Validating citation keys in {filename}...')
    id_registry = set()
    error_count = 0
    item_checks = 0
    pattern = r'[A-Za-z0-9_\-\.]+'
    path = data_dir / filename
    Z = Namespace("http://www.zotero.org/namespaces/export#")
    g = Graph()
    g.parse(path)

    # Iterate over all dc:description triples
    for s, p, o in list(g.triples((None, Z.citationKey, None))):
        bibkey = str(o)
        id_registry, error_count = validate_id(bibkey, pattern, filename, id_registry, error_count)
        item_checks += 1

    # Report results
    print(f'Checks of citation keys in {filename} completed with {item_checks} checks and {error_count} errors.\n')
    if error_count > 0:
        passing = False
    return passing, id_registry

def validate_xml_ids(passing):
    file_list = ['Records.xml', 'Manuscripts.xml', 'PrintedBooks.xml', 'Inscriptions.xml']

    # Define containers and counters
    record_ids = set()
    textcarrier_ids = set()
    error_count = 0
    item_checks = 0
    for filename in file_list:
        print(f'Validating xml:ids in {filename}...')
        path = data_dir / filename
        tree = etree.parse(path)
        root = tree.getroot()
        if filename != 'Records.xml':
            pattern = r'[A-Za-z0-9_\-\.]+'
            child = 'item'
            if filename == 'PrintedBooks.xml':
                # reset child tag
                child = 'bibl'
            for item in root.findall(child):
                item_id = item.get(namespace + 'id')
                textcarrier_ids, error_count = validate_id(item_id, pattern, filename, textcarrier_ids, error_count)
                item_checks += 1

        else: # Records.xml
            for item in root.findall('record'):
                # Check the xml:id on the record element
                record_id = item.get(namespace + 'id')
                pattern = r'record-\d+(\.\d{1,2})?'
                if record_id is not None: # NOTE: not all items have an xml:id
                    record_ids, error_count = validate_id(record_id, pattern, filename, record_ids, error_count)
                    item_checks += 1

                    # Check the xml:ids on witness elements, if present
                    witnesses = item.find('witnesses')
                    if witnesses is not None:
                        for witness in witnesses.findall('witness'):
                            wit_id = witness.get(namespace + 'id')
                            dimev_number = re.sub('record-', '', record_id)
                            pattern = 'wit-' + dimev_number + r'-\d{1,3}'
                            record_ids, error_count = validate_id(wit_id, pattern, filename, record_ids, error_count)
                            item_checks += 1

    # Report results
    print(f'Checks of xml:ids completed with {item_checks} checks and {error_count} errors.\n')
    return passing, record_ids, textcarrier_ids

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

def validate_by_schema(passing):
    error_count = 0

    # Validate a single file, if its path is given on the command line
    if len(sys.argv) > 1:
        print('Found one XML file to validate against schema...')
        filename = Path(sys.argv[1]).name
        xml_files = [ data_dir / filename ]
    else:
        print('Validating XML files against schemas...')
        xml_files = data_dir.glob('*.xml')

    for file in xml_files:
        schema, schema_filename = get_schema(file)
        print(f'Validating {file.name} with {schema_filename}...')
        # Validate the XML file
        try:
            schema.validate(file)
            print("XML is valid")
        except xmlschema.XMLSchemaValidationError as e:
            print("XML validation failed:")
            print(e)
            error_count += 1
    if error_count == 0:
        print('Validation completed with no failures.\n')
    else:
        print(f'{error_count} file(s) failed validation.\n')
        passing = False
    return passing

def get_schema(xml_file):

    # Retrieve the schema URI from procesing instructions
    tree = etree.parse(xml_file)
    processing_instructions = tree.xpath('//processing-instruction("xml-model")')
    for pi in processing_instructions:
        schema_relative_path = pi.get('href')
        schema_filename = re.sub('../schemas/', '', schema_relative_path)

    # Load the XSD schema
    schema_path = schema_dir / schema_filename
    return xmlschema.XMLSchema(schema_path), schema_filename

def check_bibl_refs(passing, textcarrier_ids, bibl_ids):
    filename = 'Records.xml'
    tree = etree.parse(data_dir / filename)
    root = tree.getroot()
    print(f'\nChecking bibliographic and source references in {filename}...')
    error_count = 0
    item_checks = 0
    bibl_ids.add('MECompendium') # NOTE: A special case

    # Check for bad outbound references in Records.xml
    referenced_textcarriers = set()
    referenced_bibl = set()
    target_tags = ['bibl', 'source', 'mss']
    for elem in root.iter():
        if elem.tag in target_tags:
            key = elem.get('key')
            if key is not None:
                if elem.tag == 'bibl':
                    referenced_bibl.add(key)
                    if key not in bibl_ids:
                        print(f'WARNING: Bibliography key {key} is referenced in Records.xml but not defined')
                        passing = False
                        error_count += 1
                    item_checks += 1
                else: # text-carriers
                    referenced_textcarriers.add(key)
                    if key not in textcarrier_ids:
                        print(f'WARNING: Source key {key} is referenced in Records.xml but not defined')
                        passing = False
                        error_count += 1
                    item_checks += 1

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
    print(f'Found {len(unreferenced_textcarrier_keys)} unreferenced textcarrier keys and {len(unreferenced_bibl_keys)} unreferenced keys to modern scholarly works')
    print(f'Checks completed with {item_checks} checks and {error_count} errors.')

    return passing

def verify_id_uniqueness(passing, list_of_sets):
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
    else:
        passing == False
    return passing

if __name__ == "__main__":
    main()
