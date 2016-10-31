import getpass
import os
class QStatLog(object):
    '''
    Wraps the qstat result
    '''
    def __init__(self, script_dir):
        self.qstat_lines = []
        self.logpath = "{0}/{1}".format(script_dir,'qstat.txt')
       
    def delete(self):
        if os.path.exists(self.logpath):
            os.unlink(self.logpath)
            
    def ingest(self):
        f = open(self.logpath, 'r')
        lines = f.readlines()
        for line in lines:
            if (line.startswith('job-ID')):
                pass
            elif(line.startswith('--')):
                pass
            else:
                self.qstat_lines.append(line)
        f.close()
        
    def get_state_info(self, cluster_run_id):
        result = 'run_unknown_to_qstat'
        for line in self.qstat_lines:
            line = line.lstrip()
            if line.startswith(cluster_run_id):
                result = self.get_relevant_info_from_line(line)
        return result    
              
    def get_run_state_from_line(self,line):
        #   5809740 0.51766 tall_coars choiyun      r     10/18/2016 15:20:19 share2@compute-7-2r.hpc.engr.o       5
        parts = line.split(" ")
        state = parts[4]
        return state
    
    def is_running(self, cluster_run_id):
        line = self.get_state_info(cluster_run_id)
        run_state= self.get_run_state_from_line(line)
        if (run_state == "r"):
            return True
        return False
        
    def is_waiting(self, cluster_run_id):
        line = self.get_state_info(cluster_run_id)
        run_state= self.get_run_state_from_line(line)
        if (run_state == "w"):
            return True
        return False
    
    '''        
    def is_cluster_job_still_running(self, cluster_job_number):
        return self.cluster_system.is_cluster_job_still_running(cluster_job_number, self.script_dir, self.qstat_log)
    '''
        
        

 
    
        