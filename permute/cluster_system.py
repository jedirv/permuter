'''
Created on Feb 10, 2014

@author: irvine
'''
import os
import subprocess
import sys

class ClusterSystem(object):
    
    def is_cluster_job_still_running(self, cluster_job_number, script_dir, qstat_log):
        if (cluster_job_number == "NA"):
            return False
        starting_dir = os.getcwd()
        os.chdir(script_dir)
        #print "opening {0}".format(self.qstat_log)
        command = "qstat | grep {0} > {1}".format(cluster_job_number, qstat_log)
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
        
    def println(self,s):
        print s 
        
    def print_without_newline(self,s):
        sys.stdout.write(s)
        sys.stdout.flush()
        
    def get_time_delay(self):
        return 1.5
    
    def execute_command(self,command):
        try: 
            print "executing: {0}".format(command)
            os.system(command) 
        except subprocess.CalledProcessError:
            print "There was a problem executing command {0}".format(command)
            print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
    
    def delete_file(self,comment,path):
        if (os.path.isfile(path)):
            print "{0} : {1}".format(comment, path)
            os.unlink(path)
         
       
    def chdir(self, path):
        os.chdir(path)
        
    def getcwd(self):
        return os.getcwd()
    
    def get_par_dir(self, path):
        pardir = os.path.dirname(path)
        return pardir
    
    def make_dirs(self,path):
        if (not(os.path.isdir(path))):
            os.makedirs(path)
            
    def listdir(self,path):
        files = os.listdir(path)
        return files
    
    def isfile(self, path):
        return os.path.isfile(path)
    
    def get_last_modification_time(self, path):
        if (not(self.exists(path))):
            return 'NA'
        else:
            return os.path.getmtime(path)
        
    def exists(self,path):
        return os.path.exists(path)
    
    def isdir(self,path):
        return os.path.isdir(path)
    
    def clean_out_dir(self,dirpath):
        if not(os.path.exists(dirpath)):
            return
        items = os.listdir(dirpath)
        for item in items:
            path = "{0}/{1}".format(dirpath, item)
            if os.path.isdir(path):
                try: 
                    print "deleting dir {0}".format(path)
                    command = "rm -rf {0}".format(path)
                    os.system(command) 
                except subprocess.CalledProcessError:
                    print "There was a problem calling rm -rf on {0}".format(path)
                    print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
                    
            else:
                try: 
                    print "deleting file {0}".format(path)
                    command = "rm -f {0}".format(path)
                    os.system(command) 
                except subprocess.CalledProcessError:
                    print "There was a problem calling rm -f on {0}".format(path)
                    print "Return code was {0}".format(subprocess.CalledProcessError.returncode)                        

    def open_file(self, path, mode):
        return open(path, mode)
    
    