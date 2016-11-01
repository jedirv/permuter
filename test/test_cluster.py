'''
Created on Oct 28, 2016

@author: Jed Irvine
'''

import unittest
import mock_cluster
import mock_stdout
from permute import cluster_runs_info
from permute import cluster_spec

class TestCluster(unittest.TestCase):
    def setUp(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:1\n")
        lines.append("tag=_myTag\n")
        lines.append("permute:number=range(1,3)\n")
        lines.append("permute:letter=AAA,BBB\n")
        lines.append("concise_print:animal,an\n")
        lines.append("concise_print:letter,l\n")
        lines.append("concise_print:resolution,res\n")
        lines.append("concise_print:AAA,a\n")
        lines.append("concise_print:BBB,b\n")
        lines.append("concise_print:number,n\n")

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

        lines.append("command:echo (letter) (number) > <permutation_results_dir>/(letter)_(number).txt\n")
        self.lines = lines
        
    def testCreateScript(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.scripts)
        cscript = cluster.create_script(pcode)
        self.assertTrue(cluster.scripts[pcode] == cscript)
        
    def testDeleteScript(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cscript = cluster.create_script(pcode)
        self.assertTrue(cluster.scripts[pcode] == cscript)
        cluster.delete_script(pcode)
        self.assertFalse(cluster.scripts)
    '''    
    def testGetScriptModTime(self):
        
    def testGetInvokeLogModTime(self):
        
    def testGetDoneMarkerModTime(self):
    '''
    def testDeleteInvokeLog(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        self.assertFalse(cluster.is_invoke_log_present(pcode))
        cluster.launch(pcode)
        self.assertTrue(cluster.is_invoke_log_present(pcode))
        cluster.delete_invoke_log(pcode)
        self.assertFalse(cluster.is_invoke_log_present(pcode))


    def testDeleteQacctLog(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_qacct_log_present(pcode))
        cluster.test_helper_set_qacct_info(pcode,'qacctInfo')
        self.assertTrue(cluster.is_qacct_log_present(pcode))
        cluster.delete_qacct_log(pcode)
        self.assertFalse(cluster.is_qacct_log_present(pcode))
         
    def testDeleteQstatLog(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_qstat_log_present())
        cluster.test_helper_set_qstat_info('qstatInfo')
        self.assertTrue(cluster.is_qstat_log_present())
        cluster.delete_qstat_log()
        self.assertFalse(cluster.is_qstat_log_present())
    
    def testDeleteResults(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        self.assertTrue(cluster.is_output_files_present(pcode))
        cluster.delete_results(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
    
        
    def testLaunch(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertTrue(cluster.running_state[pcode] == 'waiting')
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertTrue(cluster.running_state[pcode] == 'running')
 
    def testStopRunningRun(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.stop_run(pcode)
        self.assertTrue(not(cluster.running_state.has_key(pcode)))
        
    def testStopWaitingRun(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.stop_run(pcode)
        self.assertTrue(not(cluster.running_state.has_key(pcode)))
      
    def testIsScriptPresent(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_script_present(pcode))
        cluster.create_script(pcode)
        self.assertTrue(cluster.is_script_present(pcode))
    
    def testIsInvokeLogPresent(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        self.assertFalse(cluster.is_invoke_log_present(pcode))
        cluster.launch(pcode)
        self.assertTrue(cluster.is_invoke_log_present(pcode))
        cluster.test_helper_corrupt_invoke_log(pcode)
        self.assertTrue(cluster.is_invoke_log_present(pcode))

    def testIsInvokeLogCorrupt(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        self.assertFalse(cluster.is_invoke_log_corrupt(pcode))
        cluster.launch(pcode)
        self.assertFalse(cluster.is_invoke_log_corrupt(pcode))
        cluster.test_helper_corrupt_invoke_log(pcode)
        self.assertTrue(cluster.is_invoke_log_corrupt(pcode))

    
    def testIsRunning(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertFalse(cluster.is_running(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertTrue(cluster.is_running(pcode))
        cluster.stop_run(pcode)
        self.assertFalse(cluster.is_running(pcode))
        
    def testIsWaiting(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_waiting(pcode))
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertTrue(cluster.is_waiting(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertFalse(cluster.is_waiting(pcode))
        cluster.stop_run(pcode)
        self.assertFalse(cluster.is_waiting(pcode))
        
    
    def testIsPermissionBlocked(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_permission_blocked(pcode)
        self.assertTrue(cluster.is_permission_blocked(pcode))
        
    
    def testIsDoneMarkerPresentRunComplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.test_helper_set_run_finished_complete(pcode)
        self.assertTrue(cluster.is_done_marker_present(pcode))
        
    def testIsDoneMarkerPresentRunIncomplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertFalse(cluster.is_done_marker_present(pcode))
        cluster.test_helper_set_run_finished_incomplete(pcode)
        self.assertTrue(cluster.is_done_marker_present(pcode))

    def testIsOutputFilePresentRunComplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.test_helper_set_run_finished_complete(pcode)
        self.assertTrue(cluster.is_output_files_present(pcode))
        
    def testIsOutputFilePresentRunIncomplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.create_script(pcode)
        cluster.launch(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.test_helper_set_ok_to_run(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
        cluster.test_helper_set_run_finished_incomplete(pcode)
        self.assertFalse(cluster.is_output_files_present(pcode))
    
    def testGetModTimeOutputFileRunComplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_complete(pcode)
        self.assertTrue(cluster.get_output_file_mod_time(pcode) == 'outputFileModTimeX')
        
    
    def testGetModTimeOutputFileRunIncomplete(self):
        pcode = 'l_a_n_1_trials_1'
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script(pcode)
        cluster.launch(pcode)
        cluster.test_helper_set_ok_to_run(pcode)
        cluster.test_helper_set_run_finished_incomplete(pcode)
        self.assertTrue(cluster.get_output_file_mod_time(pcode) == 0)
    

if __name__ == '__main__':
    unittest.main()
    
   