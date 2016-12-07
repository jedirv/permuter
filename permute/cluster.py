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
import pooled_results_delta_file
import pooled_timings_file
import ranked_results_file
import pooled_results_file
import logging
import cluster_script

class Cluster(object):
    '''
    classdocs
    '''
    #
    # SCRIPTS
    #
    def is_script_present(self, pcode):
        if self.scripts.has_key(pcode):
            if self.scripts[pcode].exists():
                return True
        return False

    def create_script(self, pcode):
        cscript = self.cluster_runs.get_script_for_perm_code(pcode)
        self.scripts[pcode] = cscript
        cscript.generate()
        return cscript
        
    def delete_script(self, pcode):
        if self.scripts.has_key(pcode):
            cscript = self.scripts[pcode]
            if cscript.exists():
                cscript.delete()
            
    def get_script_mod_time(self,pcode):
        if self.is_script_present(pcode):
            cscript = self.scripts[pcode]
            path = cscript.pathname
            return os.path.getmtime(path)
        return 'NA'

    def launch(self, pcode):
        if self.scripts.has_key(pcode):
            if self.scripts[pcode].exists():
                cscript = self.scripts[pcode]
                result_dir = self.cluster_runs.result_dir_for_perm_code_map[pcode]
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir)
                self.stdout.println("launching run for {0}".format(pcode))
                cscript.launch(self)
            else:
                self.stdout.println("cannot launch run for {0} - script does not exist".format(pcode))
    #
    # INVOKE_LOG
    #
    
    def get_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            return self.invoke_logs[pcode]
        perm_info = self.cluster_runs.perm_info_for_perm_code_map[pcode]
        trial = perm_info['trial']
        user_job_number_as_string = self.cluster_runs.get_job_number_string_for_perm_code(pcode)
        cspec = self.cluster_runs.cspec
        qil = qsub_invoke_log.QsubInvokeLog(user_job_number_as_string, perm_info, cspec, trial, self.stdout)
        self.invoke_logs[pcode] = qil
        return qil
        
    def get_invoke_log_mod_time(self,pcode):
        if self.is_invoke_log_present(pcode):
            invoke_log = self.get_invoke_log(pcode)
            return os.path.getmtime(invoke_log.pathname)
        return 'NA'
        
    def delete_invoke_log(self, pcode):
        if self.invoke_logs.has_key(pcode):
            qil = self.invoke_logs[pcode]
            if qil.exists():
                qil.delete()
            self.invoke_logs.pop(pcode)

    def is_invoke_log_present(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.exists()

    def is_invoke_log_corrupt(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.is_corrupt()

    #
    # QACCT
    #
    def get_qacct_log(self,pcode):
        user_job_number_as_string = self.cluster_runs.get_job_number_string_for_perm_code(pcode)
        permutation_info = self.cluster_runs.perm_info_for_perm_code_map[pcode]
        cspec = self.cluster_runs.cspec
        cluster_job_number = self.get_cluster_job_number(pcode)
        if (cluster_job_number == "NA" or self.is_running(pcode) or self.is_waiting(pcode)):
            self.stdout.println("skipping qacct, job not started yet")
            return 0
        else:            
            qacctlog = qacct_log.QacctLog(user_job_number_as_string, permutation_info, cspec, permutation_info['trial'], self.stdout)
            command = "qacct -j {0} > {1}".format(cluster_job_number, qacctlog.qacct_log_path)
            self.execute_command(command) 
            qacctlog.ingest(cluster_job_number)
            return qacctlog
  
    #
    # QSTAT
    #
 
 
    def get_qstat_log(self):
        if self.qstat_log:
            return self.qstat_log
        cspec = self.cluster_runs.cspec
        self.qstat_log = qstat_log.QStatLog(cspec.script_dir, cspec.cspec_name)
        username = getpass.getuser()
        command = "qstat -u {0} -xml > {1}".format(username, self.qstat_log.logpath)
        #self.stdout.println(command)
        self.execute_command(command) 
        self.qstat_log.ingest()
        return self.qstat_log
   

    #
    # RESULTS
    #
    '''
    Once we again have a way of knowing all the output files of a run, we can change back to this
    def get_missing_output_files(self, pcode, cluster_system):
        missing_output_files = []
        permutation_info = self.cluster_runs_info.get_permutation_info_for_perm_code(pcode)
        list_of_output_files = permutations.get_list_of_output_files(permutation_info, self.cluster_runs.cspec)
        for output_file_path in list_of_output_files:
            if (not(os.path.exists(output_file_path))):
                missing_output_files.append(output_file_path)
        return missing_output_files
    '''
    def is_output_files_present(self, pcode):
        '''
        missing_output_files = self.get_missing_output_files(pcode)
        if len(missing_output_files) == 0:
            return True
        return False
        '''
        cscript = self.scripts[pcode]
        results_dir = cscript.resolved_results_dir
        done_marker_filename = cluster_script.get_done_marker_filename()
        if os.path.exists(results_dir):
            filenames = os.listdir(results_dir)
            count = 0
            for filename in filenames:
                if filename == done_marker_filename:
                    pass
                elif filename == '.':
                    pass 
                elif filename == '..':
                    pass
                else:
                    count = count + 1
            if count > 0 :
                return True
        return False

    def get_output_file_mod_time(self, pcode):
        permutation_info = self.cluster_runs.get_permutation_info_for_perm_code(pcode)
        list_of_output_files = permutations.get_list_of_output_files(permutation_info, self.cluster_runs.cspec)
        time = 0
        # find the oldest output_file mod time
        for output_file in list_of_output_files:
            if os.path.exists(output_file):
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
        
    def delete_results(self, pcode):
        cspec = self.cluster_runs.cspec
        print "pcode given : {0}".format(pcode)
        print cspec.cspec_name
        results_dir = cspec.generate_results_dir_for_permutation(pcode)
        print "results_dir to clean out : {0}".format(results_dir)
        self.clean_out_dir(results_dir)
    #
    # POOLED_RESULST
    #
    
    def create_pooled_results_delta_files(self,resultsFiles):
        for resultsFile in resultsFiles:
            deltaFile = pooled_results_delta_file.PooledResultsDeltaFile(resultsFile)
            deltaFile.generate()
            
    def create_pooled_timings_files(self,cluster_runs):
        logging.info('CREATING timings files')
        permuters_for_filename = pooled_timings_file.gather_file_permuters(cluster_runs.cspec)
        #print "permuters_for_filename {0}".format(permuters_for_filename)
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        #print "filename_permutations {0}".format(filename_permutations)
        if (len(filename_permutations) == 0):
            timingsFile = pooled_timings_file.PooledTimingsFile({}, cluster_runs)
            timingsFile.persist()
        else: 
            for filename_permutation_info in filename_permutations:
                timingsFile = pooled_timings_file.PooledTimingsFile(filename_permutation_info, cluster_runs)
                timingsFile.persist()
                
    def create_ranked_results_files(self,cluster_runs):
        logging.info('CREATING ranked results file')
        permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        if (len(filename_permutations) == 0):
            rankFile = ranked_results_file.RankedResultsFile({}, cluster_runs)
            rankFile.persist()
        else:
            for filename_permutation_info in filename_permutations:
                rankFile = ranked_results_file.RankedResultsFile(filename_permutation_info, cluster_runs)
                rankFile.persist()
        
    
    def create_pooled_results_files(self,cluster_runs, stdout):
        logging.info("CREATING pooled results files")
        source_file_map = cluster_runs.create_source_file_map(cluster_runs.cspec)
        logging.debug("...source_file_map : {0}".format(source_file_map))
        permuters_for_filename = pooled_results_file.gather_file_permuters(cluster_runs.cspec)
        logging.debug("...permuters_for_filename : {0}".format(permuters_for_filename))
        filename_permutations = permutations.expand_permutations(permuters_for_filename)
        logging.debug("...filename permutations : {0}".format(filename_permutations))
        resultsFiles = []
        if (len(filename_permutations) == 0):
            resultsFile = pooled_results_file.PooledResultsFile(source_file_map, {}, cluster_runs, stdout)
            resultsFile.persist()
            resultsFiles.append(resultsFile)
        else:
            for filename_permutation_info in filename_permutations:
                resultsFile = pooled_results_file.PooledResultsFile(source_file_map, filename_permutation_info, cluster_runs, stdout)
                resultsFile.persist()
                resultsFiles.append(resultsFile)
        logging.info("...resultsFiles : {0}".format(resultsFiles))    
        return resultsFiles
            
    def delete_pooled_results(self):
        pass
        
    def delete_pooled_results_delta_file(self):
        pass
        
    def delete_pooled_results_timings_file(self,pcode):
        pass
        
    def delete_ranked_results_file(self,pcode):
        pass
     
          
    #
    # DONE MARKER
    #
    
    def is_done_marker_present(self, pcode):
        done_marker_file_path = self.cluster_runs.get_donefile_path_for_perm_code(pcode)
        #print "done_marker_file_path {0}".format(done_marker_file_path)
        run_finished = False
        if (os.path.exists(done_marker_file_path)):
            run_finished=True
        return run_finished

    def get_done_marker_mod_time(self,pcode):
        if self.is_done_marker_present(pcode):
            done_marker_file_path = self.cluster_runs.get_donefile_path_for_perm_code(pcode)
            return os.path.getmtime(done_marker_file_path)
        return 'NA'
            

    def delete_done_marker(self, pcode):
        done_marker_file_path = self.cluster_runs.get_donefile_path_for_perm_code(pcode)
        if (os.path.exists(done_marker_file_path)):
            os.unlink(done_marker_file_path)
                
    
    
    #
    #
    #
    def delete_all_but_script(self,pcode):
        self.delete_invoke_log(pcode)
        # we always get the qacct_log fresh so no need to clean 
        # we always get the qstat_log fresh regardless, so no need to clean
        self.delete_done_marker(pcode)
        self.delete_results(pcode)

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


            
    def execute_command(self,command):
        try: 
            print "executing: {0}".format(command)
            os.system(command) 
        except subprocess.CalledProcessError:
            print "There was a problem executing command {0}".format(command)
            print "Return code was {0}".format(subprocess.CalledProcessError.returncode)

    def get_time_delay(self):
        return 1.5
       
    def get_cluster_job_number(self, pcode):
        qil = self.get_invoke_log(pcode)
        return qil.cluster_job_number
            
    def stop_run(self, pcode):
        if self.is_running(pcode) or self.is_waiting(pcode):
            cluster_job_number = self.get_cluster_job_number(pcode)
            if (cluster_job_number == "NA"):
                pass
            else:
                command = "qdel {0}".format(cluster_job_number)
                self.execute_command(command)

    def is_running(self, pcode):
        cscript = self.scripts[pcode]
        runs_name = cscript.cspec.cspec_name
        job_name = "{0}-{1}".format(runs_name, cscript.get_job_file_name())
        qstatlog= self.get_qstat_log()
        return qstatlog.is_running(job_name)

    def is_waiting(self, pcode):
        cscript = self.scripts[pcode]
        runs_name = cscript.cspec.cspec_name
        job_name = "{0}-{1}".format(runs_name, cscript.get_job_file_name())
        qstatlog= self.get_qstat_log()
        return qstatlog.is_waiting(job_name)


    def get_invoke_error(self, pcode):
        if not(self.is_running(pcode) and not(self.is_waiting(pcode)) and not(self.is_done_marker_present(pcode))):
            if self.is_invoke_log_present(pcode):
                qil = self.get_invoke_log(pcode)
                return qil.get_invoke_error()
        return ''

    def get_failure_reason(self,pcode):
        acct_log = self.get_qacct_log(pcode)
        if acct_log != 0:
            return acct_log.get_failure_reason()
        return 'NA'
        
    def load_scripts(self):
        for pcode in self.cluster_runs.run_perm_codes_list:
            cscript = self.cluster_runs.get_script_for_perm_code(pcode)
            self.scripts[pcode] = cscript
    
    def load_invoke_logs(self):
        for pcode in self.cluster_runs.run_perm_codes_list:
            self.get_invoke_log(pcode)
                        
    def __init__(self, cluster_runs, stdout):
        self.cluster_runs = cluster_runs
        self.stdout = stdout
        self.scripts = {}
        self.invoke_logs = {}
        self.qstat_log = 0
        '''
        Constructor
        '''
        self.load_scripts()
        self.load_invoke_logs()
        