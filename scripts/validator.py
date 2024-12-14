# This Python script validates an XML file against its XSD schema. To specify
# the XML file to be validated, update the value of `xml_file`. Run the script
# from the root directory.

import xmlschema

xml_file = 'Manuscripts.xml'

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

print(f'Validating XML file {xml_file} with {schema_file}')

# Load the XSD schema
schema = xmlschema.XMLSchema('schemas/' + schema_file)

# Validate the XML file
try:
    schema.validate('data/' + xml_file)
    print("XML is valid")
except xmlschema.XMLSchemaValidationError as e:
    print("XML validation failed:")
    print(e)
