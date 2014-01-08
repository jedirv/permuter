import qsub_invoke_log
import qacct_log
import pooled_results_file
import permutations

class PooledTimingsFile(object):
    '''
    classdocs
    '''
    def __init__(self,filename_permutation_info, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = pooled_results_file.generate_target_dirname(self.cspec)
        self.perm_code_for_filename  = pooled_results_file.build_code_using_dictionary(filename_permutation_info, self.cspec)
        self.target_timings_path = "{0}/{1}_timings.csv".format(self.target_dir, self.perm_code_for_filename)
        self.filename_permutation_info = filename_permutation_info
       
    def persist(self):
        cspec = self.cspec
        # generate the column names
        ft = open(self.target_timings_path, 'w')
        print "persisting {0}".format(self.target_timings_path)
        
        # scores_y_axis:letter
        # scores_x_axis:number,animal
        x_permuters = {}
        y_permuters = {}
        for item in cspec.scores_x_axis:
            x_permuters[item] = cspec.permuters[item]
        for item in cspec.scores_y_axis:
            y_permuters[item] = cspec.permuters[item]
        x_permutations = permutations.expand_permutations(x_permuters)
        y_permutations = permutations.expand_permutations(y_permuters)
        
        # write the x_axis column names
        header = "{0},".format(cspec.scores_y_axis)
        for x_permutation in x_permutations:
            concise_x_permutation = permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, False)
            header = "{0}{1},".format(header, concise_x_permutation)
        header = header.rstrip(',')
        ft.write("{0}\n".format(header))
        
        for y_permutation in y_permutations:
            concise_y_permutation = permutations.generate_permutation_code(y_permutation, cspec.concise_print_map, False)
            timings_line = "{0},".format(concise_y_permutation)
            for x_permutation in x_permutations:
                trials_list = cspec.get_trials_list()
                trial_timing_values = []
                for trial in trials_list:
                    cluster_job_perm_code = gen_cluster_job_perm_code_from_pieces(y_permutation, x_permutation, self.filename_permutation_info, cspec, trial)
                    
                    #permutation_info = pooled_results_file.gen_perm_code_from_pieces(y_axis_val, x_axis_val, self.filename_permutation_info, cspec, trial)
                    #cluster_job_perm_code = permutations.generate_permutation_code(permutation_info_with_trial,cspec.concise_print_map,True)
                    print "cluster_job_perm_code {0}".format(cluster_job_perm_code)
                    timing_value = get_timing_value_for_run(cluster_job_perm_code,self.cluster_runs)
                    trial_timing_values.append(timing_value)
                median_timing = pooled_results_file.get_median(trial_timing_values)
                print 'median_timing {0}'.format(median_timing)
                timings_line = "{0}{1},".format(timings_line, median_timing)
            timings_line.rstrip(',')
            ft.write("{0}\n".format(timings_line))
        ft.close()


def gen_cluster_job_perm_code_from_pieces(y_axis_permutation, x_axis_permutation, filename_perm_dict, cspec, trial):
    full_perm_dict = {}
    for key, val in filename_perm_dict.items():
        full_perm_dict[key] = val
    # create a full perm_dict by adding the x and y vals back in
    for key, val in y_axis_permutation.items():
        full_perm_dict[key] = val
    for key, val in x_axis_permutation.items():
        full_perm_dict[key] = val
    full_perm_dict['trials'] = trial
    # remove the scores_permute entries
    for key, vals in cspec.scores_permuters.items():
        if full_perm_dict.has_key(key):
            full_perm_dict.pop(key, None)
    result = pooled_results_file.build_code_using_dictionary(full_perm_dict, cspec)
    return result
           
#def get_median_timing(int_series):
#    sorted_int_series = sorted(int_series)
#    size = len(sorted_int_series)
#    if (len(sorted_int_series)%2 == 0):
        #even number in list
#        return (sorted_int_series[(size/2)-1]+sorted_int_series[size/2])/2.0
#    else:
        #odd number in list
#        return sorted_int_series[(size-1)/2]

def get_timing_value_for_run(perm_code, cluster_runs): 
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_code(perm_code)
    print "user_job_number_as_string {0}".format(user_job_number_as_string)
    permutation_info = cluster_runs.get_permutation_info_for_permutation_code(perm_code)
    print "permutation_info {0}".format(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    print  "cluster_job_number {0}".format(cluster_job_number)
    qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trials'])
    qacctlog.ingest(cluster_job_number)
    if (qacctlog.run_failed()):
        return "X"
    else:
        print  "qacctlog.cpu {0}".format(qacctlog.cpu)
        return qacctlog.cpu
    
   
def gather_file_permuters(cspec):
    return pooled_results_file.gather_file_permuters(cspec)
    #print "gather file permuters..."
    #file_permuters = {}
    #for key, val in cspec.permuters.items():
    #    print "adding key {0} val {1}".format(key, val)
    #    file_permuters[key] = val
    
    # remove the x and y ones
    #x_axis_permuters = cspec.scores_x_axis
    #y_axis_permuters = cspec.scores_y_axis
    #if (x_axis_permuters != ''):
    #    for item in x_axis_permuters:
    #        del file_permuters[item]
    #if (y_axis_permuters != ''):
    #    for item in y_axis_permuters:
    #        del file_permuters[item]
    #return file_permuters
