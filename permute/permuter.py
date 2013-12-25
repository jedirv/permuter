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

verbose = False

def main():
    if (len(sys.argv) < 3):
        usage()
        exit()
    permute_command = sys.argv[1]
    cspec_path = sys.argv[2]
    flags = ""
    if (len(sys.argv) == 4):
        flags = sys.argv[3]
    validate_args(permute_command, cspec_path, flags)
    if (not(cluster_spec.validate(cspec_path))):
        exit()
    cspec = cluster_spec.ClusterSpec(cspec_path)
    cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
    if (flags == "-v"):
        global verbose
        verbose = True
    if (permute_command == "gen"):
        generate_scripts(cluster_runs)
    elif (permute_command == "launch"):
        launch_scripts(cluster_runs)
    elif (permute_command == "auto"):
        generate_scripts(cluster_runs)
        launch_scripts(cluster_runs)
    elif (permute_command == "preview"):
        preview_scripts(cluster_runs)
    elif (permute_command == "test_launch"):
        test_launch_single_script(cluster_runs)
    elif (permute_command == "collect"):
        collect(cluster_runs)
    elif (permute_command == "stat"):
        check_status_of_runs(cluster_runs)
        
    else:
        pass
        
def if_verbose(message):
    global verbose
    if (verbose):
        print message
    
def collect(cluster_runs):
    #warn_of_incomplete_runs(cluster_runs)
    resultsFiles = create_pooled_results_files(cluster_runs)
    create_pooled_results_delta_files(resultsFiles)
    create_pooled_timings_files(cluster_runs)
    

def warn_of_incomplete_runs(cluster_runs):
    cspec = cluster_runs.cspec
    still_running_permutation_infos = []
    still_running_count = 0
    finished_healthy_count = 0
    finished_error_count = 0
    
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cluster_job_number = qil.cluster_job_number
        #print "cluster_job_number is {0}".format(cluster_job_number)
        # first, check qstat to see if this job is still running
        
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

    if (still_running_count != 0):
        print "{0} permutations still running".format(still_running_count)
        for still_running_permutation_info in still_running_permutation_infos:
            print "still running : {0}".format(still_running_permutation_info) 
    print "{0} permutations complete".format(finished_healthy_count) 
            

def check_status_of_runs(cluster_runs):
    cspec = cluster_runs.cspec
    for permutation_info in cluster_runs.permutation_info_list_full:
        check_status_of_run(cluster_runs, permutation_info, cspec)
        
def check_status_of_run(cluster_runs, permutation_info, cspec):
    permutation_code = permutations.generate_permutation_code(permutation_info, cspec.concisePrintMap, True)
    results_dir = cluster_runs.get_results_dir_for_permutation_code(permutation_code)
    
    LEFT OFF HERE GETTING the status from the don_marker file 
    
    also need to detect presence of at least one of the output files - need to key off the following
    scores_from:file=<permutation_results_dir>/score_out_(color).csv,column_name=auc,row_number=1
    ...need to generate list of all output files for permutation, keying off
    scores_permute:color=red,blue,
    so write a cspec.get_permutation_results_files_for_permutation(permutation_info)
    
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    #print "cluster_job_number is {0}".format(cluster_job_number)
    # first, check qstat to see if this
    statloq = qstat_log.QStatLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    if (statloq.is_cluster_job_still_running(cluster_job_number)):
        print "{0} still running".format(cluster_job_number)
    else:
        #print "{0} done".format(cluster_job_number)
        qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        qacctlog.ingest(cluster_job_number)
        if (qacctlog.run_failed()):
            print "{0} FAILED -> {1}".format(cluster_job_number, qacctlog.get_failure_reason())
        else:
            print "{0} complete".format(cluster_job_number)        
         
def create_pooled_results_delta_files(resultsFiles):
    for resultsFile in resultsFiles:
        deltaFile = pooled_results_delta_file.PooledResultsDeltaFile(resultsFile)
        deltaFile.generate()
    
    
