'''
Created on Feb 19, 2014

@author: irvine
'''

class NewSpec(object):
    '''
    classdocs
    '''


    def __init__(self, cspec_path):
        '''
        Constructor
        '''
        self.cspec_path = cspec_path
        
    def persist(self):
        print "path : {0}".format( self.cspec_path)
        f = open(self.cspec_path, 'w')
        f.write("#pspec\n")
        f.write("trials:1\n")
        f.write("\n")
        f.write("<replace>:project_root=/nfs/guille/myproject\n");
        f.write("root_dir:<project_root>\n");
        f.write("<replace>:alg_dir=<project_root>/seward/git/framework/algorithms/osu/R-algos\n");
        f.write("<replace>:tools_dir=<alg_dir>/tools\n");
        f.write("#\n");
        f.write("command:<alg_dir>/some_algorithm -i <project_root>/(year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)\n");
        f.write("command:<tools_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o -technique 1 <permutation_result_dir>/finalresult_technique1.csv\n");
        f.write("command:<tools_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o -technique 2 <permutation_result_dir>/finalresult_technique2.csv\n");
        f.write("\n")
        f.write("first_job_number:0");
        f.write("\n")
        f.write("(permute):year=2011,2012,2013\n");
        f.write("(permute):month=08,09,10\n");
        f.write("(permute):t_val=1-4\n");
        f.write("concise_print:t_val,t\n");
        f.write("concise_print:month,m\n");
        f.write("concise_print:year,y\n");
        '''
        f.write("#\n");
        f.write("scores_permute:post_proc_approach=technique1,techniqu2\n");
        f.write("scores_from:file=<permutation_output_dir>/final_result_(post_proc_approach).csv,column_name=auc,row_number=1\n");
        f.write("scores_to:/nfs/guille/myproject/collected_results\n");
        f.write("scores_y_axis:year,month\n");
        f.write("scores_x_axis:t_val\n");
        f.write("#\n");
        '''
        f.write("qsub_command:-q eecs,eecs1,eecs,share\n");
        f.write("qsub_command:-cwd\n");
        f.close() 
           
    def persist_old(self):
        print "path : {0}".format( self.cspec_path)
        f = open(self.cspec_path, 'w')
        f.write("#pspec\n")
        f.write("trials:1\n")
        f.write("\n")
        f.write("<replace>:project_root=/nfs/guille/myproject\n");
        f.write("root_dir:<project_root>\n");
        f.write("<replace>:alg_dir=<project_root>/seward/git/framework/algorithms/osu/R-algos\n");
        f.write("<replace>:tools_dir=<alg_dir>/tools\n");
        f.write("#\n");
        f.write("command:<alg_dir>/some_algorithm -i <project_root>/(year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)\n");
        f.write("command:<tools_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o -technique 1 <permutation_result_dir>/finalresult_technique1.csv\n");
        f.write("command:<tools_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o -technique 2 <permutation_result_dir>/finalresult_technique2.csv\n");
        f.write("\n")
        f.write("first_job_number:0");
        f.write("\n")
        f.write("(permute):year=2011,2012,2013\n");
        f.write("(permute):month=08,09,10\n");
        f.write("(permute):t_val=1-4\n");
        f.write("concise_print:t_val,t\n");
        f.write("concise_print:month,m\n");
        f.write("concise_print:year,y\n");
        '''
        f.write("#\n");
        f.write("scores_permute:post_proc_approach=technique1,techniqu2\n");
        f.write("scores_from:file=<permutation_output_dir>/final_result_(post_proc_approach).csv,column_name=auc,row_number=1\n");
        f.write("scores_to:/nfs/guille/myproject/collected_results\n");
        f.write("scores_y_axis:year,month\n");
        f.write("scores_x_axis:t_val\n");
        f.write("#\n");
        '''
        f.write("qsub_command:-q eecs,eecs1,eecs,share\n");
        f.write("qsub_command:-cwd\n");
        f.close()