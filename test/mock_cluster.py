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
         
    def delete_all_but_script(self,pcode):
        self.delete_invoke_log(pcode)
        self.delete_qacct_log(pcode)
        self.delete_qstat_log()
        self.delete_done_marker(pcode)
        self.delete_pooled_results_file(pcode)
        self.delete_pooled_delta_file(pcode)
        self.delete_pooled_timings_file(pcode)
        self.delete_ranked_results_file(pcode)
        self.delete_results(pcode)
        
    def delete_pooled_results(self, pcode):
        
    def delete_pooled_results_delta_file(self,pcode):
        
    def delete_pooled_results_timings_file(self,pcode):
        
    def delete_ranked_results_file(self,pcode):  
        
        
    def create_pooled_results_delta_files(self,resultsFiles):
        for resultsFile in resultsFiles:
            
    def create_pooled_timings_files(self,cluster_runs): redo this
        logging.info('CREATING timings files')
        permuters_for_filename = pooled_timings_file.gather_file_permuters(cluster_runs.cspec)
        #print "permuters_for_filename {0}".format(permuters_for_filename)
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        #print "filename_permutations {0}".format(filename_permutations)
        if (len(filename_permutations) == 0):
            timingsFile = pooled_timings_file.PooledTimingsFile({}, cluster_runs)
            timingsFile.persist()
        else: 
            for filename_permutation_info in filename_permutations:
                timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs)
                timingsFile.persist()
                           
    def create_ranked_results_files(cluster_runs): redo this
        logging.info('CREATING ranked results file')
        permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        if (len(filename_permutations) == 0):
            rankFile = ranked_results_file.RankedResultsFile({}, cluster_runs)
            rankFile.persist()
        else:
            for filename_permutation_info in filename_permutations:
                rankFile = ranked_results_file.RankedResultsFile(filename_permutation_info, cluster_runs)
                rankFile.persist()
                
    def create_pooled_results_files(self,cluster_runs, stdout):redo this
        logging.info("CREATING pooled results files")
        source_file_map = cluster_runs.create_source_file_map(cluster_runs.cspec)
        logging.debug("...source_file_map : {0}".format(source_file_map))
        permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
        logging.debug("...permuters_for_filename : {0}".format(permuters_for_filename))
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        logging.debug("...filename permutations : {0}".format(filename_permutations))
        resultsFiles = []
        if (len(filename_permutations) == 0):
            resultsFile = pooled_results_file.PooledResultsFile(source_file_map, {}, cluster_runs, stdout)
            resultsFile.persist()
            resultsFiles.append(resultsFile)
        else:
            for filename_permutation_info in filename_permutations:
                resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cluster_runs, stdout)
                resultsFile.persist()
                resultsFiles.append(resultsFile)
        logging.info("...resultsFiles : {0}".format(resultsFiles))    
        return resultsFiles        
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
            if self.get_invoke_error(pcode) != '':
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

    def test_helper_set_invoke_error(self,pcode):
        self.invoke_errors[pcode] = 'permissionBlocked'
        
    #TESTED
    def get_invoke_error(self, pcode):
        if self.invoke_errors.has_key(pcode):
            return self.invoke_errors[pcode]
        return ''

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
    
    ####################
    #  Stubs
    ####################
    def clean_out_dir(self,dirpath):
        pass
    
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
        self.invoke_errors = {}
        self.run_number = 1;
        self.cluster_job_numbers= {}
        
def get_time():
    ticks = time.time()
    return ticks
        