import os
import subprocess
import permutations
from permutation_driver_file import PermutationDriverFile

class ClusterScript(PermutationDriverFile):
    '''
    Wraps the cluster script file
    '''
        
    def configure(self):
        self.commands_for_this_permutation = permutations.resolve_list_for_permutation(self.permutation_info, self.cspec.commands, self.key_val_map)
        self.qsub_commands = self.cspec.qsub_commands
        self.script_path_root = self.get_script_path_root()
        self.stdout_capture_filepath = "{0}_invoke.txt".format(self.script_path_root)
        self.pathname = "{0}.sh".format(self.script_path_root)
        self.script_name = "{0}.sh".format(self.get_job_file_name())
       
    def delete(self): 
        os.unlink(self.pathname)
        
    def generate(self):
        if (not(os.path.isdir(self.script_dir))):
            os.makedirs(self.script_dir)
        self.stdout.println("generating script file: {0}".format(self.pathname))
        f = open(self.pathname, 'w')
        f.write("#!/bin/csh\n")
        f.write("#\n")
        f.write("#$ -cwd\n")
        for qsub_command in self.qsub_commands:
            f.write("#$ {0}\n".format(qsub_command))
        tag = ""
        if (self.key_val_map.has_key('tag')):
            tag = self.key_val_map['tag']
        if (tag != ""):
            f.write("#$ -N {0}-j{1}_{2}{3}\n".format(self.cspec.cspec_name, self.user_job_number, self.pcode, tag))
        else:
            f.write("#$ -N {0}-j{1}_{2}\n".format(self.cspec.cspec_name, self.user_job_number, self.pcode))
            
        f.write("#\n")
        
        f.write("# send stdout and stderror to this file\n")
        f.write("#$ -o {0}.out\n".format(self.get_job_file_name()))
        f.write("#$ -e {0}.err\n".format(self.get_job_file_name()))
        f.write("#\n")
        f.write("#see where the job is being run\n")
        f.write("hostname\n")
        for cur_command in self.commands_for_this_permutation:
            f.write("{0}\n".format(cur_command))
        done_file = get_done_marker_filename()
        f.write("touch {0}/{1}\n".format(self.resolved_results_dir, done_file))
        f.close()  
    
    def exists(self):
        if (os.path.exists(self.pathname)):
            return True
        return False      
    
    def get_last_modification_time(self):
        if (self.exists()):
            return os.path.getmtime(self.pathname)
        else:
            return 'NA'
        
    def preview(self):
        #self.pathname = "sample.sh"
        self.generate()
        f = open(self.pathname, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            self.stdout.println(line)
        f.close()
        os.unlink(self.pathname)
        
    def launch(self, cluster):
        try: 
            starting_dir = os.getcwd()
            os.chdir(self.script_dir)
            #args = "{0}.sh > {0}__invoke.txt".format(self.get_job_file_name())
            #args = "{0} > {1}".format(self.pathname, self.stdout_capture_filepath)
            #print "args : {0}".format(args)  
            command = "qsub {0} > {1}".format(self.script_name, self.qsub_invoke_log)
            cluster.execute_command(command) 
            #subprocess.check_call(["qsub", self.pathname, ">" , self.stdout_capture_filepath])
            #subprocess.check_call(["qsub", args])
            os.chdir(starting_dir)
            
        except subprocess.CalledProcessError:
            self.stdout.println("There was a problem invoking the script: {0}".format(self.pathname))
            self.stdout.println("Return code was {0}".format(subprocess.CalledProcessError.returncode))
        
def get_done_marker_filename():
    return "run_done_marker.txt"   
        