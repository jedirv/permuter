'''
Created on Nov 19, 2013

@author: admin-jed
'''
import sys, os, time
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
import subprocess

def main():
    if (len(sys.argv) < 3):
        usage()
        exit()
    permute_command = sys.argv[1]
    cspec_path = sys.argv[2]
    flags = ""
    if (len(sys.argv) == 4):
        flags = sys.argv[3]
        
     # set up logging 
    home_dir_permuter = os.path.expanduser('~/permuter')
    logging_level = logging.INFO
    if (flags == '-debug'):
        logging_level = logging.DEBUG
    if (not(os.path.isdir(home_dir_permuter))):
        os.makedirs(home_dir_permuter)
    logging.basicConfig(filename='{0}/permuter.log'.format(home_dir_permuter), filemode='w', level=logging_level)
    
    validate_args(permute_command, cspec_path, flags)
    if (not(cluster_spec.validate(cspec_path))):
        exit()
    cspec = cluster_spec.ClusterSpec(cspec_path)
    cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
    
   
            
    # why isn't logging working?
    if (permute_command == "gen"):
        generate_scripts(cluster_runs)
    elif (permute_command == "launch"):
        clean_results(cluster_runs)
        clean_pooled_results(cluster_runs)
        launch_scripts(cluster_runs)
    elif (permute_command == "auto"):
        generate_scripts(cluster_runs)
        launch_scripts(cluster_runs)
    elif (permute_command == "preview"):
        preview_scripts(cluster_runs)
    elif (permute_command == "test_launch"):
        clean_results(cluster_runs)
        clean_pooled_results(cluster_runs)
        test_launch_single_script(cluster_runs)
    elif (permute_command == "collect"):
        collect(cluster_runs)
        
    elif (permute_command == "stat"):
        check_status_of_runs(cluster_runs,"summary")
    elif (permute_command == "stat_full"):
        check_status_of_runs(cluster_runs,"full")
    elif (permute_command == "stat_pending"):
        check_status_of_runs(cluster_runs,"pending")
    elif (permute_command == "stat_all"):
        run_command_on_all_specs(cspec_path,"stat")
    elif (permute_command == "stat_full_all"):
        run_command_on_all_specs(cspec_path,"stat_full")
    elif (permute_command == "stat_pending_all"):
        run_command_on_all_specs(cspec_path,"stat_pending")
        
    elif (permute_command == "stop"):
        stop_runs(cluster_runs)
    elif (permute_command == "clean_scripts"):
        clean_scripts(cluster_runs)
    elif (permute_command == "clean_results"):
        clean_results(cluster_runs)
    elif (permute_command == "clean_pooled_results"):
        clean_pooled_results(cluster_runs)
    elif (permute_command == "clean_all"):
        stop_runs(cluster_runs)
        clean_scripts(cluster_runs)
        clean_results(cluster_runs)
        clean_pooled_results(cluster_runs)
        
    else:
        pass
    logging.shutdown()    
    
def clean_results(cluster_runs):
    logging.info('CLEANING results')
    print('CLEANING results')
    results_dir = cluster_runs.cspec.job_results_dir
    clean_out_dir(results_dir)
    
def clean_pooled_results(cluster_runs):
    logging.info('CLEANING pooled results')
    print('CLEANING pooled results')
    cspec = cluster_runs.cspec
    pooled_results_dir = "{0}/{1}".format(cspec.scores_to, cspec.master_job_name)
    clean_out_dir(pooled_results_dir)
    
def clean_out_dir(dirpath):
    if not(os.path.exists(dirpath)):
        return
    items = os.listdir(dirpath)
    for item in items:
        path = "{0}/{1}".format(dirpath, item)
        if os.path.isdir(path):
            try: 
                print "deleting dir {0}".format(path)
                command = "rm -rf {0}".format(path)
                os.system(command) 
            except subprocess.CalledProcessError:
                print "There was a problem calling rm -rf on {0}".format(path)
                print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
                    
        else:
            try: 
                print "deleting file {0}".format(path)
                command = "rm -f {0}".format(path)
                os.system(command) 
            except subprocess.CalledProcessError:
                print "There was a problem calling rm -f on {0}".format(path)
                print "Return code was {0}".format(subprocess.CalledProcessError.returncode)                        
        
