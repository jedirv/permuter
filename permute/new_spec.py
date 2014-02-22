'''
Created on Feb 19, 2014

@author: irvine
'''

class NewSpec(object):
    '''
    classdocs
    '''


    def __init__(self, cluster_system, cspec_path):
        '''
        Constructor
        '''
        self.cluster_system = cluster_system
        self.cspec_path = cspec_path
        
    def persist(self):
        cs = self.cluster_system
        f = cs.open_file(self.cspec_path, 'w')
        f.write("#cspec\n")
        f.write("# The very first line of the file must start with #cspec\n")
        f.write("############################################################################\n")
        f.write("#  trials - specify the number of trials you want to run. Each permutation  \n")
        f.write("#           will be run that many times.  Value must be integer.\n")
        f.write("############################################################################\n")
        f.write("trials:1\n")
        f.write("  \n")
        f.write("############################################################################\n")
        f.write("  command - one or more command lines specify which commands to run.  \n")
        f.write("      - to enable concise command lines, <replace> declarations elsewhere \n")
        f.write("        in the file can be used to enable cleaner command lines \n")
        f.write("      - each command line can contain permuters (declared elsewhere \n")
        f.write("        in this file) that control parameter choice\n")
        f.write("      - each permuter is contained in parenthesis, i.e. (t_val)\n")
        f.write("      - the algorithm must allow the output file path to be passed in as an\n")
        f.write("        argument, so that the <permutation_result_dir> can be the dir containing\n")
        f.write("        the result for that permutation.  This enables 'stat' commands and 'collect'\n")
        f.write("        to function\n")
        f.write("      - <permutation_results_dir> is computed automatically for each permutation\n")
        f.write("############################################################################\n")
        f.write("command:<alg_dir>/some_algorithm -i (year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)\n");
        f.write("command:<alg_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o <permutation_result_dir>/finalresult.csv\n");
        f.write("############################################################################\n");
        f.write("  master_job_name - this string will appear as a prefix to the cluster job name,\n")
        f.write("       and in the <permutation_result_dir> path\n")
        f.write("############################################################################\n");
        f.write("master_job_name:somename\n");
        f.write("  \n")
        f.write("############################################################################\n");
        f.write("# one_up_basis - each permutation is assigned a one-up number to make it easier\n ");
        f.write("#       to keep track of them.  The number appears after the master_job_name. \n")
        f.write("#       For example,  somename_j00_t_1_f_3.sh.");
        f.write("#       Since the remainder of the job name can become quite dense (denser the \n")
        f.write("#       more permuters in play), the number can be an easier way to discriminate\n")
        f.write("#       job and file names.  The number series will start at the one_up_basis value, \n")
        f.write("#       so if you have two cspecs in play, you might want to start the numbering \n")
        f.write("#       for one of them at 0 and another at 1000.  Any integer is ok.\n");
        f.write("############################################################################\n");
        f.write("one_up_basis:0");
        f.write("  \n")
        f.write("############################################################################\n");
        f.write("# permute - permute declarations specify variables that hold a range of one  \n");
        f.write("# or more values.  For each permutation, that variable will be replaced by the appropriate value \n");
        f.write("# from the list.\n");
        f.write("#\n");
        f.write("# examples:\n");
        f.write("#  permute:month=2010,2011,2012  # comma separated list\n");
        f.write("#  permute:f_val= 3-6 # a range of integers - this would resolve to 3,4,5,6\n");
        f.write("#  permute:t_val= 7 # singletons ok\n");
        f.write("# Elsewhere in the file, permute values are expressed inside parenthesese:  (b_val)\n");
        f.write("# \n");
        f.write("# permute values can be used to pick which dataset to use, or which algorithm arguments to use.\n")
        f.write("# In fact, permuters can be used anywhere in the command line or in replace expressions.\n");
        f.write("############################################################################\n");
        f.write("permute:some_val=1,2,3\n");
        f.write("############################################################################\n");
        f.write("# concise_print - permuters and permute values are used in filenames or as \n")
        f.write("# column names in collected results.  To help make these more readable, the \n")
        f.write("#concise_print declaration specifies a shorthand code for each value\n")
        f.write("############################################################################\n");
        f.write("concise_print:a_val,a\n");
        f.write("concise_print:b_val,b\n");
        f.write("concise_print:typeXYZ,xyz\n");
        f.write("concise_print:s_val,s\n");
        f.write("concise_print:t_val,t\n");
        f.write("concise_print:k_val,k\n");
        f.write("concise_print:AlUdRawCounts,Raw\n");
        f.write("concise_print:AlUdCoUq,CoUq\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("scores_permute:resolution=userDay,userMonth\n");
        f.write("scores_from:file=<permutation_results_dir>/score_out_(resolution).csv,column_name=auc,row_number=1\n");
        f.write("scores_to:/nfs/guille/bugid/adams/prodigalNet/RIDE_optimization/collected_scores\n");
        f.write("scores_y_axis:month,fv_type\n");
        f.write("scores_x_axis:f_val,t_val\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("<replace>:project_root=/nfs/guille/bugid/adams/prodigalNet\n");
        f.write("<replace>:fv_root=<project_root>/fv\n");
        f.write("<replace>:fv_dir=<fv_root>/(month)/<config[(month)]>/(fv_type)\n");
        f.write("<replace>:algs_dir=<project_root>/seward/git/framework/algorithms/osu/R-algos\n");
        f.write("<replace>:tools_dir=<algs_dir>/tools\n");
        f.write("<replace>:answer_key_dir=/nfs/guille/bugid/adams/answerKeys\n");
        f.write("<replace>:outfile_root=<pretty[(fv_type)]>__RIDE\n");


        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("# permutation-dependent mappings can be expressed like this.  These will be matched by\n");
        f.write("# using permutations like this:  <config[(month)]>\n");
        f.write("#\n");
        f.write("<replace>:config[2013-01]=003_a54a12478c5efcf9\n");
        f.write("<replace>:config[2013-02]=003_a54a12478c5efcf9\n");
        f.write("<replace>:config[2013-03]=003_a54a12478c5efcf9\n");
        f.write("<replace>:config[2013-04]=003_a54a12478c5efcf9\n");
        f.write("<replace>:pretty[AlUdRawCounts]=DTAllUdRawCounts\n");
        f.write("<replace>:pretty[AlUdCoUq]=DTAllUdCoUvq\n");
        f.write("#\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#  results_dir is where the generated results will be\n");
        f.write("#\n");

        f.write("root_results_dir:<project_root>/cluster_perms\n");



        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#\n");
        f.write("#  script_dir is where the generated scripts will be\n");
        f.write("#\n");

        f.write("script_dir:../../../cluster/scripts_<master_job_name><tag>\n");


        f.write("############################################################################\n");
        f.write("#\n");
        f.write("#############################################################################\n");
        f.write("qsub_command:-q eecs,eecs1,eecs,share\n");
        f.write("#qsub_command:-M jedirv@gmail.com\n");
        f.write("qsub_command:-m beas\n");
        f.write("qsub_command:-cwd\n");

        f.write("############################################################################\n");
        f.write("#\n");
        f.write("############################################################################\n");
        f.write("#\n");


        f.close()