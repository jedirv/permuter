'''
Created on Feb 9, 2014

@author: irvine
'''
import os
import time
import cluster_spec
import cluster_runs_info
import permutations
import cluster_script
import qsub_invoke_log
import qstat_log
import qacct_log
import pooled_results_delta_file
import pooled_timings_file
import pooled_results_file
import ranked_results_file
import logging

class PermutationDriver(object):
    
    def __init__(self,cspec_lines, cspec_path, cluster_system):
        self.cspec = cluster_spec.ClusterSpec(cspec_path, cspec_lines, cluster_system)
        self.cluster_runs = cluster_runs_info.ClusterRunsInfo(self.cspec, cluster_system)
        self.cspec_path = cspec_path
        self.cluster_system = cluster_system
        
    def run_command(self, permute_command):
        cluster_runs = self.cluster_runs
        cluster_system = self.cluster_system
        cspec_path = self.cspec_path
        if (permute_command == "gen"):
            generate_scripts(cluster_runs)
        elif (permute_command == "launch"):
            if (detect_still_running_runs(cluster_runs, cluster_system)):
                cluster_system.println("Permutation jobs still running.  Use 'stop' to stop them before 'launch' to avoid replicated jobs")
            else:
                clean_results(cluster_runs, cluster_system)
                clean_pooled_results(cluster_runs, cluster_system)
                launch_scripts(cluster_runs, cluster_system)
        elif (permute_command == "auto"):
            if (detect_still_running_runs(cluster_runs, cluster_system)):
                cluster_system.println("Permutation jobs still running.  Use 'stop' to stop them before 'auto' to avoid replicated jobs")
            else:
                generate_scripts(cluster_runs)
                launch_scripts(cluster_runs, cluster_system)
        elif (permute_command == "preview"):
            preview_scripts(cluster_runs, cluster_system)
        elif (permute_command == "test_launch"):
            clean_results(cluster_runs, cluster_system)
            clean_pooled_results(cluster_runs, cluster_system)
            test_launch_single_script(cluster_runs, cluster_system)
        elif (permute_command == "collect"):
            collect(cluster_runs, cluster_system)
        
        elif (permute_command == "stat"):
            check_status_of_runs(cluster_runs,"summary", cluster_system)
        elif (permute_command == "stat_full"):
            check_status_of_runs(cluster_runs,"full", cluster_system)
        elif (permute_command == "stat_pending"):
            check_status_of_runs(cluster_runs,"pending", cluster_system)
        elif (permute_command == "stat_all"):
            run_command_on_all_specs(cspec_path,"stat",cluster_system)
        elif (permute_command == "stat_full_all"):
            run_command_on_all_specs(cspec_path,"stat_full",cluster_system)
        elif (permute_command == "stat_pending_all"):
            run_command_on_all_specs(cspec_path,"stat_pending",cluster_system)
        
        elif (permute_command == "stop"):
            stop_runs(cluster_runs, cluster_system)
        elif (permute_command == "clean_scripts"):
            clean_scripts(cluster_runs, cluster_system)
        elif (permute_command == "clean_results"):
            clean_results(cluster_runs, cluster_system)
        elif (permute_command == "clean_pooled_results"):
            clean_pooled_results(cluster_runs, cluster_system)
        elif (permute_command == "clean_all"):
            stop_runs(cluster_runs, cluster_system)
            clean_scripts(cluster_runs, cluster_system)
            clean_results(cluster_runs, cluster_system)
            clean_pooled_results(cluster_runs, cluster_system)
        
        else:
            pass
        
    
def collect(cluster_runs, cluster_system):
    #warn_of_incomplete_runs(cluster_runs)
    logging.info('COLLECTING results')
    resultsFiles = create_pooled_results_files(cluster_runs, cluster_system)
    create_pooled_results_delta_files(resultsFiles)
    create_pooled_timings_files(cluster_runs)
    create_ranked_results_files(cluster_runs)
    
def detect_still_running_runs(cluster_runs, cluster_system):
    logging.info('SCANNING for incomplete runs')
    cspec = cluster_runs.cspec
    still_running_count = 0
    
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
        user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
        trial = permutation_info['trials']
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, trial, cluster_system)
        cluster_job_number = qil.cluster_job_number
        # first, check qstat to see if this job is still running
        if (cluster_job_number == "NA"):
            pass
        else:
            statloq = qstat_log.QStatLog(user_job_number_as_string, permutation_info, cspec,trial, cluster_system)
            if (statloq.is_cluster_job_still_running(cluster_job_number)):
                still_running_count = still_running_count + 1
                cluster_system.println("{0} still running".format(cluster_job_number))
            
    if (still_running_count != 0):
        return True
    return False

            
    
