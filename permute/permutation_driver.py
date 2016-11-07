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
        stdout.println('initializing cluster_spec...')
        self.cspec = cluster_spec.ClusterSpec(cspec_path, cspec_lines, stdout)
        stdout.println('initializing cluster_runs_info...')
        self.cluster_runs = cluster_runs_info.ClusterRunsInfo(self.cspec)
        result_dirs = self.cluster_runs.get_results_dirs_to_make()
        for result_dir in result_dirs:
            os.makedirs(result_dir)
        self.cspec_path = cspec_path
        self.stdout = stdout
        
    def run_command(self, permute_command):
        run_states = state_of_runs.StateOfRuns()
        cluster_runs = self.cluster_runs
        cspec_path = self.cspec_path
        if (permute_command == "gen"):
            generate_scripts(cluster_runs)
        elif (permute_command == "launch"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            if (run_states.is_ok_to_launch_all(cluster_runs, self.cluster)):
                self.stdout.println("Permutation jobs still running.  Use 'stop' to stop them before 'launch' to avoid replicated jobs")
            else:
                launch_scripts(cluster_runs, self.cluster)
        #elif (permute_command == "auto"):
        #    run_states.assess_all_runs(self.cluster_runs, self.cluster)
        #    if (run_states.is_ok_to_launch_all(cluster_runs, self.cluster)):
        #       self.stdout.println("Permutation jobs still running.  Use 'stop' to stop them before 'auto' to avoid replicated jobs")
        #    else:
        #        generate_scripts(cluster_runs)
        #        launch_scripts(cluster_runs, self.cluster)
        elif (permute_command == "retry failed"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            retry_failed_runs(cluster_runs, self.cluster, run_states, self.stdout)
        elif (permute_command == "preview"):
            preview_scripts(cluster_runs)
            
        elif (permute_command == "count"):
            count_scripts(cluster_runs, self.stdout)
            
        elif (permute_command == "test_launch"):
            pcode = self.cluster_runs.run_perm_codes_list[0]
            run_states.assess_run(pcode, self.cluster_runs, self.cluster)
            if run_states.is_ok_to_launch(pcode):
                self.cluster.launch(pcode)
            
        elif (permute_command == "collect"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            collect(cluster_runs, self.cluster, self.stdout)
        
        elif (permute_command == "stat"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            emit_run_states("summary", run_states)
            
        elif (permute_command == "stat_full"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            emit_run_states("full", run_states)
            
        elif (permute_command == "stat_pending"):
            run_states.assess_all_runs(self.cluster_runs, self.cluster)
            emit_run_states("pending", run_states)
            
        elif (permute_command == "stat_all"):
            run_command_on_all_specs(cspec_path,"stat",self.cluster)
            
        elif (permute_command == "stat_full_all"):
            run_command_on_all_specs(cspec_path,"stat_full",self.cluster)
            
        elif (permute_command == "stat_pending_all"):
            run_command_on_all_specs(cspec_path,"stat_pending",self.cluster)
        
        elif (permute_command == "stop"):
            stop_runs(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_scripts"):
            clean_scripts(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_results"):
            clean_results(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_pooled_results"):
            clean_pooled_results(cluster_runs, self.cluster)
            
        elif (permute_command == "clean_all"):
            for pcode in cluster_runs.run_perm_code_list:
                self.cluster.stop_run(pcode)
                self.cluster.delete_script()
                self.cluster.delete_all_but_script(pcode)
        
        else:
            pass
        
    
def collect(cluster_runs, cluster, stdout):
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

def stop_runs(cluster_runs, cluster):
    logging.info('STOPPING runs that are still running or waiting')
    for pcode in cluster_runs.run_perm_codes_list:
        cluster.stop_run(pcode)
                    
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

     
def retry_failed_runs(cluster_runs, cluster, run_states, stdout):
    logging.info('LAUNCHING incomplete runs')
    for pcode in cluster_runs.run_perm_codes_list:
        if cluster.is_running(pcode):
            stdout("{0} left running".format(pcode))
        elif cluster.is_waiting(pcode):
            stdout("{0} left waiting".format(pcode))
        elif run_states.state_names[run_states.run_states[pcode]] == "run complete":
            stdout("{0} completed".format(pcode))
        elif run_states.state_names[run_states.run_states[pcode]] == "run near complete":
            stdout("{0} near complete".format(pcode))
        else:
            state_name = run_states.state_names[run_states.run_states[pcode]]
            stdout("{0} {1} - retrying".format(pcode, state_name))
            cluster.stop_run(pcode)
            if not (cluster.is_script_present(pcode)):
                cluster.create_script(pcode)
            cluster.delete_all_but_script(pcode)
            cluster.launch(pcode)
            time.sleep(cluster.get_time_delay())
            
    
def emit_run_states(output_style, run_states):
    if output_style == 'summary':
        run_states.emit_state_summary()
    elif output_style == 'full':
        run_states.emit_state_full()
    elif output_style == 'pending':
        run_states.emit_state_pending()
    else:
        pass

def launch_scripts(cluster_runs, cluster):
    logging.info('LAUNCHING scripts')
    for pcode in cluster_runs.run_perm_codes_list:
        launch_script(pcode)
        time.sleep(cluster.get_time_delay())
        
def launch_script(pcode, cluster):
    cluster.delete_all_but_script(pcode)
    cluster.launch(pcode)
    
def generate_scripts(cluster_runs, cluster):
    logging.info('GENERATING scripts')
    for pcode in cluster_runs.run_perm_codes_list:
        cluster.create_scrit(pcode)

def clean_scripts(cluster_runs,cluster):
    logging.info('CLEANING scripts')
    for pcode in cluster_runs.run_perm_codes_list:
        cluster.delete_script(pcode)

            
def preview_scripts(cluster_runs):
    logging.info("PREVIEWING scripts")
    cscript = cluster_runs.get_first_script()
    cscript.preview()

def count_scripts(cluster_runs, stdout):
    logging.info("COUNTING scripts")
    count = cluster_runs.get_permutation_count()
    stdout.println('{0} scripts in play'.format(count))


def clean_results(cluster_runs, cluster):
    for pcode in cluster_runs.run_perm_code_list:
        cluster.delete_results(pcode)
    
def clean_pooled_results(cluster_runs, cluster):
    cluster.delete_pooled_results()
    cluster.delete_pooled_results_delta_file()
    cluster.delete_pooled_results_timings_file()
    cluster.delete_ranked_results_file()
    
    
    
