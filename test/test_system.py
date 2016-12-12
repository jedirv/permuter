import unittest, os
from permute import cluster_spec
from permute import cluster_script
from permute import permutation_driver
from permute import cluster_runs_info
import mock_stdout
import mock_cluster
from __builtin__ import True

class TestSystem(unittest.TestCase):
    def setUp(self):
        lines = []
        lines.append("#cspec\n")
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

        #lines.append("<replace>:root=.\n")
        #lines.append("<replace>:root=/nfs/foo/bar\n")
        #lines.append("<replace>:x_dir=<root>/(letter)/<config[(letter)]>/(number)\n")
        #lines.append("<replace>:algs_dir=/nfs/algs\n")
        #lines.append("<replace>:tools_dir=<algs_dir>/tools\n")
        #lines.append("<replace>:outfile_root=<pretty[(number)]>__TEST\n")

        lines.append("root_dir:./myRuns\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:100\n")

        lines.append("command:echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt\n")
        self.lines = lines
        
    def test_preview(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        perm_driver = permutation_driver.PermutationDriver(self.lines, "/foo/bar/baz.cspec", stdout, cluster)
        perm_driver.preview_scripts(cluster_runs)
        self.assertTrue(stdout.lines[0] == "generating script file: ./myRuns/baz/scripts/j100_an_cat_l_aa_number_1_s_300_trial_1.sh\n")
        self.assertTrue(stdout.lines[1] == "#!/bin/csh\n")
        self.assertTrue(stdout.lines[2] == "#\n")
        self.assertTrue(stdout.lines[3] == "#$ -q eecs,eecs1,eecs,share\n")
        self.assertTrue(stdout.lines[4] == "#$ -M someone@gmail.com\n")
        self.assertTrue(stdout.lines[5] == "#$ -m beas\n")
        self.assertTrue(stdout.lines[6] == "#$ -N baz-j100_an_cat_l_aa_number_1_s_300_trial_1\n")
        self.assertTrue(stdout.lines[7] == "#\n")
        self.assertTrue(stdout.lines[8] == "# send stdout and stderror to this file\n")
        self.assertTrue(stdout.lines[9] == "#$ -o j100_an_cat_l_aa_number_1_s_300_trial_1.out\n")
        self.assertTrue(stdout.lines[10] == "#$ -e j100_an_cat_l_aa_number_1_s_300_trial_1.err\n")
        self.assertTrue(stdout.lines[11] == "#\n")
        self.assertTrue(stdout.lines[12] == "#see where the job is being run\n")
        self.assertTrue(stdout.lines[13] == "hostname\n")
        self.assertTrue(stdout.lines[14] == "echo AAA 1 300 > ./myRuns/baz/results/an_cat_l_aa_number_1_s_300_trial_1/AAA_1_one.txt\n")
        done_file = cluster_script.get_done_marker_filename()
        touch_string = "touch ./myRuns/baz/results/an_cat_l_aa_number_1_s_300_trial_1/{0}\n".format(done_file)
        self.assertTrue(stdout.lines[15] == touch_string)

      
    def test_generate(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        perm_driver = permutation_driver.PermutationDriver(self.lines, "/foo/bar/baz.cspec",stdout, cluster)
        perm_driver.generate_scripts(cluster_runs, cluster)
        pcodes = cluster_runs.run_perm_codes_list
        self.assertTrue(cluster.is_script_present(pcodes[0]))
        self.assertTrue(cluster.is_script_present(pcodes[1]))
        self.assertTrue(cluster.is_script_present(pcodes[2]))
        self.assertTrue(cluster.is_script_present(pcodes[3]))
        self.assertTrue(cluster.is_script_present(pcodes[4]))
        self.assertTrue(cluster.is_script_present(pcodes[5]))
        
        self.assertTrue(cluster.is_script_present(pcodes[6]))
        self.assertTrue(cluster.is_script_present(pcodes[7]))
        self.assertTrue(cluster.is_script_present(pcodes[8]))
        self.assertTrue(cluster.is_script_present(pcodes[9]))
        self.assertTrue(cluster.is_script_present(pcodes[10]))
        self.assertTrue(cluster.is_script_present(pcodes[11]))
        
        self.assertTrue(cluster.is_script_present(pcodes[12]))
        self.assertTrue(cluster.is_script_present(pcodes[13]))
        self.assertTrue(cluster.is_script_present(pcodes[14]))
        self.assertTrue(cluster.is_script_present(pcodes[15]))
        self.assertTrue(cluster.is_script_present(pcodes[16]))
        self.assertTrue(cluster.is_script_present(pcodes[17]))
        
        self.assertTrue(cluster.is_script_present(pcodes[18]))
        self.assertTrue(cluster.is_script_present(pcodes[19]))
        self.assertTrue(cluster.is_script_present(pcodes[20]))
        self.assertTrue(cluster.is_script_present(pcodes[21]))
        self.assertTrue(cluster.is_script_present(pcodes[22]))
        self.assertTrue(cluster.is_script_present(pcodes[23]))


    def test_comma_in_arg(self):
        lines = []
        lines.append("#cspec\n")
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

        #lines.append("<replace>:root=/nfs/foo/bar\n")
        #lines.append("<replace>:x_dir=<root>/(letter)/<config[(letter)]>/(number)\n")
        #lines.append("<replace>:algs_dir=/nfs/algs\n")
        #lines.append("<replace>:tools_dir=<algs_dir>/tools\n")
        #lines.append("<replace>:outfile_root=<pretty[(number)]>__TEST\n")

        lines.append("root_dir:./myRuns\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:100\n")

        lines.append("command:echo (letter) (number) (singleton_val) > <permutation_results_dir>/(letter)_(number)_<pretty[(number)]>.txt\n")
        
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        perm_driver = permutation_driver.PermutationDriver(self.lines, "/foo/bar/baz.cspec",stdout, cluster)
        perm_driver.generate_scripts(cluster_runs, cluster)
        pcodes = cluster_runs.run_perm_codes_list
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_1_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_1_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_2_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_2_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_3_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_A-A-A_number_3_s_300_trial_2', pcodes))
        
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_1_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_1_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_2_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_2_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_3_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_cat_l_bb_number_3_s_300_trial_2', pcodes))
        
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_1_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_1_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_2_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_2_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_3_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_A-A-A_number_3_s_300_trial_2', pcodes))
        
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_1_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_1_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_2_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_2_s_300_trial_2', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_3_s_300_trial_1', pcodes))
        self.assertTrue(self.is_code_present('an_dog_l_bb_number_3_s_300_trial_2', pcodes))
    
    def is_code_present(self, code, code_list):
        for cur_code in code_list:
            if cur_code == code:
                return True
        return False
        
        
    def get_lines_for_simpleCaseCspec(self):
        lines = []
        lines.append('#cspec\n')
        lines.append('trials:1\n')
        lines.append('permute:x=range(1,5)\n')
        lines.append('scores_from:file=<permutation_results_dir>/run_test.csv,column_name=auc,row_number=1\n')
        lines.append('scores_to:/nfs/stak/students/i/irvine/python/cluster/test/runtest_out/collected_results\n')
        lines.append('#\n')
        lines.append('# permutation-dependent mappings can be expressed like this.  These will be matched by \n')
        lines.append('# using permutations like this:  <config[(month)]>\n')
        lines.append('#\n')
        lines.append('#\n')
        lines.append('<replace>:root=.\n')
        lines.append('#\n')
        lines.append('#  results_dir is where the generated results will be\n')
        lines.append('#\n')
        lines.append('root_dir:<root>/myRuns\n')
        lines.append('#\n')
        lines.append('#  script is where the generated scripts will be\n')
        lines.append('#\n')
        lines.append('#qsub_command:-q eecs,eecs1,eecs,share\n')
        lines.append('qsub_command:-q eecs,share\n')
        lines.append('#qsub_command:-M someone@gmail.com\n')
        lines.append('#qsub_command:-m beas\n')
        lines.append('qsub_command:-cwd\n')
        lines.append('one_up_basis:0\n')
        lines.append('command:python <root>/run_test.py (x)  5 <permutation_results_dir>/run_test.csv\n')
        return lines

    
    # count
    def test_count(self):
        #self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 0'] = 'script missing'
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
        pdriver.run_command('count','')
        self.assertTrue(stdout.lines[0] == "4 scripts in play\n")
        self.assertTrue(len(stdout.lines) == 1)
        
   
    def test_status_clean_slate(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
        
        
        # (clean slate) summary 
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts missing: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (clean slate) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (clean slate) pending 
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript missing\t-> gen\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (clean slate) errors 
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
        
    def test_status_generate(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
            
        # GENERATE
    
        stdout.lines = []
        pdriver.run_command('gen','')
        self.assertTrue(stdout.lines[0] == "generating script file: ./myRuns/baz/scripts/j0_x_1_trial_1.sh\n")
        self.assertTrue(stdout.lines[1] == "generating script file: ./myRuns/baz/scripts/j1_x_2_trial_1.sh\n")
        self.assertTrue(stdout.lines[2] == "generating script file: ./myRuns/baz/scripts/j2_x_3_trial_1.sh\n")
        self.assertTrue(stdout.lines[3] == "generating script file: ./myRuns/baz/scripts/j3_x_4_trial_1.sh\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after gen) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after gen) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after gen) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        # (after gen) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
    
    def test_status_test_launch(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        # TEST LAUNCH
    
        pdriver.run_command('gen','')
        stdout.lines = []
        pdriver.run_command('test_launch','')
        self.assertTrue(stdout.lines[0] == "launching run for x_1_trial_1\n")
        self.assertTrue(len(stdout.lines) == 1)
        # (after test_launch) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 3\n")
        self.assertTrue(stdout.lines[3] == "runs waiting in queue: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after test_launch) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after test_launch) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        # (after test_launch) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
        
    def test_status_launch_after_test_launch(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        
        # LAUNCH SHOULD IGNORE THE ONE THAT'S ALREADY WAITING AND LAUNCH THE OTHERS
        pdriver.run_command('gen','')
        pdriver.run_command('test_launch','') 
        
        stdout.lines = []
        pdriver.run_command('launch','')
        self.assertTrue(stdout.lines[0] == "launching run for x_2_trial_1\n")
        self.assertTrue(stdout.lines[1] == "launching run for x_3_trial_1\n")
        self.assertTrue(stdout.lines[2] == "launching run for x_4_trial_1\n")
        # (after launch) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "runs waiting in queue: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after launch) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after launch) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after launch) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
    
    def test_status_running(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage runs
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        # (after run engaged) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "running: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after run engaged) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trunning\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\trunning\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\trunning\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trunning\n")
        # (after run engaged) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trunning\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\trunning\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\trunning\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trunning\n")
        # (after run engaged) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
    
    def test_status_results_no_done_marker(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage runs
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        # CREATE RESULTS WITHOUT DONE MARKER
        cluster.test_helper_set_run_results_without_done_marker('x_1_trial_1')
        # (after results created) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "running: 3\n")
        self.assertTrue(stdout.lines[3] == "runs near complete: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after results created) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trun near complete\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\trunning\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\trunning\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trunning\n")
        # (after results created) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trun near complete\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\trunning\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\trunning\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trunning\n")
        # (after results created) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
        
    def test_status_problems1(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage runs
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        # CREATE RESULTS AND DONE MARKER
        cluster.test_helper_set_run_finished_complete('x_1_trial_1')
        cluster.test_helper_set_run_finished_complete('x_2_trial_1')
        cluster.test_helper_set_run_finished_complete('x_3_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
        
        # cause one run to be broken by missing results - "results_missing"
        cluster.delete_results('x_1_trial_1')
        # cause one run to have missing invoke_log    "stale_results?"
        cluster.delete_invoke_log('x_2_trial_1')
        # cause one run to have block error        "stale_results?"
        cluster.test_helper_set_invoke_error('x_3_trial_1')
        # cause one run to have missing script     "stale_results?"
        cluster.delete_script('x_4_trial_1')
    
        # (after these errors) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "output files missing: 1\n")
        self.assertTrue(stdout.lines[3] == "possible stale results: 3\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after these errors) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, invoke log missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(results present but evidence of invoke error)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        # (after these errors) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, invoke log missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(results present but evidence of invoke error)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        # (after these errors) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, invoke log missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(results present but evidence of invoke error)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")      
        
    def test_status_retry(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage runs
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        # CREATE RESULTS AND DONE MARKER (except for first run)
        
        cluster.test_helper_set_run_finished_complete('x_2_trial_1')
        cluster.test_helper_set_run_finished_complete('x_3_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
        
        # cause one run to have missing invoke_log    "stale_results?"
        cluster.delete_invoke_log('x_2_trial_1')
        # cause one run to have block error        "stale_results?"
        cluster.test_helper_set_invoke_error('x_3_trial_1')
        # cause one run to have missing script     "stale_results?"
        cluster.delete_script('x_4_trial_1')
    
        stdout.lines = []
        pdriver.run_command("retry",'')
        self.assertTrue(stdout.lines[0] == "x_1_trial_1 left running\n")
        self.assertTrue(stdout.lines[1] == "x_2_trial_1 stale results? - retrying\n")
        self.assertTrue(stdout.lines[2] == "launching run for x_2_trial_1\n")
        self.assertTrue(stdout.lines[3] == "x_3_trial_1 stale results? - retrying\n")
        self.assertTrue(stdout.lines[4] == "launching run for x_3_trial_1\n")
        self.assertTrue(stdout.lines[5] == "x_4_trial_1 stale results? - retrying\n")
        self.assertTrue(stdout.lines[6] == "generating script file: ./myRuns/baz/scripts/j3_x_4_trial_1.sh\n")
        self.assertTrue(stdout.lines[7] == "launching run for x_4_trial_1\n")
        # (after rery) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "running: 1\n")
        self.assertTrue(stdout.lines[3] == "runs waiting in queue: 3\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after retry) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trunning\n")
        self.assertTrue(stdout.lines[1] == "5\tx_2_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[2] == "6\tx_3_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[3] == "7\tx_4_trial_1\twaiting in queue\n")
        # (after retry) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trunning\n")
        self.assertTrue(stdout.lines[1] == "5\tx_2_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[2] == "6\tx_3_trial_1\twaiting in queue\n")
        self.assertTrue(stdout.lines[3] == "7\tx_4_trial_1\twaiting in queue\n")
        # (after retry) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)   
        
    def test_status_stop(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage one run
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        # finish one run
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
    
        stdout.lines = []
        pdriver.run_command("stop",'')
        self.assertTrue(stdout.lines[0] == "stopping 1 (j0)\n")
        self.assertTrue(stdout.lines[1] == "stopping 2 (j1)\n")
        self.assertTrue(stdout.lines[2] == "stopping 3 (j2)\n")
        self.assertTrue(stdout.lines[3] == "x_4_trial_1 not running or waiting in queue\n")
        # (after stop) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "complete: 1\n")
        self.assertTrue(stdout.lines[3] == "run state inconsistent: 3\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after stop) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trun complete\n")
        # (after stop) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after stop) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 3)   
        
    def test_status_clean(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # GET THEM RUNNING
        # engage one run
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        # finish one run
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
    
        stdout.lines = []
        pdriver.run_command("clean_runs",'')
        self.assertTrue(stdout.lines[0] == "stopping 1 (j0)\n")
        self.assertTrue(stdout.lines[1] == "stopping 2 (j1)\n")
        self.assertTrue(stdout.lines[2] == "stopping 3 (j2)\n")
        self.assertTrue(stdout.lines[3] == "x_4_trial_1 not running or waiting in queue\n")
        self.assertTrue(stdout.lines[4] == "deleting all files for x_1_trial_1\n")
        self.assertTrue(stdout.lines[5] == "deleting all files for x_2_trial_1\n")
        self.assertTrue(stdout.lines[6] == "deleting all files for x_3_trial_1\n")
        self.assertTrue(stdout.lines[7] == "deleting all files for x_4_trial_1\n")
        # (after clean) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after clean) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        # (after clean) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after clean) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)   
           
    
    def test_status_single_jobs(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        stdout.lines = []
        # try to launch with bad job number
        pdriver.run_command('launch_job','j33')
        self.assertTrue(stdout.lines[0] == "ERROR: job number j33 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # try to launch with valid job number
        stdout.lines = []
        pdriver.run_command('launch_job','j3')
        self.assertTrue(stdout.lines[0] == "launching run for x_4_trial_1\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # (after launch_job) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 3\n")
        self.assertTrue(stdout.lines[3] == "runs waiting in queue: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        
        # (after launch_job) stat_job with bad job number
        stdout.lines = []
        pdriver.run_command('stat_job','j33')
        self.assertTrue(stdout.lines[0] == "ERROR: job number j33 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # (after launch_job) stat_job 
        stdout.lines = []
        pdriver.run_command('stat_job','j3')
        self.assertTrue(stdout.lines[0] == "1\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # (after launch_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "1\tx_4_trial_1\twaiting in queue\n")
        # (after launch_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "1\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after launch_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)   
        
        # STOP THE JOB
        stdout.lines = []
        #stop job with bad job number
        pdriver.run_command('stop_job','j33')
        self.assertTrue(stdout.lines[0] == "ERROR: job number j33 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # try to stop with valid job number
        stdout.lines = []
        pdriver.run_command('stop_job','j3')
        self.assertTrue(stdout.lines[0] == "stopping 1 (j3)\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 3\n")
        self.assertTrue(stdout.lines[3] == "run state inconsistent: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after stop_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        # (after stop_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after stop_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 1)   
        #CLEAN THE JOB
           
        stdout.lines = []
        #clean job with bad job number
        pdriver.run_command('clean_job','j33')
        self.assertTrue(stdout.lines[0] == "ERROR: job number j33 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # try to clean the job with valid job number
        stdout.lines = []
        pdriver.run_command('clean_job','j3')
        self.assertTrue(stdout.lines[0] == "deleting all files for x_4_trial_1\n")
        self.assertTrue(len(stdout.lines) == 1)   

        # (after clean_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        # (after clean_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after clean_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)       

   
    def test_status_single_jobs_as_pcode(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        stdout.lines = []
        # try to launch with bad job number
        pdriver.run_command('launch_job','z_1_d_5')
        self.assertTrue(stdout.lines[0] == "ERROR: job z_1_d_5 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # try to launch with valid job number
        stdout.lines = []
        pdriver.run_command('launch_job','x_4_trial_1')
        self.assertTrue(stdout.lines[0] == "launching run for x_4_trial_1\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # (after launch_job) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 3\n")
        self.assertTrue(stdout.lines[3] == "runs waiting in queue: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        
        # (after launch_job) stat_job with bad job number
        stdout.lines = []
        pdriver.run_command('stat_job','z_1_d_5')
        self.assertTrue(stdout.lines[0] == "ERROR: job z_1_d_5 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        # (after launch_job) stat_job 
        stdout.lines = []
        pdriver.run_command('stat_job','x_4_trial_1')
        self.assertTrue(stdout.lines[0] == "1\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # (after launch_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "1\tx_4_trial_1\twaiting in queue\n")
        # (after launch_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "1\tx_4_trial_1\twaiting in queue\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after launch_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)   
        
        # STOP THE JOB
        stdout.lines = []
        #stop job with bad job number
        pdriver.run_command('stop_job','z_1_d_5')
        self.assertTrue(stdout.lines[0] == "ERROR: job z_1_d_5 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # try to stop with valid job number
        stdout.lines = []
        pdriver.run_command('stop_job','x_4_trial_1')
        self.assertTrue(stdout.lines[0] == "stopping 1 (j3)\n")
        self.assertTrue(len(stdout.lines) == 1)   
        
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "scripts ready to run: 3\n")
        self.assertTrue(stdout.lines[3] == "run state inconsistent: 1\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after stop_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        # (after stop_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after stop_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "NA\tx_4_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n")
        self.assertTrue(len(stdout.lines) == 1)   
        #CLEAN THE JOB
           
        stdout.lines = []
        #clean job with bad job number
        pdriver.run_command('clean_job','z_1_d_5')
        self.assertTrue(stdout.lines[0] == "ERROR: job z_1_d_5 not valid for this cspec\n")
        self.assertTrue(len(stdout.lines) == 1)   
        # try to clean the job with valid job number
        stdout.lines = []
        pdriver.run_command('clean_job','x_4_trial_1')
        self.assertTrue(stdout.lines[0] == "deleting all files for x_4_trial_1\n")
        self.assertTrue(len(stdout.lines) == 1)   

        # (after clean_job) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        # (after clean_job) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript ready\t-> launch\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (after clean_job) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)       

    def test_status_complete_runs(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # FINISH ALL
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        cluster.test_helper_set_run_finished_complete('x_1_trial_1')
        cluster.test_helper_set_run_finished_complete('x_2_trial_1')
        cluster.test_helper_set_run_finished_complete('x_3_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
    
        # (after complete) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "complete: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after complete) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\trun complete\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\trun complete\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\trun complete\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\trun complete\n")
        # (after complete) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(len(stdout.lines) == 0)
        # (after complete) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)   
           
    def test_status_clean_results(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # FINISH ALL
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        cluster.test_helper_set_run_finished_complete('x_1_trial_1')
        cluster.test_helper_set_run_finished_complete('x_2_trial_1')
        cluster.test_helper_set_run_finished_complete('x_3_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
        pdriver.run_command('clean_results','')
        # (after clean_results) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "output files missing: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after clean_results) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        # (after clean_results) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        # (after clean_results) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n")         
           
          
    def test_status_clean_scripts(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs, stdout)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
                
        pdriver.run_command('gen','')
        pdriver.run_command('launch','')
        # FINISH ALL
        cluster.test_helper_set_ok_to_run('x_1_trial_1')
        cluster.test_helper_set_ok_to_run('x_2_trial_1')
        cluster.test_helper_set_ok_to_run('x_3_trial_1')
        cluster.test_helper_set_ok_to_run('x_4_trial_1')
        cluster.test_helper_set_run_finished_complete('x_1_trial_1')
        cluster.test_helper_set_run_finished_complete('x_2_trial_1')
        cluster.test_helper_set_run_finished_complete('x_3_trial_1')
        cluster.test_helper_set_run_finished_complete('x_4_trial_1')
        pdriver.run_command('clean_scripts','')
        # (after clean_scripts) summary 
        stdout.lines = []
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz\t-\t4 runs total\n")
        self.assertTrue(stdout.lines[2] == "possible stale results: 4\n")
        self.assertTrue(len(stdout.lines) == 3)
        # (after clean_scripts) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        # (after clean_scripts) pending
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        # (after clean_scripts) errors
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(stdout.lines[0] == "1\tx_1_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[1] == "2\tx_2_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[2] == "3\tx_3_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
        self.assertTrue(stdout.lines[3] == "4\tx_4_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n")
         

if __name__ == '__main__':
    unittest.main()
    
   