def warn_of_incomplete_runs(cluster_runs, cluster_system):
    logging.info('CHECKING for incomplete runs')
    cspec = cluster_runs.cspec
    still_running_permutations = []
    still_running_count = 0
    not_started_count = 0
    finished_healthy_count = 0
    finished_error_count = 0
    
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
        user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
        trial = permutation_info['trials']
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, trial)
        cluster_job_number = qil.cluster_job_number
        #print "cluster_job_number is {0}".format(cluster_job_number)
        # first, check qstat to see if this job is still running
        if (cluster_job_number == "NA"):
            not_started_count = not_started_count + 1
            cluster_system.println("{0} - no evidence of having launched".format(user_job_number_as_string))
        else:
            statloq = qstat_log.QStatLog(user_job_number_as_string, permutation_info, cspec,trial)
            if (statloq.is_cluster_job_still_running(cluster_job_number)):
                still_running_permutations.append(run_permutation_code)
                still_running_count = still_running_count + 1
                cluster_system.println("{0} still running".format(cluster_job_number))
            else:
                #print "{0} done".format(cluster_job_number)
                qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, trial)
                qacctlog.ingest(cluster_job_number)
                if (qacctlog.run_failed()):
                    finished_error_count = finished_error_count + 1
                    cluster_system.println("{0} run issue : {1} -> {2}".format(cluster_job_number, run_permutation_code, qacctlog.get_failure_reason()))
                else:
                    finished_healthy_count = finished_healthy_count + 1

    if (not_started_count != 0):
        cluster_system.println("{0} permutations not started".format(not_started_count))
    if (still_running_count != 0):
        cluster_system.println("{0} permutations still running".format(still_running_count))
        for still_running_permutation in still_running_permutations:
            cluster_system.println("still running : {0}".format(still_running_permutation))
    cluster_system.println("{0} permutations complete".format(finished_healthy_count))
            

def stop_runs(cluster_runs, cluster_system):
    logging.info('STOPPING runs that are still going')
    cspec = cluster_runs.cspec
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        stop_run_if_running(cluster_runs, run_permutation_code, cspec, cluster_system)


def stop_run_if_running(cluster_runs, run_permutation_code, cspec, cluster_system):
    logging.debug('STOPPING run if still running')
    run_finished = cluster_runs_info.did_run_finish(cluster_runs, run_permutation_code, cluster_system)
    permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
    trial = permutation_info['trials']
    user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, trial, cluster_system)
    cluster_job_number = qil.cluster_job_number
    if (cluster_job_number == "NA"):
        cluster_system.println("{0} - no evidence of having launched".format(user_job_number_as_string))
    else:
        if (not(run_finished)):
            #print "{0}\t{1}\tstill running".format(cluster_job_number, qil.get_job_file_name())
            stop_run(cluster_job_number, cluster_system)
            qil.delete()
        else:
            cluster_system.println("{0} detected as finished {1}".format(cluster_job_number, user_job_number_as_string))
    
def stop_run(cluster_job_number, cluster_system):
    command = "qdel {0}".format(cluster_job_number)
    cluster_system.execute_command(command)
                    
def run_command_on_all_specs(cspec_path, permuter_command,cluster_system):
    spec_dir = os.path.dirname(cspec_path)
    file_or_dirnames = cluster_system.listdir(spec_dir)
    cspec_paths = []
    for entry in file_or_dirnames:
        full_path = "{0}/{1}".format(spec_dir,entry)
        if (cluster_system.isfile(full_path) and not(full_path.endswith("~"))):
            f = cluster_system.open_file(full_path, 'r')
            header = f.readline()
            f.close()
            if (header.startswith("#cspec")):
                cspec_paths.append(full_path)
    for path in cspec_paths:
        command = "python permuter.py {0} {1}".format(permuter_command, path)
        cluster_system.println("-------------------------------------------------------------------")
        #print command
        cluster_system.execute_command(command) 
    
