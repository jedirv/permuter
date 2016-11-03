'''
Created on Oct 28, 2016

@author: Jed Irvine
'''
import time
class MockCluster(object):
    
    '''
    classdocs
    '''
    #TESTED
    def create_script(self, pcode):
        cscript = self.cluster_runs.get_script_for_perm_code(pcode)
        self.scripts[pcode] = cscript
        self.scripts_mod_time[pcode] = get_time()
        return cscript
        
    #TESTED
    def delete_script(self, pcode):
        if self.scripts.has_key(pcode):
            self.scripts.pop(pcode)
            self.scripts_mod_time.pop(pcode)
    
    def get_script_mod_time(self,pcode):
        if self.scripts_mod_time.has_key(pcode):
            return self.scripts_mod_time[pcode]
        return 'NA'
        
    #TESTED
    def delete_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            self.invoke_logs.pop(pcode)
            self.invoke_logs_mod_time.pop(pcode)

    def test_helper_set_qacct_info(self,pcode, info):
        self.qacct_logs[pcode] = info
        self.qacct_logs_mod_time[pcode] = get_time()
        
    #TESTED
    def delete_qacct_log(self, pcode):
        if self.qacct_logs.has_key(pcode):
            self.qacct_logs.pop(pcode)
            self.qacct_logs_mod_time.pop(pcode)
         
    
    def test_helper_set_qstat_info(self, info):
        self.qstat_log = info
        self.qstat_logs_mod_time= get_time()
        
    #TESTED
    def delete_qstat_log(self):
        if (self.qstat_log):
            self.qstat_log = 0
            self.qstat_log_mod_time = 0

    def test_helper_set_run_finished_incomplete(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] =='running':
                self.done_markers[pcode] ='doneMarker'
                self.done_markers_mod_time[pcode] = get_time()
                self.running_state.pop(pcode)
                
    def test_helper_set_run_finished_complete(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] =='running':
                self.output_files[pcode] ='results'
                self.output_files_mod_time[pcode] = get_time()
                self.done_markers[pcode] = 'doneMarker'
                self.done_markers_mod_time[pcode] = get_time()
                self.running_state.pop(pcode)
    
    #TESTED    
    def delete_results(self, pcode):
        if self.output_files.has_key(pcode):
            self.output_files.pop(pcode)
            self.output_files_mod_time.pop(pcode)
            
    def delete_done_marker(self, pcode):
        if self.done_markers.has_key(pcode):
            self.done_markers.pop(pcode)
            self.done_markers_mod_time.pop(pcode)
            
    #TESTED
    def launch(self, pcode):
        if self.scripts.has_key(pcode):
            self.invoke_logs[pcode] = "invokeLog"
            self.invoke_logs_mod_time[pcode] = get_time()
            self.running_state[pcode] = "waiting"
            self.cluster_job_numbers[pcode] = self.run_number
            self.run_number = self.run_number + 1
    
    def test_helper_set_ok_to_run(self, pcode):
        if self.running_state[pcode] == "waiting":
            if self.is_permission_blocked(pcode):
                pass
            else:
                self.running_state[pcode] = "running"    
 
    def test_helper_corrupt_invoke_log(self,pcode):
        if self.invoke_logs.has_key(pcode):
            self.invoke_logs[pcode] = 'corruptInvokeLog'
            
    #TESTED        
    def stop_run(self, pcode):
        if self.running_state.has_key(pcode):
            self.running_state.pop(pcode)

    #TESTED
    def is_script_present(self, pcode):
        if self.scripts.has_key(pcode):
            return True
        return False

    #TESTED
    def is_invoke_log_present(self, pcode):
        if self.invoke_logs.has_key(pcode):
            return True
        return False
        
    def get_invoke_log_mod_time(self,pcode):
        if self.invoke_logs_mod_time.has_key(pcode):
            return self.invoke_logs_mod_time[pcode]
        return 'NA'
        
    #TESTED
    def is_qacct_log_present(self, pcode):
        if self.qacct_logs.has_key(pcode):
            return True
        return False

    #TESTED
    def is_qstat_log_present(self):
        if self.qstat_log:
            return True
        return False
    
    #TESTED
    def is_invoke_log_corrupt(self, pcode):
        result = False
        if self.invoke_logs.has_key(pcode):
            if self.invoke_logs[pcode] == 'corruptInvokeLog':
                result = True
        return result
    
    #TESTED
    def is_running(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] == 'running':
                return True
        return False

    #TESTED
    def is_waiting(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] == 'waiting':
                return True
        return False

    def test_helper_set_permission_blocked(self,pcode):
        self.permission_blocked[pcode] = 'permissionBlocked'
        
    #TESTED
    def is_permission_blocked(self, pcode):
        if self.permission_blocked.has_key(pcode):
            return True
        return False

    #TESTED
    def is_done_marker_present(self, pcode):
        if self.done_markers.has_key(pcode):
            return True
        return False


    def get_done_marker_mod_time(self,pcode):
        if self.done_markers_mod_time.has_key(pcode):
            return self.done_markers_mod_time[pcode]
        return 'NA'
     
    def get_failure_reason(self,pcode):
        if self.is_qacct_log_present(pcode):
            return 'failure_cause_xyz'
        return 'NA'
    
    #TESTED
    def is_output_files_present(self, pcode):
        if self.output_files.has_key(pcode):
            return True
        return False

    #TESTED
    def get_output_file_mod_time(self, pcode):
        if self.output_files.has_key(pcode):
            return "outputFileModTimeX"
        return 0

    def get_cluster_job_number(self, pcode):
        if self.cluster_job_numbers.has_key(pcode):
            return self.cluster_job_numbers[pcode]
        return 'NA'
    
    def __init__(self, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.scripts =          {}
        self.scripts_mod_time = {}
        self.invoke_logs =      {}
        self.invoke_logs_mod_time = {}
        self.running_state =    {}
        self.qacct_logs =       {}
        self.qacct_logs_mod_time = {}
        self.qstat_log= 0
        self.qstat_mod_time = 0
        self.output_files =     {}
        self.output_files_mod_time = {}
        self.done_markers =     {}
        self.done_markers_mod_time = {}
        self.permission_blocked = {}
        self.run_number = 1;
        self.cluster_job_numbers= {}
        
def get_time():
    ticks = time.time()
    return ticks
        