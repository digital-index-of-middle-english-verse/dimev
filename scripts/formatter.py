#!/usr/bin/env python3

from pathlib import Path
from lxml import etree

# Find all XML files in the data directory
root = Path(__file__).parent.parent.resolve()
data_dir = root / 'data'
xml_files = data_dir.glob('*.xml')

# Configure the parser

parser = etree.XMLParser(remove_blank_text=True)

# Parse and rewrite

for file in xml_files:
    print(f'Formatting {file.name}...')
    tree = etree.parse(file, parser)
    etree.indent(tree, space= 4*' ', level=0)
    tree.write(file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
print('Done')
