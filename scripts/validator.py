#!/usr/bin/env python3

"""Validate the DIMEV data files against their schemas and internal rules.

Pass the path to a single XML file on the command line to validate just that
file against its schema. With no argument, every file in the data directory is
validated against its schema and the cross-file id, reference, and controlled-
vocabulary checks are run.
"""

# /// script
# dependencies = [
#   "xmlschema",
#   "lxml",
#   "rdflib"
# ]
# ///

import argparse
import logging
import re
import sys
from pathlib import Path

import xmlschema
from lxml import etree
from rdflib import Graph, Namespace

ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = ROOT / 'data'
SCHEMA_DIR = ROOT / 'schemas'

XML_NS = '{http://www.w3.org/XML/1998/namespace}'
TEI_NS = '{http://www.tei-c.org/ns/1.0}'
ZOTERO = Namespace('http://www.zotero.org/namespaces/export#')

RECORDS_FILE = 'Records.xml'
BIBLIOGRAPHY_FILE = 'Bibliography.rdf'

# Generic id/key syntax, and the stricter form required of record xml:ids.
ID_PATTERN = re.compile(r'[A-Za-z0-9_\-.]+')
RECORD_ID_PATTERN = re.compile(r'record-\d+(\.\d{1,2})?')

# Maps each text-carrier file to the element that bears its xml:id.
TEXTCARRIER_FILES = {
    'PrintedBooks.xml': TEI_NS + 'biblStruct',
    'Manuscripts.xml': TEI_NS + 'msDesc',
    'Inscriptions.xml': TEI_NS + 'msDesc',
}

# Maps each controlled-vocabulary domain to the Records.xml element that holds
# its terms.
TERM_DOMAINS = {
    'subject': 'subjects',
    'form': 'verseForms',
    'language': 'languages',
}

logger = logging.getLogger('validator')


class ErrorCountingHandler(logging.Handler):
    """Counts records logged at ERROR level or above, so the run's pass/fail
    status can be derived from the log rather than threaded through every
    function."""

    def __init__(self):
        super().__init__(level=logging.ERROR)
        self.error_count = 0

    def emit(self, record):
        self.error_count += 1


class LevelPrefixFormatter(logging.Formatter):
    """Leaves INFO messages bare but prefixes warnings and errors with their
    level, preserving the script's original output style."""

    def format(self, record):
        message = record.getMessage()
        if record.levelno >= logging.WARNING:
            return f'{record.levelname}: {message}'
        return message


def configure_logging():
    """Wire up stdout output and the error counter; return the counter."""
    counter = ErrorCountingHandler()
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(LevelPrefixFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream)
    root_logger.addHandler(counter)
    return counter


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file', nargs='?',
                        help='path to a single XML file to validate against its '
                             'schema (default: validate all files in data/)')
    return parser.parse_args()


def main():
    args = parse_args()
    errors = configure_logging()

    validate_by_schema(args.file)

    # The content checks assume schema-valid input, so only run them once every
    # file has cleared its schema.
    if errors.error_count == 0:
        validate_ids_and_content()

    if errors.error_count == 0:
        logger.info('Success! No validation errors.')
        return 0
    logger.error('At least one validation failed. Scroll up for details.')
    return 1


def validate_by_schema(target=None):
    """Validate XML files against the XSD named in their xml-model PI."""
    if target:
        logger.info('Found one XML file to validate against schema...')
        xml_files = [DATA_DIR / Path(target).name]
    else:
        logger.info('Validating XML files against schemas...')
        xml_files = sorted(DATA_DIR.glob('*.xml'))

    for xml_file in xml_files:
        schema, schema_filename = load_schema(xml_file)
        logger.info(f'Validating {xml_file.name} with {schema_filename}...')
        try:
            schema.validate(xml_file)
            logger.info('XML is valid')
        except xmlschema.XMLSchemaValidationError as e:
            logger.error(f'XML validation failed for {xml_file.name}:\n{e}')


def load_schema(xml_file):
    """Resolve and load the XSD referenced by the file's xml-model PI."""
    tree = etree.parse(xml_file)
    schema_filename = None
    for pi in tree.xpath('//processing-instruction("xml-model")'):
        schema_filename = re.sub(r'\.\./schemas/', '', pi.get('href'))
    schema_path = SCHEMA_DIR / schema_filename
    return xmlschema.XMLSchema(schema_path), schema_filename


def validate_ids_and_content():
    """Run the cross-file id, reference, and controlled-vocabulary checks."""
    record_ids, textcarrier_ids = collect_xml_ids()
    bibl_ids = collect_bibl_ids()

    verify_id_uniqueness(record_ids, textcarrier_ids, bibl_ids)
    check_bibl_refs(textcarrier_ids, bibl_ids)
    check_crossrefs(record_ids)
    validate_terms()

    logger.info('\nAll checks complete.')


