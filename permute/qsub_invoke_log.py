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
   
    def exists(self):
        if (self.cluster_system.exists(self.qsub_invoke_log_fullpath)):
            return True
        return False      
    
    def get_last_modification_time(self):
        if (self.exists()):
            return self.cluster_system.get_last_modification_time(self.qsub_invoke_log_fullpath)
        else:
            return 'NA'  
            
    def is_first_error_permission_problem(self):
        error_file = self.qsub_invoke_log_fullpath.replace('.qil','.err')
        if not(self.cluster_system.exists(error_file)):
            return False
        f = self.cluster_system.open_file(error_file,'r')
        lines = f.readlines()
        f.close()
        if (len(lines) == 0):
            return False
        first_line = lines[0]
        if (first_line.count('Permission denied') > 0):
            return True
        return False
       
    def is_corrupt(self):
        starting_dir = self.cluster_system.getcwd()
        self.cluster_system.chdir(self.script_dir)
        #print "opening {0}".format(self.qsub_invoke_log_fullpath)
        #print self.script_dir
        if (self.cluster_system.exists(self.qsub_invoke_log_fullpath)):
            f = self.cluster_system.open_file(self.qsub_invoke_log_fullpath, 'r')
            line = f.readline()
            f.close()
            #print "closed {0}".format(self.qsub_invoke_log_fullpath)
            parts = line.split(' ')
            
            if (len(parts) != 7):
                #raise monitor_exception.MonitorException("qsub invoke log has incorrect number of fields {0}. Should look like 'Your job 4174438 (jobname) has been submitted'")
                return True
            else:
                return False
        self.cluster_system.chdir(starting_dir)
        return False
         
    def load_job_number(self):
        starting_dir = self.cluster_system.getcwd()
        self.cluster_system.chdir(self.script_dir)
        #print "opening {0}".format(self.qsub_invoke_log_fullpath)
        #print self.script_dir
        if (self.cluster_system.exists(self.qsub_invoke_log_fullpath)):
            f = self.cluster_system.open_file(self.qsub_invoke_log_fullpath, 'r')
            line = f.readline()
            f.close()
            #print "closed {0}".format(self.qsub_invoke_log_fullpath)
            parts = line.split(' ')
            
            if (len(parts) != 7):
                #raise monitor_exception.MonitorException("qsub invoke log has incorrect number of fields {0}. Should look like 'Your job 4174438 (jobname) has been submitted'")
                raise Exception("\n\nlogfile that captures the output of qsub is malformed:\n\n{0}.qil \n\nIt should look like 'Your job 4174438 (jobname) has been submitted'\n\nInstead, it looks like: '{1}'\n\nDelete this file to clear the Exception".format(self.script_path_root, line))
            result = parts[2]
        else:
            result = "NA"
        self.cluster_system.chdir(starting_dir)
        return result
        
    def delete(self):
        #print ("ok , trying to delete {0} ".format(self.qsub_invoke_log_fullpath))
        if (self.cluster_system.exists(self.qsub_invoke_log_fullpath)):
            self.cluster_system.delete_file("deleting qsub_invoke_log",self.qsub_invoke_log_fullpath)
 
    
        