'''
Created on Feb 23, 2014

@author: irvine
'''

class StateOfRuns(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.scripts_exist = False
        self.all_scripts_exist = False
        self.runs_in_progress = False
        self.runs_completed = False
        self.pooled_results_exist = False
        self.pooled_timings_exist = False
        self.ranked_results_exist = False
        
        
    def assess(self, cluster_system, cluster_runs_info):    
        self.cluster_system = cluster_system
        self.cluster_runs_info = cluster_runs_info
        self.scripts_exist = check_for_any_scripts(cluster_system, cluster_runs_info)
        self.all_scripts_exist = check_for_all_scripts(cluster_system, cluster_runs_info)
        self.runs_in_progress = check_for_runs_in_progress(cluster_system, cluster_runs_info)
        self.runs_completed = check_for_runs_complete(cluster_system,cluster_runs_info)
        self.pooled_results_exist = check_for_pooled_results(cluster_system,cluster_runs_info)
        self.pooled_timings_exist = check_for_pooled_timings(cluster_system,cluster_runs_info)
        self.ranked_results_exist = check_for_ranked_results(cluster_system,cluster_runs_info)
        
def check_for_any_scripts(self, cluster_system, cluster_runs_info):
    for run_perm_code in cluster_runs_info.run_perm_codes_list:
        cluster_script = cluster_runs_info.get_script_for_run_permutation_code(run_perm_code)
        if (cluster_system.exists(cluster_script.pathname)):
            return True
    return False
        
def check_for_all_scripts(self, cluster_system, cluster_runs_info):
    result = True
    for run_perm_code in cluster_runs_info.run_perm_codes_list:
        cluster_script = cluster_runs_info.get_script_for_run_permutation_code(run_perm_code)
        if not(cluster_system.exists(cluster_script.pathname)):
            result = False
    return result
        

def check_for_runs_in_progress(self, cluster_system, cluster_runs_info):
    pass

def check_for_runs_complete(self, cluster_system, cluster_runs_info):
    pass

def check_for_pooled_results(self, cluster_system, cluster_runs_info):
    pass

def check_for_pooled_timings(self, cluster_system, cluster_runs_info):
    pass

def check_for_ranked_results(self, cluster_system, cluster_runs_info):
    pass