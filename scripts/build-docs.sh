#!/bin/bash

# This script builds the documentation as a PDF from components in the
# directory `doc/`. The script is intended to test local builds; it is
# equivalent to the build performed in the GitHub Action. Dependencies are
# those provided in the GitHub Action.
#
# Run the script from a child directory of root.

pushd ../docs/
echo "Building the PDF..."
pandoc --metadata-file ./config/default.yaml --citeproc --number-sections --toc --pdf-engine xelatex documentation.md -o documentation.pdf
popd
