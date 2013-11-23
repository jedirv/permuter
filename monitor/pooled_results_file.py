'''
Created on Nov 22, 2013

@author: admin-jed
'''
from permute import cluster_spec

class PooledResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,source_file_map, perm_dict, cspec):
        '''
        Constructor
        '''
        self.target_path = self.generate_target_path(cspec)
        self.cspec = cspec
        self.source_file_map = source_file_map
        self.perm_dict = perm_dict
        
        y_axis_list = cspec.permuters[cspec.scores_y_axis]
        for y_axis_val in y_axis_list:
            x_axis_list = cspec.permuters[cspec.scores_x_axis]
            for x_axis_val in x_axis_list:
                perm_code = gen_perm_code_from_pieces(y_axis_val, x_axis_val, )
                source_file_path = source_file_map[perm_code]
                get_result_from_file(source_file_path, cspec.scores_from_colname, cspec.scores_from_rownum)
    
    
def generate_target_path(cspec):
    result = ""
        
    return result
    
    def gen_perm_code_from_pieces(self, y_axis_val, x_axis_val):
        result = ""
        
        return result