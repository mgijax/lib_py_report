#
# Library for gathering and processing
#	annotation extension data
#
#
# Usage:
#	1) Use the Processor class to query the 
#	sanctioned property and evidence term keys
#	to use for selecting GO annotation extension data
#
#	2) Use the Processor class to process the property values
#

import db

### Private Constants ###

# Property terms we don't use for annotation extensions or GAF file
_EXCLUDED_TERMS = [
	'evidence',
	'anatomy',
	'cell type',
	'gene product',
	'modification',
	'target',
	'external ref',
	'text',
	'dual-taxon ID',
	'noctua-model-id', 
	'model-state',
	'individual', 
	'go_qualifier'
]

_PROPERTY_VOCAB_NAME = 'GO Property'


_EXCLUDED_EVIDENCE_CODES = [
	'ISO'
]

_EVIDENCE_VOCAB_NAME = 'GO Evidence Codes'


### Public classes and functions ###

class Processor(object):
	"""
	Processes annotation extension data
	"""
	
	def __init__(self):

		self.excludedTerms = _EXCLUDED_TERMS
		self.propertyVocabName = _PROPERTY_VOCAB_NAME

		self.excludedEvidenceCodes = _EXCLUDED_EVIDENCE_CODES
		self.evidenceVocabName = _EVIDENCE_VOCAB_NAME


	def querySanctionedPropertyTermKeys(self):
		"""
		Query MGD for the sanctioned _propertyterm_keys
		we can use for GO annotation extensions
		"""

		cmd = '''
		select _term_key
		from voc_term t 
		join voc_vocab v on
			v._vocab_key = t._vocab_key
		where v.name = '%s'
			and t.term not in ('%s')
		''' % ( self.propertyVocabName, "','".join(self.excludedTerms) )

		results = db.sql(cmd, 'auto')

		sanctionedTermKeys = [c['_term_key'] for c in results]
		return sanctionedTermKeys

	def querySanctionedEvidenceTermKeys(self):
		"""
		Query MGD for the sanctioned _evidenceterm_keys
		we can use for GO annotation extensions
		"""
		
		cmd = '''
		select _term_key
		from voc_term t 
		join voc_vocab v on
			v._vocab_key = t._vocab_key
		where v.name = '%s'
			and t.abbreviation not in ('%s')
		''' % ( self.evidenceVocabName, "','".join(self.excludedEvidenceCodes) )

		results = db.sql(cmd, 'auto')

		sanctionedTermKeys = [c['_term_key'] for c in results]
		return sanctionedTermKeys

	def processValue(self, value):
		"""
		process the value of an annotation extension property
			for public consumption
	
		returns processed value
		"""

		#
		# curator's may enter addtional information in the 'value' 
		# this additional information needs to be excluded
		#
		# example for Hk1:  "ATP ; ChEBI:33221" ==> "ChEBI:33221"
		#
		parts = value.split(';')
		idValue = parts[-1]
		idValue = idValue.strip()

		# remove TS from EMAPA values
		if idValue.startswith('EMAPA:'):
			idValue = idValue.split(' ')[0]

		return idValue
 
