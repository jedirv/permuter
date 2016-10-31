'''
Created on Oct 26, 2016

@author: Jed Irvine
'''
import unittest
from permute import cluster_spec
from permute import permutations
from permute import state_of_runs
from permute import cluster_runs_info
import mock_cluster_system

class TestStateOfRuns(unittest.TestCase):

    def get_cspec(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("tag=_myTag\n")
        lines.append("(permute):number=1,2\n") # new form
        lines.append("permute:letter=A,B\n")
        lines.append("concise_print:number,n\n")
        lines.append("concise_print:letter,l\n")

        lines.append("scores_from:file=<permutation_results_dir>/out_(letter)_(number).csv,column_name=auc,row_number=1\n")
        lines.append("scores_to:./collected_results\n")
        lines.append("scores_y_axis:letter\n")
        lines.append("scores_x_axis:number\n")

        lines.append("root_results_dir:./sample_results\n")
        lines.append("script_dir:./scripts_<master_job_name>\n")

        lines.append("qsub_command:-q eecs,eecs1,eecs,share\n")
        lines.append("qsub_command:-M someone@gmail.com\n")
        lines.append("qsub_command:-m beas\n")
        lines.append("one_up_basis:0\n")

        lines.append("command:echo (letter) (number) > <permutation_results_dir>/(letter)_(number).txt\n")
        
    def test_x(self):
        cluster_system = mock_cluster_system.MockClusterSystem()
        lines = self.get_cspec();
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        run_states = state_of_runs.StateOfRuns()
        run_states.assess(cluster_runs, cluster_system)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
    
   