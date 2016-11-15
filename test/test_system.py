import unittest, os
from permute import cluster_spec
from permute import cluster_script
from permute import permuter
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
        self.lines = lines
        
    def test_preview(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",cluster_system)
        permutation_driver.preview_scripts(cluster_runs)
        self.assertTrue(stdout.lines[0] == "#!/bin/csh\n")
        self.assertTrue(stdout.lines[1] == "#\n")
        self.assertTrue(stdout.lines[2] == "#$ -q eecs,eecs1,eecs,share\n")
        self.assertTrue(stdout.lines[3] == "#$ -M someone@gmail.com\n")
        self.assertTrue(stdout.lines[4] == "#$ -m beas\n")
        self.assertTrue(stdout.lines[5] == "#$ -N baz-j100_an_cat_l_aa_number_1_s_300_trial_1\n")
        self.assertTrue(stdout.lines[6] == "#\n")
        self.assertTrue(stdout.lines[7] == "# send stdout and stderror to this file\n")
        self.assertTrue(stdout.lines[8] == "#$ -o j100_an_cat_l_aa_number_1_s_300_trial_1.out\n")
        self.assertTrue(stdout.lines[9] == "#$ -e j100_an_cat_l_aa_number_1_s_300_trial_1.err\n")
        self.assertTrue(stdout.lines[10] == "#\n")
        self.assertTrue(stdout.lines[11] == "#see where the job is being run\n")
        self.assertTrue(stdout.lines[12] == "hostname\n")
        self.assertTrue(stdout.lines[13] == "echo AAA 1 300 > ./myRuns/baz/results/an_cat_l_aa_number_1_s_300_trial_1/AAA_1_one.txt\n")
        done_file = cluster_script.get_done_marker_filename()
        touch_string = "touch ./myRuns/baz/results/an_cat_l_aa_number_1_s_300_trial_1/{0}\n".format(done_file)
        self.assertTrue(stdout.lines[14] == touch_string)

      
    def test_generate(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        #permdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec",cluster_system)
        permutation_driver.generate_scripts(cluster_runs, cluster)
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
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        permutation_driver.generate_scripts(cluster_runs, cluster)
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
        lines.append('<replace>:root=/nfs/stak/students/i/irvine/python/cluster/test\n')
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
        cluster = mock_cluster.MockCluster(cluster_runs)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
        pdriver.run_command('count','')
        self.assertTrue(stdout.lines[0] == "4 scripts in play\n")
        self.assertTrue(len(stdout.lines) == 1)
        
   
    def test_status_commands(self):
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pdriver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
        
        # (clean slate) summary 
        pdriver.run_command('summary','')
        self.assertTrue(stdout.lines[0] == "....\n")
        self.assertTrue(stdout.lines[1] == "baz(4)\tscripts missing: 4\n")
        self.assertTrue(len(stdout.lines) == 2)
        # (clean slate) stat 
        stdout.lines = []
        pdriver.run_command('stat','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript missing\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (clean slate) pending 
        stdout.lines = []
        pdriver.run_command('pending','')
        self.assertTrue(stdout.lines[0] == "NA\tx_1_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[1] == "NA\tx_2_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[2] == "NA\tx_3_trial_1\tscript missing\n")
        self.assertTrue(stdout.lines[3] == "NA\tx_4_trial_1\tscript missing\n")
        self.assertTrue(len(stdout.lines) == 4)
        # (clean slate) errors 
        stdout.lines = []
        pdriver.run_command('errors','')
        self.assertTrue(len(stdout.lines) == 0)
    
        pdriver.run_command('gen','')
        # (after gen) summary 
        
        # (after gen) stat 
        # (after gen) pending
        # (after gen) errors
    
    # (after test_launch) summary 
    # (after test_launch) stat 
    # (after test_launch) pending
    # (after test_launch) errors
    
    # (after launch) summary 
    # (after launch) stat 
    # (after launch) pending
    # (after launch) errors
    
    
    # (after invoke_log_removed) summary 
    # (after invoke_log_removed) stat 
    # (after invoke_log_removed) pending
    # (after invoke_log_removed) errors
    
    # clean all but scripts, launch, engage runs
    # (after run engaged) summary 
    # (after run engaged) stat 
    # (after run engaged) pending
    # (after run engaged) errors
    
    # (after results created) summary 
    # (after results created) stat 
    # (after results created) pending
    # (after results created) errors
    
    # cause one run to be broken by missing results
    # cause one run to have missing done marker
    # cause one run to have block error
    # cause one run to have missing script
    # (after these errors) summary 
    # (after these errors) stat 
    # (after these errors) pending
    # (after these errors) errors
    
    # retry
    # (after retry) summary 
    # (after retry) stat 
    # (after retry) pending
    # (after retry) errors
    
    # clean all but scripts, launch, engage one run
    # stop
    # (after stop) summary 
    # (after stop) stat 
    # (after stop) pending
    # (after stop) errors
    
    # clean 
    # (after clean) summary 
    # (after clean) stat 
    # (after clean) pending
    # (after clean) errors
    
    # clean all but scripts, launch
    # clean
    # (after clean that should also stop) summary 
    # (after clean that should also stop) stat 
    # (after clean that should also stop) pending
    # (after clean that should also stop) errors

    # clean all but scripts
    # launch_job
    # (after launch job) stat_job 
    # (after launch job) pending
    # stop_job
    # (after stop job) stat_job
    # clean job
    # (after clean job) stat_job
    # (after stop job) errors
    
    # clean all but scripts, launch, engage, complete
    # (after this) summary 
    # (after this) stat 
    # (after this) pending
    # (after this) errors
    # clean_results
    # (after clean_results) summary 
    # (after clean_results) stat 
    # (after clean_results) pending
    # (after clean_results) errors
    # clean_scripts
    
    # (after clean_scripts) summary 
    # (after clean_scripts) stat 
    # (after clean_scripts) pending
    # (after clean_scripts) errors
    '''             
    def test_stat_before_gen(self):
        #self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 0'] = 'script missing'
        stdout = mock_stdout.MockStdout()
        lines = self.get_lines_for_simpleCaseCspec()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        permutation_driver = permutation_driver.PermutationDriver(lines, "/foo/bar/baz.cspec", stdout, cluster)
        permutation_driver.run_command()
        self.assertTrue(stdout.stdout[0] == "NA trials_1_x_1  script missing\n")
        self.assertTrue(stdout.stdout[1] == "NA trials_1_x_2  script missing\n")
        self.assertTrue(stdout.stdout[2] == "NA trials_1_x_3  script missing\n")
        self.assertTrue(stdout.stdout[3] == "NA trials_1_x_4  script missing\n")
        self.assertTrue(len(stdout.stdout) == 4)
     '''
      


if __name__ == '__main__':
    unittest.main()
    
   