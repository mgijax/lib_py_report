#!/bin/sh

#
# Run all unit tests
#

echo "Running go_annot_extensions tests"
python go_annot_extensions_tests.py  || exit 1;

