from permutation_driver_file import PermutationDriverFile
import logging
#from monitor import monitor_exception

class QacctLog(PermutationDriverFile):
    '''
    Wraps the cluster script file
    '''
    
    def configure(self):
        self.script_path_root = self.get_script_path_root()
        self.pathname = "{0}.qacct".format(self.script_path_root)
        self.qacct_log = "{0}.qacct".format(self.get_job_file_name())
        self.type = "qacct_log"
        self.cpu = "missing"
        self.mem = "missing"
        self.maxvmem = "missing"
        self.hostname = "missing"
        self.owner = "missing"
        self.jobname = "missing"
        self.qsub_time = "missing"
        self.start_time = "missing"
        self.end_time = "missing"
        self.failed = "missing"
        self.exit_status = "missing"
        self.io = "missing"
        
        self.error_reading = False
        
      
    def run_failed(self):
        result = self.error_reading or (self.failed != '0'  and self.failed != "?")
        #print "{0} run failed: {1}".format(self.script_path_root, result)
        #print "self.error_reading {0}".format(self.error_reading)
        #print "self.failed {0}".format(self.failed)
        return result
    
    def get_failure_reason(self):
        if (self.error_reading):
            return "qacct command failed"
        elif (self.failed != '0'):
            return "runtime error"
        else:
            return "no failure detected"
        
    def create_log(self, cluster_job_number):
        if (cluster_job_number == "NA"):
            print "skipping qacct, job not started yet"
        else:
            #print "opening {0}".format(self.qstat_log)
            command = "qacct -j {0} > {1}".format(cluster_job_number, self.qacct_log)
            self.cluster_system.execute_command(command) 
        
    def ingest(self, cluster_job_number):
        if (cluster_job_number == "NA"):
            error = "qacct_log cannot ingest job number 'NA'"
            logging.error(error)
            print error
        else:
            starting_dir = self.cluster_system.getcwd()
            self.cluster_system.chdir(self.script_dir)
            self.cluster_job_number = cluster_job_number

            if (self.cluster_system.isfile(self.qacct_log) and has_content(self.qacct_log, self.cluster_system)):
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
            
            
        
        
        self.cluster_system.chdir(starting_dir)
        #os.unlink(self.qstat_log)
        #print "closed {0}".format(self.qstat_log)
    
    def load_qacct_log(self):
        self.error_reading = False
        f = self.cluster_system.open_file(self.qacct_log,'r')
        lines = f.readlines()
        f.close()
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
                if (parts[1] == '-/-'):
                    self.start_time = parts[1]
                else:
                    #print 'start time parts : {0}'.format(line)
                    self.start_time = "{0} {1} {2} {3} {4}".format(parts[1], parts[2], parts[3], parts[4], parts[5])
            elif (parts[0] == 'end_time'):
                if (parts[1] == '-/-'):
                    self.end_time = parts[1]
                else:
                    #print 'start time parts : {0}'.format(line)
                    self.end_time = "{0} {1} {2} {3} {4}".format(parts[1], parts[2], parts[3], parts[4], parts[5])
            elif (parts[0] == 'failed'):
                self.failed = parts[1]
            elif (parts[0] == 'exit_status'):
                self.exit_status = parts[1]
            elif (parts[0] == 'io'):
                self.io = parts[1]
            
        if (self.cpu == 'missing' or self.maxvmem == 'missing'):
            self.error_reading = True
            #print "{0} CANNOT LOAD".format(self.cluster_job_number)
        #else:
        #    print "{0} cpu : {1}".format(self.cluster_job_number,self.cpu)   
        #    print "{0} maxvmem : {1}".format(self.cluster_job_number,self.maxvmem)   
        #    print "{0} start_time : {1}".format(self.cluster_job_number,self.start_time)   
        #    print "{0} end_time : {1}".format(self.cluster_job_number,self.end_time)   

def has_content(path, cluster_system):
    f = cluster_system.open_file(path,'r')
    lines = f.readlines()
    f.close()
    if (len(lines) > 10):
        return True
    return False 

        