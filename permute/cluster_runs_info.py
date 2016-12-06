'''
Created on Dec 17, 2013

@author: admin-jed
'''
import permutations
import logging
import cluster_script

class ClusterRunsInfo(object):
    
    def __init__(self,cspec, stdout):
        self.cspec = cspec
        
        self.job_number_for_perm_code_map = {}
        self.perm_code_for_job_number_map = {}
        self.cluster_script_for_perm_code_map = {}
        self.perm_info_for_perm_code_map = {}
        self.perm_code_for_perm_info_map = {}
        self.result_dir_for_perm_code_map = {}
        
        self.permuters_including_trials = cspec.get_permuters_trials_included()
        self.permutation_info_list_full = permutations.expand_permutations(self.permuters_including_trials)
        self.run_perm_codes_list = []
        self.job_num_width = self.get_job_number_width(self.permutation_info_list_full)
        
        # associate job numbers here and lookup from then on
        user_job_number = 1
        if cspec.one_up_basis != '':
            user_job_number = int(cspec.one_up_basis)
        for perm_info in self.permutation_info_list_full:
            perm_code = permutations.generate_perm_code(perm_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
            self.run_perm_codes_list.append(perm_code)
            
            user_job_number_as_string = get_formatted_user_job_number(user_job_number, self.job_num_width)
            self.job_number_for_perm_code_map[perm_code] = user_job_number_as_string
            self.perm_code_for_job_number_map[user_job_number_as_string] = perm_code
            self.perm_info_for_perm_code_map[perm_code] = perm_info
            perm_info_string = "{0}".format(perm_info)
            self.perm_code_for_perm_info_map[perm_info_string] = perm_code
            resolved_results_dir =  permutations.get_resolved_results_dir_for_permutation(perm_info, cspec)
            self.result_dir_for_perm_code_map[perm_code] = resolved_results_dir
            
            cscript = cluster_script.ClusterScript(user_job_number_as_string, perm_info, cspec, perm_info['trial'], stdout)
            self.cluster_script_for_perm_code_map[perm_code] = cscript
            user_job_number = user_job_number + 1
            
    def get_results_dirs_to_make(self):
        result = []
        for pcode in self.run_perm_codes_list:
            result.append(self.result_dir_for_perm_code_map[pcode])
        return result;
           
    def get_permutation_count(self): 
        count = len(self.permutation_info_list_full)
        return count    
                
    def get_results_dir_for_perm_code(self, pcode):
        result = self.result_dir_for_perm_code_map[pcode]
        return result
        
    def get_job_number_width(self, permutation_info_list):
        highest_permutation_number = len(permutation_info_list)
        if self.cspec.one_up_basis != '':
            highest_permutation_number = int(self.cspec.one_up_basis) + highest_permutation_number
        permute_count_as_string = str(highest_permutation_number)
        permute_count_width = len(permute_count_as_string)
        return permute_count_width
        
    def get_job_number_string_for_perm_code(self, pcode):
        #print 'START'
        #for key, val in self.job_number_for_permutation_code_map.items():
        #    print '{0} {1}'.format(key, val)
        #print 'END'
        result = self.job_number_for_perm_code_map[pcode]
        return result
        
        
    def get_job_number_string_for_permutation_info(self, perm_info):
        pcode = permutations.generate_perm_code(perm_info, self.cspec.concise_print_map, permutations.INCLUDE_TRIALS)
        result = self.job_number_for_perm_code_map[pcode]
        return result
        

    def get_permutation_info_for_perm_code(self, pcode):
        result = self.perm_info_for_perm_code_map[pcode]
        return result
    
    def get_first_script(self):
        return self.cluster_script_for_perm_code_map[self.run_perm_codes_list[0]]
    
    def get_script_for_perm_code(self, pcode):
        return self.cluster_script_for_perm_code_map[pcode]
    
    def get_donefile_path_for_perm_code(self,pcode):
        results_dir = self.get_results_dir_for_perm_code(pcode)
        done_file = cluster_script.get_done_marker_filename()
        done_marker_file_path = "{0}/{1}".format(results_dir, done_file)
        return done_marker_file_path
    
def get_formatted_user_job_number(user_job_number, width):
    return str(user_job_number).zfill(width)






def get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, scores_permutations_info):
    # first resolve the regular_permutations info in the scores_from_filepath
    list_of_one = [ from_file_path_with_results_dir_resolved ]
    revised_list_of_one = permutations.resolve_list_for_permutation(permutation_info, list_of_one, cspec.key_val_map)
    partially_resolved_from_filepath = revised_list_of_one[0]
    # now resolve the scores_permutation info in the scores_from_filepath
    list_of_one = [ partially_resolved_from_filepath ]
    revised_list_of_one = permutations.resolve_list_for_permutation(scores_permutations_info, list_of_one, cspec.key_val_map)
    fully_resolved_from_filepath = revised_list_of_one[0]
    return fully_resolved_from_filepath
    

def get_full_perm_code(permutation_info,scores_permutations_info, cspec):
    master_permutation_info = {}
    for key, val in permutation_info.items():
        master_permutation_info[key] = val
    if (len(scores_permutations_info) != 0):
        for key, val in scores_permutations_info.items():
            master_permutation_info[key] = val
    full_perm_code = permutations.generate_perm_code(master_permutation_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
    return full_perm_code
                
  
def create_source_file_map(cspec):
    logging.info('CREATING source file map')   
    source_file_map = {}
    #need to add trials in with cspec.permuters before expanding
    trials_list = cspec.get_trials_list() 
    permuters_with_trials = {}
    for key, val in cspec.permuters.items():
        permuters_with_trials[key] = val
    permuters_with_trials['trial'] = trials_list
    
    permutation_list = permutations.expand_permutations(permuters_with_trials)
    for permutation_info in permutation_list:
        pcode = permutations.generate_perm_code(permutation_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
        #print "permutation_code {0}".format(permutation_code)
        permutation_results_dir = cspec.generate_results_dir_for_permutation(pcode) 
        from_file_path_with_results_dir_resolved = cspec.scores_from_filepath.replace('<permutation_results_dir>',permutation_results_dir)
        #print "from_file_path_with_results_dir_resolved {0}".format(from_file_path_with_results_dir_resolved)
        scores_permutations_list = permutations.expand_permutations(cspec.scores_permuters)
        if (len(scores_permutations_list) == 0):
            fully_resolved_from_filepath = get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, {})
            full_perm_code = get_full_perm_code(permutation_info,{}, cspec)
            source_file_map[full_perm_code] = fully_resolved_from_filepath
        else:
            for scores_permutations_info in scores_permutations_list:
                fully_resolved_from_filepath = get_fully_resolved_from_filepath(from_file_path_with_results_dir_resolved, permutation_info, cspec, scores_permutations_info)
                full_perm_code = get_full_perm_code(permutation_info,scores_permutations_info, cspec)
                source_file_map[full_perm_code] = fully_resolved_from_filepath
                #print "source_file_map[{0}] = {1}".format(full_perm_code, fully_resolved_from_filepath)
    return source_file_map
