import os, sys
from permute import cluster_spec
from permute import cluster_script
from permute import permutations

def main():
    if (len(sys.argv) < 1):
        usage()
        exit()
    cspec_path = sys.argv[1]
    if (not(cluster_spec.validate(cspec_path))):
        exit()
    cspec = cluster_spec.ClusterSpec(cspec_path)
    
    permute_dictionary_list = permutations.expand_permutations(cspec.permuters)
    job_num_width = permutations.get_job_number_width(permute_dictionary_list)
    kvm = cspec.key_val_map
    user_job_number = 1
    cluster_scripts = []
    if cspec.one_up_basis != '':
        user_job_number = int(cspec.one_up_basis)
    for permute_dict in permute_dictionary_list:
        user_job_number_as_string = str(user_job_number).zfill(job_num_width)
        cscript = cluster_script.ClusterScript(user_job_number_as_string, kvm, permute_dict, cspec)
        cluster_scripts.append(cscript)
        user_job_number = user_job_number + 1
    
    
    count_total = 0
    count_present = 0
    for cscript in cluster_scripts:
        result_path = "{0}/score_out_userDay.csv".format(cscript.resolved_results_dir) 
        #print result_path
        count_total = count_total + 1
        if (os.path.isfile(result_path)):
            count_present = count_present + 1
            print "...{0}  DONE".format(cscript.permute_code)
        else:
            print "...{0} ".format(cscript.permute_code)
    print "{0} of {1} completed".format(count_present, count_total) 
    


def usage():
    print "usage:  python countDone.py <path of cluster_spec>"
if __name__ == '__main__':
    main()
    
