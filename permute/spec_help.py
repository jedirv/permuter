'''
Created on Feb 23, 2014

@author: irvine
'''

class SpecHelp(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def express(self):   
        print("#cspec\n")
        print("# The very first line of the file must start with #cspec\n")
        print("############################################################################\n")
        print("#  trials - specify the number of trials you want to run. Each permutation  \n")
        print("#           will be run that many times.  Value must be integer.\n")
        print("############################################################################\n")
        print("trials:1\n")
        print("  \n")
        print("############################################################################\n")
        print("  command - one or more command lines specify which commands to run.  \n")
        print("      - to enable concise command lines, <replace> declarations elsewhere \n")
        print("        in the file can be used to enable cleaner command lines \n")
        print("      - each command line can contain permuters (declared elsewhere \n")
        print("        in this file) that control parameter choice\n")
        print("      - each permuter is contained in parenthesis, i.e. (t_val)\n")
        print("      - the algorithm must allow the output file path to be passed in as an\n")
        print("        argument, so that the <permutation_result_dir> can be the dir containing\n")
        print("        the result for that permutation.  This enables 'stat' commands and 'collect'\n")
        print("        to function\n")
        print("      - <permutation_results_dir> is computed automatically for each permutation\n")
        print("############################################################################\n")
        print("command:<alg_dir>/some_algorithm -i (year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)\n");
        print("command:<alg_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o <permutation_result_dir>/finalresult.csv\n");
        print("############################################################################\n");
        print("  master_job_name - this string will appear as a prefix to the cluster job name,\n")
        print("       and in the <permutation_result_dir> path\n")
        print("############################################################################\n");
        print("master_job_name:somename\n");
        print("  \n")
        print("############################################################################\n");
        print("# one_up_basis - each permutation is assigned a one-up number to make it easier\n ");
        print("#       to keep track of them.  The number appears after the master_job_name. \n")
        print("#       For example,  somename_j00_t_1_f_3.sh.");
        print("#       Since the remainder of the job name can become quite dense (denser the \n")
        print("#       more permuters in play), the number can be an easier way to discriminate\n")
        print("#       job and file names.  The number series will start at the one_up_basis value, \n")
        print("#       so if you have two cspecs in play, you might want to start the numbering \n")
        print("#       for one of them at 0 and another at 1000.  Any integer is ok.\n");
        print("############################################################################\n");
        print("one_up_basis:0");
        print("  \n")
        print("############################################################################\n");
        print("# permute - permute declarations specify variables that hold a range of one  \n");
        print("# or more values.  For each permutation, that variable will be replaced by the appropriate value \n");
        print("# from the list.\n");
        print("#\n");
        print("# examples:\n");
        print("#  permute:month=2010,2011,2012  # comma separated list\n");
        print("#  permute:f_val= 3-6 # a range of integers - this would resolve to 3,4,5,6\n");
        print("#  permute:t_val= 7 # singletons ok\n");
        print("# Elsewhere in the file, permute values are expressed inside parenthesese:  (b_val)\n");
        print("# \n");
        print("# permute values can be used to pick which dataset to use, or which algorithm arguments to use.\n")
        print("# In fact, permuters can be used anywhere in the command line or in replace expressions.\n");
        print("############################################################################\n");
        print("permute:some_val=1,2,3\n");
        print("############################################################################\n");
        print("# concise_print - permuters and permute values are used in filenames or as \n")
        print("# column names in collected results.  To help make these more readable, the \n")
        print("#concise_print declaration specifies a shorthand code for each value\n")
        print("############################################################################\n");
        print("concise_print:a_val,a\n");
        print("concise_print:b_val,b\n");
        print("concise_print:typeXYZ,xyz\n");
        print("concise_print:s_val,s\n");
        print("concise_print:t_val,t\n");
        print("concise_print:k_val,k\n");
        print("concise_print:AlUdRawCounts,Raw\n");
        print("concise_print:AlUdCoUq,CoUq\n");
        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("scores_permute:resolution=userDay,userMonth\n");
        print("scores_from:file=<permutation_results_dir>/score_out_(resolution).csv,column_name=auc,row_number=1\n");
        print("scores_to:/nfs/guille/bugid/adams/prodigalNet/RIDE_optimization/collected_scores\n");
        print("scores_y_axis:month,fv_type\n");
        print("scores_x_axis:f_val,t_val\n");
        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("<replace>:project_root=/nfs/guille/bugid/adams/prodigalNet\n");
        print("<replace>:fv_root=<project_root>/fv\n");
        print("<replace>:fv_dir=<fv_root>/(month)/<config[(month)]>/(fv_type)\n");
        print("<replace>:algs_dir=<project_root>/seward/git/framework/algorithms/osu/R-algos\n");
        print("<replace>:tools_dir=<algs_dir>/tools\n");
        print("<replace>:answer_key_dir=/nfs/guille/bugid/adams/answerKeys\n");
        print("<replace>:outfile_root=<pretty[(fv_type)]>__RIDE\n");


        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("#\n");
        print("# permutation-dependent mappings can be expressed like this.  These will be matched by\n");
        print("# using permutations like this:  <config[(month)]>\n");
        print("#\n");
        print("<replace>:config[2013-01]=003_a54a12478c5efcf9\n");
        print("<replace>:config[2013-02]=003_a54a12478c5efcf9\n");
        print("<replace>:config[2013-03]=003_a54a12478c5efcf9\n");
        print("<replace>:config[2013-04]=003_a54a12478c5efcf9\n");
        print("<replace>:pretty[AlUdRawCounts]=DTAllUdRawCounts\n");
        print("<replace>:pretty[AlUdCoUq]=DTAllUdCoUvq\n");
        print("#\n");
        print("#\n");
        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("#  results_dir is where the generated results will be\n");
        print("#\n");

        print("root_results_dir:<project_root>/cluster_perms\n");



        print("#\n");
        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("#\n");
        print("#  script_dir is where the generated scripts will be\n");
        print("#\n");

        print("script_dir:../../../cluster/scripts_<master_job_name><tag>\n");


        print("############################################################################\n");
        print("#\n");
        print("#############################################################################\n");
        print("qsub_command:-q eecs,eecs1,eecs,share\n");
        print("#qsub_command:-M jedirv@gmail.com\n");
        print("qsub_command:-m beas\n");
        print("qsub_command:-cwd\n");

        print("############################################################################\n");
        print("#\n");
        print("############################################################################\n");
        print("#\n");