def collect(cluster_runs):
    #warn_of_incomplete_runs(cluster_runs)
    logging.info('COLLECTING results')
    resultsFiles = create_pooled_results_files(cluster_runs)
    create_pooled_results_delta_files(resultsFiles)
    create_pooled_timings_files(cluster_runs)
    create_ranked_results_files(cluster_runs)
    

def warn_of_incomplete_runs(cluster_runs):
    logging.info('CHECKING for incomplete runs')
    cspec = cluster_runs.cspec
    still_running_permutation_infos = []
    still_running_count = 0
    not_started_count = 0
    finished_healthy_count = 0
    finished_error_count = 0
    
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cluster_job_number = qil.cluster_job_number
        #print "cluster_job_number is {0}".format(cluster_job_number)
        # first, check qstat to see if this job is still running
        if (cluster_job_number == "NA"):
            not_started_count = not_started_count + 1
            print "{0} - no evidence of having launched".format(user_job_number_as_string)
        else:
            statloq = qstat_log.QStatLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
            if (statloq.is_cluster_job_still_running(cluster_job_number)):
                still_running_permutation_infos.append(permutation_info)
                still_running_count = still_running_count + 1
                print "{0} still running".format(cluster_job_number)
            else:
                #print "{0} done".format(cluster_job_number)
                qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
                qacctlog.ingest(cluster_job_number)
                if (qacctlog.run_failed()):
                    finished_error_count = finished_error_count + 1
                    print "{0} run issue : {1} -> {2}".format(cluster_job_number, permutation_info, qacctlog.get_failure_reason())
                else:
                    finished_healthy_count = finished_healthy_count + 1

    if (not_started_count != 0):
        print "{0} permutations not started".format(not_started_count)
    if (still_running_count != 0):
        print "{0} permutations still running".format(still_running_count)
        for still_running_permutation_info in still_running_permutation_infos:
            print "still running : {0}".format(still_running_permutation_info) 
    print "{0} permutations complete".format(finished_healthy_count) 
            

def stop_runs(cluster_runs):
    logging.info('STOPPING runs that are still going')
    cspec = cluster_runs.cspec
    for permutation_info in cluster_runs.permutation_info_list_full:
        stop_run_if_running(cluster_runs, permutation_info, cspec)


def stop_run_if_running(cluster_runs, permutation_info, cspec):
    logging.debug('STOPPING run if still running')
    permutation_code = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, True)
    run_finished = cluster_runs_info.did_run_finish(cluster_runs, permutation_code)

    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    if (cluster_job_number == "NA"):
        print "{0} - no evidence of having launched".format(user_job_number_as_string)
    else:
        if (not(run_finished)):
            #print "{0}\t{1}\tstill running".format(cluster_job_number, qil.get_job_file_name())
            stop_run(cluster_job_number)
            qil.delete()
        else:
            print "{0} detected as finished {1}".format(cluster_job_number, user_job_number_as_string)
    
def stop_run(cluster_job_number):
    try: 
        print "calling qdel {0}".format(cluster_job_number)
        command = "qdel {0}".format(cluster_job_number)
        os.system(command) 
    except subprocess.CalledProcessError:
        print "There was a problem calling qdel on job {0}".format(cluster_job_number)
        print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
                    
def run_command_on_all_specs(cspec_path, permuter_command):
    spec_dir = os.path.dirname(cspec_path)
    file_or_dirnames = os.listdir(spec_dir)
    cspec_paths = []
    for entry in file_or_dirnames:
        full_path = "{0}/{1}".format(spec_dir,entry)
        if (os.path.isfile(full_path) and not(full_path.endswith("~"))):
            f = open(full_path, 'r')
            header = f.readline()
            f.close()
            if (header.startswith("#cspec")):
                cspec_paths.append(full_path)
    for path in cspec_paths:
        command = "python permuter.py {0} {1}".format(permuter_command, path)
        print "-------------------------------------------------------------------"
        #print command
        os.system(command) 
    
