'''
Created on Oct 26, 2016

@author: Jed Irvine
'''
import unittest
from permute import cluster_spec
from permute import permutations
from permute import state_of_runs
from permute import cluster_runs_info
import mock_stdout
import mock_cluster

class TestStateOfRuns(unittest.TestCase):

    def setUp(self):
        self.lines = []
        self.lines.append("#cspec\n")
        self.lines.append("trials:1\n")
        self.lines.append("tag=_myTag\n")
        self.lines.append("(permute):number=1,2\n") # new form
        self.lines.append("permute:letter=A,B\n")
        self.lines.append("concise_print:number,n\n")
        self.lines.append("concise_print:letter,l\n")

        self.lines.append("scores_from:file=<permutation_results_dir>/out_(letter)_(number).csv,column_name=auc,row_number=1\n")
        self.lines.append("scores_to:./collected_results\n")
        self.lines.append("scores_y_axis:letter\n")
        self.lines.append("scores_x_axis:number\n")

        self.lines.append("root_dir:./myRuns\n")

        self.lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        self.lines.append("qsub_command:-M someone@gmail.com\n")
        self.lines.append("qsub_command:-m beas\n")
        self.lines.append("one_up_basis:0\n")

        self.lines.append("command:echo (letter) (number) > <permutation_results_dir>/(letter)_(number).txt\n")
        
    # '-----'
    def test_assess_run_______before_run(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-----')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tscripts missing: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == 'NA\tl_A_n_1_trial_1\tscript missing\n')
    # '-----'
    def test_assess_run_______after_cleanup(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-----')
            
    # 'S----'
    def test_assess_run__S____(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S----')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tscripts ready to run: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tscript ready\t-> launch\n')
        
    # '-L---'
    def test_assess_run___L___(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-L---')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke log present but no script_file)\t-> retry\n')
        
    # 'SL---'
    def test_assess_run__SL___(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SL---')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(files suggest system should be running, but not seen in qstat)\t-> retry\n')

        
    # '--B--'
    def test_assess_run____B__(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--B--')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(script file missing, evidence of prior invoke error)\t-> retry\n')

        
    # 'S-B--'
    def test_assess_run__S_B__(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-B--')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke log missing, though evidence of invoke error)\t-> retry\n')

        
    #'-LB--'
    def test_assess_run___LB__(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LB--')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(script missing, invoke log present)\t-> retry\n')

        
    # 'SLB--'
    def test_assess_run__SLB__(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLB--')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tinvoke error: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinvoke error\t(run error detected)\t-> look into error, then retry\n')

        
    # '---D-'
    def test_assess_run_____D_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '---D-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(done marker found, but no script or results found)\t-> retry\n')

            
    # 'S--D-'
    def test_assess_run__S__D_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S--D-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(done marker found, but no evidence of script being invoked - stale results?)\t-> retry\n')

        
    # '-L-D-'
    def test_assess_run___L_D_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-L-D-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(done marker found, but no script found and no results present)\t-> retry\n')

        
    # 'SL-D-'
    def test_assess_run__SL_D_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SL-D-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\toutput files missing: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tresults missing\t(done marker found, but no results)\t-> troubleshoot, then retry\n')

        
    # '--BD-'
    def test_assess_run____BD_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--BD-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke error detected, but done marker present)\t-> troubleshoot, then retry\n')


    # 'S-BD-'
    def test_assess_run__S_BD_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-BD-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke error detected, but done marker present)\t-> troubleshoot, then retry\n')


    # '-LBD-'
    def test_assess_run___LBD_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LBD-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke error detected, but done marker present)\t-> troubleshoot, then retry\n')



    # 'SLBD-'
    def test_assess_run__SLBD_(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLBD-')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(invoke error detected, but done marker present)\t-> retry\n')



    # '----O'
    def test_assess_run______O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '----O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output present but no script or done marker)\t-> retry if unexpected\n')

        
    # 'S---O'
    def test_assess_run__S___O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S---O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output present but no done marker)\t-> retry if unexpected\n')

        
    # '-L--O'
    def test_assess_run___L__O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-L--O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output present but no script or done marker)\t-> retry if unexpected\n')

      
    # 'SL--O'
    def test_assess_run__SL__O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SL--O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\truns near complete: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\trun near complete\n')

        
    # '--B-O'
    def test_assess_run____B_O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--B-O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists but no done marker or script)\t-> retry if unexpected\n')

        
    # 'S-B-O'
    def test_assess_run__S_B_O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-B-O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, done marker and invoke log missing)\t-> retry if unexpected\n')

        
    # '-LB-O'
    def test_assess_run___LB_O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LB-O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, done marker missing, script missing)\t-> retry if unexpected\n')

        
    # 'SLB-O'
    def test_assess_run__SLB_O(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLB-O')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\trun state inconsistent: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tinconsistent\t(output exists, done marker missing and evidence of invoke error)\t-> retry if unexpected\n')

           
    # '---DO'
    def test_assess_run_____DO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '---DO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, script and invoke log missing)\t-> retry if unexpected\n')
        print "=="

        
    # 'S--DO'
    def test_assess_run__S__DO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S--DO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, invoke log missing)\t-> retry if unexpected\n')

        
    # '-L-DO'
    def test_assess_run___L_DO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-L-DO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, script missing)\t-> retry if unexpected\n')

        
    # '--BDO'
    def test_assess_run____BDO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--BDO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(script and invoke log missing)\t-> retry if unexpected\n')

            
    # 'S-BDO'
    def test_assess_run__S_BDO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-BDO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(output exists, invoke error detected)\t-> retry if unexpected\n')

    
    # '-LBDO'
    def test_assess_run___LBDO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LBDO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(results present but script missing and evidence of invoke error)\t-> retry if unexpected\n')

    
    # 'SLBDO'
    def test_assess_run__SLBDO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_invoke_error(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLBDO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tpossible stale results: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tstale results?\t(results present but evidence of invoke error)\t-> retry if unexpected\n')


    
    # 'SL-DO'
    def test_assess_run__SL_DO(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SL-DO')
        
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == 'baz(4)\tcomplete: 1\n')
        self.assertTrue(stdout.lines[2] == 'state undefined: 3\n')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\trun complete\n')

       
    # 'SC'
    def test_assess_run__SC(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_corrupt_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SC-XX')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tpossible error\t(invoke log corrupt, launch may have failed)\t-> retry\n')

        
    # '-C'
    def test_assess_run___C(self):
        #pcode = 'l_A_n_1_trial_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, stdout)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_corrupt_invoke_log(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-C-XX')
        
        stdout.lines = []
        states.emit_run_state_full(stdout, pcode)
        #for line in stdout.lines:
        #    print line
        self.assertTrue(stdout.lines[0] == '1\tl_A_n_1_trial_1\tpossible error\t(invoke log corrupt, launch may have failed)\t-> retry\n')

if __name__ == '__main__':
    unittest.main()
    
   