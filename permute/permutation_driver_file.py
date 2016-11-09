'''
Created on Dec 12, 2013

@author: admin-jed
'''
import permutations

class PermutationDriverFile(object):
    '''
    classdocs
    '''

    def __init__(self, user_job_number, permutation_info, cspec, trial, stdout):
        '''
        Constructor
        '''
        #self.cluster_system = cluster_system
        self.stdout = stdout
        self.cspec = cspec
        self.trial = trial
        self.permutation_info = permutation_info
        self.pcode = permutations.generate_permutation_code(permutation_info, cspec.concise_print_map, permutations.INCLUDE_TRIALS)
        self.key_val_map = {}
        for key, val in cspec.key_val_map.items():
            self.key_val_map[key] = val
        self.type = "permutation_driver_file"
        self.resolved_results_dir =  permutations.get_resolved_results_dir_for_permutation(permutation_info, cspec)
        #print "SETTING resolved_results_dir : {0}".format(self.resolved_results_dir)
        self.key_val_map['permutation_results_dir'] = self.resolved_results_dir
        self.user_job_number = user_job_number
        self.script_dir = cspec.script_dir
        self.qsub_invoke_log = "{0}.qil".format(self.get_job_file_name())
        self.qsub_invoke_log_fullpath = "{0}/{1}".format(self.script_dir,self.qsub_invoke_log)
        self.configure()
        
    # override this
    def configure(self):
        pass
       
    def get_job_file_name(self):
        tag = ""
        job_filename = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
            job_filename = "j{0}_{1}{2}".format(self.user_job_number, self.pcode, tag)
        else:
            job_filename = "j{0}_{1}".format(self.user_job_number, self.pcode)
        # replace any commas (like the ones in gmm args) with dashes
        job_filename = job_filename.replace(",","-")
        return job_filename   
      
    def get_script_path_root(self):
        job_filename = self.get_job_file_name()
        pathname_root = "{0}{1}{2}".format(self.script_dir, "/", job_filename)
        return pathname_root 
    
    