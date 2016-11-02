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
        self.lines.append("master_job_name:unittest\n")
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

        self.lines.append("root_results_dir:./sample_results\n")
        self.lines.append("script_dir:./scripts_<master_job_name>\n")

        self.lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        self.lines.append("qsub_command:-M someone@gmail.com\n")
        self.lines.append("qsub_command:-m beas\n")
        self.lines.append("one_up_basis:0\n")

        self.lines.append("command:echo (letter) (number) > <permutation_results_dir>/(letter)_(number).txt\n")
        
    # '-----'
    def test_assess_run_______before_run(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-----')
        states.emit_state_summary(stdout, cluster_runs)
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == '\n')
        self.assertTrue(stdout.lines[2] == 'unittest(4)\tscripts missing: 1\n')
        self.assertTrue(stdout.lines[3] == 'state undefined: 3\n')
    
    # '-----'
    def test_assess_run_______after_cleanup(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        self.assertTrue(stdout.lines[1] == '\n')
        self.assertTrue(stdout.lines[2] == 'unittest(4)\tscripts ready to run: 1\n')
        self.assertTrue(stdout.lines[3] == 'state undefined: 3\n')
        
    # '-L---'
    def test_assess_run___L___(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        for line in stdout.lines:
            print line
        self.assertTrue(stdout.lines[0] == '....\n')
        self.assertTrue(stdout.lines[1] == '\n')
        self.assertTrue(stdout.lines[2] == 'unittest(4)\tscripts ready to run: 1\n')
        self.assertTrue(stdout.lines[3] == 'state undefined: 3\n')
        
    # 'SL---'
    def test_assess_run__SL___(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '--B--'
    def test_assess_run____B__(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--B--')
        
    # 'S-B--'
    def test_assess_run__S_B__(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-B--')
        
    #'-LB--'
    def test_assess_run___LB__(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LB--')
        
    # 'SLB--'
    def test_assess_run__SLB__(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_results(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLB--')
        
    # '---D-'
    def test_assess_run_____D_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
            
    # 'S--D-'
    def test_assess_run__S__D_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '-L-D-'
    def test_assess_run___L_D_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # 'SL-D-'
    def test_assess_run__SL_D_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '--BD-'
    def test_assess_run____BD_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--BD-')

    # 'S-BD-'
    def test_assess_run__S_BD_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-BD-')

    # '-LBD-'
    def test_assess_run___LBD_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LBD-')


    # 'SLBD-'
    def test_assess_run__SLBD_(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_results(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLBD-')


    # '----O'
    def test_assess_run______O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # 'S---O'
    def test_assess_run__S___O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '-L--O'
    def test_assess_run___L__O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # 'SL--O'
    def test_assess_run__SL__O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '--B-O'
    def test_assess_run____B_O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--B-O')
        
    # 'S-B-O'
    def test_assess_run__S_B_O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-B-O')
        
    # '-LB-O'
    def test_assess_run___LB_O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LB-O')
        
    # 'SLB-O'
    def test_assess_run__SLB_O(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_done_marker(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLB-O')
            
    # '---DO'
    def test_assess_run_____DO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # 'S--DO'
    def test_assess_run__S__DO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '-L-DO'
    def test_assess_run___L_DO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
        
    # '--BDO'
    def test_assess_run____BDO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '--BDO')
            
    # 'S-BDO'
    def test_assess_run__S_BDO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'S-BDO')
    
    # '-LBDO'
    def test_assess_run___LBDO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        cluster.delete_script(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == '-LBDO')
        
    # 'SLBDO'
    def test_assess_run__SLBDO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SLBDO')

    
    # 'SL-DO'
    def test_assess_run__SL_DO(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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

    # 'SC'
    def test_assess_run__SC(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        pcodes = cluster_runs.run_perm_codes_list
        pcode = pcodes[0]
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_corrupt_invoke_log(pcode)
        states = state_of_runs.StateOfRuns()
        states.assess_run(pcode, cluster_runs, cluster)
        self.assertTrue(states.run_states[pcode] == 'SC-XX')
        
    # '-C'
    def test_assess_run___C(self):
        #pcode = 'l_A_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
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
if __name__ == '__main__':
    unittest.main()
    
   