import os
from permutation_driver_file import PermutationDriverFile
#from monitor import monitor_exception

class QsubInvokeLog(PermutationDriverFile):
    '''
    Wraps the cluster script file
    '''
    
    def configure(self):
        self.script_path_root = self.get_script_path_root()
        self.stdout_capture_filepath = "{0}_invoke.txt".format(self.script_path_root)
        self.pathname = "{0}.sh".format(self.script_path_root)
        self.script_name = "{0}.sh".format(self.get_job_file_name())
        self.cluster_job_number = self.load_job_number()
        self.type = "qsub_invoke_log"
        
    def load_job_number(self):
        starting_dir = os.getcwd()
        os.chdir(self.script_dir)
        #print "opening {0}".format(self.qsub_invoke_log)
        #print self.script_dir
        f = open(self.qsub_invoke_log, 'r')
        line = f.readline()
        f.close()
        #print "closed {0}".format(self.qsub_invoke_log)
        parts = line.split(' ')
        os.chdir(starting_dir)
        if (len(parts) != 7):
            #raise monitor_exception.MonitorException("qsub invoke log has incorrect number of fields {0}. Should look like 'Your job 4174438 (jobname) has been submitted'")
            raise Exception("qsub invoke log has incorrect number of fields {0}. Should look like 'Your job 4174438 (jobname) has been submitted'")
        result = parts[2]
        return result
        

 
    
        