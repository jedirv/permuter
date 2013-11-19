import os
import subprocess


class ClusterScript(object):
    '''
    Wraps the cluster script file
    '''
    
    def __init__(self, user_job_number, key_val_map, permute_code, commands_for_this_permutation, qsub_commands):
        '''
        Constructor
        '''
        self.key_val_map = key_val_map
        self.permute_code = permute_code
        self.commands_for_this_permutation = commands_for_this_permutation
        self.qsub_commands = qsub_commands
        self.user_job_number = user_job_number
        self.script_path_root = self.get_script_path_root()
        self.pathname = "{0}.sh".format(self.script_path_root)

    def get_script_path_root(self):
        dir_script = self.key_val_map['dir_script']
        if (not(os.path.isdir(dir_script))):
            os.makedirs(dir_script)
        tag = ""
        pathname_root = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
            pathname_root = "{0}{1}j{2}_{3}{4}".format(dir_script, os.sep, self.user_job_number, self.permute_code, tag)
        else:
            pathname_root = "{0}{1}j{2}_{3}".format(dir_script, os.sep, self.user_job_number, self.permute_code)
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
            f.write("#$ -N j{0}_{1}{2}\n".format(self.user_job_number, self.permute_code, tag))
        else:
            f.write("#$ -N j{0}_{1}\n".format(self.user_job_number, self.permute_code))
            
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
    
    def launch(self):
        try: 
            print "calling qsub {0}".format(self.pathname)
            subprocess.check_call(["qsub", self.pathname])
        except subprocess.CalledProcessError:
            print "There was a problem invoking the script: {0}".format(self.pathname)
            print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
        
        
        