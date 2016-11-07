import unittest
from permute import cluster_spec
import mock_cluster_system
import mock_stdout

class TestClusterSpec(unittest.TestCase):

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
        
    def test_load_cspec(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("trials:2\n")
        lines.append("tag=_myTag\n")
        lines.append("(permute):number=range(1,4)\n") # new form
        lines.append("permute:letter=AAA,BBB\n")
        lines.append("permute:singleton_val=300\n")
        lines.append("permute:animal=dog,cat\n")
        lines.append("concise_print:animal,an\n")
        lines.append("encode:letter,l\n") # alternate form
        lines.append("concise_print:singleton_val,s\n")
        lines.append("concise_print:resolution,res\n")
        lines.append("concise_print:AAA,aa\n")
        lines.append("concise_print:BBB,bb\n")

        lines.append("scores_permute:resolution=userDay,userMonth\n")
        lines.append("scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1\n")
        lines.append("scores_to:./collected_results\n")
        lines.append("scores_y_axis:letter\n")
        lines.append("scores_x_axis:number,animal\n")
        
        lines.append("<replace>:config[AAA]=aaa\n")
        lines.append("<replace>:config[BBB]=bbb\n")

        lines.append("<replace>:pretty[1]=one\n")
        lines.append("<replace>:pretty[2]=two\n")
        lines.append("<replace>:pretty[3]=three\n")

        lines.append("<replace>:root=/nfs/foo/bar\n")
        lines.append("<replace>:x_dir=<root>/(letter)/<config[(letter)]>/(number)\n")
        lines.append("<replace>:algs_dir=/nfs/algs\n")
        lines.append("<replace>:tools_dir=<algs_dir>/tools\n")
        lines.append("<replace>:outfile_root=<pretty[(number)]>__TEST\n")

        lines.append("root_dir:./myRuns\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:100\n")

        lines.append("command:echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt\n")
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines,stdout)
        #print self.cspec.concise_print_map
        # concise_name
        self.assertTrue(cspec.get_concise_name('number') == 'number')
        self.assertTrue(cspec.get_concise_name('letter') == 'l')
        self.assertTrue(cspec.get_concise_name('singleton_val') == 's')
        self.assertTrue(cspec.get_concise_name('resolution') == 'res')
        
        #scores_info
        self.assertTrue(cspec.scores_permuters['resolution'][0] == 'userDay')
        self.assertTrue(cspec.scores_permuters['resolution'][1] == 'userMonth')
        
        self.assertTrue(cspec.scores_from_filepath=='<permutation_results_dir>/(resolution).csv')
        self.assertTrue(cspec.scores_from_colname=='auc')
        self.assertTrue(cspec.scores_from_rownum=='1')
        #print 'self.cspec.scores_to : {0}'.format(self.cspec.scores_to)
        self.assertTrue(cspec.scores_to=='./collected_results')
        
        self.assertTrue(cspec.scores_x_axis==['number', 'animal'])
        self.assertTrue(cspec.scores_y_axis==['letter'])

        #script_dir
        self.assertTrue(cspec.script_dir=='./myRuns/baz/scripts')
        
        #trials:
        self.assertTrue(cspec.trials=='2')
    
        #master_job_name:
        self.assertTrue(cspec.cspec_name=='baz')
            
        #one_up_basis:
        self.assertTrue(cspec.one_up_basis == '100')
        
        #root_dir:
        self.assertTrue(cspec.root_dir == './myRuns')


        # permuters:
        self.assertTrue(cspec.permuters['number'][0] == '1')
        self.assertTrue(cspec.permuters['number'][1] == '2')
        self.assertTrue(cspec.permuters['number'][2] == '3')
        self.assertTrue(cspec.permuters['letter'][0] == 'AAA')
        self.assertTrue(cspec.permuters['letter'][1] == 'BBB')
        
        # generate_results_dir_for_permutation:
        self.assertTrue(cspec.generate_results_dir_for_permutation('xyz_trial3') == './myRuns/baz/results/xyz_trial3')
        
        #concise_print_map:
        self.assertTrue(cspec.concise_print_map['letter'] == 'l')
        self.assertTrue(cspec.concise_print_map['singleton_val'] == 's')

        #key_val_map:
        kvm = cspec.key_val_map
        self.assertTrue(kvm['config[AAA]']=='aaa')
        self.assertTrue(kvm['config[BBB]']=='bbb')
        self.assertTrue(kvm['pretty[1]']=='one')
        self.assertTrue(kvm['pretty[2]']=='two')
        self.assertTrue(kvm['pretty[3]']=='three')
        self.assertTrue(kvm['cspec_name']=='baz')
        self.assertTrue(kvm['root']=='/nfs/foo/bar')
        self.assertTrue(kvm['x_dir']=='/nfs/foo/bar/(letter)/<config[(letter)]>/(number)')
        self.assertTrue(kvm['algs_dir']=='/nfs/algs')
        self.assertTrue(kvm['tools_dir']=='/nfs/algs/tools')
        self.assertTrue(kvm['outfile_root']=='<pretty[(number)]>__TEST')
            
        #commands:
        commands_as_string = "{0}".format(cspec.commands)
        self.assertTrue(commands_as_string == "['echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt']")
           
        #qsub_commands:
        qsub_commands_as_string = "{0}".format(cspec.qsub_commands)
        self.assertTrue(qsub_commands_as_string == "['-q eecs,eecs1,eecs,share', '-M someone@gmail.com', '-m beas']")
        
        
    def test_permute_stepwise_range(self):
        lines = []
        lines.append("(permute):number=range(1,10,2)\n") # by 2
        permuters = cluster_spec.load_permuters(lines, 'permute:', '(permute):')
        self.assertTrue(permuters['number'] == ['1','3','5','7','9'])
        
        lines = []
        lines.append("(permute):number=range(1,10,3)\n") # by 3
        permuters = cluster_spec.load_permuters(lines, 'permute:', '(permute):')
        self.assertTrue(permuters['number'] == ['1','4','7'])
        
        lines = []
        lines.append("(permute):number=range(1, 10,2)\n") # with spaces
        permuters = cluster_spec.load_permuters(lines, 'permute:', '(permute):')
        self.assertTrue(permuters['number'] == ['1','3','5','7','9'])
        
        
        lines = []
        lines.append("(permute):number=range(1,6)\n") # traditional start and end range
        permuters = cluster_spec.load_permuters(lines, 'permute:', '(permute):')
        self.assertTrue(permuters['number'] == ['1','2','3','4','5'])
       
    def test_load_cspec_with_white_spaces(self):
        lines = []
        lines.append("#cspec \n")
        lines.append("trials:\t2\n")
        lines.append("tag=_myTag \n")
        lines.append("(permute):number=range(1   , 4)\n") # new form
        lines.append("permute:letter=AAA, BBB\n")
        lines.append("permute:singleton_val=\t300\n")
        lines.append("permute:animal= dog,cat\n")
        lines.append("concise_print:animal,an \n")
        lines.append("encode: letter,l \n") # alternate form
        lines.append("concise_print:singleton_val,   s   \n")
        lines.append("concise_print:resolution,\tres\t\n")
        lines.append("concise_print:AAA ,aa\n")
        lines.append("concise_print:BBB, bb\n")

        lines.append("scores_permute:resolution=userDay,userMonth\n")
        lines.append("scores_from:file= <permutation_results_dir>/(resolution).csv, column_name=auc,row_number=1\n")
        lines.append("scores_to: ./collected_results\n")
        lines.append("scores_y_axis: letter \n")
        lines.append("scores_x_axis:number,\t\t\tanimal\n")
        
        lines.append("<replace>:config[AAA]=aaa \n")
        lines.append("<replace>:config[BBB]= bbb\n")

        lines.append("<replace>:pretty[1]= one\n")
        lines.append("<replace>:pretty[2]= two\n")
        lines.append("<replace>:pretty[3]=three \n")

        lines.append("<replace>:root= /nfs/foo/bar\n")
        lines.append("<replace>:x_dir=<root>/(letter)/<config[(letter)]>/(number)\n ")
        lines.append("<replace>:algs_dir=/nfs/ algs\n")
        lines.append("<replace>:tools_dir=<algs_di r>/tools\n")
        lines.append("<replace>:    outfile_root =     <pretty[(number)]>__TEST\n")

        lines.append("root_dir:./myRuns\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:100 \n")

        lines.append("command:echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt\n")
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines,stdout)
        #print self.cspec.concise_print_map
        # concise_name
        self.assertTrue(cspec.get_concise_name('number') == 'number')
        self.assertTrue(cspec.get_concise_name('letter') == 'l')
        self.assertTrue(cspec.get_concise_name('singleton_val') == 's')
        self.assertTrue(cspec.get_concise_name('resolution') == 'res')
        
        #scores_info
        self.assertTrue(cspec.scores_permuters['resolution'][0] == 'userDay')
        self.assertTrue(cspec.scores_permuters['resolution'][1] == 'userMonth')
        
        self.assertTrue(cspec.scores_from_filepath=='<permutation_results_dir>/(resolution).csv')
        self.assertTrue(cspec.scores_from_colname=='auc')
        self.assertTrue(cspec.scores_from_rownum=='1')
        #print 'self.cspec.scores_to : {0}'.format(self.cspec.scores_to)
        self.assertTrue(cspec.scores_to=='./collected_results')
        
        self.assertTrue(cspec.scores_x_axis==['number', 'animal'])
        self.assertTrue(cspec.scores_y_axis==['letter'])

        #script_dir
        self.assertTrue(cspec.script_dir=='./myRuns/baz/scripts')
        
        #trials:
        self.assertTrue(cspec.trials=='2')
    
        #cspec_name:
        self.assertTrue(cspec.cspec_name=='baz')
            
        #one_up_basis:
        self.assertTrue(cspec.one_up_basis == '100')
        
        #root_dir:
        self.assertTrue(cspec.root_dir == './myRuns')


        # permuters:
        self.assertTrue(cspec.permuters['number'][0] == '1')
        self.assertTrue(cspec.permuters['number'][1] == '2')
        self.assertTrue(cspec.permuters['number'][2] == '3')
        self.assertTrue(cspec.permuters['letter'][0] == 'AAA')
        self.assertTrue(cspec.permuters['letter'][1] == 'BBB')
        
        # generate_results_dir_for_permutation:
        self.assertTrue(cspec.generate_results_dir_for_permutation('xyz_trial_3') == './myRuns/baz/results/xyz_trial_3')
        
        #concise_print_map:
        self.assertTrue(cspec.concise_print_map['letter'] == 'l')
        self.assertTrue(cspec.concise_print_map['singleton_val'] == 's')

        #key_val_map:
        kvm = cspec.key_val_map
        self.assertTrue(kvm['config[AAA]']=='aaa')
        self.assertTrue(kvm['config[BBB]']=='bbb')
        self.assertTrue(kvm['pretty[1]']=='one')
        self.assertTrue(kvm['pretty[2]']=='two')
        self.assertTrue(kvm['pretty[3]']=='three')
        self.assertTrue(kvm['cspec_name']=='baz')
        self.assertTrue(kvm['root']=='/nfs/foo/bar')
        self.assertTrue(kvm['x_dir']=='/nfs/foo/bar/(letter)/<config[(letter)]>/(number)')
        self.assertTrue(kvm['algs_dir']=='/nfs/algs')
        self.assertTrue(kvm['tools_dir']=='/nfs/algs/tools')
        self.assertTrue(kvm['outfile_root']=='<pretty[(number)]>__TEST')
            
        #commands:
        commands_as_string = "{0}".format(cspec.commands)
        self.assertTrue(commands_as_string == "['echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt']")
           
        #qsub_commands:
        qsub_commands_as_string = "{0}".format(cspec.qsub_commands)
        self.assertTrue(qsub_commands_as_string == "['-q eecs,eecs1,eecs,share', '-M someone@gmail.com', '-m beas']")

    def test_validate_statement_present_in_lines(self):
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append("root_dir\n")
        self.assertFalse(cluster_spec.validate_statement_present(lines,"root_dir:","some_dir", stdout))
        lines.append("root_dir:\n")
        self.assertFalse(cluster_spec.validate_statement_present(lines,"root_dir:","some_dir", stdout))
        lines.append("root_dir:/foo/bar\n")
        self.assertTrue(cluster_spec.validate_statement_present(lines,"root_dir:","some_dir", stdout))
        # with spaces
        lines = []
        lines.append("root_dir: /foo/bar \n")
        self.assertTrue(cluster_spec.validate_statement_present(lines,"root_dir:","some_dir", stdout))
        
                
    def test_validate_permutes(self):
        lines = []
        lines.append("permute:number=1:3") # wrong colon count
        self.assertFalse(cluster_spec.validate_permute_entries(lines))
        
        lines = []
        lines.append("permute:number=range(a,3)") # first integer bad in range
        self.assertFalse(cluster_spec.validate_permute_entries(lines))
        
        lines = []
        lines.append("permute:number=range(1,a)") # second integer bad in range
        self.assertFalse(cluster_spec.validate_permute_entries(lines))
        
        lines = []
        lines.append("permute:number=range(3,2)") # integer range out of order
        self.assertFalse(cluster_spec.validate_permute_entries(lines))
        
        lines = []
        lines.append("permute:number=range(1,10)") # integer range
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        lines = []
        lines.append("permute:number= range(1,10)") # integer range with spaces
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        lines = []
        lines.append("permute:number=range(1,10) ") # integer range
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        
        
        lines = []
        lines.append("(permute):number=range(1,1,2)\n") # single result
        self.assertFalse(cluster_spec.validate_permute_entries(lines))
        
        
        lines = []
        lines.append("permute:foo=2") # singleton integer 
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        lines = []
        lines.append("permute:foo= 2") # singleton integer with spaces
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        lines = []
        lines.append("permute:foo=2\t") # singleton integer 
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        
        lines = []
        lines.append("permute:foo=a,33,zxc") # comma list 
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        lines = []
        lines.append("permute:foo=\t\t\ta , 33 , zxc     ") # comma list with spaces
        self.assertTrue(cluster_spec.validate_permute_entries(lines))
        
        
        
    def test_validate_replaces(self):
        lines = []
        lines.append("<replace>:=/nfs/foo/bar") # key missing
        self.assertFalse(cluster_spec.validate_replace_entries(lines))
        
        lines = []
        lines.append("<replace>:foo=") # val missing
        self.assertFalse(cluster_spec.validate_replace_entries(lines))
        
        lines = []
        lines.append("<replace>:root:/nfs/foo/bar") # colon count wrong
        self.assertFalse(cluster_spec.validate_replace_entries(lines))
        
        lines = []
        lines.append("<replace>:root=/nfs/foo/bar") # correct
        self.assertTrue(cluster_spec.validate_replace_entries(lines))
        lines = []
        lines.append("<replace>:root= /nfs/foo/bar") # correct with spaces
        self.assertTrue(cluster_spec.validate_replace_entries(lines))
        lines = []
        lines.append("<replace>:root=/nfs/foo/bar ") # correct with spaces
        self.assertTrue(cluster_spec.validate_replace_entries(lines))
        
  
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
        
        # with spaces
        lines.append('permute:fop= 1 , 2 \n')
        lines.append('scores_permute:bag=a\t,b\n')
        self.assertTrue(cluster_spec.is_valid_permuter('fop', lines))
        self.assertTrue(cluster_spec.is_valid_permuter('bag', lines))
        
        
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
        
        # entry has one good permuter (with spaces)
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis: foo \n')
        self.assertTrue(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has two good permuters
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:foo,bar\n')
        self.assertTrue(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
        # entry has two good permuters (with spaces)
        lines = []
        lines.append('permute:foo=1,2\n')
        lines.append('permute:bar=a,b\n')
        lines.append('scores_x_axis:\tfoo ,bar \n')
        self.assertTrue(cluster_spec.validate_axis_list(lines,'scores_x_axis'))
        
    def test_validate_scores_to(self):
        lines = []
        lines.append('scores_to:./junk\n')
        lines.append('scores_to:./junk2\n')
        self.assertFalse(cluster_spec.validate_scores_to(lines))
        lines = []
        lines.append('scores_to:./junk\n')
        self.assertTrue(cluster_spec.validate_scores_to(lines))
        
        lines = []
        lines.append('scores_to: ./junk\n')  #with spaces
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
        
        #good one with spaces
        lines = []
        lines.append('scores_from:file= <permutation_results_dir>/(resolution).csv, column_name = auc , row_number = 1')
        self.assertTrue(cluster_spec.validate_scores_from(lines))
        
        
    def test_single_entry_present(self):
        lines = []
        lines.append('prefixA:foo\n')
        lines.append('prefixB:foo\n')
        lines.append('prefixB:foo\n')
        self.assertTrue(cluster_spec.single_entry_present(lines,'prefixA'))
        self.assertFalse(cluster_spec.single_entry_present(lines,'prefixB'))
        self.assertFalse(cluster_spec.single_entry_present(lines,'prefixC'))


    def test_validate_scores_gathering_info(self):
        stdout = mock_stdout.MockStdout()
        # none present is ok
        lines = []
        lines.append("foo\n")
        self.assertTrue(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
        #if any present, then 4 need to be present
        
        #missing from
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('scores_to:./collected_results')
        lines.append('scores_y_axis:letter')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
        #missing to
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_y_axis:letter')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
        #missing x axis
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results')
        lines.append('scores_y_axis:letter')
        self.assertFalse(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
        #missing y axis
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results')
        lines.append('scores_x_axis:number,animal')
        self.assertFalse(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
        
        #all present
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('(permute):number=range(1,3)\n')
        lines.append('(permute):animal=cat,dog\n')
        lines.append('(permute):letter=a,b,c\n')
        lines.append('scores_from:file=<permutation_results_dir>/foo.csv,column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results')
        lines.append('scores_x_axis:number,animal')
        lines.append('scores_y_axis:letter')
        self.assertTrue(cluster_spec.validate_scores_gathering_info(lines, stdout))
        

        #all present with spaces
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append('(permute):number=range(1,3)\n')
        lines.append('(permute):animal=cat,dog\n')
        lines.append('(permute):letter=a,b,c\n')
        lines.append('scores_from:file= <permutation_results_dir>/foo.csv, column_name=auc,row_number=1')
        lines.append('scores_to:./collected_results ')
        lines.append('scores_x_axis:number, animal')
        lines.append('scores_y_axis: letter')
        self.assertTrue(cluster_spec.validate_scores_gathering_info(lines, stdout))
        
    def test_lines_contains_prefix(self):
        lines = []
        lines.append('lineA\n')
        lines.append('prefix3:lineB\n')
        lines.append('lineC\n')
        self.assertFalse(cluster_spec.lines_contains_prefix(lines,'prefix2'))
        self.assertTrue(cluster_spec.lines_contains_prefix(lines,'prefix3'))
    
    def test_generate_new_spec(self):
        cluster_spec.generate_new_spec("./xyz.cspec")
        f = open("./xyz.cspec", 'r')
        lines = f.readlines()
        f.close()
        self.assertTrue(lines[0] == "#cspec\n")
    
if __name__ == '__main__':
    unittest.main()
    
   