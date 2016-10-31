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
        
    def testCreateScript(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.scripts)
        cluster.create_script("foo", "scriptFoo")
        self.assertTrue(cluster.scripts["foo"] == "scriptFoo")
        
    def testDeleteScript(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        self.assertTrue(cluster.scripts["foo"] == "scriptFoo")
        cluster.delete_script("foo")
        self.assertFalse(cluster.scripts)
        
    
    def testDeleteInvokeLog(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script('foo', "scriptFoo")
        self.assertFalse(cluster.is_invoke_log_present('foo'))
        cluster.launch('foo')
        self.assertTrue(cluster.is_invoke_log_present('foo'))
        cluster.delete_invoke_log('foo')
        self.assertFalse(cluster.is_invoke_log_present('foo'))


    def testDeleteQacctLog(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_qacct_log_present('foo'))
        cluster.test_helper_set_qacct_info('foo','qacctInfo')
        self.assertTrue(cluster.is_qacct_log_present('foo'))
        cluster.delete_qacct_log('foo')
        self.assertFalse(cluster.is_qacct_log_present('foo'))
         
    def testDeleteQstatLog(self):
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
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.test_helper_set_ok_to_run("foo")
        cluster.test_helper_set_run_finished_complete('foo')
        self.assertTrue(cluster.is_output_files_present('foo'))
        cluster.delete_results('foo')
        self.assertFalse(cluster.is_output_files_present('foo'))
    
        
    def testLaunch(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertTrue(cluster.running_state["foo"] == 'waiting')
        cluster.test_helper_set_ok_to_run("foo")
        self.assertTrue(cluster.running_state["foo"] == 'running')
 
    def testStopRunningRun(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.test_helper_set_ok_to_run("foo")
        cluster.stop_run("foo")
        self.assertTrue(not(cluster.running_state.has_key("foo")))
        
    def testStopWaitingRun(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.stop_run("foo")
        self.assertTrue(not(cluster.running_state.has_key("foo")))
      
    def testIsScriptPresent(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_script_present('foo'))
        cluster.create_script("foo", "scriptFoo")
        self.assertTrue(cluster.is_script_present('foo'))
    
    def testIsInvokeLogPresent(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script('foo', "scriptFoo")
        self.assertFalse(cluster.is_invoke_log_present('foo'))
        cluster.launch('foo')
        self.assertTrue(cluster.is_invoke_log_present('foo'))
        cluster.test_helper_corrupt_invoke_log('foo')
        self.assertTrue(cluster.is_invoke_log_present('foo'))

    def testIsInvokeLogCorrupt(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        self.assertFalse(cluster.is_invoke_log_corrupt('foo'))
        cluster.launch("foo")
        self.assertFalse(cluster.is_invoke_log_corrupt('foo'))
        cluster.test_helper_corrupt_invoke_log('foo')
        self.assertTrue(cluster.is_invoke_log_corrupt('foo'))

    
    def testIsRunning(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertFalse(cluster.is_running('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertTrue(cluster.is_running('foo'))
        cluster.stop_run("foo")
        self.assertFalse(cluster.is_running('foo'))
        
    def testIsWaiting(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_waiting('foo'))
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertTrue(cluster.is_waiting('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertFalse(cluster.is_waiting('foo'))
        cluster.stop_run("foo")
        self.assertFalse(cluster.is_waiting('foo'))
        
    
    def testIsPermissionBlocked(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.test_helper_set_permission_blocked('foo')
        self.assertTrue(cluster.is_permission_blocked('foo'))
        
    
    def testIsDoneMarkerPresentRunComplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.test_helper_set_run_finished_complete('foo')
        self.assertTrue(cluster.is_done_marker_present('foo'))
        
    def testIsDoneMarkerPresentRunIncomplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertFalse(cluster.is_done_marker_present('foo'))
        cluster.test_helper_set_run_finished_incomplete('foo')
        self.assertTrue(cluster.is_done_marker_present('foo'))

    def testIsOutputFilePresentRunComplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.test_helper_set_run_finished_complete('foo')
        self.assertTrue(cluster.is_output_files_present('foo'))
        
    def testIsOutputFilePresentRunIncomplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.test_helper_set_ok_to_run("foo")
        self.assertFalse(cluster.is_output_files_present('foo'))
        cluster.test_helper_set_run_finished_incomplete('foo')
        self.assertFalse(cluster.is_output_files_present('foo'))
    
    def testGetModTimeOutputFileRunComplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.test_helper_set_ok_to_run("foo")
        cluster.test_helper_set_run_finished_complete('foo')
        self.assertTrue(cluster.get_output_file_mod_time('foo') == 'outputFileModTimeX')
        
    
    def testGetModTimeOutputFileRunIncomplete(self):
        stdout = mock_stdout.MockStdout()
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", self.lines, stdout)
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        cluster = mock_cluster.MockCluster(cluster_runs)
        cluster.create_script("foo", "scriptFoo")
        cluster.launch("foo")
        cluster.test_helper_set_ok_to_run("foo")
        cluster.test_helper_set_run_finished_incomplete('foo')
        self.assertTrue(cluster.get_output_file_mod_time('foo') == 0)
    

if __name__ == '__main__':
    unittest.main()
    
   