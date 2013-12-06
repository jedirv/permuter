'''
Created on Nov 26, 2013

@author: admin-jed
'''
import unittest
from monitor import pooled_results_file
from monitor import monitor_exception
from permute import cluster_spec

class TestPooledResultsFile(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)

    def test_gather_file_permuters(self):
        perm_dict = pooled_results_file.gather_file_permuters(self.cspec)
        keys = perm_dict.keys()
        self.assertTrue(len(keys) == 2)
        self.assertTrue(perm_dict.has_key('singleton_val'))
        self.assertTrue(perm_dict.has_key('resolution'))

    def test_gen_perm_code_from_pieces(self):
        y_axis_val = 'AAA'
        x_axis_val = 3
        filename_perm_dict = perm_dict = {'singleton_val':'300', 'res':'userDay' }
        result = pooled_results_file.gen_perm_code_from_pieces(y_axis_val, x_axis_val, filename_perm_dict, self.cspec)
        #print "RESULT : {0}".format(result)
        self.assertTrue(result == 'l_aa_number_3_res_userDay_s_300')
         
    def test_generate_target_dirname(self):
        dirname = pooled_results_file.generate_target_dirname(self.cspec)
        #print "DIR IS : {0}".format(dirname)
        self.assertTrue(dirname == './collected_results/unittest')
        
    def test_build_code_using_dictionary(self):
        perm_dict = {'singleton_val':'300', 'res':'userDay' }
        code = pooled_results_file.build_code_using_dictionary(perm_dict, self.cspec)
        self.assertTrue(code == 'res_userDay_s_300')
        
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