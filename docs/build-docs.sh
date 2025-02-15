#!/bin/bash

# This script builds the documentation as a PDF from components in the
# directory `docs/`. The script is intended to test local builds; it is
# equivalent to the build performed in the GitHub Action. Dependencies are
# those provided in the GitHub Action.
#
# Run the script from the `docs/` directory.

echo "Building the PDF as documentation.pdf..."
pandoc --metadata-file ./config/default.yaml --citeproc --number-sections --toc --pdf-engine xelatex documentation.md -o documentation.pdf
echo "Done"
