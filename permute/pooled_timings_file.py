import qsub_invoke_log
import qacct_log
import pooled_results_file
import permutations

class PooledTimingsFile(object):
    '''
    classdocs
    '''
    def __init__(self,filename_permutation_info, cluster_runs, stdout):
        '''
        Constructor
        '''
        self.stdout = stdout
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = pooled_results_file.generate_target_dirname(self.cspec)
        self.perm_code_for_filename  = pooled_results_file.build_code_using_dictionary(filename_permutation_info, self.cspec)
        if (self.perm_code_for_filename == ""):
            self.target_timings_path = "{0}/pooled_results_timings.csv".format(self.target_dir)
        else:
            self.target_timings_path = "{0}/pooled_results_{1}_timings.csv".format(self.target_dir, self.perm_code_for_filename)
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
        
        # make a list of x permutation codes for use later
        x_perm_codes = []
        for x_permutation in x_permutations:
            x_perm_codes.append(permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, permutations.IGNORE_TRIALS))
        medians = {}    
        # write the x_axis column names
        header = "{0},".format(pooled_results_file.beautify_header("{0}".format(cspec.scores_y_axis)))
        for x_permutation in x_permutations:
            concise_x_permutation = permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, permutations.IGNORE_TRIALS)
            header = "{0}{1},".format(header, concise_x_permutation)
        header = header.rstrip(',')
        ft.write("{0}\n".format(header))
        
        for y_permutation in y_permutations:
            concise_y_permutation = permutations.generate_permutation_code(y_permutation, cspec.concise_print_map, permutations.IGNORE_TRIALS)
            timings_line = "{0},".format(concise_y_permutation)
            for x_permutation in x_permutations:
                trials_list = cspec.get_trials_list()
                trial_timing_values = []
                for trial in trials_list:
                    cluster_job_perm_code = gen_cluster_job_perm_code_from_pieces(y_permutation, x_permutation, self.filename_permutation_info, cspec, trial)
                    timing_value = get_timing_value_for_run(cluster_job_perm_code,self.cluster_runs, self.stdout)
                    #print 'timing_value : {0}'.format(timing_value)
                    trial_timing_values.append(timing_value)
                median_timing = pooled_results_file.get_median(trial_timing_values, True)
                #print 'median_timing {0}'.format(median_timing)
                timings_line = "{0}{1},".format(timings_line, median_timing)
                x_perm_code = permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, permutations.IGNORE_TRIALS)
                pooled_results_file.record_median(x_perm_code, medians, median_timing)
            timings_line.rstrip(',')
            ft.write("{0}\n".format(timings_line))
        # add the averages line
        line = "averages,"    
        for x_perm_code in x_perm_codes:
            medians_list = medians[x_perm_code]
            average = pooled_results_file.compute_average_medians(medians_list, True)
            
            line = "{0}{1},".format(line,average)
        line = line.rstrip(',')
        ft.write("{0}\n".format(line))
        
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
    full_perm_dict['trial'] = trial
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

def get_timing_value_for_run(perm_code, cluster_runs, stdout): 
    user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(perm_code)
    #print "user_job_number_as_string {0}".format(user_job_number_as_string)
    permutation_info = cluster_runs.get_permutation_info_for_permutation_code(perm_code)
    #print "permutation_info {0}".format(permutation_info)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trial'], stdout)
    cluster_job_number = qil.cluster_job_number
    if (cluster_job_number == "NA"):
        return "missing"
    else:
        #print  "cluster_job_number {0}".format(cluster_job_number)
        qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trial'], stdout)
        qacctlog.ingest(cluster_job_number)
        if (qacctlog.run_failed()):
            return "missing"
        else:
            #print  "qacctlog.cpu {0}".format(qacctlog.cpu)
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
