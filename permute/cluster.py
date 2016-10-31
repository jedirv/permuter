'''
Created on Oct 28, 2016

@author: Jed Irvine
'''
import os
import subprocess
import qsub_invoke_log
import qacct_log
import qstat_log
import stdout
import getpass
import permutations

class Cluster(object):
    '''
    classdocs
    '''
    def create_script(self, pcode):
        cscript = self.cluster_runs.get_script_for_run_permutation_code(pcode)
        self.scripts[pcode] = cscript
        cscript.persist()
        
    def delete_script(self, pcode):
        if self.scripts.has_key(pcode):
            cscript = self.scripts[pcode]
            cscript.delete()

    def delete_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            qil = self.invoke_logs[pcode]
            qil.delete()
            self.invoke_logs.pop(pcode)

    def delete_qacct_log(self, pcode):
        if self.qacct_logs.has_key(pcode):
            qacct_log = self.qacct_logs[pcode]
            qacct_log.delete()
            self.qacct_logs.pop(pcode)
         
    def delete_qstat_log(self, pcode):
        if self.qstat_log:
            self.qstat_log.delete()
            self.qstat_log = 0

    def delete_results(self, pcode):
        results_dir = self.cluster_runs.cspec.job_results_dir
        self.clean_out_dir(results_dir)

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


    def launch(self, pcode):
        if self.scripts.has_key(pcode):
            cscript = self.scripts[pcode]
            cscript.launch()
            
    def execute_command(self,command):
        try: 
            print "executing: {0}".format(command)
            os.system(command) 
        except subprocess.CalledProcessError:
            print "There was a problem executing command {0}".format(command)
            print "Return code was {0}".format(subprocess.CalledProcessError.returncode)
    
    def get_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            return self.invoke_logs[pcode]
        perm_info = self.cluster_runs.run_permutation_info_for_run_permutation_code_map[pcode]
        trial = perm_info['trials']
        user_job_number_as_string = self.cluster_runs.get_job_number_string_for_run_permutation_code(pcode)
        cspec = self.cluster_runs.cspec
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, perm_info, cspec, trial)
        self.invoke_logs[pcode] = qil
        
    def get_cluster_job_number(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.cluster_job_number
            
    def stop_run(self, pcode):
        if self.is_running(pcode) or self.is_waiting(pcode):
            cluster_job_number = self.get_cluster_job_number(pcode)
            user_job_number_as_string = self.cluster_runs.get_job_number_string_for_run_permutation_code(pcode)
            if (cluster_job_number == "NA"):
                self.stdout.println("{0} - no evidence of having launched".format(user_job_number_as_string))
            else:
                self.stdout.println("stopping {0} (j{1}...)".format(cluster_job_number, user_job_number_as_string))
                command = "qdel {0}".format(cluster_job_number)
                self.execute_command(command)
            

    def is_script_present(self, pcode):
        if self.scripts.has_key(pcode):
            return True
        return False

    def is_invoke_log_present(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.exists()

    def is_invoke_log_corrupt(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.is_corrupt()

    def get_qacct_log(self,pcode):
        user_job_number_as_string = self.cluster_runs.get_job_number_string_for_run_permutation_code(pcode)
        permutation_info = self.cluster_runs.run_permutation_info_for_run_permutation_code_map[pcode]
        cspec = self.cluster_runs.cspec
        cluster_job_number = self.get_cluster_job_number(pcode)
        if (cluster_job_number == "NA"):
            self.stdout.println("skipping qacct, job not started yet")
            return 0
        else:
            #print "opening {0}".format(self.qstat_log)
            
            qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trials'])
            command = "qacct -j {0} > {1}".format(cluster_job_number, qacctlog.qacct_log_path)
            self.execute_command(command) 
            qacctlog.ingest(cluster_job_number)
            self.qacct_logs[pcode]= qacctlog
            return qacctlog
            
            
    def is_qacct_log_present(self, pcode):
        if self.qacct_logs.has_key(pcode):
            return True
        return False
    
    def get_qstat_log(self):
        #always get this one fresh for most up to date info
        cspec = self.cluster_runs.cspec
        self.qstat_log = qstat_log.QStatLog(cspec.script_dir)
        username = getpass.getuser()
        command = "qstat -u {0} > {1}".format(username, self.qstat_log.logpath)
        self.execute_command(command) 
        self.qstat_log.ingest()
        return self.qstat_log
        
        
    def is_qstat_log_present(self):
        if self.qstat_log:
            return True
        return False
    
    def is_running(self, pcode):
        qstatlog= self.get_stat_log()
        return qstatlog.is_running(pcode)

    def is_waiting(self, pcode):
        qstatlog= self.get_stat_log()
        return qstatlog.is_waiting(pcode)


    def is_permission_blocked(self, pcode):
        if not(self.is_running(pcode) and not(self.is_waiting(pcode)) and not(self.is_done_marker_present(pcode))):
            if self.is_invoke_log_present(pcode):
                qil = self.get_invoke_log(pcode)
                if qil.is_first_error_permission_problem():
                    return True
        return False
            
        
        if qil.is_first_error_permission_problem():
    
    def is_done_marker_present(self, pcode):
        done_marker_file_path = self.cluster_runs.get_donefile_path_for_run_permutation_code(pcode)
        #print "done_marker_file_path {0}".format(done_marker_file_path)
        run_finished = False
        if (os.path.exists(done_marker_file_path)):
            run_finished=True
        return run_finished

    def get_missing_output_files(self, pcode, cluster_system):
        missing_output_files = []
        permutation_info = self.cluster_runs_info.get_permutation_info_for_permutation_code(pcode)
        list_of_output_files = permutations.get_list_of_output_files(permutation_info, self.cluster_runs.cspec)
        for output_file_path in list_of_output_files:
            if (not(os.path.exists(output_file_path))):
                missing_output_files.append(output_file_path)
        return missing_output_files

    def is_output_files_present(self, pcode):
        missing_output_files = self.get_missing_output_files(pcode)
        if len(missing_output_files) == 0:
            return True
        return False

    def get_output_file_mod_time(self, pcode):
        permutation_info = self.cluster_runs.get_permutation_info_for_permutation_code(pcode)
        list_of_output_files = permutations.get_list_of_output_files(permutation_info, self.cluster_runs.cspec)
        time = 0
        # find the oldest output_file mod time
        for output_file in list_of_output_files:
            curtime = os.path.getmtime(output_file)
            if time == 0:
                time = curtime
            else:
                if curtime < time:
                    time = curtime
        if time == 0:
            return 'NA'
        else:
            return time
        


    def __init__(self, cluster_runs):
        self.cluster_runs = cluster_runs
        self.stdout = stdout.Stdout()
        self.scripts = {}
        self.invoke_logs = {}
        self.qacct_logs = {}
        self.qstat_log= 0
        '''
        Constructor
        '''
        