def check_status_of_runs(cluster_runs, output_style, cluster_system):
    logging.info('CHECKING status of runs')
    cspec = cluster_runs.cspec
    running_count = 0
    permission_block_count = 0
    failed_count = 0
    complete_count = 0
    total_count = 0
    not_yet_launched_count = 0
    unknown_count = 0
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        status = check_status_of_run(cluster_runs, run_permutation_code, cspec, output_style, cluster_system)
        if (status=="not_yet_launched"):
            not_yet_launched_count = not_yet_launched_count + 1
        elif (status=="permission_block"):
            permission_block_count = permission_block_count + 1
        elif (status=="still_running"):
            running_count = running_count + 1
        elif (status=="complete"):
            complete_count = complete_count + 1
        elif (status=="failed"):
            failed_count = failed_count + 1
        else:
            unknown_count = unknown_count + 1
        total_count = total_count + 1
    message = "{0}({1})\t".format(cspec.master_job_name, total_count)
    if complete_count != 0:
        message = "{0}complete: {1}\t".format(message, complete_count)
    if not_yet_launched_count != 0:
        message = "{0}not yet launched: {1}\t".format(message, not_yet_launched_count)
    if running_count != 0:
        message = "{0}running: {1}\t".format(message, running_count)
    if permission_block_count != 0:
        message = "{0}nfs permission issue: {1}\t".format(message, permission_block_count)
    if failed_count != 0:
        message = "{0}failed: {1}\t".format(message, failed_count)
    if unknown_count != 0:
        message = "{0}unknown fate: {1}\t".format(message, unknown_count)
    #message = "{0}\n".format(message)
    print message
        
def check_status_of_run(cluster_runs, run_permutation_code, cspec, output_style, cluster_system):
    logging.debug('CHECKING status of run')
    run_finished = cluster_runs_info.did_run_finish(cluster_runs, run_permutation_code, cluster_system)
    missing_output_file = False
    permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
    missing_output_files = cluster_runs_info.get_missing_output_files(permutation_info, cspec, cluster_system)
    if (len(missing_output_files) != 0):
        missing_output_file = True 
            
    user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
    cluster_job_number = qil.cluster_job_number
    # summary , full, pending
    if (cluster_job_number == "NA"):
        if (output_style == "full" or output_style == "pending"):
            cluster_system.println("{0} - no evidence of having launched".format(user_job_number_as_string))
        return "not_yet_launched"
    else:
        if (not(run_finished)):
            if qil.is_first_error_permission_problem():
                if (output_style == "full" or output_style == "pending"):
                    cluster_system.println("{0}\t{1}\tblocked on permissions".format(cluster_job_number, qil.get_job_file_name()))
                return "permission_block"
            else:
                if (output_style == "full" or output_style == "pending"):
                    cluster_system.println("{0}\t{1}\tstill running".format(cluster_job_number, qil.get_job_file_name()))
                return "still_running"
        elif (run_finished and not(missing_output_file)):
            #done
            if (output_style == "full"):
                cluster_system.println("{0}\t{1}\tcomplete".format(cluster_job_number, qil.get_job_file_name()))
            return "complete"
        else:
            #fun finished but missing an output file, find out the error
            qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
            qacctlog.ingest(cluster_job_number)
            if (output_style == "full" or output_style == "pending"):
                cluster_system.println("{0} FAILED -> {1}".format(cluster_job_number, qacctlog.get_failure_reason()))
            for missing_file in missing_output_files:
                cluster_system.println("output file missing: {0}".format(missing_file))
            return "failed"
   

def create_pooled_results_delta_files(resultsFiles, cluster_system):
    logging.info('CREATING results delta files')
    for resultsFile in resultsFiles:
        deltaFile = pooled_results_delta_file.PooledResultsDeltaFile(resultsFile, cluster_system)
        deltaFile.generate()
    
    
def create_pooled_timings_files(cluster_runs, cluster_system):
    logging.info('CREATING timings files')
    permuters_for_filename = pooled_timings_file.gather_file_permuters(cluster_runs.cspec)
    #print "permuters_for_filename {0}".format(permuters_for_filename)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    #print "filename_permutations {0}".format(filename_permutations)
    if (len(filename_permutations) == 0):
        timingsFile = pooled_timings_file.PooledTimingsFile({}, cluster_runs, cluster_system)
        timingsFile.persist()
    else: 
        for filename_permutation_info in filename_permutations:
            timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs, cluster_system)
            timingsFile.persist()


  
def create_ranked_results_files(cluster_runs, cluster_system):
    logging.info('CREATING ranked results file')
    permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    if (len(filename_permutations) == 0):
        rankFile = ranked_results_file.RankedResultsFile({}, cluster_runs, cluster_system)
        rankFile.persist()
    else:
        for filename_permutation_info in filename_permutations:
            rankFile = ranked_results_file.RankedResultsFile(filename_permutation_info, cluster_runs, cluster_system)
            rankFile.persist()
        
  
