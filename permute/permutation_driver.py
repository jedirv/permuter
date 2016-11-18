'''
Created on Feb 9, 2014

@author: irvine
'''
import os
import time
import cluster_spec
import cluster_runs_info
import state_of_runs
import logging

class PermutationDriver(object):
    
    def __init__(self,cspec_lines, cspec_path, stdout, cluster):
        self.cluster = cluster
        self.cspec = cluster_spec.ClusterSpec(cspec_path, cspec_lines, stdout)
        self.cluster_runs = cluster_runs_info.ClusterRunsInfo(self.cspec, stdout)
        self.cspec_path = cspec_path
        self.stdout = stdout
        
    def run_command(self, permute_command, scope):
        run_states = state_of_runs.StateOfRuns()
        cluster_runs = self.cluster_runs
        cspec_path = self.cspec_path
        if (permute_command == "gen"):
            self.generate_scripts(cluster_runs, self.cluster)
        elif (permute_command == "launch"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            self.launch_scripts(cluster_runs, self.cluster, run_states)
        #elif (permute_command == "auto"):
        #    run_states.assess_all_runs(self.cluster_runs, self.cluster)
        #    if (run_states.is_ok_to_launch_all(cluster_runs, self.cluster)):
        #       self.stdout.println("Permutation jobs still running.  Use 'stop' to stop them before 'auto' to avoid replicated jobs")
        #    else:
        #        generate_scripts(cluster_runs)
        #        launch_scripts(cluster_runs, self.cluster)
        elif (permute_command == "retry"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            self.retry_failed_runs(cluster_runs, self.cluster, run_states, self.stdout)
        elif (permute_command == "preview"):
            self.preview_scripts(cluster_runs)
            
        elif (permute_command == "count"):
            self.count_scripts(cluster_runs, self.stdout)
            
        elif (permute_command == "test_launch"):
            pcode = self.cluster_runs.run_perm_codes_list[0]
            run_states.assess_run(pcode, self.cluster_runs, self.cluster)
            if run_states.is_ok_to_launch_run(pcode,self.cluster):
                self.cluster.launch(pcode)
          
        #elif (permute_command == "collect"):
        #    run_states.assess_all_runs(self.cluster_runs, self.cluster)
        #    collect(cluster_runs, self.cluster, self.stdout)
            
        elif (permute_command == "summary"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            run_states.emit_state_summary(self.stdout, self.cluster_runs)
            
        elif (permute_command == "stat"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            run_states.emit_run_states_full(self.stdout, self.cluster_runs)
            
        elif (permute_command == "pending"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            run_states.emit_run_states_pending(self.stdout, self.cluster_runs)
          
        elif (permute_command == "errors"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            run_states.emit_state_errors(self.stdout, self.cluster_runs)
    
        #elif (permute_command == "stat_all"):
        #    run_command_on_all_specs(cspec_path,"stat",self.cluster)
            
        #elif (permute_command == "stat_full_all"):
        #    run_command_on_all_specs(cspec_path,"stat_full",self.cluster)
            
        #elif (permute_command == "stat_pending_all"):
        #    run_command_on_all_specs(cspec_path,"stat_pending",self.cluster)

        elif (permute_command == "stop"):
            self.stop_runs(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_scripts"):
            self.clean_scripts(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_results"):
            self.clean_results(cluster_runs, self.cluster)
            
        #elif (permute_command == "clean_pooled_results"):
        #    clean_pooled_results(cluster_runs, self.cluster)
            
        elif (permute_command == "clean"):
            self.stop_runs(cluster_runs, self.cluster)
            self.clean_scripts(cluster_runs, self.cluster)
            for pcode in cluster_runs.run_perm_codes_list:
                self.stdout.println("deleting all files for {0}\n".format(pcode))
                self.cluster.delete_all_but_script(pcode)
        elif (permute_command == 'launch_job'):
            user_job_number = scope.replace('j','')
            pcode = cluster_runs.perm_code_for_job_number_map[user_job_number]
            self.launch_script(pcode)
            
        elif (permute_command == 'stat_job'):
            user_job_number = scope.replace('j','')
            pcode = cluster_runs.perm_code_for_job_number_map[user_job_number]
            run_states.emit_run_state_full(self.stdout, pcode)
            
        elif (permute_command == 'stop_job'):
            user_job_number = scope.replace('j','')
            pcode = cluster_runs.perm_code_for_job_number_map[user_job_number]
            self.cluster.stop_run(pcode)
            
        elif (permute_command == 'clean_job'):
            user_job_number = scope.replace('j','')
            pcode = cluster_runs.perm_code_for_job_number_map[user_job_number]
            self.cluster.delete_all_but_script(pcode)
            
        else:
            pass
        
    
    def collect(self, cluster_runs, cluster, stdout):
        #warn_of_incomplete_runs(cluster_runs)
        #logging.info('COLLECTING results')
        stdout.println('creating pooled results files...')
        resultsFiles = cluster.create_pooled_results_files(cluster_runs, stdout)
        stdout.println('creating pooled results delta files...')
        cluster.create_pooled_results_delta_files(resultsFiles)
        stdout.println('creating pooled timings files...')
        cluster.create_pooled_timings_files(cluster_runs)
        stdout.println('creating ranked results files...')
        cluster.create_ranked_results_files(cluster_runs)
    
    def stop_runs(self, cluster_runs, cluster):
        logging.info('STOPPING runs that are still running or waiting')
        for pcode in cluster_runs.run_perm_codes_list:
            if cluster.is_running(pcode) or cluster.is_waiting(pcode):
                cluster_job_number = cluster.get_cluster_job_number(pcode)
                user_job_number_as_string = cluster_runs.get_job_number_string_for_run_permutation_code(pcode)
                self.stdout.println("stopping {0} (j{1})".format(cluster_job_number, user_job_number_as_string))
                cluster.stop_run(pcode)
            else:
                self.stdout.println("{0} not running or waiting in queue".format(pcode))
    '''                    
    def run_command_on_all_specs(cspec_path, permuter_command,stdout, cluster):
        spec_dir = os.path.dirname(cspec_path)
        file_or_dirnames = os.listdir(spec_dir)
        cspec_paths = []
        for entry in file_or_dirnames:
            full_path = "{0}/{1}".format(spec_dir,entry)
            if (os.path.isfile(full_path) and not(full_path.endswith("~"))):
                f = open(full_path, 'r')
                header = f.readline()
                f.close()
                if (header.startswith("#cspec")):
                    cspec_paths.append(full_path)
        for path in cspec_paths:
            command = "python permuter.py {0} {1}".format(permuter_command, path)
            stdout.println("-------------------------------------------------------------------")
            #print command
            cluster.execute_command(command) 
    '''
         
    def retry_failed_runs(self, cluster_runs, cluster, run_states, stdout):
        logging.info('LAUNCHING incomplete runs')
        for pcode in cluster_runs.run_perm_codes_list:
            if cluster.is_running(pcode):
                stdout.println("{0} left running".format(pcode))
            elif cluster.is_waiting(pcode):
                stdout.println("{0} left waiting".format(pcode))
            elif run_states.state_names[run_states.run_states[pcode]] == "run complete":
                stdout.println("{0} completed".format(pcode))
            elif run_states.state_names[run_states.run_states[pcode]] == "run near complete":
                stdout.println("{0} near complete".format(pcode))
            else:
                state_name = run_states.state_names[run_states.run_states[pcode]]
                stdout.println("{0} {1} - retrying".format(pcode, state_name))
                cluster.stop_run(pcode)
                if not (cluster.is_script_present(pcode)):
                    cluster.create_script(pcode)
                cluster.delete_all_but_script(pcode)
                cluster.launch(pcode)
                time.sleep(cluster.get_time_delay())
    
    def launch_scripts(self, cluster_runs, cluster, run_states):
        logging.info('LAUNCHING scripts')
        for pcode in cluster_runs.run_perm_codes_list:
            if run_states.is_ok_to_launch_run(pcode, cluster):
                self.launch_script(pcode, cluster)
                time.sleep(cluster.get_time_delay())
            
    def launch_script(self, pcode, cluster):
        cluster.delete_all_but_script(pcode)
        cluster.launch(pcode)
        
    def generate_scripts(self, cluster_runs, cluster):
        logging.info('GENERATING scripts')
        for pcode in cluster_runs.run_perm_codes_list:
            cluster.create_script(pcode)
    
    def clean_scripts(self, cluster_runs,cluster):
        logging.info('CLEANING scripts')
        for pcode in cluster_runs.run_perm_codes_list:
            self.stdout.println("deleting script for {0}".format(pcode))
            cluster.delete_script(pcode)
    
                
    def preview_scripts(self, cluster_runs):
        logging.info("PREVIEWING scripts")
        cscript = cluster_runs.get_first_script()
        cscript.preview()
    
    def count_scripts(self, cluster_runs, stdout):
        logging.info("COUNTING scripts")
        count = cluster_runs.get_permutation_count()
        stdout.println('{0} scripts in play'.format(count))
    
    
    def clean_results(self, cluster_runs, cluster):
        for pcode in cluster_runs.run_perm_code_list:
            cluster.delete_results(pcode)
        
    def clean_pooled_results(self, cluster_runs, cluster):
        cluster.delete_pooled_results()
        cluster.delete_pooled_results_delta_file()
        cluster.delete_pooled_results_timings_file()
        cluster.delete_ranked_results_file()
    
    
    
