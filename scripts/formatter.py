#!/usr/bin/env python3

# /// script
# dependencies = [
#   "lxml"
# ]
# ///

from pathlib import Path
from lxml import etree
from itertools import chain

# Find XML and XSD files
root = Path(__file__).parent.parent.resolve()
data_dir = root / 'data'
schema_dir = root / 'schemas'
xml_files = data_dir.glob('*.xml')
xsd_files = schema_dir.glob('*xsd')
files_to_format = chain(xml_files, xsd_files)

# Configure the parser

parser = etree.XMLParser(remove_blank_text=True)

# Parse and rewrite

for file in files_to_format:
    print(f'Formatting {file.name}...')
    tree = etree.parse(file, parser)
    etree.indent(tree, space= 4*' ', level=0)
    tree.write(file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
print('Done')
