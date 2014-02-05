import unittest
from permute import cluster_spec

class TestClusterSpec(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)

    def test_convert_escaped_commas(self):
        foo = [ '1_comma_2_comma_3', '4', '5_comma_6']
        bar = cluster_spec.convert_escaped_commas(foo)
        self.assertTrue(bar[0] == '1,2,3')
        self.assertTrue(bar[1] == '4')
        self.assertTrue(bar[2] == '5,6')
        
    def test_zero_pad_to_widest(self):
        all_integers = ['0','10','345']
        padded_integers = cluster_spec.zero_pad_to_widest(all_integers)
        self.assertTrue(padded_integers == ['000', '010', '345'])
        
        all_numbers = ['0','.10','34.52']
        padded_numbers = cluster_spec.zero_pad_to_widest(all_numbers)
        #print "PADDED_NUMBERS {0}".format(padded_numbers)
        self.assertTrue(padded_numbers == ['00', '00.1', '34.52'])
        
        non_numbers = ['a','bbb','cc']
        padded_non_numbers = cluster_spec.zero_pad_to_widest(non_numbers)
        self.assertTrue(padded_non_numbers == ['a','bbb','cc'])
        
        partial_numbers =  ['a','bbb','33','4']
        padded_partial_numbers = cluster_spec.zero_pad_to_widest(partial_numbers)
        self.assertTrue(padded_partial_numbers == ['a','bbb','33','4'])
        
    def test_get_concise_name(self):
        #print self.cspec.concise_print_map
        self.assertTrue(self.cspec.get_concise_name('number') == 'number')
        self.assertTrue(self.cspec.get_concise_name('letter') == 'l')
        self.assertTrue(self.cspec.get_concise_name('singleton_val') == 's')
        self.assertTrue(self.cspec.get_concise_name('resolution') == 'res')
        
    def test_scores_info(self):
        self.assertTrue(self.cspec.scores_permuters['resolution'][0] == 'userDay')
        self.assertTrue(self.cspec.scores_permuters['resolution'][1] == 'userMonth')
        
        self.assertTrue(self.cspec.scores_from_filepath=='<permutation_results_dir>/(resolution).csv')
        self.assertTrue(self.cspec.scores_from_colname=='auc')
        self.assertTrue(self.cspec.scores_from_rownum=='1')
        print 'self.cspec.scores_to : {0}'.format(self.cspec.scores_to)
        self.assertTrue(self.cspec.scores_to=='./collected_results')
        
        self.assertTrue(self.cspec.scores_x_axis==['number', 'animal'])
        self.assertTrue(self.cspec.scores_y_axis==['letter'])

    def test_script_dir(self):
        #print self.cspec.script_dir
        self.assertTrue(self.cspec.script_dir=='./scripts_unittest')
        
    def test_trials(self):
        self.assertTrue(self.cspec.trials=='2')
    
    def test_master_job_name(self):
        #print self.cspec.script_dir
        self.assertTrue(self.cspec.master_job_name=='unittest')
            
    def test_one_up_basis(self):
        #print ""
        #print "one up is _{0}_".format(self.cspec.one_up_basis)
        self.assertTrue(self.cspec.one_up_basis == '100')
        
    def test_root_results_dir(self):
        #print ""
        #print "one up is _{0}_".format(self.cspec.one_up_basis)
        self.assertTrue(self.cspec.root_results_dir == './sample_results')
    
    def test_validate_master_job_name(self):
        self.assertFalse(cluster_spec.validate_master_job_name("malformed_cspecs/missing_basics.cspec"))
            
    def test_validate_root_results_dir(self):
        self.assertFalse(cluster_spec.validate_root_results_dir("malformed_cspecs/missing_basics.cspec"))
                
    def test_validate_permutes(self):
        self.assertFalse(cluster_spec.validate_permute_entries("malformed_cspecs/permute_colon_count.cspec"))
        self.assertFalse(cluster_spec.validate_permute_entries("malformed_cspecs/permute_start_integer.cspec"))
        self.assertFalse(cluster_spec.validate_permute_entries("malformed_cspecs/permute_end_integer.cspec"))
        self.assertFalse(cluster_spec.validate_permute_entries("malformed_cspecs/permute_integer_order.cspec"))
        
        self.assertTrue(cluster_spec.validate_permute_entries("well_formed_cspecs/permute_integer_range.cspec"))
        self.assertTrue(cluster_spec.validate_permute_entries("well_formed_cspecs/permute_singleton_range.cspec"))
        self.assertTrue(cluster_spec.validate_permute_entries("well_formed_cspecs/permute_comma_list_range.cspec"))
        
    def test_validate_replaces(self):
        self.assertFalse(cluster_spec.validate_replace_entries("malformed_cspecs/replace_empty_key.cspec"))
        self.assertFalse(cluster_spec.validate_replace_entries("malformed_cspecs/replace_empty_val.cspec"))
        self.assertFalse(cluster_spec.validate_replace_entries("malformed_cspecs/replace_colon_count.cspec"))
        
        self.assertTrue(cluster_spec.validate_replace_entries("well_formed_cspecs/replace_basic.cspec"))
        
    def test_validate_trials(self):
        self.assertFalse(cluster_spec.validate_trials("malformed_cspecs/missing_basics.cspec"))
        self.assertTrue(cluster_spec.validate_trials("well_formed_cspecs/basics.cspec"))
        
    def test_load_permutes(self):
        self.assertTrue(self.cspec.permuters['number'][0] == '1')
        self.assertTrue(self.cspec.permuters['number'][1] == '2')
        self.assertTrue(self.cspec.permuters['number'][2] == '3')
        self.assertTrue(self.cspec.permuters['letter'][0] == 'AAA')
        self.assertTrue(self.cspec.permuters['letter'][1] == 'BBB')
        
    def test_generate_results_dir_for_permutation(self):
        self.assertTrue(self.cspec.generate_results_dir_for_permutation('3','xyz') == './sample_results/unittest/trial3/xyz')
        
    def test_concise_print_map(self):
        self.assertTrue(self.cspec.concise_print_map['letter'] == 'l')
        self.assertTrue(self.cspec.concise_print_map['singleton_val'] == 's')

    def test_key_val_map(self):
        kvm = self.cspec.key_val_map
        self.assertTrue(kvm['config[AAA]']=='aaa')
        self.assertTrue(kvm['config[BBB]']=='bbb')
        self.assertTrue(kvm['pretty[1]']=='one')
        self.assertTrue(kvm['pretty[2]']=='two')
        self.assertTrue(kvm['pretty[3]']=='three')
        self.assertTrue(kvm['master_job_name']=='unittest')
        self.assertTrue(kvm['root']=='/nfs/foo/bar')
        self.assertTrue(kvm['x_dir']=='/nfs/foo/bar/(letter)/<config[(letter)]>/(number)')
        self.assertTrue(kvm['algs_dir']=='/nfs/algs')
        self.assertTrue(kvm['tools_dir']=='/nfs/algs/tools')
        self.assertTrue(kvm['outfile_root']=='<pretty[(number)]>__TEST')
            
    def test_commands(self):
        commands_as_string = "{0}".format(self.cspec.commands)
        self.assertTrue(commands_as_string == "['echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt']")
           
    def test__qsub_commands(self):
        qsub_commands_as_string = "{0}".format(self.cspec.qsub_commands)
        self.assertTrue(qsub_commands_as_string == "['-q eecs,eecs1,eecs,share', '-M someone@gmail.com', '-m beas']")
  
    def test_resolve_value(self):
        kv = {}
        kv['x'] = 'foo'
        self.assertTrue('somethingfoo' == cluster_spec.resolve_value(kv, 'something<x>'))
        
    def test_is_valid_permuter(self):
        lines = []
        lines.append('something_irrelevant\n')
        lines.append('permute:foo=1,2\n')
        lines.append('scores_permute:bar=a,b\n')
        self.assertTrue(cluster_spec.is_valid_permuter('foo', lines))
        self.assertTrue(cluster_spec.is_valid_permuter('bar', lines))
        self.assertFalse(cluster_spec.is_valid_permuter('whim', lines))
        
        
    def test_validate_axis_list(self):
        # more than one entry
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:foo\n')
        lines.append('scores_x_axis:bar\n')
        self.assertFalse(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # no entry
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        self.assertFalse(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has one good, one bad permuter
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:foo,baz\n')
        self.assertFalse(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has three bad permuters
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:eeny,meeny,miny\n')
        self.assertFalse(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has one good permuter
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:foo\n')
        self.assertTrue(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has two good permuters
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:foo,bar\n')
        self.assertTrue(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
    def test_validate_scores_to(self):
        lines = []
        lines.append('scores_to:./junk\n')
        lines.append('scores_to:./junk2\n')
        self.assertFalse(cluster_spec.validate_scores_to(lines))
        
        lines = []
        lines.append('scores_to:./junk\n')
        self.assertTrue(cluster_spec.validate_scores_to(lines))
        
    def test_validate_scores_from(self):
        #scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1
        # multiple entries
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1')
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        #no permuteion_results_dir
        lines = []
        lines.append('scores_from:file=./(resolution).csv,column_name=auc,row_number=1')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        # not a csv file
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).txt,column_name=auc,row_number=1')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        # wrong colname flag
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).csv,col_name=auc,row_number=1')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        #wrong rownum flag
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_num=1')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        
        #non integer rownum
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=a')
        self.assertFalse(cluster_spec.validate_scores_from(lines))
        
        #good one
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1')
        self.assertTrue(cluster_spec.validate_scores_from(lines))
        
        
    def test_single_entry_present(self):
        lines = []
        lines.append('prefixA:foo\n')
        lines.append('prefixB:foo\n')
        lines.append('prefixB:foo\n')
        self.assertTrue(cluster_spec.single_entry_present(lines,'prefixA'))
        self.assertFalse(cluster_spec.single_entry_present(lines,'prefixB'))
        self.assertFalse(cluster_spec.single_entry_present(lines,'prefixC'))


    def test_validate_scores_gathering_info_from_lines(self):
        # none present is ok
        lines = []
        lines.append("foo\n")
        self.assertTrue(cluster_spec.validate_scores_gathering_info_from_lines(lines))
        
        #if any present, then 4 need to be present
        
        #missing from
        lines = []
        lines.append('scores_to:./collected_results')
        lines.append('scores_y_axis:letter')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info_from_lines(lines))
        
        #missing to
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_y_axis:letter')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info_from_lines(lines))
        
        #missing x axis
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results')
        lines.append('scores_y_axis:letter')
        self.assertFalse(cluster_spec.validate_scores_gathering_info_from_lines(lines))
        
        #missing y axis
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info_from_lines(lines))
        

        
    def test_lines_contains_prefix(self):
        lines = []
        lines.append('lineA\n')
        lines.append('prefix3:lineB\n')
        lines.append('lineC\n')
        self.assertFalse(cluster_spec.lines_contains_prefix(lines,'prefix2'))
        self.assertTrue(cluster_spec.lines_contains_prefix(lines,'prefix3'))
    
if __name__ == '__main__':
    unittest.main()
    
   