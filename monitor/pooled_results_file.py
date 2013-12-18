'''
Created on Nov 22, 2013

@author: admin-jed
'''
import os
from monitor_exception import MonitorException
from permute import qsub_invoke_log
from permute import qacct_log

class PooledResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,source_file_map, filename_perm_info, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = generate_target_dirname(self.cspec)
        self.perm_code_for_filename  = build_code_using_dictionary(filename_perm_info, self.cspec)
        self.target_path = "{0}/{1}.csv".format(self.target_dir, self.perm_code_for_filename)
        self.target_timings_path = "{0}/{1}_timings.csv".format(self.target_dir, self.perm_code_for_filename)
        self.source_file_map = source_file_map
        self.filename_perm_info = filename_perm_info
       
    def persist(self):
        cspec = self.cspec
        
        # generate the column names
        f = open(self.target_path, 'w')
        ft = open(self.target_timings_path, 'w')
        header = "{0},".format(cspec.scores_y_axis)
    
        x_prefix = cspec.get_concise_name(cspec.scores_x_axis)
        print "cspec.scores_x_axis : {0}".format(cspec.scores_x_axis)
        print "cspec.permuters : {0}".format(cspec.permuters)
        for value in cspec.permuters[cspec.scores_x_axis]:
            header = "{0}{1}_{2},".format(header, x_prefix, value)
        header = header.rstrip(',')
        f.write("{0}\n".format(header))
        ft.write("{0}\n".format(header))
        # generate the values
        y_axis_list = cspec.permuters[cspec.scores_y_axis]
        for y_axis_val in y_axis_list:
            line = "{0},".format(y_axis_val)
            timings_line = "{0},".format(y_axis_val)
            x_axis_list = cspec.permuters[cspec.scores_x_axis]
            for x_axis_val in x_axis_list:
                trials_list = cspec.get_trials_list()
                trial_values = []
                trial_timing_values = []
                for trial in trials_list:
                    perm_code = gen_perm_code_from_pieces(y_axis_val, x_axis_val, self.filename_perm_info, cspec, trial)
                    source_file_path = self.source_file_map[perm_code]
                    #print "SOURCE_FILE_PATH : {0}".format(source_file_path)
                    value = get_result_from_file(source_file_path, cspec.scores_from_colname, cspec.scores_from_rownum)
                    
                    timing_value = get_timing_value_for_run(perm_code, y_axis_val, x_axis_val, self.cluster_runs, trial)
                    trial_values.append(float(value))
                    trial_timing_values.append(timing_value)
                median_value = get_median(trial_values)
                median_timing = get_median_timing(trial_timing_values)
                line = "{0}{1},".format(line, median_value)
                timings_line = "{0}{1},".format(line, median_timing)
            line = line.rstrip(',')
            timings_line.rstrip(',')
            f.write("{0}\n".format(line))
            ft.write("{0}\n".format(timings_line))
        f.close()
        ft.close()
           
def get_median_timing(timings):
    pass

def get_timing_value_for_run(perm_code, y_axis_val, x_axis_val, cluster_runs, trial): 
    #(user_job_number, job_num_width, permute_info
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
    
    
def get_median(float_series):
    sorted_float_series = sorted(float_series)
    size = len(sorted_float_series)
    if (len(sorted_float_series)%2 == 0):
        #even number in list
        return (sorted_float_series[(size/2)-1]+sorted_float_series[size/2])/2.0
    else:
        #odd number in list
        return sorted_float_series[(size-1)/2]
        
def generate_target_dirname(cspec):
    dir = "{0}/{1}".format(cspec.scores_to, cspec.master_job_name)
    if (not(os.path.isdir(dir))):
        os.makedirs(dir)
    return dir
    
def gen_perm_code_from_pieces(y_axis_val, x_axis_val, filename_perm_dict, cspec, trial):
    full_perm_dict = {}
    for key, val in filename_perm_dict.items():
        full_perm_dict[key] = val
    # get the x and y permuter keys
    x_axis_permute = cspec.scores_x_axis
    y_axis_permute = cspec.scores_y_axis
    # create a full perm_dict by adding the x and y back in
    full_perm_dict[x_axis_permute] = x_axis_val
    full_perm_dict[y_axis_permute] = y_axis_val
    full_perm_dict['trials'] = trial
    result = build_code_using_dictionary(full_perm_dict, cspec)
    return result
    
def get_result_from_file(source_file_path, colname, rownum):
    try:
        f = open(source_file_path, 'r')
        # determine columne number of colname
        lines = f.readlines()
        header = lines[0]
        header = header.rstrip()
        if (header == ""):
            raise MonitorException("missing header in results file")
        parts = header.split(',')
        index = parts.index(colname)
        value_line = lines[int(rownum)]
        value_line = value_line.rstrip()
        value_parts = value_line.split(',')
        value = value_parts[index]
        return value
    except Exception as detail:
        print "detail {0}".format(detail)
        raise MonitorException("Problem while reading results file : {0}".format(detail))

def gather_file_permuters(cspec):
    file_permuters = {}
    for key, val in cspec.permuters.items():
        file_permuters[key] = val
    
    # combine permuters 
    for key, val in cspec.scores_permuters.items():
        file_permuters[key] = val
    # remove the x and y ones
    x_axis_permuter = cspec.scores_x_axis
    y_axis_permuter = cspec.scores_y_axis
    if (x_axis_permuter != ''):
        del file_permuters[x_axis_permuter]
    if (y_axis_permuter != ''):
        del file_permuters[y_axis_permuter]
    return file_permuters

def build_code_using_dictionary(perm_info, cspec):
    result = ''
    # build a map using the coded keys
    # and a list of the keys
    coded_key_info = {}
    coded_keys = []
    for key, val in perm_info.items():
        coded_key = cspec.get_concise_name(key)
        #print "coded key for {0} is {1}".format(key, coded_key)
        coded_val = cspec.get_concise_name(val)
        coded_key_info[coded_key] = coded_val
        coded_keys.append(coded_key)
    # sort the coded keys and iterate through to create the name
    sorted_coded_keys = sorted(coded_keys)
    
    for key in sorted_coded_keys:
        val = coded_key_info[key]
        result = "{0}{1}_{2}_".format(result, key, val)
    # strip off the right_most underscore
    result = result.rstrip('_')     
    return result 
        