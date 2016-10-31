'''
Created on Feb 23, 2014

@author: irvine
'''

import cluster_runs_info
import logging
import qsub_invoke_log
import qstat_log
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
        self.qstat_state_info =       {}
        
        self.missing_output_files =   {}
        self.run_error_info =         {}
        self.cluster_job_numbers =    {}

        self.state_names = {}
        self.cause  = {}
        self.action = {}
        # se  ile rpb dme ofe stand for:
        # run_script_exists,invoke_log_exists,run_permission_blocked,done_marker_exists,output_files_exist
        # se  ile  rpb  dme  ofe
        # S    L   B    D    O  
        self.state_names['-----'] = 'script missing'
        self.state_cause['-----'] = ''
        self.state_todos['-----'] = ''
        
        self.state_names['S----'] = 'script ready'
        self.state_cause['S----'] = ''
        self.state_todos['S----'] = ''
        
        self.state_names['-L---'] = 'run_state_error - launch_log but no script_file : clean logs'
        self.state_cause['-L---'] = ''
        self.state_todos['-L---'] = ''
        
        self.state_names['SL---'] = 'running'
        self.state_cause['SL---'] = ''
        self.state_todos['SL---'] = ''
        
        self.state_names['--B--'] = 'run_state_error - permission_block_error without script_file : clean logs'
        self.state_cause['--B--'] = ''
        self.state_todos['--B--'] = ''
        
        self.state_names['S-B--'] = 'run_state_error - permission_block_error without launch_log : clean logs'
        self.state_cause['S-B--'] = ''
        self.state_todos['S-B--'] = ''
        
        self.state_names['-LB--'] = 'run_state_error - launch_log present without script_file : clean logs'
        self.state_cause['-LB--'] = ''
        self.state_todos['-LB--'] = ''
        
        self.state_names['SLB--'] = 'run permission issue'
        self.state_cause['SLB--'] = ''
        self.state_todos['SLB--'] = ''
        
        
        
        

 
        self.state_names['---D-'] = 'run_state_error - done_marker exists without script_file : clean results'
        self.state_cause['---D-'] = ''
        self.state_todos['---D-'] = ''
        
        self.state_names['S--D-'] = 'run_state_error - done_marker exists without launch_log : clean results'
        self.state_cause['S--D-'] = ''
        self.state_todos['S--D-'] = ''
        
        self.state_names['-L-D-'] = 'run_state_error - done_marker exists without script_file but launch_log present : clean results, logs'
        self.state_cause['-L-D-'] = ''
        self.state_todos['-L-D-'] = ''
        
        self.state_names['SL-D-'] = 'run error'
        self.state_cause['SL-D-'] = ''
        self.state_todos['SL-D-'] = ''
        
        self.state_names['--BD-'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_cause['--BD-'] = ''
        self.state_todos['--BD-'] = ''
        
        self.state_names['S-BD-'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_cause['S-BD-'] = ''
        self.state_todos['S-BD-'] = ''
        
        self.state_names['-LBD-'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_cause['-LBD-'] = ''
        self.state_todos['-LBD-'] = ''
        
        self.state_names['SLBD-'] = 'run_state_error - done_marker and permission_error should not coexist'
        self.state_cause['SLBD-'] = ''
        self.state_todos['SLBD-'] = ''
        
 
 
 
 
        self.state_names['----O'] = 'run_state_error - output_file exists without script_file : clean results'
        self.state_cause['----O'] = ''
        self.state_todos['----O'] = ''
        
        self.state_names['S---O'] = 'run_state_error - output_file exists without launch_log : clean results'
        self.state_cause['S---O'] = ''
        self.state_todos['S---O'] = ''
        
        self.state_names['-L--O'] = 'run_state_error - output_file exists without script_file, but has launch_log : clean results, logs'
        self.state_cause['-L--O'] = ''
        self.state_todos['-L--O'] = ''
        
        self.state_names['SL--O'] = 'run near complete'
        self.state_cause['SL--O'] = ''
        self.state_todos['SL--O'] = ''
        
        self.state_names['--B-O'] = 'inconsistent'
        self.state_cause['--B-O'] = 'output exists, but done marker, launch log and script missing'
        self.state_todos['--B-O'] = ''
        
        self.state_names['S-B-O'] = 'inconsistent'
        self.state_cause['S-B-O'] = 'output exists, done marker and launch log missing'
        self.state_todos['S-B-O'] = 'redo'
        
        self.state_names['-LB-O'] = 'inconsistent'
        self.state_cause['-LB-O'] = 'output exists, done marker missing, script missing'
        self.state_todos['-LB-O'] = 'redo'
        
        self.state_names['SLB-O'] = 'inconsistent'
        self.state_cause['SLB-O'] = 'output exists, done marker missing and permission issue'
        self.state_todos['SLB-O'] = 'redo'
        
 
 
 
 
        self.state_names['---DO'] = 'run complete'
        self.state_cause['---DO'] = 'warning: output exists, script and launch file missing'
        self.state_todos['---DO'] = 'redo?'
        
        self.state_names['S--DO'] = ''
        self.state_cause['S--DO'] = ''
        self.state_todos['S--DO'] = ''
        
        self.state_names['-L-DO'] = 'run complete'
        self.state_cause['-L-DO'] = 'warning: output exists, script missing'
        self.state_todos['-L-DO'] = 'redo?'
        
        self.state_names['SL-DO'] = 'run complete'
        self.state_cause['SL-DO'] = ''
        self.state_todos['SL-DO'] = ''
        
        self.state_names['--BDO'] = 'run complete'
        self.state_cause['--BDO'] = 'warning: script and launch log missing'
        self.state_todos['--BDO'] = 'redo?'
        
        self.state_names['S-BDO'] = 'run complete'
        self.state_cause['S-BDO'] = 'warning: output exists, run was blocked, launch log missing'
        self.state_todos['S-BDO'] = 'redo?'
        
        self.state_names['-LBDO'] = 'run complete'
        self.state_cause['-LBDO'] = 'warning: output exists, run was blocked, script missing'
        self.state_todos['-LBDO'] = 'redo?'
        
        self.state_names['SLBDO'] = 'run complete'
        self.state_cause['SLBDO'] = 'warning: permission problem should have prevented run'
        self.state_todos['SLBDO'] = 'redo?'
       
        # se ile ilc   stand for 
        # run_script_exists,invoke_log_corrupt
        self.state_names['-C'] = 'run_state_error - launch_log but no script_file : clean logs'
        self.state_names['SC'] = 'launch may have failed - can not acquire cluster_run_number'

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
        
    def assess_all_runs(self, cluster_runs_info, cluster_system):
        # get qstat output in case it has relevant info for later
        qstat = qstat_log.QStatLog(cluster_system)
        for perm_code in cluster_runs_info.run_perm_codes_list:
            self.assess_run(perm_code, qstat, cluster_runs_info, cluster_system)
            
    def assess_run(self, perm_code, qstat, cluster_runs_info, cluster_system):
        # see of script is there
        self.check_script(perm_code, cluster_runs_info, cluster_system)
        # see if invoke log is there and if it is corrupt
        self.check_invoke_log(perm_code, cluster_runs_info, cluster_system)
        cluster_run_id = self.get_cluster_run_id(perm_code, cluster_system)
        self.qstat_state_info[perm_code] = 'unknown'
        if (not(cluster_run_id == 'unknown')):
            # use cluster run id to find run status using qstat
            self.qstat_state_info[perm_code]= qstat.get_state_info(cluster_run_id)
                
        # check file system evidence
        self.check_for_permission_problem(perm_code)
        self.check_done_marker(perm_code, cluster_runs_info, cluster_system)
        self.check_output_files(perm_code, cluster_runs_info, cluster_system)
        self.derive_state_of_run(cluster_runs_info,perm_code)
               
    def check_output_files(self, perm_code, cluster_runs_info, cluster_system):
        # populate self.output_files_exist
        # populate self.output_files_mtime
        cspec = cluster_runs_info.cspec
        permutation_info = cluster_runs_info.run_permutation_info_for_run_permutation_code_map[perm_code]
        missing_output_file = False
        missing_output_files = cluster_runs_info.get_missing_output_files(permutation_info, cspec, cluster_system)
        self.missing_output_files[perm_code] = missing_output_files
        if (len(missing_output_files) != 0):
            missing_output_file = True 
        self.output_files_exist[perm_code] = not(missing_output_file)
        
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
            self.output_files_mtime[perm_code] = 'NA'
        else:
            self.output_files_mtime[perm_code] = time
        
    def check_done_marker(self, perm_code, cluster_runs_info, cluster_system):
        # populate  self.done_marker_exists
        self.done_marker_exists[perm_code] = cluster_runs_info.did_run_finish(cluster_runs_info, perm_code, cluster_system)
        if (self.done_marker_exists[perm_code] == True):
            results_dir = cluster_runs_info.get_results_dir_for_run_permutation_code(perm_code)
            done_file = cluster_script.get_done_marker_filename()
            done_marker_file_path = "{0}/{1}".format(results_dir, done_file)
            self.done_marker_mtime[perm_code] = cluster_system.get_last_modification_time(done_marker_file_path)
        else:
            self.done_marker_mtime[perm_code] = 'NA'
           
    def check_for_permission_problem(self, perm_code):
        # populate self.run_permission_blocked
        qil = self.qil_files[perm_code]    
        self.run_permission_blocked[perm_code] = qil.is_first_error_permission_problem()
        
    def get_cluster_run_id(self, perm_code, cluster_system):
        if (not(self.invoke_log_exists[perm_code])):
            return 'unknown'
        if (self.invoke_log_corrupt[perm_code]):
            return 'unknown'
        # this would have been set in the check_invoke_log phase
        return self.cluster_job_numbers[perm_code]
                
        
    def check_invoke_log(self, run_permutation_code, cluster_runs_info, cluster_system):
        # populate self.invoke_log_exists
        # populate self.invoke_log_corrupt
        # populate self.invoke_log_mtime
        self.cluster_job_numbers[run_permutation_code] = 'unknown'
        permutation_info = cluster_runs_info.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
        user_job_number_as_string = cluster_runs_info.get_job_number_string_for_run_permutation_code(run_permutation_code)
        cspec = cluster_runs_info.cspec
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
        self.qil_files[run_permutation_code] = qil
        self.invoke_log_exists[run_permutation_code] = cluster_system.isfile(qil.qsub_invoke_log_fullpath)
        if self.invoke_log_exists[run_permutation_code] == True:
            self.invoke_log_corrupt[run_permutation_code] = qil.is_corrupt()
            if self.invoke_log_corrupt[run_permutation_code] == True:
                self.cluster_job_numbers[run_permutation_code] = 'unknown'
                self.invoke_log_mtime[run_permutation_code] = 'NA'
            else:
                self.cluster_job_numbers[run_permutation_code] = qil.cluster_job_number
                self.invoke_log_mtime[run_permutation_code] = qil.get_last_modification_time()
        else:
            self.cluster_job_numbers[run_permutation_code] = 'unknown'
            self.invoke_log_corrupt[run_permutation_code] = 'NA'
            self.invoke_log_mtime[run_permutation_code] = 'NA'
            
    def check_script(self, run_permutation_code, cluster_runs, cluster_system):
        # populate self.run_script_exists
        cluster_script_instance = cluster_runs.get_script_for_run_permutation_code(run_permutation_code)
        script_exists = cluster_system.exists(cluster_script_instance.pathname)
        self.run_script_exists[run_permutation_code] = script_exists
        self.script_mtime[run_permutation_code] = cluster_script_instance.get_last_modification_time()        
        
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
        # se ilc   stand for 
        # run_script_exists,invoke_log_corrupt
        se = '-'
        ilc = 'C'     # given
        if self.run_script_exists[runID] == True:
            se = 'S'
        state_code = '{0}{1}'.format(se, ilc)
        run_state = self.stat_names[state_code]       
        self.run_states[runID] = run_state
  
 
    def derive_state_of_run_basic(self,cluster_runs,runID):
        # se  ile rpb dme ofe stand for:
        # run_script_exists,invoke_log_exists,run_permission_blocked,done_marker_exists,output_files_exist
        # build a string that looks like this: 'se 0 ile 0 rpb 0 dme 0 ofe 0'
        se = '-'
        ile = '-'
        rpb = '-'
        dme = '-'
        ofe = '-'
        
        if self.run_script_exists[runID] == True:
            se = 'S'
        if self.invoke_log_exists[runID] == True:
            ile = 'L'
        if self.run_permission_blocked[runID] == True:
            rpb = 'B'
        if self.done_marker_exists[runID] == True:
            dme = 'D'
        if self.output_files_exist[runID] == True:
            ofe = 'O'
        #import ipdb;ipdb.set_trace()   
        state_code = '{0}{1}{2}{3}{4}'.format(se, ile, rpb, dme, ofe)
        run_state_name = self.state_names[state_code]
        self.run_error_info[runID] = ''
        if run_state_name == 'run_state_error':
            self.run_error_info[runID] = self.get_error_reason(runID,cluster_runs, self.cluster_system)
        self.run_states[runID] = state_code
   
   
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
        
