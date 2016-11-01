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
    
    # 'S----'
    
    # '-L---'
    
    # 'SL---'
    
    # '--B--'
    
    # 'S-B--'
    
    #'-LB--'
    
    # 'SLB--'
    
    # '---D-'
        
    # 'S--D-'
    
    # '-L-D-'
    
    # 'SL-D-'
    
    # '--BD-'
    
    # 'S-BD-'
    
    # '-LBD-'
    
    # 'SLBD-'
    
    # '----O'
    
    # 'S---O'
    
    # '-L--O'
    
    # 'SL--O'
    
    # '--B-O'
    
    # 'S-B-O'
    
    # '-LB-O'
    
    # 'SLB-O'
        
    # '---DO'
    
    # 'S--DO'
    
    # '-L-DO'
    
    # '--BDO'
        
    # 'S-BDO'
    def test_assess_run__S_BDO(self):
        pcode = 'l_A_n_1_trials_1'
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
        pcode = 'l_A_n_1_trials_1'
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
        pcode = 'l_A_n_1_trials_1'
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
        pcode = 'l_A_n_1_trials_1'
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

if __name__ == '__main__':
    unittest.main()
    
   