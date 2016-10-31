import unittest, os
from permute import cluster_spec
from permute import cluster_script
from permute import permuter
from permute import permutation_driver
from permute import cluster_runs_info
import mock_cluster_system
import mock_stdout

class TestSystem(unittest.TestCase):
    def setUp(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("tag=_myTag\n")
        lines.append("permute:number=range(1,4)\n")
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
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",cluster_system)
        permutation_driver.preview_scripts(cluster_runs)
        self.assertTrue(stdout.stdout[0] == "#!/bin/csh\n")
        self.assertTrue(stdout.stdout[1] == "#\n")
        self.assertTrue(stdout.stdout[2] == "#$ -q eecs,eecs1,eecs,share\n")
        self.assertTrue(stdout.stdout[3] == "#$ -M someone@gmail.com\n")
        self.assertTrue(stdout.stdout[4] == "#$ -m beas\n")
        self.assertTrue(stdout.stdout[5] == "#$ -N unittest-j100_1_an_cat_l_aa_number_1_s_300\n")
        self.assertTrue(stdout.stdout[6] == "#\n")
        self.assertTrue(stdout.stdout[7] == "# send stdout and stderror to this file\n")
        self.assertTrue(stdout.stdout[8] == "#$ -o j100_1_an_cat_l_aa_number_1_s_300.out\n")
        self.assertTrue(stdout.stdout[9] == "#$ -e j100_1_an_cat_l_aa_number_1_s_300.err\n")
        self.assertTrue(stdout.stdout[10] == "#\n")
        self.assertTrue(stdout.stdout[11] == "#see where the job is being run\n")
        self.assertTrue(stdout.stdout[12] == "hostname\n")
        self.assertTrue(stdout.stdout[13] == "echo AAA 1 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/AAA_1_one.txt\n")
        done_file = cluster_script.get_done_marker_filename()
        touch_string = "touch ./sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/{0}\n".format(done_file)
        self.assertTrue(stdout.stdout[14] == touch_string)

        
    def test_generate(self):
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, cluster_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",cluster_system)
        permutation_driver.generate_scripts(cluster_runs)
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j100_1_an_cat_l_aa_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j101_2_an_cat_l_aa_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j102_1_an_cat_l_aa_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j103_2_an_cat_l_aa_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j104_1_an_cat_l_aa_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j105_2_an_cat_l_aa_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j112_1_an_dog_l_aa_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j113_2_an_dog_l_aa_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j114_1_an_dog_l_aa_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j115_2_an_dog_l_aa_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j116_1_an_dog_l_aa_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j117_2_an_dog_l_aa_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j100_1_an_cat_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j101_2_an_cat_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j102_1_an_cat_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j103_2_an_cat_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j104_1_an_cat_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial1/an_cat_l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j105_2_an_cat_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial2/an_cat_l_aa_number_3_s_300/AAA_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j112_1_an_dog_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j113_2_an_dog_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j114_1_an_dog_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j115_2_an_dog_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j116_1_an_dog_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial1/an_dog_l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j117_2_an_dog_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./sample_results/unittest/trial2/an_dog_l_aa_number_3_s_300/AAA_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
    def is_echo_line_match(self, cluster_system, path, expected_content):
        print expected_content
        result = False
        f = cluster_system.open_file(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if (line.startswith('echo')):
                print line
                if (line == expected_content):
                    result = True
        f.close()
        return result
    
    def test_comma_in_arg(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("tag=_myTag\n")
        lines.append("permute:number=range(1,4)\n")
        lines.append("permute:letter=A_comma_A_comma_A,BBB\n") # changing AAA to A_comma_A_comma_A
        lines.append("permute:singleton_val=300\n")
        lines.append("permute:animal=dog,cat\n")
        lines.append("concise_print:animal,an\n")
        lines.append("concise_print:letter,l\n")
        lines.append("concise_print:singleton_val,s\n")
        lines.append("concise_print:resolution,res\n")
        lines.append("concise_print:AAA,aa\n")# can't accommodate this one due to comma substitution, i.e. A,A,A would throw parsing of this line
        lines.append("concise_print:BBB,bb\n")

        lines.append("scores_permute:resolution=userDay,userMonth\n")
        lines.append("scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1\n")
        lines.append("scores_to:./collected_results\n")
        lines.append("scores_y_axis:letter\n")
        lines.append("scores_x_axis:number,animal\n")
        
        lines.append("<replace>:config[A,A,A]=aaa\n")
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
        
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",cluster_system)
        permutation_driver.generate_scripts(cluster_runs)
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j100_1_an_cat_l_A-A-A_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j101_2_an_cat_l_A-A-A_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j102_1_an_cat_l_A-A-A_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j103_2_an_cat_l_A-A-A_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j104_1_an_cat_l_A-A-A_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j105_2_an_cat_l_A-A-A_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j112_1_an_dog_l_A-A-A_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j113_2_an_dog_l_A-A-A_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j114_1_an_dog_l_A-A-A_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j115_2_an_dog_l_A-A-A_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j116_1_an_dog_l_A-A-A_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j117_2_an_dog_l_A-A-A_number_3_s_300.sh'))
        
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh'))
        self.assertTrue(cluster_system.isfile('./scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j100_1_an_cat_l_A-A-A_number_1_s_300.sh','echo A,A,A 1 300 > ./sample_results/unittest/trial1/an_cat_l_A-A-A_number_1_s_300/A,A,A_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j101_2_an_cat_l_A-A-A_number_1_s_300.sh','echo A,A,A 1 300 > ./sample_results/unittest/trial2/an_cat_l_A-A-A_number_1_s_300/A,A,A_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j102_1_an_cat_l_A-A-A_number_2_s_300.sh','echo A,A,A 2 300 > ./sample_results/unittest/trial1/an_cat_l_A-A-A_number_2_s_300/A,A,A_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j103_2_an_cat_l_A-A-A_number_2_s_300.sh','echo A,A,A 2 300 > ./sample_results/unittest/trial2/an_cat_l_A-A-A_number_2_s_300/A,A,A_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j104_1_an_cat_l_A-A-A_number_3_s_300.sh','echo A,A,A 3 300 > ./sample_results/unittest/trial1/an_cat_l_A-A-A_number_3_s_300/A,A,A_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j105_2_an_cat_l_A-A-A_number_3_s_300.sh','echo A,A,A 3 300 > ./sample_results/unittest/trial2/an_cat_l_A-A-A_number_3_s_300/A,A,A_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j106_1_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j107_2_an_cat_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j108_1_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j109_2_an_cat_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j110_1_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j111_2_an_cat_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_cat_l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j112_1_an_dog_l_A-A-A_number_1_s_300.sh','echo A,A,A 1 300 > ./sample_results/unittest/trial1/an_dog_l_A-A-A_number_1_s_300/A,A,A_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j113_2_an_dog_l_A-A-A_number_1_s_300.sh','echo A,A,A 1 300 > ./sample_results/unittest/trial2/an_dog_l_A-A-A_number_1_s_300/A,A,A_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j114_1_an_dog_l_A-A-A_number_2_s_300.sh','echo A,A,A 2 300 > ./sample_results/unittest/trial1/an_dog_l_A-A-A_number_2_s_300/A,A,A_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j115_2_an_dog_l_A-A-A_number_2_s_300.sh','echo A,A,A 2 300 > ./sample_results/unittest/trial2/an_dog_l_A-A-A_number_2_s_300/A,A,A_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j116_1_an_dog_l_A-A-A_number_3_s_300.sh','echo A,A,A 3 300 > ./sample_results/unittest/trial1/an_dog_l_A-A-A_number_3_s_300/A,A,A_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j117_2_an_dog_l_A-A-A_number_3_s_300.sh','echo A,A,A 3 300 > ./sample_results/unittest/trial2/an_dog_l_A-A-A_number_3_s_300/A,A,A_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j118_1_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j119_2_an_dog_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j120_1_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j121_2_an_dog_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j122_1_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial1/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))
        self.assertTrue(self.is_echo_line_match(cluster_system, './scripts_unittest/j123_2_an_dog_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./sample_results/unittest/trial2/an_dog_l_bb_number_3_s_300/BBB_3_three.txt'))

    def test_clean_dir_except_for_scripts(self):   
        mcs = mock_cluster_system.MockClusterSystem()
        f = mcs.open_file("/foo/bar.txt",'w')
        f.close()
        f = mcs.open_file("/foo/bar.dat",'w')
        f.close()
        f = mcs.open_file("/foo/bar.sh",'w')
        f.close()
        permutation_driver.clean_dir_except_for_scripts("/foo", mcs)
        self.assertTrue(mcs.isfile("/foo/bar.sh"))
        self.assertFalse(mcs.isfile("/foo/bar.txt"))
        self.assertFalse(mcs.isfile("/foo/bar.dat"))
        
    def get_lines_for_simpleCaseCspec(self):
        lines = []
        lines.append('#cspec\n')
        lines.append('master_job_name:runtest\n')
        lines.append('trials:1\n')
        lines.append('permute:x=range(1,5)\n')
        lines.append('scores_from:file=<permutation_results_dir>/run_test.csv,column_name=auc,row_number=1\n')
        lines.append('scores_to:/nfs/stak/students/i/irvine/python/cluster/test/runtest_out/collected_results\n')
        lines.append('#\n')
        lines.append('# permutation-dependent mappings can be expressed like this.  These will be matched by \n')
        lines.append('# using permutations like this:  <config[(month)]>\n')
        lines.append('#\n')
        lines.append('#\n')
        lines.append('<replace>:root=/nfs/stak/students/i/irvine/python/cluster/test\n')
        lines.append('#\n')
        lines.append('#  results_dir is where the generated results will be\n')
        lines.append('#\n')
        lines.append('root_results_dir:<root>/runtest_out/results\n')
        lines.append('#\n')
        lines.append('#  script is where the generated scripts will be\n')
        lines.append('#\n')
        lines.append('script_dir:<root>/runtest_out/scripts\n')
        lines.append('#\n')
        lines.append('#qsub_command:-q eecs,eecs1,eecs,share\n')
        lines.append('qsub_command:-q eecs,share\n')
        lines.append('#qsub_command:-M someone@gmail.com\n')
        lines.append('#qsub_command:-m beas\n')
        lines.append('qsub_command:-cwd\n')
        lines.append('one_up_basis:0\n')
        lines.append('command:python <root>/run_test.py (x)  5 <permutation_results_dir>/run_test.csv\n')
        return lines
    
    def get_simple_case_answer_key(self):
        answers_trial1 = {}
        answers_trial1['x_1'] = '1.0'
        answers_trial1['x_2'] = '2.0'
        answers_trial1['x_3'] = '3.0'
        answers_trial1['x_4'] = '4.0'
        
        trials_list = [ answers_trial1]
        answerkey = {}
        answerkey[''] = trials_list
        return answerkey
                 
    def test_stat_before_gen(self):
        #self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 0'] = 'script missing'
        lines = self.get_lines_for_simpleCaseCspec()
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        stdout = mock_stdout.MockStdout()
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        self.assertTrue(stdout.stdout[0] == "NA trials_1_x_1  script missing\n")
        self.assertTrue(stdout.stdout[1] == "NA trials_1_x_2  script missing\n")
        self.assertTrue(stdout.stdout[2] == "NA trials_1_x_3  script missing\n")
        self.assertTrue(stdout.stdout[3] == "NA trials_1_x_4  script missing\n")
        self.assertTrue(len(stdout.stdout) == 4)
        
    def test_stat_after_gen(self):
        #self.state_codes['se 1 ile 0 rpb 0 dme 0 ofe 0'] = 'script ready'
        lines = self.get_lines_for_simpleCaseCspec()
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        permutation_driver.generate_scripts(cluster_runs)
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        
        stdout = mock_stdout.MockStdout()
        self.assertTrue(stdout.stdout[0] == "NA trials_1_x_1  script ready\n")
        self.assertTrue(stdout.stdout[1] == "NA trials_1_x_2  script ready\n")
        self.assertTrue(stdout.stdout[2] == "NA trials_1_x_3  script ready\n")
        self.assertTrue(stdout.stdout[3] == "NA trials_1_x_4  script ready\n")
        self.assertTrue(len(stdout.stdout) == 4)
 
         
    def test_stat_after_test_launch(self):
        #self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 1'] = 'run complete'
        lines = self.get_lines_for_simpleCaseCspec()
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_system.set_cluster_spec(cspec)
        answerkey = self.get_simple_case_answer_key()
        cluster_system.set_unittest_answers(answerkey)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        permutation_driver.generate_scripts(cluster_runs)
        permutation_driver.test_launch_single_script(cluster_runs, cluster_system)
        
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        
        stdout = mock_stdout.MockStdout()
        self.assertTrue(stdout.stdout[0] == "1 trials_1_x_1  run complete\n")
        self.assertTrue(stdout.stdout[1] == "NA trials_1_x_2  script ready\n")
        self.assertTrue(stdout.stdout[2] == "NA trials_1_x_3  script ready\n")
        self.assertTrue(stdout.stdout[3] == "NA trials_1_x_4  script ready\n")
        
        stdout.stdout = []
        permutation_driver.check_status_of_runs(cluster_runs, 'pending', cluster_system)
        self.assertTrue(stdout.stdout[0] == "NA trials_1_x_2  script ready\n")
        self.assertTrue(stdout.stdout[1] == "NA trials_1_x_3  script ready\n")
        self.assertTrue(stdout.stdout[2] == "NA trials_1_x_4  script ready\n")
      
        stdout.stdout = []
        permutation_driver.check_status_of_runs(cluster_runs, 'summary', cluster_system)
        self.assertTrue(stdout.stdout[0] == ".")
        self.assertTrue(stdout.stdout[1] == ".")
        self.assertTrue(stdout.stdout[2] == ".")
        self.assertTrue(stdout.stdout[3] == ".")
        self.assertTrue(stdout.stdout[4] == "\n")
        self.assertTrue(stdout.stdout[5] == "runtest(4)\tscripts ready to run: 3\tcomplete: 1\t\n")
    

    def test_stat_after_all_runs_finished(self):
        #self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 1'] = 'run complete'
        lines = self.get_lines_for_simpleCaseCspec()
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_system.set_cluster_spec(cspec)
        answerkey = self.get_simple_case_answer_key()
        cluster_system.set_unittest_answers(answerkey)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        permutation_driver.generate_scripts(cluster_runs)
        permutation_driver.launch_scripts(cluster_runs, cluster_system)
        
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        
        stdout = mock_stdout.MockStdout()
        self.assertTrue(stdout.stdout[0] == "1 trials_1_x_1  run complete\n")
        self.assertTrue(stdout.stdout[1] == "2 trials_1_x_2  run complete\n")
        self.assertTrue(stdout.stdout[2] == "3 trials_1_x_3  run complete\n")
        self.assertTrue(stdout.stdout[3] == "4 trials_1_x_4  run complete\n")
        
        stdout.stdout = []
        permutation_driver.check_status_of_runs(cluster_runs, 'pending', cluster_system)
        self.assertTrue(len(stdout.stdout) == 0)
      
        stdout.stdout = []
        permutation_driver.check_status_of_runs(cluster_runs, 'summary', cluster_system)
        self.assertTrue(stdout.stdout[0] == ".")
        self.assertTrue(stdout.stdout[1] == ".")
        self.assertTrue(stdout.stdout[2] == ".")
        self.assertTrue(stdout.stdout[3] == ".")
        self.assertTrue(stdout.stdout[4] == "\n")
        self.assertTrue(stdout.stdout[5] == "runtest(4)\tcomplete: 4\t\n")
        
        
    def test_retry(self):
        # first, complete all four runs
        #    i.e. self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 1'] = 'run complete'
        lines = self.get_lines_for_simpleCaseCspec()
        cluster_system = mock_cluster_system.MockClusterSystem()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, cluster_system)
        cluster_system.set_cluster_spec(cspec)
        answerkey = self.get_simple_case_answer_key()
        cluster_system.set_unittest_answers(answerkey)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        permutation_driver.generate_scripts(cluster_runs)
        permutation_driver.launch_scripts(cluster_runs, cluster_system)
        
        stdout = mock_stdout.MockStdout()
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        self.assertTrue(stdout.stdout[0] == "1 trials_1_x_1  run complete\n")
        self.assertTrue(stdout.stdout[1] == "2 trials_1_x_2  run complete\n")
        self.assertTrue(stdout.stdout[2] == "3 trials_1_x_3  run complete\n")
        self.assertTrue(stdout.stdout[3] == "4 trials_1_x_4  run complete\n")
        
        stdout.stdout = []
        # now, convince state_of_runs that two of the runs have no output file
        source_file_map = cluster_runs_info.create_source_file_map(cspec)
        result_path1= source_file_map["trials_1_x_1"]
        result_path3= source_file_map["trials_1_x_3"]
        cluster_system.delete_file("deleting output for perm_code1",result_path1)
        cluster_system.delete_file("deleting output for perm_code3",result_path3)
        donefile_path1 = cluster_runs.get_donefile_path_for_run_permutation_code("trials_1_x_1")
        donefile_path3 = cluster_runs.get_donefile_path_for_run_permutation_code("trials_1_x_3")
        cluster_system.delete_file("deleting done_file for perm_code1",donefile_path1)
        cluster_system.delete_file("deleting done_file for perm_code3",donefile_path3)
        
        permutation_driver.stop_runs(cluster_runs, cluster_system)
        stdout = mock_stdout.MockStdout()
        self.assertTrue(stdout.stdout[0] == "qdel 1\n")
        self.assertTrue(stdout.stdout[1] == "2 detected as finished (j1...)\n")
        self.assertTrue(stdout.stdout[2] == "qdel 3\n")
        self.assertTrue(stdout.stdout[3] == "4 detected as finished (j3...)\n")
        stdout.stdout = []
        permutation_driver.launch_incomplete_runs(cluster_runs, cluster_system)
        
        
        stdout.stdout = []
        permutation_driver.check_status_of_runs(cluster_runs, 'full', cluster_system)
        self.assertTrue(stdout.stdout[0] == "5 trials_1_x_1  run complete\n")
        self.assertTrue(stdout.stdout[1] == "2 trials_1_x_2  run complete\n")
        self.assertTrue(stdout.stdout[2] == "6 trials_1_x_3  run complete\n")
        self.assertTrue(stdout.stdout[3] == "4 trials_1_x_4  run complete\n")
        
'''       
    def test_stat_after_(self):
        self.assertTrue(False)

    def test_stat_after_(self):
        self.assertTrue(False)        
        self.state_codes['se 0 ile 1 rpb 0 dme 0 ofe 0'] = 'run_state_error - launch_log but no script_file : clean logs'
        
    def test_stat_after_launch_one_still_running(self):
        self.assertTrue(False)
        #self.state_codes['se 1 ile 1 rpb 0 dme 0 ofe 0'] = 'running'
        
        
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 1 dme 0 ofe 0'] = 'run_state_error - permission_block_error without script_file : clean logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 1 dme 0 ofe 0'] = 'run_state_error - permission_block_error without launch_log : clean logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 1 dme 0 ofe 0'] = 'run_state_error - launch_log present without script_file : clean logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 1 dme 0 ofe 0'] = 'run permission issue'
 
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without script_file : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without launch_log : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without script_file but launch_log present : clean results, logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 0'] = 'run error'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
 
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without script_file : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without launch_log : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without script_file, but has launch_log : clean results, logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 0 dme 0 ofe 1'] = 'run near complete'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
 
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without script_file : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without launch_log : clean results'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without script_file, but launch_log present : clean results, logs'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 0 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 0 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 0 ile 1 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
    def test_stat_after_(self):
        self.assertTrue(False)   
        self.state_codes['se 1 ile 1 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
'''                     


if __name__ == '__main__':
    unittest.main()
    
   