import os
from permutation_driver_file import PermutationDriverFile
from monitor import monitor_exception

class QacctLog(PermutationDriverFile):
    '''
    Wraps the cluster script file
    '''
    
    def configure(self):
        self.script_path_root = self.get_script_path_root()
        self.pathname = "{0}.qacct".format(self.script_path_root)
        self.qacct_log = "{0}.qacct".format(self.get_job_file_name())
 
        self.cpu = "?"
        self.mem = "?"
        self.maxvmem = "?"
        self.hostname = "?"
        self.owner = "?"
        self.jobname = "?"
        self.qsub_time = "?"
        self.start_time = "?"
        self.end_time = "?"
        self.failed = "?"
        self.exit_status = "?"
        self.io = "?"
        
        self.error_reading = False
        
      
    def run_failed(self):
        return self.error_reading or self.failed != '0'
    
    def get_failure_reason(self):
        if (self.error_reading):
            return "qacct command failed"
        elif (self.failed != '0'):
            return "runtime error"
        else:
            return "no failure detected"
        
    def create_log(self, cluster_job_number):
        #print "opening {0}".format(self.qstat_log)
        command = "qacct -j {0} > {1}".format(cluster_job_number, self.qacct_log)
        os.system(command) 
        
    def ingest(self, cluster_job_number):
        starting_dir = os.getcwd()
        os.chdir(self.script_dir)
        self.cluster_job_number = cluster_job_number

        if (os.path.isfile(self.qacct_log)):
            #print "file exists"
            self.load_qacct_log()
            if (self.error_reading):
                # pre-existing log was corrupted, try again
                print "pre-existing log for {0} was corrupted, try again".format(cluster_job_number)
                self.create_log(self.cluster_job_number)
                self.load_qacct_log()
                #print "done reloading"
        else:    
            self.create_log(self.cluster_job_number)
            
            
        
        
        os.chdir(starting_dir)
        #os.unlink(self.qstat_log)
        #print "closed {0}".format(self.qstat_log)
        
    def load_qacct_log(self):
        self.error_reading = False
        f = open(self.qacct_log, 'r')
        lines = f.readlines()
        for line in lines:
            line = ' '.join(line.split())
            parts = line.split(' ')
            if (parts[0] == 'cpu'):
                self.cpu = parts[1]
            elif (parts[0] == 'mem'):
                self.mem = parts[1]
            elif (parts[0] == 'maxvmem'):
                self.maxvmem = parts[1]
            elif (parts[0] == 'hostname'):
                self.hostname = parts[1]
            elif (parts[0] == 'owner'):
                self.owner = parts[1]
            elif (parts[0] == 'jobname'):
                self.jobname = parts[1]
            elif (parts[0] == 'qsub_time'):
                self.qsub_time = parts[1]
            elif (parts[0] == 'start_time'):
                self.start_time = "{0} {1} {2} {3} {4}".format(parts[1], parts[2], parts[3], parts[4], parts[5])
            elif (parts[0] == 'end_time'):
                self.end_time = "{0} {1} {2} {3} {4}".format(parts[1], parts[2], parts[3], parts[4], parts[5])
            elif (parts[0] == 'failed'):
                self.failed = parts[1]
            elif (parts[0] == 'exit_status'):
                self.exit_status = parts[1]
            elif (parts[0] == 'io'):
                self.io = parts[1]
            
        if (self.cpu == '?' or self.maxvmem == '?'):
            self.error_reading = True
            #print "{0} CANNOT LOAD".format(self.cluster_job_number)
        #else:
        #    print "{0} cpu : {1}".format(self.cluster_job_number,self.cpu)   
        #    print "{0} maxvmem : {1}".format(self.cluster_job_number,self.maxvmem)   
        #    print "{0} start_time : {1}".format(self.cluster_job_number,self.start_time)   
        #    print "{0} end_time : {1}".format(self.cluster_job_number,self.end_time)   
        f.close()

 

        