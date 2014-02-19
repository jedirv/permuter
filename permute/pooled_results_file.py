'''
Created on Nov 22, 2013

@author: admin-jed
'''
import qsub_invoke_log
import qacct_log
import permutations
import logging

class PooledResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,source_file_map, filename_permutation_info, cluster_runs, cluster_system):
        '''
        Constructor
        '''
        self.cluster_system = cluster_system
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = generate_target_dirname(self.cspec, self.cluster_system)
        self.perm_code_for_filename  = build_code_using_dictionary(filename_permutation_info, self.cspec)
        print "self.perm_code_for_filename : {0}".format(self.perm_code_for_filename)
        if (self.perm_code_for_filename == ""):
            self.target_path = "{0}/pooled_results.csv".format(self.target_dir)
        else:
            self.target_path = "{0}/pooled_results_{1}.csv".format(self.target_dir, self.perm_code_for_filename)
        self.source_file_map = source_file_map
        self.filename_permutation_info = filename_permutation_info
       
    def persist(self):
        cspec = self.cspec
        # generate the column names
        f = self.cluster_system.open_file(self.target_path, 'w')
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
        header = "{0},".format(beautify_header("{0}".format(cspec.scores_y_axis)))
        for x_permutation in x_permutations:
            concise_x_permutation = permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, False)
            header = "{0}{1},".format(header, concise_x_permutation)
        header = header.rstrip(',')
        f.write("{0}\n".format(header))
        medians = {}
        # make a list of x permutation codes for use later
        x_perm_codes = []
        for x_permutation in x_permutations:
            x_perm_codes.append(permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, False))
        # the main loop    
        for y_permutation in y_permutations:
            concise_y_permutation = permutations.generate_permutation_code(y_permutation, cspec.concise_print_map, False)
            line = "{0},".format(concise_y_permutation)
            for x_permutation in x_permutations:
                trials_list = cspec.get_trials_list()
                trial_values = []
                for trial in trials_list:
                    result_file_perm_code = gen_result_perm_code_from_pieces(y_permutation, x_permutation, self.filename_permutation_info, cspec, trial)
                    #print "self.source_file_map {0}".format(self.source_file_map)
                    source_file_path = self.source_file_map[result_file_perm_code]
                    #print "SOURCE_FILE_PATH : {0}".format(source_file_path)
                    value = get_result_from_file(source_file_path, cspec.scores_from_colname, cspec.scores_from_rownum, self.cluster_system)
                    trial_values.append(value)
                median_value = get_median(trial_values, False)
                line = "{0}{1},".format(line, median_value)
                x_perm_code = permutations.generate_permutation_code(x_permutation, cspec.concise_print_map, False)
                record_median(x_perm_code, medians, median_value)
            line = line.rstrip(',')
            f.write("{0}\n".format(line))
        # add the averages line
        line = "averages,"
        for x_perm_code in x_perm_codes:
            medians_list = medians[x_perm_code]
            average = compute_average_medians(medians_list, False)
            
            line = "{0}{1},".format(line,average)
        line = line.rstrip(',')
        f.write("{0}\n".format(line))
        f.close()

# convert this:  ['month', 'fv_type'] to this: month-fv_type
def beautify_header(header):
    header = header.replace("[","")
    header = header.replace("]","")
    header = header.replace("'","")
    header = header.replace(",","-")
    header = header.replace(" ", "")
    return header
# median_expression could look like 0.123, 0.123_X, 0.123_x_x, etc
def median_expression_has_float(median_expression):
    new_val = median_expression.replace('x','')
    if (new_val == ''):
        return False
    return True
    
# median_expression could look like 0.123, 0.123_X, 0.123_x_x, etc
def median_expression_has_Xs(median_expression):
    X_count = median_expression.count('x')
    if (X_count > 0):
        return True
    return False

def get_float_from_median_expression(median_expression):
    new_val = median_expression.replace('x','')
    return float(new_val)

def get_Xs_from_median_expression(median_expression):
    X_count = median_expression.count('x')
    result = ''
    for i in range(0, X_count):
        result = "{0}x".format(result)
    return result

def compute_average_medians(medians_list, as_integer):
    float_count = 0
    total_count = 0
    median_float_sum = 0.0
    x_all = ''
    for median in medians_list:
        total_count = total_count + 1
        if median_expression_has_float(median):
            median_float = get_float_from_median_expression(median)
            median_float_sum = median_float_sum + median_float
            float_count = float_count + 1
        if median_expression_has_Xs(median):
            x_portion = get_Xs_from_median_expression(median)
            x_all = '{0}{1}'.format(x_all, x_portion)
    result = ""
    if float_count > 0:
        average = median_float_sum / float_count
        if as_integer:
            average_int = int(average)
            result = "{0}{1}".format(result,average_int)
        else:
            average_rounded = "%.3f" % average
            result = "{0}{1}".format(result,average_rounded)
    result = "{0}{1}".format(result, x_all)
    return result
    
def record_median(x_perm_code, medians, median_value):
    if (not(medians.has_key(x_perm_code))):
        new_list = []
        new_list.append(median_value)
        medians[x_perm_code] = new_list
    else:
        medians[x_perm_code].append(median_value)
    
def get_median(string_series, as_integer):
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
    result_string = ''
    if as_integer:
        if (median == ''):
            pass
        else:
            result_string = '{0}'.format(int(median))
    else:
        result_string = '{0}'.format(median)
    for i in range(0,missing_count):
        result_string = '{0}x'.format(result_string)
    return result_string
        
def generate_target_dirname(cspec, cluster_system):
    dirname = "{0}/{1}".format(cspec.scores_to, cspec.master_job_name)
    if (not(cluster_system.isdir(dirname))):
        cluster_system.make_dirs(dirname)
    return dirname
    
def gen_result_perm_code_from_pieces(y_axis_permutation, x_axis_permutation, filename_perm_dict, cspec, trial):
    full_perm_dict = {}
    if (len(filename_perm_dict) != 0):
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
    
def get_result_from_file(source_file_path, colname, rownum, cluster_system):
    try:
        if (not(cluster_system.exists(source_file_path))):
            print 'MISSING {0}'.format(source_file_path)
            return 'missing'
        f = cluster_system.open_file(source_file_path, 'r')
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
        float_value = float(value)
        value_rounded = "%.3f" % float_value
        #print "value found for {0} is {1}".format(source_file_path, value)
        return value_rounded
    except Exception as detail:
        print "detail {0}".format(detail)
        raise Exception("Problem while reading results file : {0}".format(detail))

def gather_file_permuters(cspec):
    file_permuters = {}
    for key, val in cspec.permuters.items():
        logging.debug("......file_permuters[{0}] = {1}".format(key, val))
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
    logging.info("...file_permuters".format(file_permuters))
    return file_permuters

def build_code_using_dictionary(perm_info, cspec):
    result = ''
    if (len(perm_info) == 0):
        return ""
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
        