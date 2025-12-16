#!/usr/bin/env python3

import glob
from lxml import etree

# Find all XML files in the directory
data_dir = 'data/'
xml_files = glob.glob(data_dir + '*.xml')

for file in xml_files:
    tree = etree.parse(file)
    etree.indent(tree, space= 4*' ', level=0)
    tree.write(file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
print('Done')
