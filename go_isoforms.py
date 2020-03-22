#
# Library for gathering and processing
#       GO annotation isoform data
#
#
# Usage:
#       1) Use the Processor class to query the 
#               correct _propertyterm_keys
#       to use for selecting GO isoform data
#
#       2) Use the Processor class to process the property values
#

import db
import re

### Private Constants ###

# Property terms we use for isoforms
_INCLUDED_TERMS = [
        'gene product',
]

_PROPERTY_VOCAB_NAME = 'GO Property'


### Public classes and functions ###

class Processor(object):
        """
        Processes isoform data
        """
        
        def __init__(self):

                self.includedTerms = _INCLUDED_TERMS
                self.propertyVocabName = _PROPERTY_VOCAB_NAME
                self.whitespacePattern = re.compile(r'([^\s\\\n]*)', re.I)

        def querySanctionedPropertyTermKeys(self):
                """
                Query MGD for the sanctioned _propertyterm_keys
                we can use for GO isoforms
                """

                cmd = '''
                select _term_key
                from voc_term t 
                join voc_vocab v on
                        v._vocab_key = t._vocab_key
                where v.name = '%s'
                        and t.term in ('%s')
                ''' % ( self.propertyVocabName, "','".join(self.includedTerms) )

                results = db.sql(cmd, 'auto')

                sanctionedTermKeys = [c['_term_key'] for c in results]
                return sanctionedTermKeys


        def processValue(self, value):
                """
                process the value of a pipe-delimited isoform property
                        for public consumption
        
                returns list of processed values
                """
                isoforms = []

                seen = set([])

                # split on whitespace
                for token in self.whitespacePattern.findall(value):

                    token = token.strip()

                    if not token:
                        continue

                    if token in seen:
                        continue

                    seen.add(token)

                    # replace NCBI with RefSeq
                    token = token.replace('NCBI:', 'RefSeq:')
                    
                    isoforms.append(token)

                return isoforms

