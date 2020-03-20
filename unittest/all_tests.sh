#!/bin/sh

#
# Run all unit tests
#

echo "Running go_annot_extensions tests"
${PYTHON} ./go_annot_extensions_tests.py  || exit 1;

echo "Running go_isoforms tests"
${PYTHON} ./go_isoforms_tests.py  || exit 1;
