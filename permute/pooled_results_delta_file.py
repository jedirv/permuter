'''
Created on Dec 12, 2013

@author: admin-jed
'''

import os
import pooled_results_file

class PooledResultsDeltaFile(object):
    '''
    classdocs
    '''


    def __init__(self,resultsFile):
        '''
        Constructor
        '''
        self.resultsFile = resultsFile
        self.dirname = resultsFile.target_dir
        self.filename_code = resultsFile.perm_code_for_filename
        if (self.filename_code == ""):
            self.source_file_path = "{0}/pooled_results.csv".format(self.dirname)
            self.target_file_path = "{0}/pooled_results_deltas.csv".format(self.dirname)
        else:
            self.source_file_path = "{0}/pooled_results_{1}.csv".format(self.dirname, self.filename_code)
            self.target_file_path = "{0}/pooled_results_{1}_deltas.csv".format(self.dirname, self.filename_code)
        
    def generate(self):
        f_source = open(self.source_file_path,'r')
        f_target = open(self.target_file_path,'w')
        lines = f_source.readlines()
        f_target.write(lines[0])
        for i in range(1,len(lines)):
            delta_line = create_delta_line(lines[i].rstrip(os.linesep))
            f_target.write("{0}{1}".format(delta_line, os.linesep))
        f_source.close()
        f_target.close()
        
def create_delta_line(line):
    parts = line.split(',')
    result = "{0}".format(parts[0])

    index_first_float = get_index_first_float(parts,1)
    # if no numbers at all - this means all results are missing, the input line is all Xs, so just return it 
    if (-1 == index_first_float):
        return line
    
    # copy the missing values until we have a float
    for i in range(1,index_first_float):
        result = "{0},{1}".format(result,parts[i])
    
    # establish reference float
    first_val_with_float = parts[index_first_float]
    first_float = pooled_results_file.get_float_from_median_expression(first_val_with_float)
    X_count = first_val_with_float.count('x')
    result = "{0},0".format(result)
    for i in range(0, X_count):
        result = "{0}x".format(result)
    
    # 
    for i in range(index_first_float+1, len(parts)):
        median_expression = parts[i]
        if (pooled_results_file.median_expression_has_float(median_expression)):
            this_float = pooled_results_file.get_float_from_median_expression(median_expression)
            X_count = median_expression.count('x')
            cur_delta = this_float - first_float
            delta_string = "%.2f" % cur_delta
            for i in range(0, X_count):
                delta_string = "{0}x".format(delta_string) 
            result = "{0},{1}".format(result,delta_string)
        else:
            result = "{0},{1}".format(result,median_expression)
    result = result.rstrip(',')
    return result

def get_index_first_float(parts, starting_index):
    for i in range(starting_index, len(parts)):
        new_val = parts[i].replace('x','')
        if (len(new_val) != 0):
            return i
    return -1