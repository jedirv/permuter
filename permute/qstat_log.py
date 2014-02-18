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
        return self.cluster_system.is_cluster_job_still_running(cluster_job_number, self.script_dir, self.qstat_log)
        
        

 
    
        