def create_pooled_results_files(cluster_runs, cluster_system):
    logging.info("CREATING pooled results files")
    source_file_map = cluster_runs_info.create_source_file_map(cluster_runs.cspec)
    logging.debug("...source_file_map : {0}".format(source_file_map))
    permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
    logging.debug("...permuters_for_filename : {0}".format(permuters_for_filename))
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    logging.debug("...filename permutations : {0}".format(filename_permutations))
    resultsFiles = []
    if (len(filename_permutations) == 0):
        resultsFile = pooled_results_file.PooledResultsFile(source_file_map, {}, cluster_runs, cluster_system)
        resultsFile.persist()
        resultsFiles.append(resultsFile)
    else:
        for filename_permutation_info in filename_permutations:
            resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cluster_runs, cluster_system)
            resultsFile.persist()
            resultsFiles.append(resultsFile)
    logging.info("...resultsFiles : {0}".format(resultsFiles))    
    return resultsFiles

def delete_results(cspec, cluster_system):
    logging.info('DELETING results')
    source_file_map = cluster_runs_info.create_source_file_map(cspec)
    for permutation, result_path in source_file_map.items():
        comment = "deleting result file for {0}".format(permutation)
        cluster_system.delete_file(comment, result_path)
        pardir = cluster_system.get_par_dir(result_path)
        done_marker_path = "{0}/permutation_done_marker.txt".format(pardir)
        deletion_message = "deleting done marker path {0}".format(done_marker_path)
        cluster_system.delete_file(deletion_message, done_marker_path)
     
def launch_scripts(cluster_runs, cluster_system):
    logging.info('LAUNCHING scripts')
    cspec = cluster_runs.cspec
    delete_results(cspec, cluster_system)
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        #user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
        #permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
        #cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
        cscript = cluster_runs.get_script_for_run_permutation_code(run_permutation_code)
        cscript.launch()
        time.sleep(cluster_system.get_time_delay())

    
def generate_scripts(cluster_runs):
    logging.info('GENERATING scripts')
    #cspec = cluster_runs.cspec
    #for trial in range(1, int(cspec.trials) + 1):
    for run_permutation_code in cluster_runs.run_perm_codes_list:
        #results_dir = cluster_runs.get_results_dir_for_run_permutation_code(run_permutation_code)
        #cluster_system.make_dirs(results_dir)
        #user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(run_permutation_code)
        #permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
        #cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
        cscript = cluster_runs.get_script_for_run_permutation_code(run_permutation_code)
        cscript.generate()

def clean_scripts(cluster_runs,cluster_system):
    logging.info('CLEANING scripts')
    script_dir = cluster_runs.cspec.script_dir
    files = cluster_system.listdir(script_dir)
    for f in files:
        path = "{0}/{1}".format(script_dir, f)
        cluster_system.delete_file("deleting script file", path)

def preview_scripts(cluster_runs, cluster_system):
    logging.info("PREVIEWING scripts")
    #cspec = cluster_runs.cspec
    #permutation_info = cluster_runs.permutation_info_list_full[0]
    #user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    #cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'], cluster_system)
    
    cscript = cluster_runs.get_first_script()
    cscript.preview()


def test_launch_single_script(cluster_runs, cluster_system):
    logging.info('TEST_LAUNCH single script')
    #cspec = cluster_runs.cspec
    #run_permutation_code = cluster_runs.run_perm_codes_list[0]
    #user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_code(run_permutation_code)
    #permutation_info = cluster_runs.run_permutation_info_for_run_permutation_code_map[run_permutation_code]
    cscript = cluster_runs.get_first_script()
    cscript.launch()
           

def clean_results(cluster_runs, cluster_system):
    logging.info('CLEANING results')
    print('CLEANING results')
    results_dir = cluster_runs.cspec.job_results_dir
    cluster_system.clean_out_dir(results_dir)
    
def clean_pooled_results(cluster_runs, cluster_system):
    logging.info('CLEANING pooled results')
    print('CLEANING pooled results')
    cspec = cluster_runs.cspec
    pooled_results_dir = "{0}/{1}".format(cspec.scores_to, cspec.master_job_name)
    cluster_system.clean_out_dir(pooled_results_dir)
    
    
