'''
Created on Dec 12, 2013

@author: admin-jed
'''
import permutations
import os

class PermutationDriverFile(object):
    '''
    classdocs
    '''


    def __init__(self, user_job_number, permutation_info, cspec, trial):
        '''
        Constructor
        '''
        self.cspec = cspec
        self.trial = trial
        self.permutation_info = permutation_info
        self.permute_code = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, False)
        interim_results_dir = cspec.generate_results_dir_for_permutation(trial, self.permute_code) 
        list_of_size_1 = [interim_results_dir] 
        self.key_val_map = cspec.key_val_map
        self.resolved_results_dir =  permutations.resolve_permutation(permutation_info, list_of_size_1, self.key_val_map)[0]
        #print "resolved_results_dir : {0}".format(self.resolved_results_dir)
        self.key_val_map['permutation_results_dir'] = self.resolved_results_dir
        self.user_job_number = user_job_number
        self.script_dir = cspec.script_dir
        self.qsub_invoke_log = "{0}.qil".format(self.get_job_file_name())
        self.configure()
        
    # override this
    def configure(self):
        pass
       
    def get_job_file_name(self):
        tag = ""
        job_filename = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
            job_filename = "j{0}_{1}_{2}{3}".format(self.user_job_number, self.trial, self.permute_code, tag)
        else:
            job_filename = "j{0}_{1}_{2}".format(self.user_job_number, self.trial, self.permute_code)
        return job_filename   
      
    def get_script_path_root(self):
        if (not(os.path.isdir(self.script_dir))):
            os.makedirs(self.script_dir)
        job_filename = self.get_job_file_name()
        pathname_root = "{0}{1}{2}".format(self.script_dir, os.sep, job_filename)
        return pathname_root 
    
    