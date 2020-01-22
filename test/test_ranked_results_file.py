'''
Created on Jan 10, 2014

@author: admin-jed
'''
import unittest
import ranked_results_file
 
class TestRankedResultsFile(unittest.TestCase):

        
    def test_sort_by_higher_score_then_lower_timing(self):
        # basic numbers
        tuples = []
        tuples.append(('e', 0.5, 'x', 100, 'xx'))
        tuples.append(('f', .003, '', 5, ''))
        tuples.append(('g', -1, 'xxx', -1, 'xxx'))
        tuples.append(('b', 0.8, '',  400, ''))
        tuples.append(('c', 0.7, '',  200, ''))
        tuples.append(('a', 0.923, 'xx',500, 'x'))
        tuples.append(('d', 0.7, '',  300, '' ))
        sorted_tuples = ranked_results_file.sort_by_higher_score_then_lower_timing(tuples)
        self.assertTrue(sorted_tuples[0] == ('a', 0.923, 'xx',500, 'x'))
        self.assertTrue(sorted_tuples[1] == ('b', 0.8, '',  400, ''))
        self.assertTrue(sorted_tuples[2] == ('c', 0.7, '',  200, ''))
        self.assertTrue(sorted_tuples[3] == ('d', 0.7, '',  300, '' ))
        self.assertTrue(sorted_tuples[4] == ('e', 0.5, 'x', 100, 'xx'))
        self.assertTrue(sorted_tuples[5] == ('f', .003, '', 5, ''))
        self.assertTrue(sorted_tuples[6] == ('g', -1, 'xxx', -1, 'xxx'))
        
        # numbers with variable number of digits
        tuples = []
        
        # 
