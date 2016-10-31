'''
Created on Oct 28, 2016

@author: Jed Irvine
'''

class MockCluster(object):
    
    '''
    classdocs
    '''
    #TESTED
    def create_script(self, pcode, cscript):
        self.scripts[pcode] = cscript
        
    #TESTED
    def delete_script(self, pcode):
        if self.scripts.has_key(pcode):
            self.scripts.pop(pcode)

    #TESTED
    def delete_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            self.invoke_logs.pop(pcode)

    def test_helper_set_qacct_info(self,pcode, info):
        self.qacct_logs[pcode] = info
        
    #TESTED
    def delete_qacct_log(self, pcode):
        if self.qacct_logs.has_key(pcode):
            self.qacct_logs.pop(pcode)
         
    
    def test_helper_set_qstat_info(self, info):
        self.qstat_log = info
        
    #TESTED
    def delete_qstat_log(self):
        if (self.qstat_log):
            self.qstat_log = 0

    def test_helper_set_run_finished_incomplete(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] =='running':
                self.done_markers[pcode] ='doneMarker'
                self.running_state.pop(pcode)
                
    def test_helper_set_run_finished_complete(self, pcode):
        if self.running_state.has_key(pcode):
            if self.running_state[pcode] =='running':
                self.output_files[pcode] ='results'
                self.done_markers[pcode] = 'doneMarker'
                self.running_state.pop(pcode)
    
    #TESTED    
    def delete_results(self, pcode):
        if self.output_files.has_key(pcode):
            self.output_files.pop(pcode)

    #TESTED
    def launch(self, pcode):
        if self.scripts.has_key(pcode):
            self.invoke_logs[pcode] = "invokeLog"
            self.running_state[pcode] = "waiting"
    
    def test_helper_set_ok_to_run(self, pcode):
        if self.running_state[pcode] == "waiting":
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

    def __init__(self, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.scripts =          {}
        self.invoke_logs =      {}
        self.running_state =    {}
        self.qacct_logs =       {}
        self.qstat_log= 0
        self.output_files =           {}
        self.done_markers =     {}
        self.permission_blocked = {}
        