def check_status_of_runs(cluster_runs, output_style):
    logging.info('CHECKING status of runs')
    cspec = cluster_runs.cspec
    running_count = 0
    permission_block_count = 0
    failed_count = 0
    complete_count = 0
    total_count = 0
    not_yet_launched_count = 0
    unknown_count = 0
    for permutation_info in cluster_runs.permutation_info_list_full:
        status = check_status_of_run(cluster_runs, permutation_info, cspec, output_style)
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
        
def check_status_of_run(cluster_runs, permutation_info, cspec, output_style):
    logging.debug('CHECKING status of run')
    permutation_code = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, True)
    run_finished = cluster_runs_info.did_run_finish(cluster_runs, permutation_code)
    missing_output_file = False
    missing_output_files = cluster_runs_info.get_missing_output_files(permutation_info, cspec)
    if (len(missing_output_files) != 0):
        missing_output_file = True 
            

    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    # summary , full, pending
    if (cluster_job_number == "NA"):
        if (output_style == "full" or output_style == "pending"):
            print "{0} - no evidence of having launched".format(user_job_number_as_string)
        return "not_yet_launched"
    else:
        if (not(run_finished)):
            if qil.is_first_error_permission_problem():
                if (output_style == "full" or output_style == "pending"):
                    print "{0}\t{1}\tblocked on permissions".format(cluster_job_number, qil.get_job_file_name())
                return "permission_block"
            else:
                if (output_style == "full" or output_style == "pending"):
                    print "{0}\t{1}\tstill running".format(cluster_job_number, qil.get_job_file_name())
                return "still_running"
        elif (run_finished and not(missing_output_file)):
            #done
            if (output_style == "full"):
                print "{0}\t{1}\tcomplete".format(cluster_job_number, qil.get_job_file_name())
            return "complete"
        else:
            #fun finished but missing an output file, find out the error
            qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
            qacctlog.ingest(cluster_job_number)
            if (output_style == "full" or output_style == "pending"):
                print "{0} FAILED -> {1}".format(cluster_job_number, qacctlog.get_failure_reason())
            for missing_file in missing_output_files:
                print "output file missing: {0}".format(missing_file)
            return "failed"
    #print "DONE checking run status"
    #print "cluster_job_number is {0}".format(cluster_job_number)
    # first, check qstat to see if this
    #statloq = qstat_log.QStatLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    #if (statloq.is_cluster_job_still_running(cluster_job_number)):
    #    print "{0} still running".format(cluster_job_number)
    #else:
    #    #print "{0} done".format(cluster_job_number)
    #    qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    #    qacctlog.ingest(cluster_job_number)
    #    if (qacctlog.run_failed()):
    #        print "{0} FAILED -> {1}".format(cluster_job_number, qacctlog.get_failure_reason())
    #    else:
    #        print "{0} complete".format(cluster_job_number)        
         
def create_pooled_results_delta_files(resultsFiles):
    logging.info('CREATING results delta files')
    for resultsFile in resultsFiles:
        deltaFile = pooled_results_delta_file.PooledResultsDeltaFile(resultsFile)
        deltaFile.generate()
    
    
def create_pooled_timings_files(cluster_runs):
    logging.info('CREATING timings files')
    permuters_for_filename = pooled_timings_file.gather_file_permuters(cluster_runs.cspec)
    print "permuters_for_filename {0}".format(permuters_for_filename)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    print "filename_permutations {0}".format(filename_permutations)
    if (len(filename_permutations) == 0):
        timingsFile = pooled_timings_file.PooledTimingsFile({}, cluster_runs)
        timingsFile.persist()
    else: 
        for filename_permutation_info in filename_permutations:
            timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs)
            timingsFile.persist()


  
