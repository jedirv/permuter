'''
Created on Nov 22, 2013

@author: admin-jed
'''
import os
from permute import cluster_spec
from monitor_exception import MonitorException

class PooledResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,source_file_map, filename_perm_info, cspec):
        '''
        Constructor
        '''
        self.target_path = generate_target_path(filename_perm_info,cspec)
        self.cspec = cspec
        self.source_file_map = source_file_map
        self.filename_perm_info = filename_perm_info
       
    def persist(self):
        cspec = self.cspec
        
        # generate the column names
        f = open(self.target_path, 'w')
        header = "{0},".format(cspec.scores_y_axis)
    
        x_prefix = cspec.get_concise_name(cspec.scores_x_axis)
        print "cspec.scores_x_axis : {0}".format(cspec.scores_x_axis)
        print "cspec.permuters : {0}".format(cspec.permuters)
        for value in cspec.permuters[cspec.scores_x_axis]:
            header = "{0}{1}_{2},".format(header, x_prefix, value)
        header = header.rstrip(',')
        f.write("{0}\n".format(header))
        
        # generate the values
        y_axis_list = cspec.permuters[cspec.scores_y_axis]
        for y_axis_val in y_axis_list:
            line = "{0},".format(y_axis_val)
            x_axis_list = cspec.permuters[cspec.scores_x_axis]
            for x_axis_val in x_axis_list:
                perm_code = gen_perm_code_from_pieces(y_axis_val, x_axis_val, self.filename_perm_info)
                source_file_path = self.source_file_map[perm_code]
                value = get_result_from_file(source_file_path, cspec.scores_from_colname, cspec.scores_from_rownum)
                line = "{0}{1},".format(line, value)
            line = line.rstrip(',')
            f.write("{0}\n".format(line))
        f.close()
        
def generate_target_path(filename_perm_info, cspec):
    filename = build_code_using_dictionary(filename_perm_info, cspec)
    path = "{0}/{1}.csv".format(cspec.scores_to, filename)
    return path
    
def gen_perm_code_from_pieces(y_axis_val, x_axis_val, filename_perm_dict, cspec):
    full_perm_dict = {}
    for key, val in filename_perm_dict.items():
        full_perm_dict[key] = val
    # get the x and y permuter keys
    x_axis_permute = cspec.scores_x_axis
    y_axis_permute = cspec.scores_y_axis
    # create a full perm_dict by adding the x and y back in
    full_perm_dict[x_axis_permute] = x_axis_val
    full_perm_dict[y_axis_permute] = y_axis_val
    #
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

def build_code_using_dictionary(perm_dict, cspec):
    result = ''
    # build a map using the coded keys
    # and a list of the keys
    coded_key_dict = {}
    coded_keys = []
    for key, val in perm_dict.items():
        coded_key = cspec.get_concise_name(key)
        coded_key_dict[coded_key] = val
        coded_keys.append(coded_key)
    # sort the coded keys and iterate through to create the name
    sorted_coded_keys = sorted(coded_keys)
    
    for key in sorted_coded_keys:
        val = coded_key_dict[key]
        result = "{0}{1}_{2}_".format(result, key, val)
    # strip off the right_most underscore
    result = result.rstrip('_')     
    return result 
        