import os
import subprocess
import permutations

class ClusterScript(object):
    '''
    Wraps the cluster script file
    '''
    
    def __init__(self, user_job_number, key_val_map, permute_dict, cspec, trial):
        '''
        Constructor
        '''
        self.trial = trial
        self.permute_code = permutations.generate_permutation_code(permute_dict, cspec.concise_print_map, False)
        interim_results_dir = cspec.generate_results_dir_for_permutation(trial, self.permute_code) 
        list_of_size_1 = [interim_results_dir] 
        self.resolved_results_dir =  permutations.resolve_permutation(permute_dict, list_of_size_1, key_val_map)[0]
        #print "resolved_results_dir : {0}".format(self.resolved_results_dir)
        self.key_val_map = key_val_map
        self.key_val_map['permutation_results_dir'] = self.resolved_results_dir
        self.commands_for_this_permutation = permutations.resolve_permutation(permute_dict, cspec.commands, self.key_val_map)
        
        
        #commands_for_this_permutation = self.late_resolve_results_dir(commands_for_this_permutation, resolved_results_dir)
       
        self.qsub_commands = cspec.qsub_commands
        self.user_job_number = user_job_number
        self.script_dir = cspec.script_dir
        self.script_path_root = self.get_script_path_root()
        self.pathname = "{0}.sh".format(self.script_path_root)

            
    def get_script_path_root(self):
        if (not(os.path.isdir(self.script_dir))):
            os.makedirs(self.script_dir)
        tag = ""
        pathname_root = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
            pathname_root = "{0}{1}j{2}_{3}_{4}{5}".format(self.script_dir, os.sep, self.user_job_number, self.trial, self.permute_code, tag)
        else:
            pathname_root = "{0}{1}j{2}_{3}_{4}".format(self.script_dir, os.sep, self.user_job_number, self.trial, self.permute_code)
        return pathname_root
    
    def generate(self):
        print "  pathname of script file: {0}".format(self.pathname)
        f = open(self.pathname, 'w')
        f.write("#!/bin/csh\n")
        f.write("#\n")
        for qsub_command in self.qsub_commands:
            f.write("#$ {0}\n".format(qsub_command))
        tag = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
        if (tag != ""):
            f.write("#$ -N j{0}_{1}_{2}{3}\n".format(self.user_job_number, self.permute_code, self.trial, tag))
        else:
            f.write("#$ -N j{0}_{1}_{2}\n".format(self.user_job_number, self.permute_code, self.trial))
            
        f.write("#\n")
        
        f.write("# send stdout and stderror to this file\n")
        f.write("#$ -o {0}.out\n".format(self.script_path_root))
        f.write("#$ -e {0}.err\n".format(self.script_path_root))
        f.write("#\n")
        f.write("#see where the job is being run\n")
        f.write("hostname\n")
        for cur_command in self.commands_for_this_permutation:
            f.write("{0}\n".format(cur_command))
        f.close()  
    
    def preview(self):
        self.pathname = "junk.sh"
        self.generate()
        f = open(self.pathname, 'r')
        lines = f.readlines()
        for line in lines:
            print(line)
        f.close()
        os.remove(self.pathname)
        
    def launch(self):
        try: 
            print "calling qsub {0}".format(self.pathname)
            subprocess.check_call(["qsub", self.pathname])
        except subprocess.CalledProcessError:
            print "There was a problem invoking the script: {0}".format(self.pathname)
            print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
        
        
        