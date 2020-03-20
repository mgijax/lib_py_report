#
# Unit tests for the go_isoforms module
# 
#

import sys,os.path
# adjust the path for running the tests locally, so that it can find the modules (1 dir up)
sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
import unittest

import go_isoforms

class IsoformProcessorTest(unittest.TestCase):
        """
        Test processing of isoform values
        """

        def setUp(self):
                
                # create a processor for each test
                self.processor = go_isoforms.Processor()


        ### Basic cases ###

        def test_empty_value(self):
                value = ''
                expected = []
                self.assertEqual(expected, self.processor.processValue(value))

        def test_unknown_value(self):
                value = 'testing'
                expected = ['testing']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_UniProtKB(self):
                value = 'UniProtKB:Q3TVE1'
                expected = ['UniProtKB:Q3TVE1']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_UniProtKB_lowercase(self):
                value = 'uniprotkb:12345'
                expected = ['uniprotkb:12345']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_protein_id(self):
                value = 'protein_id:AAC53152'
                expected = ['protein_id:AAC53152']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_NCBI_NP(self):
                value = 'NCBI:NP_032724'
                expected = ['RefSeq:NP_032724']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_NCBI_XP(self):
                value = 'NCBI:XP_032724'
                expected = ['RefSeq:XP_032724']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_PR(self):
                value = 'PR:Q99KP6-2'
                expected = ['PR:Q99KP6-2']
                self.assertEqual(expected, self.processor.processValue(value))

        ### Complex cases ###

        def test_multiple_ids(self):
                value = 'PR:001 PR:002\t PR:003'
                expected = ['PR:001','PR:002','PR:003']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_multiple_different_ids(self):
                value = 'PR:001 UniProtKB:002 protein_id:003'
                expected = ['PR:001','UniProtKB:002','protein_id:003']
                self.assertEqual(expected, self.processor.processValue(value))

        def test_duplicates(self):
                value = 'PR:001 PR:001  PR:001'
                expected = ['PR:001']
                self.assertEqual(expected, self.processor.processValue(value))

if __name__ == '__main__':
        unittest.main()
