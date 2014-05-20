'''
Created on Feb 23, 2014

@author: irvine
'''

import cluster_runs_info
import logging
import qsub_invoke_log
import qacct_log
import permutations
import os
import cluster_script

class StateOfRuns(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.scripts_exist = False
        self.all_scripts_exist = False
        self.runs_in_progress = False
        self.runs_completed = False
        self.pooled_results_exist = False
        self.pooled_timings_exist = False
        self.ranked_results_exist = False
        
        self.run_permutation_codes = []
        # status table
        # NOTE - QStatLog is used by detect_still_running_runs 
        self.run_script_exists =      {}
        self.script_mtime =           {}
        self.invoke_log_exists =      {}
        self.invoke_log_corrupt =     {}
        self.invoke_log_mtime =       {}
        self.qacct_log_exists =       {}
        self.qacct_log_corrupt =      {}
        self.qacct_log_mtime =        {}
        self.done_marker_exists =     {}
        self.done_marker_mtime =      {}
        self.output_files_exist =     {}
        self.output_files_mtime =     {}
        self.run_permission_blocked = {}
        
        # file objects
        self.qil_files =              {}
        self.qacct_files =            {}
        
        self.missing_output_files =   {}
        self.run_error_info =         {}
        self.cluster_job_numbers =    {}

        self.state_codes = {}
        # se  ile rpb dme ofe stand for:
        # run_script_exists,invoke_log_exists,run_permission_blocked,done_marker_exists,output_files_exist
        self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 0'] = 'script missing'
        self.state_codes['se 1 ile 0 rpb 0 dme 0 ofe 0'] = 'script ready'
        self.state_codes['se 0 ile 1 rpb 0 dme 0 ofe 0'] = 'run_state_error - launch_log but no script_file : clean logs'
        self.state_codes['se 1 ile 1 rpb 0 dme 0 ofe 0'] = 'running'
        self.state_codes['se 0 ile 0 rpb 1 dme 0 ofe 0'] = 'run_state_error - permission_block_error without script_file : clean logs'
        self.state_codes['se 1 ile 0 rpb 1 dme 0 ofe 0'] = 'run_state_error - permission_block_error without launch_log : clean logs'
        self.state_codes['se 0 ile 1 rpb 1 dme 0 ofe 0'] = 'run_state_error - launch_log present without script_file : clean logs'
        self.state_codes['se 1 ile 1 rpb 1 dme 0 ofe 0'] = 'run permission issue'
 
        self.state_codes['se 0 ile 0 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without script_file : clean results'
        self.state_codes['se 1 ile 0 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without launch_log : clean results'
        self.state_codes['se 0 ile 1 rpb 0 dme 1 ofe 0'] = 'run_state_error - done_marker exists without script_file but launch_log present : clean results, logs'
        self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 0'] = 'run error'
        self.state_codes['se 0 ile 0 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_codes['se 1 ile 0 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_codes['se 0 ile 1 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_codes['se 1 ile 1 rpb 1 dme 1 ofe 0'] = 'run_state_error - done_marker and permission_error should not coexist'
 
        self.state_codes['se 0 ile 0 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without script_file : clean results'
        self.state_codes['se 1 ile 0 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without launch_log : clean results'
        self.state_codes['se 0 ile 1 rpb 0 dme 0 ofe 1'] = 'run_state_error - output_file exists without script_file, but has launch_log : clean results, logs'
        self.state_codes['se 1 ile 1 rpb 0 dme 0 ofe 1'] = 'run near complete'
        self.state_codes['se 0 ile 0 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
        self.state_codes['se 1 ile 0 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
        self.state_codes['se 0 ile 1 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
        self.state_codes['se 1 ile 1 rpb 1 dme 0 ofe 1'] = 'run_state_error - done_marker and run_error should not coexist'
 
        self.state_codes['se 0 ile 0 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without script_file : clean results'
        self.state_codes['se 1 ile 0 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without launch_log : clean results'
        self.state_codes['se 0 ile 1 rpb 0 dme 1 ofe 1'] = 'run_state_error - done_marker exists without script_file, but launch_log present : clean results, logs'
        self.state_codes['se 1 ile 1 rpb 0 dme 1 ofe 1'] = 'run complete'
        self.state_codes['se 0 ile 0 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
        self.state_codes['se 1 ile 0 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
        self.state_codes['se 0 ile 1 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
        self.state_codes['se 1 ile 1 rpb 1 dme 1 ofe 1'] = 'run_state_error - done_marker and result_file should not coexist'
       
        self.corrupt_qil_state_codes = {} 
        # se ile ilc   stand for 
        # run_script_exists,invoke_log_exists,invoke_log_corrupt
        self.corrupt_qil_state_codes['se 0 ile 1 ilc 1'] = 'run_state_error - launch_log but no script_file : clean logs'
        self.corrupt_qil_state_codes['se 1 ile 1 ilc 1'] = 'launch may have failed - can not acquire cluster_run_number'

        # derived_state_table
        #self.run_not_yet_launched =   {}
        #self.run_still_running =      {}
        #self.run_succeeded =          {}
        #self.output_files_exist =     {}
        
        self.run_states = {}
        
        self.running_count = 0
        self.permission_block_count = 0
        self.failed_count = 0
        self.complete_count = 0
        self.total_count = 0
        self.not_yet_launched_count = 0
        self.unknown_count = 0
        
    def assess(self, cluster_runs_info, cluster_system):    
        self.cluster_system = cluster_system
        self.cluster_runs_info = cluster_runs_info
        
        self.check_milestones_of_runs(cluster_runs_info, cluster_system)
        self.derive_state_of_runs(cluster_runs_info)
        
    def emit_state_full(self):
        for runID in self.run_permutation_codes:
            run_state = self.run_states[runID]
            cluster_job_number = self.cluster_job_numbers[runID]
            self.cluster_system.println('{0} {1}  {2}'.format(cluster_job_number, runID,run_state))
            
            
    def emit_state_summary(self):
        script_missing_count = 0
        script_ready_count = 0
        run_state_error_count = 0
        running_count = 0
        run_permission_error_count = 0
        run_error_count = 0
        run_near_complete_count = 0
        run_complete_count = 0
        unknown_run_state_count = 0
        total_count = len(self.run_permutation_codes)
        for runID in self.run_permutation_codes:   
            self.cluster_system.print_without_newline('.')  
            run_state = self.run_states[runID]
            if run_state == 'script missing':
                script_missing_count = script_missing_count + 1
            elif run_state == 'script ready':
                script_ready_count = script_ready_count + 1
            elif run_state.startswith('run_state_error'):
                run_state_error_count = run_state_error_count + 1
            elif run_state == 'running':
                running_count = running_count + 1
            elif run_state == 'run permission issue':
                run_permission_error_count = run_permission_error_count + 1
            elif run_state == 'run error':
                run_error_count = run_error_count + 1
            elif run_state == 'run near complete':
                run_near_complete_count = run_near_complete_count + 1
            elif run_state == 'run complete':
                run_complete_count = run_complete_count + 1
            else:
                unknown_run_state_count = unknown_run_state_count + 1
        
        self.cluster_system.println("")          
        master_job_name = self.cluster_runs_info.cspec.master_job_name
        message = "{0}({1})\t".format(master_job_name, total_count)
        
        if script_missing_count != 0:
            message = "{0}scripts missing: {1}\t".format(message, script_missing_count)
        if script_ready_count != 0:
            message = "{0}scripts ready to run: {1}\t".format(message, script_ready_count)
        if running_count != 0:
            message = "{0}running: {1}\t".format(message, running_count)
        if run_near_complete_count != 0:
            message = "{0}near complete: {1}\t".format(message, run_near_complete_count)
        if run_complete_count != 0:
            message = "{0}complete: {1}\t".format(message, run_complete_count)
        if run_permission_error_count != 0:
            message = "{0}run permission error: {1}\t".format(message, run_permission_error_count)
        if run_error_count != 0:
            message = "{0}run errors: {1}\t".format(message, run_error_count)
        if run_state_error_count != 0:
            message = "{0}run state error: {1}\t".format(message, run_state_error_count)
        if unknown_run_state_count != 0:
            message = "{0}state undefined: {1}\t".format(message, unknown_run_state_count)
        #message = "{0}\n".format(message)
        self.cluster_system.println(message)
        
    def emit_state_pending(self):
        for runID in self.run_permutation_codes:     
            run_state = self.run_states[runID]
            cluster_job_number = self.cluster_job_numbers[runID]
            if run_state != 'run complete':
                self.cluster_system.println('{0} {1}  {2}'.format(cluster_job_number, runID, run_state))
             
    def check_milestones_of_runs(self, cluster_runs, cluster_system):
        for run_permutation_code in cluster_runs.run_perm_codes_list:
            self.run_permutation_codes.append(run_permutation_code)
            self.check_milestones_of_run(cluster_runs, run_permutation_code, cluster_runs.cspec, cluster_system)
        
    def derive_state_of_runs(self,cluster_runs):
        for run_permutation_code in cluster_runs.run_perm_codes_list:
            self.derive_state_of_run(cluster_runs,run_permutation_code)    
            
    def derive_state_of_run(self,cluster_runs,runID):
        if self.invoke_log_corrupt[runID] == True:
            self.derive_state_of_run_invoke_log_corrupt(cluster_runs, runID)
        else:
            self.derive_state_of_run_basic(cluster_runs, runID)
    
    def derive_state_of_run_invoke_log_corrupt(self,cluster_runs,runID):
        # se ile ilc   stand for 
        # run_script_exists,invoke_log_exists,invoke_log_corrupt
        se = 'se 0'
        ile = 'ile 1'     # if it's corrupt , it must exist
        ilc = 'ilc 1'     # given
        if self.run_script_exists[runID] == True:
            se = 'se 1'
        state_code = '{0} {1} {2}'.format(se, ile, ilc)
        run_state = self.corrupt_qil_state_codes[state_code]       
        self.run_states[runID] = run_state
  
 
    def derive_state_of_run_basic(self,cluster_runs,runID):
        # se  ile rpb dme ofe stand for:
        # run_script_exists,invoke_log_exists,run_permission_blocked,done_marker_exists,output_files_exist
        # build a string that looks like this: 'se 0 ile 0 rpb 0 dme 0 ofe 0'
        se = 'se 0'
        ile = 'ile 0'
        rpb = 'rpb 0'
        dme = 'dme 0'
        ofe = 'ofe 0'
        
        if self.run_script_exists[runID] == True:
            se = 'se 1'
        if self.invoke_log_exists[runID] == True:
            ile = 'ile 1'
        if self.run_permission_blocked[runID] == True:
            rpb = 'rpb 1'
        if self.done_marker_exists[runID] == True:
            dme = 'dme 1'
        if self.output_files_exist[runID] == True:
            ofe = 'ofe 1'
        #import ipdb;ipdb.set_trace()   
        state_code = '{0} {1} {2} {3} {4}'.format(se, ile, rpb, dme, ofe)
        run_state = self.state_codes[state_code]
        self.run_error_info[runID] = ''
        if run_state == 'run had errors':
            self.run_error_info[runID] = self.get_error_reason(runID,cluster_runs, self.cluster_system)
        self.run_states[runID] = run_state
   
   
    def get_error_reason(self,runID, cluster_runs, cluster_system): 
        # get info for QacctLog
        permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[runID]  
        user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(runID) 
        cspec = cluster_runs.cspec
        
        qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cluster_job_number = self.cluster_job_numbers[runID]
        qacctlog.ingest(cluster_job_number)
        failure_reason = qacctlog.get_failure_reason()
        return failure_reason
    
 
    def check_milestones_of_run(self, cluster_runs, run_permutation_code, cspec, cluster_system):
        runID = run_permutation_code
        logging.debug('CHECKING status of run')
        # populate self.run_script_exists
        cluster_script_instance = cluster_runs.get_script_for_run_permutation_code(runID)
        script_exists = cluster_system.exists(cluster_script_instance.pathname)
        self.run_script_exists[runID] = script_exists
        self.script_mtime[runID] = cluster_script_instance.get_last_modification_time()
        
        # populate self.invoke_log_exists
        # populate self.invoke_log_corrupt
        # populate self.invoke_log_mtime
        permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[runID]
        user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(runID)
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
        self.cluster_job_numbers[runID] = qil.cluster_job_number
        self.qil_files[runID] = qil
        self.invoke_log_exists[runID] = cluster_system.isfile(qil.qsub_invoke_log_fullpath)
        if self.invoke_log_exists[runID] == True:
            self.invoke_log_corrupt[runID] = qil.is_corrupt()
            if self.invoke_log_corrupt[runID] == True:
                self.invoke_log_mtime[runID] = 'NA'
            else:
                self.invoke_log_mtime[runID] = qil.get_last_modification_time()
        else:
            self.invoke_log_corrupt[runID] = 'NA'
            self.invoke_log_mtime[runID] = 'NA'
            
            
        # populate self.run_permission_blocked    
        self.run_permission_blocked[runID] = qil.is_first_error_permission_problem()
        
        # populate self.qacct_log_exists
        # populate self.qacct_log_corrupt
        # populate self.qacct_log_mtime
        qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
        self.qacct_files[runID] = qacctlog
        self.qacct_log_exists[runID] = cluster_system.isfile(qacctlog.qacct_log)
        if self.qacct_log_exists[runID] == True:
            self.qacct_log_corrupt[runID] = qacctlog.is_corrupt()
            if self.qacct_log_corrupt[runID] == True:
                self.qacct_log_mtime[runID] = 'NA'
            else:
                self.qacct_log_mtime[runID] = qacctlog.get_last_modification_time()
        else:
            self.qacct_log_corrupt[runID] = 'NA'
            self.qacct_log_mtime[runID] = 'NA'
        
        
        
        # populate  self.done_marker_exists
        self.done_marker_exists[runID] = cluster_runs_info.did_run_finish(cluster_runs, runID, cluster_system)
        if (self.done_marker_exists[runID] == True):
            results_dir = cluster_runs.get_results_dir_for_run_permutation_code(runID)
            done_file = cluster_script.get_done_marker_filename()
            done_marker_file_path = "{0}/{1}".format(results_dir, done_file)
            self.done_marker_mtime[runID] = cluster_system.get_last_modification_time(done_marker_file_path)
        else:
            self.done_marker_mtime[runID] = 'NA'
        
        # populate self.output_files_exist
        # populate self.output_files_mtime
        missing_output_file = False
        missing_output_files = cluster_runs_info.get_missing_output_files(permutation_info, cspec, cluster_system)
        self.missing_output_files[runID] = missing_output_files
        if (len(missing_output_files) != 0):
            missing_output_file = True 
        self.output_files_exist[runID] = not(missing_output_file)
        
        list_of_output_files = permutations.get_list_of_output_files(permutation_info, cspec)
        time = 0
        # find the oldest output_file mod time
        for output_file in list_of_output_files:
            curtime = cluster_system.get_last_modification_time(output_file)
            if time == 0:
                time = curtime
            else:
                if curtime < time:
                    time = curtime
        if time == 0:
            self.output_files_mtime[runID] = 'NA'
        else:
            self.output_files_mtime[runID] = time
   
  
    def check_for_any_scripts(self, cluster_system, cluster_runs_info):
        for run_perm_code in cluster_runs_info.run_perm_codes_list:
            cluster_script_instance = cluster_runs_info.get_script_for_run_permutation_code(run_perm_code)
            if (cluster_system.exists(cluster_script_instance.pathname)):
                return True
            return False
        
    def check_for_all_scripts(self, cluster_system, cluster_runs_info):
        result = True
        for run_perm_code in cluster_runs_info.run_perm_codes_list:
            cluster_script_instance = cluster_runs_info.get_script_for_run_permutation_code(run_perm_code)
            if not(cluster_system.exists(cluster_script_instance.pathname)):
                result = False
        return result
        
