'''
Created on Nov 19, 2013

@author: admin-jed
'''
import sys, os, time
import cluster_spec
import permutations
import cluster_script

verbose = False

def main():
    if (len(sys.argv) < 3):
        usage()
        exit()
    permute_command = sys.argv[2]
    cspec_path = sys.argv[1]
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
    else:
        pass
        
def if_verbose(message):
    global verbose
    if (verbose):
        print message
    
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
    if (not(permute_command == "gen" or permute_command == "launch" or permute_command == "auto" or permute_command == "preview" or permute_command == "test_launch")):
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
    
def usage():
    print "usage:  python permuter.py <path of cluster_spec> gen|launch|auto|preview|test_launch [-v]"
    
if __name__ == '__main__':
    main()
    
