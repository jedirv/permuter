import unittest, os
from permute import cluster_spec
from permute import permuter
from permute import permutation_driver
from permute import cluster_runs_info
import mock_cluster_system

class TestSystem(unittest.TestCase):
    def setUp(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("tag=_myTag\n")
        lines.append("permute:number=1 3\n")
        lines.append("permute:letter=AAA,BBB\n")
        lines.append("permute:singleton_val=300\n")
        lines.append("permute:animal=dog,cat\n")
        lines.append("concise_print:animal,an\n")
        lines.append("concise_print:letter,l\n")
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

        lines.append("root_results_dir:./sample_results\n")
        lines.append("script_dir:./scripts_<master_job_name>\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:100\n")

        lines.append("command:echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt\n")
        self.lines = lines
        
    def test_preview(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, mc_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",mc_system)
        permutation_driver.preview_scripts(cluster_runs, mc_system)
        
    def test_generate(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, mc_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",mc_system)
        permutation_driver.generate_scripts(cluster_runs, mc_system)
        
        self.assertTrue(mc_system.isfile('./scripts_unittest/j100_1_an_cat_l_aa_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j101_2_an_cat_l_aa_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j102_1_an_cat_l_aa_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j103_2_an_cat_l_aa_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j104_1_an_cat_l_aa_number_3_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j105_2_an_cat_l_aa_number_3_s_300.sh'))
        
        self.assertTrue(mc_system.isfile('./scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(mc_system.isfile('./scripts_unittest/j112_1_an_dog_l_aa_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j113_2_an_dog_l_aa_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j114_1_an_dog_l_aa_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j115_2_an_dog_l_aa_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j116_1_an_dog_l_aa_number_3_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j117_2_an_dog_l_aa_number_3_s_300.sh'))
        
        self.assertTrue(mc_system.isfile('./scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh'))
        self.assertTrue(mc_system.isfile('./scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j100_1_an_cat_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j101_2_an_cat_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j102_1_an_cat_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j103_2_an_cat_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j104_1_an_cat_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j105_2_an_cat_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_3_s_300/AAA_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j112_1_an_dog_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j113_2_an_dog_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j114_1_an_dog_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j115_2_an_dog_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j116_1_an_dog_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j117_2_an_dog_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_3_s_300/AAA_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(mc_system, './scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
    def is_echo_line_match(self, mc_system, path, expected_content):
        print expected_content
        result = False
        f = mc_system.open_file(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if (line.startswith('echo')):
                print line
                if (line == expected_content):
                    result = True
        f.close()
        return result
    
if __name__ == '__main__':
    unittest.main()
    
   