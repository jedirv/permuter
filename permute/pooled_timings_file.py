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
        header = "{0},".format(cspec.scores_y_axis)
    
        x_prefix = cspec.get_concise_name(cspec.scores_x_axis)
        print "cspec.scores_x_axis : {0}".format(cspec.scores_x_axis)
        print "cspec.permuters : {0}".format(cspec.permuters)
        for value in cspec.permuters[cspec.scores_x_axis]:
            header = "{0}{1}_{2},".format(header, x_prefix, value)
        header = header.rstrip(',')
        ft.write("{0}\n".format(header))
        # generate the values
        y_axis_list = cspec.permuters[cspec.scores_y_axis]
        for y_axis_val in y_axis_list:
            timings_line = "{0},".format(y_axis_val)
            x_axis_list = cspec.permuters[cspec.scores_x_axis]
            for x_axis_val in x_axis_list:
                trials_list = cspec.get_trials_list()
                trial_timing_values = []
                for trial in trials_list:
                    permutation_info = pooled_results_file.gen_perm_code_from_pieces(y_axis_val, x_axis_val, self.filename_perm_info, cspec, trial)
                    cluster_job_perm_code = permutations.generate_permutation_code(permutation_info,cspec.concise_print_map,True)
                    timing_value = get_timing_value_for_run(cluster_job_perm_code, y_axis_val, x_axis_val, self.cluster_runs, trial)
                    trial_timing_values.append(timing_value)
                median_timing = get_median_timing(trial_timing_values)
                timings_line = "{0}{1},".format(timings_line, median_timing)
            timings_line.rstrip(',')
            ft.write("{0}\n".format(timings_line))
        ft.close()
           
def get_median_timing(int_series):
    sorted_int_series = sorted(int_series)
    size = len(sorted_int_series)
    if (len(sorted_int_series)%2 == 0):
        #even number in list
        return (sorted_int_series[(size/2)-1]+sorted_int_series[size/2])/2.0
    else:
        #odd number in list
        return sorted_int_series[(size-1)/2]

def get_timing_value_for_run(perm_code, y_axis_val, x_axis_val, cluster_runs, trial): 
    user_job_number_as_string = cluster_runs.get_job_number_string_for_permutation_code(perm_code)
    permutation_info = cluster_runs.get_permutation_info_for_permutation_code(perm_code)
    qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trials'])
    cluster_job_number = qil.cluster_job_number
    qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cluster_runs.cspec, permutation_info['trials'])
    qacctlog.ingest(cluster_job_number)
    if (qacctlog.run_failed()):
        return "NOT_AVAILABLE"
    else:
        return qacctlog.cpu
    
   
def gather_file_permuters(cspec):
    file_permuters = {}
    for key, val in cspec.permuters.items():
        file_permuters[key] = val
    
    # remove the x and y ones
    x_axis_permuter = cspec.scores_x_axis
    y_axis_permuter = cspec.scores_y_axis
    if (x_axis_permuter != ''):
        del file_permuters[x_axis_permuter]
    if (y_axis_permuter != ''):
        del file_permuters[y_axis_permuter]
    return file_permuters
