'''
Created on Nov 26, 2013

@author: admin-jed
'''
import unittest
from permute import pooled_results_file
from permute import pooled_results_delta_file
from permute import pooled_timings_file
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

    def test_gen_result_perm_code_from_pieces(self):
        y_permutation = {'letter': 'AAA' }
        x_permutation = {'number': '3', 'animal':'dog'}
        filename_perm_dict = {'singleton_val':'300', 'resolution':'userDay' }
        result = pooled_results_file.gen_result_perm_code_from_pieces(y_permutation, x_permutation, filename_perm_dict, self.cspec, '2')
        #print "RESULT : {0}".format(result)
        self.assertTrue(result == 'an_dog_l_aa_number_3_res_userDay_s_300_trials_2')
        
    def test_gen_cluster_job_perm_code_from_pieces(self):
        y_permutation = {'letter': 'AAA' }
        x_permutation = {'number': '3', 'animal':'dog'}
        filename_perm_dict = {'singleton_val':'300', 'resolution':'userDay' }
        result = pooled_timings_file.gen_cluster_job_perm_code_from_pieces(y_permutation, x_permutation, filename_perm_dict, self.cspec, '2')
        print "RESULT : {0}".format(result)
        self.assertTrue(result == 'an_dog_l_aa_number_3_s_300_trials_2')
         
    def test_generate_target_dirname(self):
        dirname = pooled_results_file.generate_target_dirname(self.cspec)
        #print "DIR IS : {0}".format(dirname)
        self.assertTrue(dirname == './collected_results/unittest')
        
    def test_get_median(self):
        x = ['0.1']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.1')
        
        x = ['0.2', '0.1']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(float(str(result)) == 0.15) # hack to get float 0.15 to equal float 0.15!
        
        x = ['0.3', '0.1', '0.2']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.2')
        
        x = ['0.4', '0.1', '0.3', '0.2']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.25')
        
        x = ['0.1', '0.5', '0.2', '0.3', '0.4']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.3')
        
        x = ['0.1', '0.6', '0.5', '0.4', '0.2', '0.3' ]
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.35')
        
        x = ['0.1', '0.6', '0.5', '0.7', '0.4', '0.2', '0.3' ]
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.4')
         
        x = ['missing', 'missing', 'missing']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == 'xxx')
        
        x = ['0.1', 'missing', 'missing']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.1xx')
        
        x = ['0.1', 'missing', '0.3']
        result = pooled_results_file.get_median(x, False)
        self.assertTrue(result == '0.2x')
        
        x = ['400.111', '500.111', '600.111']
        result = pooled_results_file.get_median(x, True)
        self.assertTrue(result == '500')
        
        x = ['500.111', 'missing', 'missing']
        result = pooled_results_file.get_median(x, True)
        self.assertTrue(result == '500xx')
        
        x = ['missing', 'missing', 'missing']
        result = pooled_results_file.get_median(x, True)
        self.assertTrue(result == 'xxx')
        
    def test_build_code_using_dictionary(self):
        perm_dict = {'singleton_val':'300', 'res':'userDay' }
        code = pooled_results_file.build_code_using_dictionary(perm_dict, self.cspec)
        self.assertTrue(code == 'res_userDay_s_300')
        
    def test_get_result_from_file(self):
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'auc', 1)
            self.assertTrue(result == '0.877')
        except Exception as detail:
            self.fail(detail)

        #try the last field in the line
        try:
            result = pooled_results_file.get_result_from_file('./sample_result_file.txt', 'ap', 1)
            self.assertTrue(result == '0.001')
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
      
    def test_median_expression_has_Xs(self):
        self.assertFalse(pooled_results_file.median_expression_has_Xs('0.123'))
        self.assertTrue(pooled_results_file.median_expression_has_Xs('0.123x'))
        self.assertTrue(pooled_results_file.median_expression_has_Xs('0.123xx'))
        self.assertTrue(pooled_results_file.median_expression_has_Xs('0.123xxx'))
        self.assertTrue(pooled_results_file.median_expression_has_Xs('xxx'))
        
    def test_median_expression_has_float(self):
        self.assertTrue(pooled_results_file.median_expression_has_float('0.123'))
        self.assertTrue(pooled_results_file.median_expression_has_float('0.123x'))
        self.assertTrue(pooled_results_file.median_expression_has_float('0.123xx'))
        self.assertTrue(pooled_results_file.median_expression_has_float('0.123xxx'))
        self.assertFalse(pooled_results_file.median_expression_has_float('xxx'))
    
    def test_get_float_from_median_expression(self):
        self.assertTrue(pooled_results_file.get_float_from_median_expression('0.123') == 0.123)
        self.assertTrue(pooled_results_file.get_float_from_median_expression('0.123x') == 0.123)
        self.assertTrue(pooled_results_file.get_float_from_median_expression('0.123xx') == 0.123)
        self.assertTrue(pooled_results_file.get_float_from_median_expression('0.123xxx') == 0.123)
        # only called after its determined that a float is present, so no need to test the '_X_X_X' case
    
    def test_get_Xs_from_median_expression(self):
        self.assertTrue(pooled_results_file.get_Xs_from_median_expression('xxx') == 'xxx')
        self.assertTrue(pooled_results_file.get_Xs_from_median_expression('0.123x') == 'x')
        self.assertTrue(pooled_results_file.get_Xs_from_median_expression('0.123xx') == 'xx')
        self.assertTrue(pooled_results_file.get_Xs_from_median_expression('0.123xxx') == 'xxx')
            
    def test_compute_average_medians(self):
        medians_list = ['0.8', '0.7', '0.9']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800')
        medians_list = ['0.8x', '0.7', '0.9']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800x')
        medians_list = ['0.8xx', '0.7', '0.9']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800xx')
        medians_list = ['0.8xxx', '0.7', '0.9']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800xxx')
        medians_list = ['0.8x', '0.7x', '0.9']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800xx')
        medians_list = ['0.8x', '0.7x', '0.9x']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800xxx')
        medians_list = ['0.8xx', '0.7xx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.750xxxxxxx')
        medians_list = ['xxx', 'xxx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == 'xxxxxxxxx')
        medians_list = ['0.8xx', 'xxx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, False) == '0.800xxxxxxxx')

        medians_list = ['800', '700', '900']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800')
        medians_list = ['800x', '700', '900']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800x')
        medians_list = ['800xx', '700', '900']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800xx')
        medians_list = ['800xxx', '700', '900']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800xxx')
        medians_list = ['800x', '700x', '900']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800xx')
        medians_list = ['800x', '700x', '900x']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800xxx')
        medians_list = ['800xx', '700xx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '750xxxxxxx')
        medians_list = ['xxx', 'xxx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == 'xxxxxxxxx')
        medians_list = ['800xx', 'xxx', 'xxx']
        self.assertTrue(pooled_results_file.compute_average_medians(medians_list, True) == '800xxxxxxxx')
    def test_get_index_first_float(self):
        parts = []
        parts.append('foo')
        parts.append('0.123')
        parts.append('0.3xx')
        self.assertTrue(pooled_results_delta_file.get_index_first_float(parts, 1) == 1)
        
        parts = []
        parts.append('foo')
        parts.append('xxx')
        parts.append('0.123')
        self.assertTrue(pooled_results_delta_file.get_index_first_float(parts, 1) == 2)
        
        parts = []
        parts.append('foo')
        parts.append('xxx')
        parts.append('0.123x')
        self.assertTrue(pooled_results_delta_file.get_index_first_float(parts, 1) == 2)
        
        parts = []
        parts.append('foo')
        parts.append('0.123xx')
        parts.append('xxx')
        self.assertTrue(pooled_results_delta_file.get_index_first_float(parts, 1) == 1)
        
        parts = []
        parts.append('foo')
        parts.append('xxx')
        parts.append('xxx')
        self.assertTrue(pooled_results_delta_file.get_index_first_float(parts, 1) == -1)
            
    def test_create_delta_line(self):
        number_line = "2013-04,0.82333,0.92333,0.72333"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.10,-0.10")
        
        number_line = "2013-04,0.082333,0.092333,0.072333"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.01,-0.01")
        
        number_line = "2013-04,0.0082333,0.0092333,0.0072333"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.00,-0.00")
        
        
        number_line = "2013-04,0.82333,0.92333x,0.72333"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        print "delta line : {0}".format(delta_line)
        self.assertTrue(delta_line == "2013-04,0,0.10x,-0.10")
        
        
        number_line = "2013-04,0.82333,0.92333xx,0.72222"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.10xx,-0.10")
        
        
        number_line = "2013-04,0.82333,xxx,0.72222"
        delta_line = pooled_results_delta_file.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,xxx,-0.10")
       
    def test_beautify_header(self):  
        header = "['month', 'fv_type']" 
        header = pooled_results_file.beautify_header(header)  
        self.assertTrue(header == "month-fv_type")  
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()