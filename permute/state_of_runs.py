'''
Created on Feb 23, 2014

@author: irvine
'''

import logging
from __builtin__ import False

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
        self.run_invoke_error = {}
        
        # file objects
        #self.qil_files =              {}
        #self.qacct_files =            {}
        
        self.missing_output_files =   {}
        self.run_error_info =         {}
        self.cluster_job_numbers =    {}

        self.state_names = {}
        self.state_cause = {}
        self.state_todos = {}
        # se  ile rpb dme ofe stand for:
        # run_script_exists,invoke_log_exists,run_invoke_error,done_marker_exists,output_files_exist
        # se  ile  rpb  dme  ofe
        # S    L   B    D    O  
        self.state_names['-----'] = 'script missing'
        self.state_cause['-----'] = ''
        self.state_todos['-----'] = 'launch'
        
        self.state_names['S----'] = 'script ready'
        self.state_cause['S----'] = ''
        self.state_todos['S----'] = 'launch'
        
        self.state_names['-L---'] = 'inconsistent'
        self.state_cause['-L---'] = 'invoke log present but no script_file'
        self.state_todos['-L---'] = 'retry'
        
        self.state_names['SL---'] = 'inconsistent'
        self.state_cause['SL---'] = 'files suggest system should be running, but not seen in qstat'
        self.state_todos['SL---'] = 'retry'
        
        self.state_names['--B--'] = 'inconsistent'
        self.state_cause['--B--'] = 'script file missing, evidence of prior invoke error'
        self.state_todos['--B--'] = 'retry'
        
        self.state_names['S-B--'] = 'inconsistent'
        self.state_cause['S-B--'] = 'invoke log missing, though evidence of invoke error'
        self.state_todos['S-B--'] = 'retry'
        
        self.state_names['-LB--'] = 'inconsistent'
        self.state_cause['-LB--'] = 'script missing, invoke log present'
        self.state_todos['-LB--'] = 'retry'
        
        self.state_names['SLB--'] = 'invoke error'
        self.state_cause['SLB--'] = 'run error detected'
        self.state_todos['SLB--'] = 'look into error, then retry'
        
        

 
        self.state_names['---D-'] = 'inconsistent'
        self.state_cause['---D-'] = 'done marker found, but no script or results found'
        self.state_todos['---D-'] = 'retry'
        
        self.state_names['S--D-'] = 'inconsistent'
        self.state_cause['S--D-'] = 'done marker found, but no evidence of script being invoked - stale results?'
        self.state_todos['S--D-'] = 'retry'
        
        self.state_names['-L-D-'] = 'inconsistent'
        self.state_cause['-L-D-'] = 'done marker found, but no script found and no results present'
        self.state_todos['-L-D-'] = 'retry'
        
        self.state_names['SL-D-'] = 'results missing'
        self.state_cause['SL-D-'] = 'done marker found, but no results'
        self.state_todos['SL-D-'] = 'troubleshoot, then retry'
        
        self.state_names['--BD-'] = 'inconsistent'
        self.state_cause['--BD-'] = 'invoke error detected, but done marker present'
        self.state_todos['--BD-'] = 'troubleshoot, then retry'
        
        self.state_names['S-BD-'] = 'inconsistent'
        self.state_cause['S-BD-'] = 'invoke error detected, but done marker present'
        self.state_todos['S-BD-'] = 'troubleshoot, then retry'
        
        self.state_names['-LBD-'] = 'inconsistent'
        self.state_cause['-LBD-'] = 'invoke error detected, but done marker present'
        self.state_todos['-LBD-'] = 'troubleshoot, then retry'
        
        self.state_names['SLBD-'] = 'inconsistent'
        self.state_cause['SLBD-'] = 'invoke error detected, but done marker present'
        self.state_todos['SLBD-'] = 'retry'
 
 
 
        self.state_names['----O'] = 'stale results?'
        self.state_cause['----O'] = 'output present but no script or done marker'
        self.state_todos['----O'] = 'retry if unexpected'
        
        self.state_names['S---O'] = 'stale results?'
        self.state_cause['S---O'] = 'output present but no done marker'
        self.state_todos['S---O'] = 'retry if unexpected'
        
        self.state_names['-L--O'] = 'stale results?'
        self.state_cause['-L--O'] = 'output present but no script or done marker'
        self.state_todos['-L--O'] = 'retry if unexpected'
        
        self.state_names['SL--O'] = 'run near complete'
        self.state_cause['SL--O'] = ''
        self.state_todos['SL--O'] = ''
        
        self.state_names['--B-O'] = 'stale results?'
        self.state_cause['--B-O'] = 'output exists but no done marker or script'
        self.state_todos['--B-O'] = 'retry if unexpected'
        
        self.state_names['S-B-O'] = 'stale results?'
        self.state_cause['S-B-O'] = 'output exists, done marker and invoke log missing'
        self.state_todos['S-B-O'] = 'retry if unexpected'
        
        self.state_names['-LB-O'] = 'stale results?'
        self.state_cause['-LB-O'] = 'output exists, done marker missing, script missing'
        self.state_todos['-LB-O'] = 'retry if unexpected'
        
        self.state_names['SLB-O'] = 'inconsistent'
        self.state_cause['SLB-O'] = 'output exists, done marker missing and evidence of invoke error'
        self.state_todos['SLB-O'] = 'retry if unexpected'
        
 
 
        self.state_names['---DO'] = 'stale results?'
        self.state_cause['---DO'] = 'output exists, script and invoke log missing'
        self.state_todos['---DO'] = 'retry if unexpected'
        
        self.state_names['S--DO'] = 'stale results?'
        self.state_cause['S--DO'] = 'output exists, invoke log missing'
        self.state_todos['S--DO'] = 'retry if unexpected'
        
        self.state_names['-L-DO'] = 'stale results?'
        self.state_cause['-L-DO'] = 'output exists, script missing'
        self.state_todos['-L-DO'] = 'retry if unexpected'
        
        self.state_names['SL-DO'] = 'run complete'
        self.state_cause['SL-DO'] = ''
        self.state_todos['SL-DO'] = ''
        
        self.state_names['--BDO'] = 'stale results?'
        self.state_cause['--BDO'] = 'script and invoke log missing'
        self.state_todos['--BDO'] = 'retry if unexpected'
        
        self.state_names['S-BDO'] = 'stale results?'
        self.state_cause['S-BDO'] = 'output exists, invoke error detected'
        self.state_todos['S-BDO'] = 'retry if unexpected'
        
        self.state_names['-LBDO'] = 'stale results?'
        self.state_cause['-LBDO'] = 'results present but script missing and evidence of invoke error'
        self.state_todos['-LBDO'] = 'retry if unexpected'
        
        self.state_names['SLBDO'] = 'stale results?'
        self.state_cause['SLBDO'] = 'results present but evidence of invoke error'
        self.state_todos['SLBDO'] = 'retry if unexpected'
       
        # se ile ilc   stand for 
        # run_script_exists,invoke_log_corrupt
        self.state_names['-C-XX'] = 'possible error'
        self.state_cause['-C-XX'] = "invoke log corrupt, launch may have failed"
        self.state_todos['-C-XX'] = 'retry'
    
        
        self.state_names['SC-XX'] = 'possible error'
        self.state_cause['SC-XX'] = "invoke log corrupt, launch may have failed"
        self.state_todos['SC-XX'] = 'retry'

        self.state_names['running'] = 'running'
        self.state_cause['running'] = ""
        self.state_todos['running'] = ''

        self.state_names['waiting'] = 'waiting'
        self.state_cause['waiting'] = ""
        self.state_todos['waiting'] = ''

        self.qstat_state_info =   {}
        self.run_states = {}
        
        self.running_count = 0
        self.permission_block_count = 0
        self.failed_count = 0
        self.complete_count = 0
        self.total_count = 0
        self.not_yet_launched_count = 0
        self.unknown_count = 0
    
    def assess_all_runs(self, cluster_runs, cluster):
        # get qstat output in case it has relevant info for later
        for pcode in cluster_runs.run_perm_codes_list:
            self.assess_run(pcode, cluster_runs, cluster)
            
    def assess_run(self, pcode, cluster_runs, cluster):
        # script status
        self.run_script_exists[pcode]   = cluster.is_script_present(pcode)
        self.script_mtime[pcode]        = cluster.get_script_mod_time(pcode)        
        
        #invoke_log_status
        self.invoke_log_exists[pcode]   = cluster.is_invoke_log_present(pcode)
        self.invoke_log_corrupt[pcode]  = cluster.is_invoke_log_corrupt(pcode)
        self.cluster_job_numbers[pcode] = cluster.get_cluster_job_number(pcode)
        self.invoke_log_mtime[pcode]    = cluster.get_invoke_log_mod_time(pcode)
        
        #qstat status
        if cluster.is_running(pcode):
            self.qstat_state_info[pcode]= 'running'
        elif cluster.is_waiting(pcode):
            self.qstat_state_info[pcode] = 'waiting'
        else:
            self.qstat_state_info[pcode] = 'NA'
                
        # check file system evidence
        self.run_invoke_error[pcode] = cluster.get_invoke_error(pcode)
        
        self.done_marker_exists[pcode] = cluster.is_done_marker_present(pcode)
        self.done_marker_mtime[pcode] = cluster.get_done_marker_mod_time(pcode)
        
        self.output_files_exist[pcode] = cluster.is_output_files_present(pcode)
        self.output_files_mtime[pcode] = cluster.get_output_file_mod_time(pcode)
        self.derive_state_of_run(cluster_runs,pcode, cluster)
    
    def emit_run_states_full(self, stdout, cluster_runs):
        for pcode in cluster_runs.run_perm_codes_list:
            self.emit_run_state_full(stdout, pcode)
            
    def emit_run_state_full(self, stdout, pcode):
        state = self.run_states[pcode]
        cluster_job_number = self.cluster_job_numbers[pcode]
        self.emit_state(stdout, cluster_job_number, pcode, state)
     
    def emit_state_errors(self, stdout, cluster_runs):
        for pcode in cluster_runs.run_perm_codes_list:
            if self.is_run_in_error_state(pcode):
                self.emit_run_state_full(stdout, pcode)
                   
    def emit_run_states_pending(self, stdout, cluster_runs):
        for pcode in cluster_runs.run_perm_codes_list:     
            self.emit_run_state_pending(stdout, pcode)
                
    def emit_run_state_pending(self, stdout, pcode):
        state = self.run_states[pcode]
        cluster_job_number = self.cluster_job_numbers[pcode]
        if state != 'run complete':
            self.emit_state(stdout, cluster_job_number, pcode, state)
    
    def emit_state(self, stdout, cluster_job_number, pcode, state):
        if self.state_cause[state] == '':
            cause = ''
        else:
            cause = "\t({0})".format(self.state_cause[state])
        if self.state_todos[state] == '':
            todos = ''
        else:
            todos = "\t-> {0}".format(self.state_todos[state])
        stdout.println('{0}\t{1}\t{2}{3}{4}'.format(cluster_job_number, pcode ,self.state_names[state], cause, todos))
        if self.state_names[state] == 'invoke_error':
            if self.run_invoke_error.has_key(pcode):
                error_message = self.run_invoke_error[pcode]
                stdout.println("...{0}".format(error_message))
                           
    def emit_state_summary(self, stdout, cluster_runs):
        script_missing_count = 0
        script_ready_count = 0
        run_state_inconsistent_count = 0
        waiting_count = 0
        running_count = 0
        invoke_error_count = 0
        output_missing_count = 0
        run_near_complete_count = 0
        run_complete_count = 0
        unknown_run_state_count = 0
        stale_results_count = 0
        total_count = len(cluster_runs.run_perm_codes_list)
        for pcode in cluster_runs.run_perm_codes_list:   
            stdout.print_without_newline('.')  
            if self.run_states.has_key(pcode):
                state_code = self.run_states[pcode]
                state_name = self.state_names[state_code]
                if state_name == 'script missing':
                    script_missing_count = script_missing_count + 1
                elif state_name == 'script ready':
                    script_ready_count = script_ready_count + 1
                elif state_name == 'inconsistent':
                    run_state_inconsistent_count = run_state_inconsistent_count + 1
                elif state_name == 'running':
                    running_count = running_count + 1
                elif state_name == 'waiting':
                    waiting_count = waiting_count + 1
                elif state_name == 'invoke error':
                    invoke_error_count = invoke_error_count + 1
                elif state_name == 'results missing':
                    output_missing_count = output_missing_count + 1
                elif state_name == 'run near complete':
                    run_near_complete_count = run_near_complete_count + 1
                elif state_name == 'run complete':
                    run_complete_count = run_complete_count + 1
                elif state_name == 'stale results?':
                    stale_results_count = stale_results_count + 1
                else:
                    unknown_run_state_count = unknown_run_state_count + 1
            else:
                unknown_run_state_count = unknown_run_state_count + 1 
        
        stdout.println("")          
        master_job_name = cluster_runs.cspec.master_job_name
        message = "{0}({1})\t".format(master_job_name, total_count)
        
        if script_missing_count != 0:
            message = "{0}scripts missing: {1}\n".format(message, script_missing_count)
        if script_ready_count != 0:
            message = "{0}scripts ready to run: {1}\n".format(message, script_ready_count)
        if running_count != 0:
            message = "{0}running: {1}\n".format(message, running_count)
        if waiting_count != 0:
            message = "{0}waiting: {1}\n".format(message, waiting_count)
        if run_near_complete_count != 0:
            message = "{0}near complete: {1}\n".format(message, run_near_complete_count)
        if run_complete_count != 0:
            message = "{0}complete: {1}\n".format(message, run_complete_count)
        if output_missing_count != 0:
            message = "{0}output files missing: {1}\n".format(message, output_missing_count)
        if stale_results_count != 0:
            message = "{0}possible stale results: {1}\n".format(message, stale_results_count)
        if invoke_error_count != 0:
            message = "{0}invoke error: {1}\n".format(message, invoke_error_count)
        if run_state_inconsistent_count != 0:
            message = "{0}run state inconsistent: {1}\n".format(message, run_state_inconsistent_count)
        if unknown_run_state_count != 0:
            message = "{0}state undefined: {1}\n".format(message, unknown_run_state_count)
        #message = "{0}\n".format(message)
        stdout.println(message)

    def is_ok_to_launch_all(self,cluster_runs, cluster):
        result = True
        for pcode in cluster_runs.run_perm_code_list:
            if not(self.is_ok_to_launch_run(pcode, cluster)):
                result = False
        return result

    def is_run_in_error_state(self, pcode):
        state_code = self.run_states[pcode]
        state_name = self.state_names[state_code]
        if state_name == 'inconsistent':
            return True
        if state_name == 'results missing':
            return True
        if state_name == 'invoke error':
            return True
        if state_name == 'stale results?':
            return True
        if state_name == 'possible error':
            return True
        
        
    def is_ok_to_launch_run(self, pcode, cluster):
        if cluster.is_waiting(pcode) or cluster.is_running(pcode):
            return False
        return True
        
    def derive_state_of_runs(self,cluster_runs, cluster):
        for pcode in cluster_runs.run_perm_codes_list:
            self.derive_state_of_run(cluster_runs,pcode, cluster)    
            
    def derive_state_of_run(self,cluster_runs,pcode, cluster):
        if self.invoke_log_corrupt[pcode] == True:
            self.derive_state_of_run_invoke_log_corrupt(cluster_runs, pcode)
        else:
            self.derive_state_of_run_basic(cluster_runs, pcode, cluster)
    
    def derive_state_of_run_invoke_log_corrupt(self,cluster_runs,pcode):
        # se ilc   stand for 
        # run_script_exists,invoke_log_corrupt
        se = '-'
        ilc = 'C'     # given
        if self.run_script_exists[pcode] == True:
            se = 'S'
        live_evidence = '-' 
        # if corrupt, couldn't have parsed out the run number to do qstat command to find run live_evidence will always be '-'
        state_code = '{0}{1}{2}XX'.format(se, ilc, live_evidence)
        self.run_states[pcode] = state_code
  
 
    def derive_state_of_run_basic(self,cluster_runs,pcode, cluster):
        # if we get evidence from qstat that run is waiting or running, just believe that
        if self.qstat_state_info[pcode] == 'running':
            self.run_states[pcode] = 'running'
        elif self.qstat_state_info[pcode]== 'waiting':
            self.run_states[pcode] = 'waiting'
        else:
            # se  ile rpb dme ofe stand for:
            # run_script_exists,invoke_log_exists,run_invoke_error,done_marker_exists,output_files_exist
            # build a string that looks like this: 'se 0 ile 0 rpb 0 dme 0 ofe 0'
            se = '-'
            ile = '-'
            rpb = '-'
            dme = '-'
            ofe = '-'
        
            if self.run_script_exists[pcode] == True:
                se = 'S'
            if self.invoke_log_exists[pcode] == True:
                ile = 'L'
            if self.run_invoke_error[pcode] != '':
                rpb = 'B'
        
            if self.done_marker_exists[pcode] == True:
                dme = 'D'
            if self.output_files_exist[pcode] == True:
                ofe = 'O'
            #import ipdb;ipdb.set_trace()   
            state_code = '{0}{1}{2}{3}{4}'.format(se, ile, rpb, dme, ofe)
            run_state_name = self.state_names[state_code]
            self.run_error_info[pcode] = ''
            if run_state_name == 'run_state_error':
                self.run_error_info[pcode] = self.cluster.get_failure_reason(pcode)
            self.run_states[pcode] = state_code
        
