'''
Created on Feb 13, 2014

@author: irvine
'''
'''
Created on Feb 10, 2014

@author: irvine
'''
import os
import mock_file

class MockClusterSystem(object):
    def __init__(self):
        self.files = {}
        self.dirs = []
        self.cur_dir = '.'
        self.commands = []
        self.running_jobs = {}
        self.next_job_number = 1
        self.qacct_files = {}
        
    
    def is_cluster_job_still_running(self, cluster_job_number, script_dir, qstat_log):
        if cluster_job_number in self.running_jobs:
            return True
        return False
        
    def execute_command(self,command, cspec):
        self.commands.append(command)
        if command.startswith("qsub"): #assume this is always the unit test context
            self.process_unittest_script(command, cspec)
            parts = command.split(" ")
            job_script = parts[1]
            next_job_number_string = "{0}".format(self.next_job_number)
            self.running_jobs[next_job_number_string] = job_script
            self.next_job_number = self.next_job_number + 1
        elif command.startswith("qdel"):
            parts = command.split(" ")
            job_number = parts[1]
            job_number_string = "{0}".format(job_number)
            self.running_jobs.pop(job_number_string)
        elif command.startswith("python permuter.py"):
            raise 'execute_command("python permuter.py...") not yet implement'
        elif command.startswith("qacct"):
            parts = command.split(" ")
            job_number_string = parts[2]
            target_filename = parts[4]
            f = self.open_file(target_filename,'w')
            qacct_file_count = len(self.qacct_files)
            cpu_time = qacct_file_count * 10 + 10
            cpu_string = "cpu\t\t{0}".format(cpu_time)
            mem_string = "mem\t\t{0}".format(cpu_time)
            maxvmem_string = "maxvmem\t\t{0}G".format(cpu_time)
            f.write("{0}\n".format(cpu_string))
            f.write("{0}\n".format(mem_string))
            f.write("{0}\n".format(maxvmem_string))
            f.close()
            self.qacct_files[job_number_string] = f
            
    def set_unittest_answers(self, answerkey):
        self.answerkey = answerkey
        
    def get_time_delay(self):
        return 0.0
    
    def process_unittest_script(self,command, cspec):
        parts = command.split(" ")
        script_name = parts[1]
        trial, permcode = self.get_trial_permcode_from_script_name(script_name)
        # j105_2_an_cat_l_aa_number_3_s_300.sh
        
        result_permuters = self.answerkey.keys()
        # now we know how many result files there needs to be
        for result_permuter in result_permuters:
            # look up the answer for the result file of this result permuation
            list_of_trial_answer_dictionaries = self.answerkey[result_permuter]
            trial_index = int(trial) - 1
            trial_answer_dictionary = list_of_trial_answer_dictionaries[trial_index]
            answer = trial_answer_dictionary[permcode]
            self.persist_answer(answer, permcode, trial, cspec, result_permuter)
            
    def persist_answer(self, answer, permcode, trial, cspec, result_permuter): 
        scores_from_filepath = cspec.scores_from_filepath
        root_results_dir = cspec.root_results_dir
        permutation_results_dir = "{0}/{1}/trial{2}/{3}".format(root_results_dir, cspec.master_job_name, trial, permcode)
        scores_from_filepath_perm_dir_resolved = scores_from_filepath.replace("<permutation_results_dir>", permutation_results_dir)
        scores_permute_keys = cspec.scores_permuters.keys()
        scores_permuter_key = scores_permute_keys[0]
        permuter_match_string = "({0})".format(scores_permuter_key)
        resolved_path = scores_from_filepath_perm_dir_resolved.replace(permuter_match_string,result_permuter)
        f = self.open_file(resolved_path,'w')
        f.write("foo,auc,bar\n")
        f.write("na,")
        f.write(answer)
        f.write(",na\n")
        f.close()
    
    def get_trial_permcode_from_script_name(self, script_name):
        parts = script_name.split('\.')
        root_name = parts[0]
        jobnum, sep, rest = root_name.partition('_')
        trial, sep, permcode_and_file_extension = rest.partition('_')
        permcode = permcode_and_file_extension.replace(".sh", "")
        return trial, permcode
      
        
    def delete_file(self,comment,path):
        if (self.files.has_key(path)):
            print "{0} : {1}".format(comment, path)
            self.files.pop(path)
         
       
    def chdir(self, path):
        self.cur_dir = path
        
    def getcwd(self):
        return self.cur_dir
    
    def get_par_dir(self, path):
        pardir = os.path.dirname(path)
        return pardir
    
    def make_dirs(self,path):
        self.mkdir(path)
        more_dirs = True
        while more_dirs:
            path = os.path.dirname(path)
            if path == '/' or path == '.':
                more_dirs = False
            else:
                self.mkdir(path)
      
    def mkdir(self, path):
        if not(path in self.dirs):
            self.dirs.append(path)  
              
    def listdir(self,path):
        result_list = []
        if not(path in self.dirs):
            raise IOError("dir does not exist {0}".format(path))
        for key in self.files.keys():
            if key.startswith(path):
                if key == path:
                    raise IOError("given dir is file{0}".format(path))
                else:
                    trimmed_key = key.replace(path,"")
                    # /foo/bar.txt
                    # /foo.txt
                    trimmed_key_parts = trimmed_key.split("/")
                    result_list.append(trimmed_key_parts[1])
        return result_list
    
    def isfile(self, path):
        if self.files.has_key(path):
            return True
        return False
    
    def exists(self,path):
        if self.files.has_key(path):
            return True
        if path in self.dirs:
            return True
        return False
    
    def isdir(self,path):
        if path in self.dirs:
            return True
        return False
    
    def rmdir(self, path):
        if path in self.dirs:
            self.dirs.remove(path)
            
    def clean_out_dir(self,dirpath):
        keys_to_remove = []
        for key in self.files.keys():
            if key.startswith(dirpath):
                keys_to_remove.append(key)    
        for key in keys_to_remove:
            print "removing file {0}".format(key)
            self.files.pop(key)                   

    def open_file(self, path, mode):
        if (mode == 'w'):
            mfile = mock_file.MockFile(path)
            self.files[path] = mfile
            parent = os.path.dirname(path)
            if (not(parent in self.dirs)):
                self.dirs.append(parent)
            return mfile
        else: # mode == 'r'
            if not(self.files.has_key(path)):
                raise IOError("file does not exist : {0}".format(path))
            mfile = self.files[path]
            return mfile  
                
    
    