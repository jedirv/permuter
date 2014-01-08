'''
Created on Nov 22, 2013

@author: admin-jed
'''
import os
import qsub_invoke_log
import qacct_log
import permutations

class PooledResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,source_file_map, filename_permutation_info, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = generate_target_dirname(self.cspec)
        self.perm_code_for_filename  = build_code_using_dictionary(filename_permutation_info, self.cspec)
        self.target_path = "{0}/{1}.csv".format(self.target_dir, self.perm_code_for_filename)
        self.source_file_map = source_file_map
        self.filename_permutation_info = filename_permutation_info
       
    def persist(self):
        cspec = self.cspec
        # generate the column names
        f = open(self.target_path, 'w')
        print "persisting {0}".format(self.target_path)
        
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
        f.write("{0}\n".format(header))
        
        for y_permutation in y_permutations:
            concise_y_permutation = permutations.generate_permutation_code(y_permutation, cspec.concise_print_map, False)
            line = "{0},".format(concise_y_permutation)
            for x_permutation in x_permutations:
                trials_list = cspec.get_trials_list()
                trial_values = []
                for trial in trials_list:
                    result_file_perm_code = gen_result_perm_code_from_pieces(y_permutation, x_permutation, self.filename_permutation_info, cspec, trial)
                    source_file_path = self.source_file_map[result_file_perm_code]
                    #print "SOURCE_FILE_PATH : {0}".format(source_file_path)
                    value = get_result_from_file(source_file_path, cspec.scores_from_colname, cspec.scores_from_rownum)
                    trial_values.append(value)
                median_value = get_median(trial_values)
                line = "{0}{1},".format(line, median_value)
            line = line.rstrip(',')
            f.write("{0}\n".format(line))
        f.close()
    
def get_median(string_series):
    missing_count = 0
    float_series = []
    for item in string_series:
        if (item=='missing'):
            missing_count = missing_count + 1
        else:
            float_series.append(float(item))
       
    sorted_float_series = sorted(float_series)
    size = len(sorted_float_series)
    median = ''
    if (size == 0):
        median = ''
    elif (size == 1):
        median = sorted_float_series[0]
    else:
        result = 0.0
        if (len(sorted_float_series)%2 == 0):
            #even number in list
            median = (sorted_float_series[(size/2)-1]+sorted_float_series[size/2])/2.0
        else:
            #odd number in list
            median = sorted_float_series[(size-1)/2]
    result_string = '{0}'.format(median)
    for i in range(0,missing_count):
        result_string = '{0}_X'.format(result_string)
    return result_string
        
def generate_target_dirname(cspec):
    dir = "{0}/{1}".format(cspec.scores_to, cspec.master_job_name)
    if (not(os.path.isdir(dir))):
        os.makedirs(dir)
    return dir
    
def gen_result_perm_code_from_pieces(y_axis_permutation, x_axis_permutation, filename_perm_dict, cspec, trial):
    full_perm_dict = {}
    for key, val in filename_perm_dict.items():
        full_perm_dict[key] = val
    # create a full perm_dict by adding the x and y vals back in
    for key, val in y_axis_permutation.items():
        full_perm_dict[key] = val
    for key, val in x_axis_permutation.items():
        full_perm_dict[key] = val
    full_perm_dict['trials'] = trial
    result = build_code_using_dictionary(full_perm_dict, cspec)
    return result
    
def get_result_from_file(source_file_path, colname, rownum):
    try:
        if (not(os.path.exists(source_file_path))):
            print 'MISSING {0}'.format(source_file_path)
            return 'missing'
        f = open(source_file_path, 'r')
        # determine columne number of colname
        lines = f.readlines()
        header = lines[0]
        header = header.rstrip()
        if (header == ""):
            raise Exception("missing header in results file")
        parts = header.split(',')
        index = parts.index(colname)
        value_line = lines[int(rownum)]
        value_line = value_line.rstrip()
        value_parts = value_line.split(',')
        value = value_parts[index]
        print "value found for {0} is {1}".format(source_file_path, value)
        return value
    except Exception as detail:
        print "detail {0}".format(detail)
        raise Exception("Problem while reading results file : {0}".format(detail))

def gather_file_permuters(cspec):
    file_permuters = {}
    for key, val in cspec.permuters.items():
        file_permuters[key] = val
    
    # combine permuters 
    for key, val in cspec.scores_permuters.items():
        file_permuters[key] = val
    # remove the x and y ones
    x_permuters = cspec.scores_x_axis
    y_permuters = cspec.scores_y_axis
    for x_permuter in x_permuters:
        del file_permuters[x_permuter]
    for y_permuter in y_permuters:
        del file_permuters[y_permuter]
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
        