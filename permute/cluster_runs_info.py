'''
Created on Dec 17, 2013

@author: admin-jed
'''
import permutations
         
class ClusterRunsInfo(object):
    
    def __init__(self,cspec):
        self.cspec = cspec
        
        self.job_number_for_permutation_code_map = {}
        self.permutation_info_for_permutation_code_map = {}
        
        self.permuters_including_trials = cspec.get_permuters_trials_included()
        self.permute_info_list_full = permutations.expand_permutations(self.permuters_including_trials)
        self.job_num_width = self.get_job_number_width(self.permute_info_list_full)
        # associate job numbers here and lookup from then on
        user_job_number = 1
        if cspec.one_up_basis != '':
            user_job_number = int(cspec.one_up_basis)
        for permute_info in self.permute_info_list_full:
            permutation_code = permutations.generate_permutation_code(permute_info, cspec.concise_print_map, True)
            self.job_number_for_permutation_code_map[permutation_code] = get_formatted_user_job_number(user_job_number, self.job_num_width)
            self.permutation_info_for_permutation_code_map[permutation_code] = permute_info
            user_job_number = user_job_number + 1
            
            
        
    def get_job_number_width(self, permute_dictionary_list):
        highest_permutation_number = len(permute_dictionary_list)
        if self.cspec.one_up_basis != '':
            highest_permutation_number = int(self.cspec.one_up_basis) + highest_permutation_number
        permute_count_as_string = str(highest_permutation_number)
        permute_count_width = len(permute_count_as_string)
        return permute_count_width
    
    def get_job_number_string_for_permutation_code(self, permutation_code):
        result = self.job_number_for_permutation_code_map[permutation_code]
        return result
        

    def get_permutation_info_for_permutation_code(self, permutation_code):
        result = self.permutation_info_for_permutation_code_map[permutation_code]
        return result
def get_formatted_user_job_number(user_job_number, width):
    return str(user_job_number).zfill(width)