def create_pooled_timings_files(cluster_runs):
    permuters_for_filename = pooled_timings_file.gather_file_permuters(cluster_runs.cspec)
    print "permuters_for_filename {0}".format(permuters_for_filename)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    print "filename_permutations {0}".format(filename_permutations)
    for filename_permutation_info in filename_permutations:
        timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs)
        timingsFile.persist()

  
def create_pooled_results_files(cluster_runs):
    source_file_map = create_source_file_map(cluster_runs.cspec)
    permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    resultsFiles = []
    for filename_permutation_info in filename_permutations:
        resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cluster_runs)
        resultsFile.persist()
        resultsFiles.append(resultsFile)
    return resultsFiles

def delete_results(cspec):
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
    cspec = cluster_runs.cspec
    delete_results(cspec)
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cscript.launch()
        time.sleep(1.5)

    
def generate_scripts(cluster_runs):
    cspec = cluster_runs.cspec
    #for trial in range(1, int(cspec.trials) + 1):
    for permutation_info in cluster_runs.permutation_info_list_full:
        user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        cscript.generate()
       

def preview_scripts(cluster_runs):
    cspec = cluster_runs.cspec
    if_verbose("preview mode")
    permutation_info = cluster_runs.permutation_info_list_full[0]
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cscript.preview()


def test_launch_single_script(cluster_runs):
    if_verbose("preview mode")
    cspec = cluster_runs.cspec
    permutation_info = cluster_runs.permutation_info_list_full[0]
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cscript.launch()
           
                  
 
def validate_args(permute_command, cspec_path, flags):
    if (not(permute_command == "collect" or 
            permute_command == "stat" or 
            permute_command == "gen" or 
            permute_command == "launch" or 
            permute_command == "auto" or 
            permute_command == "preview" or 
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
        print "An error occured trying to open {0}".format(cspec_path)
        exit()
    if (flags != ""):
        if (flags != "-v"):
            print "Invalid flag {0}. Only -v for verbose is supported".format(flags)
            exit()
  
def create_source_file_map(cspec):   
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
        permutation_results_dir = cspec.generate_results_dir_for_permutation(permutation_info['trials'], permutation_code) 
        from_file_path_with_results_dir_resolved = cspec.scores_from_filepath.replace('<permutation_results_dir>',permutation_results_dir)
        scores_permutations_list = permutations.expand_permutations(cspec.scores_permuters)
        for scores_permutations_info in scores_permutations_list:
            # first resolve the regular_permutations info in the scores_from_filepath
            list_of_one = [ from_file_path_with_results_dir_resolved ]
            revised_list_of_one = permutations.resolve_permutation(permutation_info, list_of_one, cspec.key_val_map)
            partially_resolved_from_filepath = revised_list_of_one[0]
            # now resolve the scores_permutation info in the scores_from_filepath
            list_of_one = [ partially_resolved_from_filepath ]
            revised_list_of_one = permutations.resolve_permutation(scores_permutations_info, list_of_one, cspec.key_val_map)
            fully_resolved_from_filepath = revised_list_of_one[0]
            #print "RESOLVED_LIST_OF_ONE: {0}".format(fully_resolved_from_filepath)
            # create the full perm code (includes the scores_permutations)
            master_permutation_info = {}
            for key, val in permutation_info.items():
                master_permutation_info[key] = val
            for key, val in scores_permutations_info.items():
                master_permutation_info[key] = val
                
            full_perm_code = permutations.generate_permutation_code(master_permutation_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
            source_file_map[full_perm_code] = fully_resolved_from_filepath
            #print "source_file_map[{0}] = {1}".format(full_perm_code, fully_resolved_from_filepath)
    return source_file_map


  
def usage():
    print "usage:  python permuter.py  gen|launch|auto|preview|test_launch|collect|stat <path of cluster_spec> [-v]"
    
if __name__ == '__main__':
    main()
    
