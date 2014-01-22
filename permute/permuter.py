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
    logging.shutdown()    
    
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
            

def check_status_of_runs(cluster_runs):
    logging.info('CHECKING status of runs')
    cspec = cluster_runs.cspec
    for permutation_info in cluster_runs.permutation_info_list_full:
        check_status_of_run(cluster_runs, permutation_info, cspec)
        
def check_status_of_run(cluster_runs, permutation_info, cspec):
    logging.debug('CHECKING status of run')
    permutation_code = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, True)
    results_dir = cluster_runs.get_results_dir_for_permutation_code(permutation_code)
    done_marker_file_path = "{0}/permutation_done_marker.txt".format(results_dir)
    #print "done_marker_file_path {0}".format(done_marker_file_path)
    run_finished = False
    if (os.path.isfile(done_marker_file_path)):
        run_finished=True
    
    missing_output_file = False
    missing_output_files = []
#    maybe the following line should pass in the results_dir
    list_of_output_files = permutations.get_list_of_output_files(permutation_info, cspec)
    for output_file_path in list_of_output_files:
        if (not(os.path.isfile(output_file_path))):
            missing_output_file = True
            missing_output_files.append(output_file_path)
            

    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_info(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    if (not(run_finished)):
        print "{0}\t{1}\tstill running".format(cluster_job_number, qil.get_job_file_name())
    elif (run_finished and not(missing_output_file)):
        #done
        print "{0}\t{1}\tcomplete".format(cluster_job_number, qil.get_job_file_name())
    else:
        #fun finished but missing an output file, find out the error
        qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
        qacctlog.ingest(cluster_job_number)
        print "{0} FAILED -> {1}".format(cluster_job_number, qacctlog.get_failure_reason())
        for missing_file in missing_output_files:
            print "output file missing: {0}".format(missing_file)
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
    for filename_permutation_info in filename_permutations:
        timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs)
        timingsFile.persist()


  
def create_ranked_results_files(cluster_runs):
    logging.info('CREATING ranked results file')
    permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
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
        print "An error occurred trying to open {0}".format(cspec_path)
        exit()
    if (flags != "-debug" and flags != ""):
        print "Invalid flag {0}. -debug is only flag supported".format(flags)
        exit()
  
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
    print "usage:  python permuter.py  gen|launch|auto|preview|test_launch|collect|stat <path of cluster_spec>  [-debug]"
    
if __name__ == '__main__':
    main()
    