def create_ranked_results_files(cluster_runs):
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
        
  
def create_pooled_results_files(cluster_runs):
    logging.info("CREATING pooled results files")
    source_file_map = create_source_file_map(cluster_runs.cspec)
    logging.debug("...source_file_map : {0}".format(source_file_map))
    permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
    logging.debug("...permuters_for_filename : {0}".format(permuters_for_filename))
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    logging.debug("...filename permutations : {0}".format(filename_permutations))
    resultsFiles = []
    if (len(filename_permutations) == 0):
        resultsFile = pooled_results_file.PooledResultsFile(source_file_map, {}, cluster_runs)
        resultsFile.persist()
        resultsFiles.append(resultsFile)
    else:
        for filename_permutation_info in filename_permutations:
            resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cluster_runs)
            resultsFile.persist()
            resultsFiles.append(resultsFile)
    logging.info("...resultsFiles : {0}".format(resultsFiles))    
    return resultsFiles

def delete_results(cspec):
    logging.info('DELETING results')
    source_file_map = create_source_file_map(cspec)
    for permutation, result_path in source_file_map.items():
        if (os.path.isfile(result_path)):
            print "deleting result_file for {0} : {1}".format(permutation, result_path)
            os.unlink(result_path)
        pardir = os.path.dirname(result_path)
        done_marker_path = "{0}/permutation_done_marker.txt".format(pardir)
        if (os.path.isfile(done_marker_path)):
            print "deleting done_marker_path for {0} : {1}".format(permutation, done_marker_path)
            os.unlink(done_marker_path)
     
def launch_scripts(cluster_runs):
    logging.info('LAUNCHING scripts')
    cspec = cluster_runs.cspec
    delete_results(cspec)
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cscript.launch()
        time.sleep(1.5)

    
def generate_scripts(cluster_runs):
    logging.info('GENERATING scripts')
    cspec = cluster_runs.cspec
    #for trial in range(1, int(cspec.trials) + 1):
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cscript.generate()

def clean_scripts(cluster_runs):
    logging.info('GENERATING scripts')
    script_dir = cluster_runs.cspec.script_dir
    files = os.listdir(script_dir)
    for f in files:
        path = "{0}/{1}".format(script_dir, f)
        os.remove(path)

def preview_scripts(cluster_runs):
    logging.info("PREVIEWING scripts")
    cspec = cluster_runs.cspec
    permutation_info = cluster_runs.permutation_info_list_full[0]
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cscript.preview()


def test_launch_single_script(cluster_runs):
    logging.info('TEST_LAUNCH single script')
    cspec = cluster_runs.cspec
    permutation_info = cluster_runs.permutation_info_list_full[0]
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cscript.launch()
           
                  
 
def validate_args(permute_command, cspec_path, flags):
    if (not(permute_command == "collect" or 
            permute_command == "stat" or 
            permute_command == "stat_full" or 
            permute_command == "stat_pending" or 
            permute_command == "stat_all" or 
            permute_command == "stat_full_all" or 
            permute_command == "stat_pending_all" or 
            permute_command == "gen" or 
            permute_command == "launch" or 
            permute_command == "auto" or 
            permute_command == "preview" or 
            permute_command == "stop" or 
            permute_command == "clean_scripts" or 
            permute_command == "clean_results" or 
            permute_command == "clean_pooled_results" or 
            permute_command == "clean_all" or 
            permute_command == "test_launch")):
        usage()
        exit()
    # verify spec path exists
    try:
        f = open(cspec_path, 'r')
        # verify first line has cspec flag
        header = f.readline()
        if (header != "#cspec\n"):
            print "cspec file must have this header:  '#cspec', {0} does not. Exiting.".format(cspec_path)
            f.close()
            exit()
        f.close()
    except IOError:
        print "An error occurred trying to open {0}".format(cspec_path)
        exit()
    if (flags != "-debug" and flags != ""):
        print "Invalid flag {0}. -debug is only flag supported".format(flags)
        exit()
  
