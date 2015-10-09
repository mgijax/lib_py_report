#!/usr/local/bin/python
#
# Unit tests for the go_annot_extensions module
# 
#

import sys,os.path
# adjust the path for running the tests locally, so that it can find the modules (1 dir up)
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
import unittest

import go_annot_extensions

class AnnotationExtensionProcessorTest(unittest.TestCase):
	"""
	Test processing of annotation extension values
	"""

	def setUp(self):
		
		# create a processor for each test
		self.processor = go_annot_extensions.Processor()


	### Basic cases ###

	def test_empty_value(self):
		value = ''
		expected = ''
		self.assertEquals(expected, self.processor.processValue(value))

	def test_simple_text(self):
		value = 'spleen'
		expected = 'spleen'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_simple_id(self):
		value = 'CL:0000009'
		expected = 'CL:0000009'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_id_with_padding(self):
		value = '    CL:0000009   '
		expected = 'CL:0000009'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_mgiid(self):
		value = 'MGI:123456'
		expected = 'MGI:123456'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_comments(self):
		value = 'spleen ; MA:1234'
		expected = 'MA:1234'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_emapaid(self):
		value = 'EMAPA:123456'
		expected = 'EMAPA:123456'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_emapaid_with_stage(self):
		"""
		theiler stage gets stripped
		"""
		value = 'EMAPA:123456 TS12'
		expected = 'EMAPA:123456'
		self.assertEquals(expected, self.processor.processValue(value))


	### Complex cases ###

	def test_comments_with_no_spacing(self):
		value = 'spleen;MA:1234'
		expected = 'MA:1234'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_long_comment(self):
		value = 'This is a long comment (with syn:testing syntax) ; MA:123456'
		expected = 'MA:123456'
		self.assertEquals(expected, self.processor.processValue(value))

	def test_comment_with_many_semicolons(self):
		value = ' This has ;multiple semicolons ; ;;MA:123456 '
		expected = 'MA:123456'
		self.assertEquals(expected, self.processor.processValue(value))
		

if __name__ == '__main__':
        unittest.main()