def collect_xml_ids():
    """Gather and validate the xml:ids of records, witnesses, and text
    carriers. Witness ids join the record id set, since pointers target both."""
    textcarrier_ids = set()
    for filename, child in TEXTCARRIER_FILES.items():
        logger.info(f'Validating xml:ids in {filename}...')
        root = etree.parse(DATA_DIR / filename).getroot()
        for item in root.findall(child):
            register_id(item.get(XML_NS + 'id'), ID_PATTERN, filename, textcarrier_ids)

    record_ids = set()
    logger.info(f'Validating xml:ids in {RECORDS_FILE}...')
    root = etree.parse(DATA_DIR / RECORDS_FILE).getroot()
    for record in root.findall('record'):
        record_id = record.get(XML_NS + 'id')
        if record_id is None:
            continue  # not all items have an xml:id
        register_id(record_id, RECORD_ID_PATTERN, RECORDS_FILE, record_ids)

        witnesses = record.find('witnesses')
        if witnesses is None:
            continue
        dimev_number = record_id.removeprefix('record-')
        witness_pattern = re.compile(rf'wit-{re.escape(dimev_number)}-\d{{1,3}}')
        for witness in witnesses.findall('witness'):
            register_id(witness.get(XML_NS + 'id'), witness_pattern, RECORDS_FILE, record_ids)

    logger.info('Checks of xml:ids completed.\n')
    return record_ids, textcarrier_ids


def collect_bibl_ids():
    """Gather and validate the Zotero citation keys from the bibliography."""
    logger.info(f'Validating citation keys in {BIBLIOGRAPHY_FILE}...')
    registry = set()
    graph = Graph()
    graph.parse(DATA_DIR / BIBLIOGRAPHY_FILE)
    for _, _, citation_key in graph.triples((None, ZOTERO.citationKey, None)):
        register_id(str(citation_key), ID_PATTERN, BIBLIOGRAPHY_FILE, registry)
    logger.info(f'Found {len(registry)} citation keys in {BIBLIOGRAPHY_FILE}.\n')
    return registry


def register_id(item_id, pattern, filename, registry):
    """Validate a single id against `pattern`, check it for local duplication,
    and add it to `registry`. Logs an error for any problem found."""
    if not pattern.fullmatch(item_id):
        logger.error(f'malformed id "{item_id}" in {filename}')
    if item_id in registry:
        logger.error(f'duplicate xml:id "{item_id}" in {filename}')
    else:
        registry.add(item_id)


def verify_id_uniqueness(*id_sets):
    """Confirm no id is shared across the supplied id sets."""
    logger.info('Checking for duplicate ids across all sets of ids...')
    seen = set()
    for id_set in id_sets:
        for item in id_set:
            if item in seen:
                logger.error(f'duplicate xml:id "{item}" across id sets')
            else:
                seen.add(item)
    logger.info(f'Completed with {len(seen)} unique ids checked.')


def check_bibl_refs(textcarrier_ids, bibl_ids):
    """Check that every outbound bibl/source/mss key in Records.xml resolves,
    and report defined keys that go unreferenced."""
    logger.info(f'\nChecking bibliographic and source references in {RECORDS_FILE}...')
    root = etree.parse(DATA_DIR / RECORDS_FILE).getroot()

    referenced_bibl = set()
    referenced_textcarriers = set()
    for elem in root.iter('bibl', 'source', 'mss'):
        key = elem.get('key')
        if key is None:
            continue
        if elem.tag == 'bibl':
            referenced_bibl.add(key)
            if key not in bibl_ids:
                logger.error(f'Bibliography key {key} is referenced in {RECORDS_FILE} but not defined')
        else:  # text carriers: source, mss
            referenced_textcarriers.add(key)
            if key not in textcarrier_ids:
                logger.error(f'Source key {key} is referenced in {RECORDS_FILE} but not defined')

    # Reporting unreferenced keys is informational only: it yields many false
    # positives, since keys referenced solely from (e.g.) Manuscripts.xml are
    # not seen here.
    unreferenced_textcarriers = textcarrier_ids - referenced_textcarriers
    unreferenced_bibl = bibl_ids - referenced_bibl
    if unreferenced_textcarriers:
        logger.warning(f'Found {len(unreferenced_textcarriers)} unreferenced textcarrier '
                       f'key(s): {", ".join(sorted(unreferenced_textcarriers))}')
    if unreferenced_bibl:
        logger.warning(f'Found {len(unreferenced_bibl)} unreferenced keys to modern scholarly works')


def check_crossrefs(record_ids):
    """Check that internal pointer targets resolve to a known record or witness.

    Pointers (`ptr`) carry either an internal fragment reference ("#" + the
    xml:id of a record or witness) or an absolute URI to an external resource.
    Only internal targets are resolved here; external URIs are left to verify by
    other means."""
    logger.info(f'\nChecking pointer targets in {RECORDS_FILE}...')
    root = etree.parse(DATA_DIR / RECORDS_FILE).getroot()
    for ptr in root.iter('ptr'):
        target = ptr.get('target')
        if not target.startswith('#'):
            continue  # external resource (absolute URI)
        if target[1:] not in record_ids:
            logger.error(f'bad target value "{target}"')


def validate_terms():
    """Check that subject, verse-form, and language terms in Records.xml are
    drawn from their controlled vocabularies."""
    logger.info(f'\nValidating {", ".join(TERM_DOMAINS)} terms...')
    root = etree.parse(DATA_DIR / RECORDS_FILE).getroot()
    for domain, target_tag in TERM_DOMAINS.items():
        valid_terms = load_valid_terms(domain)
        for record in root.findall('record'):
            target = record.find(target_tag)
            if target is None:
                continue
            for term in target:
                if term.text not in valid_terms:
                    logger.error(f'unrecognized {domain} term "{term.text}"')


def load_valid_terms(domain):
    """Return the set of valid terms for a controlled-vocabulary domain."""
    root = etree.parse(DATA_DIR / f'{domain}-terms.xml').getroot()
    return {item.findtext('term') for item in root.findall('item')}


if __name__ == '__main__':
    sys.exit(main())
