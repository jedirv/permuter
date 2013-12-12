'''
Created on Dec 12, 2013

@author: admin-jed
'''

import os
from monitor_exception import MonitorException

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
        self.source_file_path = "{0}/{1}.csv".format(self.dirname, self.filename_code)
        self.target_file_path = "{0}/deltas_{1}.csv".format(self.dirname, self.filename_code)
        
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
    result = "{0},0,".format(parts[0])
    first_number = parts[1]
    first_num_float = float(first_number)
    for i in range(2,len(parts)):
        cur_num_float = float(parts[i])
        cur_delta = cur_num_float - first_num_float
        delta_string = "%.2f" % cur_delta
        result = "{0}{1},".format(result,delta_string)
    result = result.rstrip(',')
    return result