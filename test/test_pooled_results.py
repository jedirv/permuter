'''
Created on Nov 26, 2013

@author: admin-jed
'''
import unittest
from monitor import pooled_results_file
from monitor import monitor_exception

class TestPooledResultsFile(unittest.TestCase):


    def test_get_result_from_file(self):
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'auc', 1)
            self.assertTrue(result == '0.87682755275285')
        except monitor_exception.MonitorException as detail:
            self.fail(detail)

        #try the last field in the line
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'ap', 1)
            self.assertTrue(result == '0.000748909371611072')
        except monitor_exception.MonitorException as detail:
            self.fail(detail)

        # try a nonexistent column
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'foo', 1)
            self.fail("should have complained about non-existent column")
        except monitor_exception.MonitorException as detail:
            self.assertTrue(True)
            
        # try a nonexistent line
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'auc', 10)
            self.fail("should have complained about non-existent column")
        except monitor_exception.MonitorException as detail:
            self.assertTrue(True)
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()