def get_full_perm_code(permutation_info,scores_permutations_info, cspec):
    master_permutation_info = {}
    for key, val in permutation_info.items():
        master_permutation_info[key] = val
    if (len(scores_permutations_info) != 0):
        for key, val in scores_permutations_info.items():
            master_permutation_info[key] = val
    full_perm_code = permutations.generate_permutation_code(master_permutation_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
    return full_perm_code
                
def get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, scores_permutations_info):
    # first resolve the regular_permutations info in the scores_from_filepath
    list_of_one = [ from_file_path_with_results_dir_resolved ]
    revised_list_of_one = permutations.resolve_permutation(permutation_info, list_of_one, cspec.key_val_map)
    partially_resolved_from_filepath = revised_list_of_one[0]
    # now resolve the scores_permutation info in the scores_from_filepath
    list_of_one = [ partially_resolved_from_filepath ]
    revised_list_of_one = permutations.resolve_permutation(scores_permutations_info, list_of_one, cspec.key_val_map)
    fully_resolved_from_filepath = revised_list_of_one[0]
    return fully_resolved_from_filepath
    
def create_source_file_map(cspec):
    logging.info('CREATING source file map')   
    source_file_map = {}
    #need to add trials in with cspec.permuters before expanding
    trials_list = cspec.get_trials_list() 
    permuters_with_trials = {}
    for key, val in cspec.permuters.items():
        permuters_with_trials[key] = val
    permuters_with_trials['trials'] = trials_list
     
    permutation_list = permutations.expand_permutations(permuters_with_trials)
    for permutation_info in permutation_list:
        permutation_code = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, permutations.IGNORE_TRIALS)
        #print "permutation_code {0}".format(permutation_code)
        permutation_results_dir = cspec.generate_results_dir_for_permutation(permutation_info['trials'], permutation_code) 
        from_file_path_with_results_dir_resolved = cspec.scores_from_filepath.replace('<permutation_results_dir>',permutation_results_dir)
        #print "from_file_path_with_results_dir_resolved {0}".format(from_file_path_with_results_dir_resolved)
        scores_permutations_list = permutations.expand_permutations(cspec.scores_permuters)
        if (len(scores_permutations_list) == 0):
            fully_resolved_from_filepath = get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, {})
            full_perm_code = get_full_perm_code(permutation_info,{}, cspec)
            source_file_map[full_perm_code] = fully_resolved_from_filepath
        else:
            for scores_permutations_info in scores_permutations_list:
                fully_resolved_from_filepath = get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, scores_permutations_info)
                full_perm_code = get_full_perm_code(permutation_info,scores_permutations_info, cspec)
                source_file_map[full_perm_code] = fully_resolved_from_filepath
                #print "source_file_map[{0}] = {1}".format(full_perm_code, fully_resolved_from_filepath)
    return source_file_map


  
def usage():
    print "usage:  python permuter.py  some_command <path of cluster_spec>  [-debug]"
    print ""
    print "        where some_command can be:"
    print"               preview                # print to stdout what the first script generated will look like"     
    print"               gen                    # generate cluster scripts"              
    print"               test_launch            # launch the first script to see if it runs successfully"            
    print"               launch                 # launch all the generated cluster scripts"                   
    print"               auto                   # runs gen and then launch in sequence - only use if very confident" 
    print""
    print" once the runs are launched, the following commands are relevant:"                         
    print"               stat                   # show the summary counts of status of runs"                   
    print"               stat_full              # show the status of each permutation run"                   
    print"               stat_pending           # show the status of each permutation run that is not finished"                    
    print"               stat_all               # show the summary status of all specs."                                     
    print"               stat_full_all          # show the status of each permutation run for all specs."                                     
    print"               stat_pending_all       # show the status of each permutation run that is not finished for all specs"                  
    print"               stop                   # call qdel on any runs that are unfinished to abort them"                    
    print"               clean_scripts          # clean the launch scripts and associated .out, .err, and .qil files"                   
    print"               clean_results          # clean only the contents of <permutation_results_dir>" 
    print"               clean_pooled_results   # clean only the pooled results"           
    print"               clean_all              # clean scripts, results, pooled results, and stop running jobs" 
    print"               collect                # created pooled results from results"  
    print""
    print""
    print"  -debug will enable DEBUG level logging which is 'INFO' level by default.  Log sent to ~/permuter/permuter.log"  

    
if __name__ == '__main__':
    main()
    
