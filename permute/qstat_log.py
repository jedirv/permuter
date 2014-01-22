import os
from permutation_driver_file import PermutationDriverFile

class QStatLog(PermutationDriverFile):
    '''
    Wraps the cluster script file
    '''
    
    def configure(self):
        self.script_path_root = self.get_script_path_root()
        self.pathname = "{0}.qstat".format(self.script_path_root)
        self.qstat_log = "{0}.qstat".format(self.get_job_file_name())
        self.type = "qstat_log"
        
    def is_cluster_job_still_running(self, cluster_job_number):
        if (cluster_job_number == "NA"):
            return False
        self.cluster_job_number = cluster_job_number
        starting_dir = os.getcwd()
        os.chdir(self.script_dir)
        #print "opening {0}".format(self.qstat_log)
        command = "qstat | grep {0} > {1}".format(cluster_job_number, self.qstat_log)
        os.system(command) 
        f = open(self.qstat_log, 'r')
        lines = f.readlines()
        result = False
        for line in lines:
            if (line.startswith(cluster_job_number)):
                result = True
        f.close()
        os.unlink(self.qstat_log)
        #print "closed {0}".format(self.qstat_log)
        os.chdir(starting_dir)
        return result
        

 
    
        