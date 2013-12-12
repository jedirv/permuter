'''
Created on Nov 19, 2013

@author: admin-jed
'''
import sys, os, time
import cluster_spec
import permutations
import cluster_script
from monitor import pooled_results_file
from monitor import pooled_results_delta_file

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
    if (flags == "-v"):
        global verbose
        verbose = True
    if (permute_command == "gen"):
        generate(cspec)
    elif (permute_command == "launch"):
        launch(cspec)
    elif (permute_command == "auto"):
        generate(cspec)
        launch(cspec)
    elif (permute_command == "preview"):
        preview(cspec)
    elif (permute_command == "test_launch"):
        test_launch(cspec)
    elif (permute_command == "collect"):
        collect(cspec)
        
    else:
        pass
        
def if_verbose(message):
    global verbose
    if (verbose):
        print message
    
def collect(cspec):
    resultsFiles = create_pooled_results_files(cspec)
    create_pooled_results_delta_files(resultsFiles)
        
def generate(cspec):
    permuters_including_trials = cspec.get_permuters_trials_included()
    permute_dictionary_list = permutations.expand_permutations(permuters_including_trials)
    generate_scripts(cspec, permute_dictionary_list)
    
def launch(cspec):
    permuters_including_trials = cspec.get_permuters_trials_included()
    permute_dictionary_list = permutations.expand_permutations(permuters_including_trials)
    launch_scripts(cspec, permute_dictionary_list)
    
def preview(cspec):
    permuters_including_trials = cspec.get_permuters_trials_included()
    permute_dictionary_list = permutations.expand_permutations(permuters_including_trials)
    preview_scripts(cspec, permute_dictionary_list)
    
 
def create_pooled_results_delta_files(resultsFiles):
    for resultsFile in resultsFiles:
        deltaFile = pooled_results_delta_file.PooledResultsDeltaFile(resultsFile)
        deltaFile.generate()
    

    
def create_pooled_results_files(cspec):
    source_file_map = create_source_file_map(cspec)
    permuters_for_filename = pooled_results_file.gather_file_permuters(cspec)
    filename_permutations = permutations.expand_permutations(permuters_for_filename)
    resultsFiles = []
    for filename_permutation_info in filename_permutations:
        resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cspec)
        resultsFile.persist()
        resultsFiles.append(resultsFile)
    return resultsFiles
           
def test_launch(cspec):
    permuters_including_trials = cspec.get_permuters_trials_included()
    permute_dictionary_list = permutations.expand_permutations(permuters_including_trials)
    test_launch_single_script(cspec, permute_dictionary_list)

def launch_scripts(cspec, permute_dictionary_list):
    job_num_width = permutations.get_job_number_width(permute_dictionary_list)
    kvm = cspec.key_val_map
    user_job_number = 1
    if cspec.one_up_basis != '':
        user_job_number = int(cspec.one_up_basis)
    for permute_info in permute_dictionary_list:
        #permute_code = permutations.generate_permutation_code(permute_dict, cspec.concise_print_map)
        #commands_for_this_permutation = permutations.resolve_permutation(permute_dict, cspec.commands, kvm)
        user_job_number_as_string = str(user_job_number).zfill(job_num_width)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, kvm, permute_info, cspec, permute_info['trials'])
        cscript.launch()
        user_job_number = user_job_number + 1
        time.sleep(1.5)

    
def generate_scripts(cspec, permute_dictionary_list):
    print permute_dictionary_list
    job_num_width = permutations.get_job_number_width(permute_dictionary_list)
    print 'job_number_width {0}'.format(job_num_width)
    kvm = cspec.key_val_map
    user_job_number = 1
    if cspec.one_up_basis != '':
        user_job_number = int(cspec.one_up_basis)
    #for trial in range(1, int(cspec.trials) + 1):
    for permute_info in permute_dictionary_list:
        #permute_code = permutations.generate_permutation_code(permute_dict, cspec.concise_print_map)
        #commands_for_this_permutation = permutations.resolve_permutation(permute_dict, cspec.commands, kvm)
        user_job_number_as_string = str(user_job_number).zfill(job_num_width)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, kvm, permute_info, cspec, permute_info['trials'])
        cscript.generate()
        user_job_number = user_job_number + 1
       

def preview_scripts(cspec, permute_dictionary_list):
    job_num_width = permutations.get_job_number_width(permute_dictionary_list)
    if_verbose("preview mode")
    kvm = cspec.key_val_map
    user_job_number = 1
    if cspec.one_up_basis != '':
        user_job_number = int(cspec.one_up_basis)
    permute_info = permute_dictionary_list[0]
    #permute_code = permutations.generate_permutation_code(permute_dict, cspec.concise_print_map)
    #commands_for_this_permutation = permutations.resolve_permutation(permute_dict, cspec.commands, kvm)
    user_job_number_as_string = str(user_job_number).zfill(job_num_width)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, kvm, permute_info, cspec, permute_info['trials'])
    cscript.preview()


def test_launch_single_script(cspec, permute_dictionary_list):
    job_num_width = permutations.get_job_number_width(permute_dictionary_list)
    if_verbose("preview mode")
    kvm = cspec.key_val_map
    user_job_number = 1
    if cspec.one_up_basis != '':
        user_job_number = int(cspec.one_up_basis)
    permute_info = permute_dictionary_list[0]
    #permute_code = permutations.generate_permutation_code(permute_dict, cspec.concise_print_map)
    #commands_for_this_permutation = permutations.resolve_permutation(permute_dict, cspec.commands, kvm)
    user_job_number_as_string = str(user_job_number).zfill(job_num_width)
    cscript = cluster_script.ClusterScript(user_job_number_as_string, kvm, permute_info, cspec, permute_info['trials'])
    cscript.launch()
           
                  
 
def validate_args(permute_command, cspec_path, flags):
    if (not(permute_command == "collect" or 
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
    print "usage:  python permuter.py  gen|launch|auto|preview|test_launch|collect <path of cluster_spec> [-v]"
    
if __name__ == '__main__':
    main()
    
