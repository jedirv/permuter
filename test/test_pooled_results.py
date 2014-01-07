'''
Created on Nov 26, 2013

@author: admin-jed
'''
import unittest
from permute import pooled_results_file
from permute import pooled_results_delta_file
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
        y_permutation = {'letter': 'AAA' }
        x_permutation = {'number': '3', 'animal':'dog'}
        filename_perm_dict = {'singleton_val':'300', 'res':'userDay' }
        result = pooled_results_file.gen_perm_code_from_pieces(y_permutation, x_permutation, filename_perm_dict, self.cspec, '2')
        #print "RESULT : {0}".format(result)
        self.assertTrue(result == 'an_dog_l_aa_number_3_res_userDay_s_300_trials_2')
         
    def test_generate_target_dirname(self):
        dirname = pooled_results_file.generate_target_dirname(self.cspec)
        #print "DIR IS : {0}".format(dirname)
        self.assertTrue(dirname == './collected_results/unittest')
        
    def test_get_median(self):
        x = [0.1]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.1)
        
        x = [0.2, 0.1]
        result = pooled_results_file.get_median(x)
        self.assertTrue(float(str(result)) == 0.15) # hack to get float 0.15 to equal float 0.15!
        
        x = [0.3, 0.1, 0.2]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.2)
        
        x = [0.4, 0.1, 0.3, 0.2]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.25)
        
        x = [0.1, 0.5, 0.2, 0.3, 0.4]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.3)
        
        x = [0.1, 0.6, 0.5, 0.4, 0.2, 0.3 ]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.35)
        
        x = [0.1, 0.6, 0.5, 0.7, 0.4, 0.2, 0.3 ]
        result = pooled_results_file.get_median(x)
        self.assertTrue(result == 0.4)
         
        
    def test_build_code_using_dictionary(self):
        perm_dict = {'singleton_val':'300', 'res':'userDay' }
        code = pooled_results_file.build_code_using_dictionary(perm_dict, self.cspec)
        self.assertTrue(code == 'res_userDay_s_300')
        
    def test_get_result_from_file(self):
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'auc', 1)
            self.assertTrue(result == '0.87682755275285')
        except Exception as detail:
            self.fail(detail)

        #try the last field in the line
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'ap', 1)
            self.assertTrue(result == '0.000748909371611072')
        except Exception as detail:
            self.fail(detail)

        # try a nonexistent column
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'foo', 1)
            self.fail("should have complained about non-existent column")
        except Exception as detail:
            self.assertTrue(True)
            
        # try a nonexistent line
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'auc', 10)
            self.fail("should have complained about non-existent column")
        except Exception as detail:
            self.assertTrue(True)
      
      
    def test_create_delta_line(self):
        number_line = "2013-04,0.82333,0.92333,0.72222"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.10,-0.10")
        
        number_line = "2013-04,0.082333,0.092333,0.072222"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.01,-0.01")
        
        number_line = "2013-04,0.0082333,0.0092333,0.0072222"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.00,-0.00")
              
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()