'''
Created on Feb 19, 2014

@author: irvine
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, cluster_system, cspec_path):
        '''
        Constructor
        '''
        self.cluster_system = cluster_system
        self.spec_path = cspec_path
        
    def persist(self):
        cs = self.cluster_system
        f = cs.open_file(self.cspec_path)
        f.write("#cspec\n")
        f.write("# The very first line of the file must start with “#cspec”\n")
        f.write("##########################################################\n")
        f.write("# Gotchas - \n")
        f.write("# - no white spaces in declarations.\n")
        f.write("##########################################################\n")
        f.write("#  trials - specify the number of trials you want to run.\n")
        f.write("#  Each permutation will be run that many times.\n")
        f.write("##########################################################\n")
        f.write("trials:1\n")
        f.write("##########################################################\n")
        f.write("\n")
        f.write("##########################################################\n")
        

        f.write("############################################################################");
        f.write("master_job_name:ride_t_f");

        f.write("############################################################################");
        f.write("# one_up_basis - each permutation is assigned a one-up number to make it easier to keep ");
        f.write("# track of them.  The number appears at the start of the job name, such as j00_t_1_f_3.sh.");
        f.write("# Since the remainder of the job name can become quite dense (denser the more permuters in play), the number can be an easier  way  to discriminate job and file names.  The number series will start at the one_up_basis value, so if you have two cspecs in play, you might want to start the numbering for one of them at 0 and another at 1000.  Any integer is ok.");
        f.write("############################################################################");
        f.write("one_up_basis:0");

        f.write("############################################################################");
        f.write("# permute - Each permute declaration specifies that a variable name that will be used later ");
        f.write("# in the cspec.  For each permutation, that variable will be replaced by the appropriate value ");
        f.write("# from the list.");
        f.write("#");
        f.write("# acceptable format are a comma separated list:");
        f.write("#  permute:month=2010,2011,2012");
        f.write("# … or a range of integers specified by two integers separated by a space::");
        f.write("#  permute:f_val= 3 6");
        f.write("# … or a range of decimal numbers specified with a step size:");
        f.write("#  FIXME");
        f.write("# ");
        f.write("# Later on in the file, permute values are expressed inside parenthesese:  (b_val)");
        f.write("# ");
        f.write("# Note that permute values can be used to pick which dataset to use, or which algorithm arguments to use.  In fact, permuters can be used anywhere in the ");
        f.write("############################################################################");
        f.write("permute:a_val=0.02,0.03,0.04,0.05");
        f.write("permute:b_val=5,6,7,20");
        f.write("permute:type=typeXYZ, typeABC");
        f.write("############################################################################");
        f.write("# concise_print - permuters and permute values are used in filenames or as \n")
        f.write("# column names in collected results.  To help make these more readable, the \n")
        f.write("#concise_print declaration specifies a shorthand code for each value\n")
        f.write("############################################################################");
        f.write("concise_print:a_val,a");
        f.write("concise_print:b_val,b");
        f.write("concise_print:typeXYZ,xyz");
        f.write("concise_print:s_val,s");
        f.write("concise_print:t_val,t");
        f.write("concise_print:k_val,k");
        f.write("concise_print:AlUdRawCounts,Raw");
        f.write("concise_print:AlUdCoUq,CoUq");
        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("scores_permute:resolution=userDay,userMonth");
        f.write("scores_from:file=<permutation_results_dir>/score_out_(resolution).csv,column_name=auc,row_number=1");
        f.write("scores_to:/nfs/guille/bugid/adams/prodigalNet/RIDE_optimization/collected_scores");
        f.write("scores_y_axis:month,fv_type");
        f.write("scores_x_axis:f_val,t_val");
        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("<replace>:project_root=/nfs/guille/bugid/adams/prodigalNet");
        f.write("<replace>:fv_root=<project_root>/fv");
        f.write("<replace>:fv_dir=<fv_root>/(month)/<config[(month)]>/(fv_type)");
        f.write("<replace>:algs_dir=<project_root>/seward/git/framework/algorithms/osu/R-algos");
        f.write("<replace>:tools_dir=<algs_dir>/tools");
        f.write("<replace>:answer_key_dir=/nfs/guille/bugid/adams/answerKeys");
        f.write("<replace>:outfile_root=<pretty[(fv_type)]>__RIDE");


        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("#");
        f.write("# permutation-dependent mappings can be expressed like this.  These will be matched by");
        f.write("# using permutations like this:  <config[(month)]>");
        f.write("#");
        f.write("<replace>:config[2013-01]=003_a54a12478c5efcf9");
        f.write("<replace>:config[2013-02]=003_a54a12478c5efcf9");
        f.write("<replace>:config[2013-03]=003_a54a12478c5efcf9");
        f.write("<replace>:config[2013-04]=003_a54a12478c5efcf9");
        f.write("<replace>:pretty[AlUdRawCounts]=DTAllUdRawCounts");
        f.write("<replace>:pretty[AlUdCoUq]=DTAllUdCoUvq");
        f.write("#");
        f.write("#");
        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("#  results_dir is where the generated results will be");
        f.write("#");

        f.write("root_results_dir:<project_root>/cluster_perms");



        f.write("#");
        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("#");
        f.write("#  script_dir is where the generated scripts will be");
        f.write("#");

        f.write("script_dir:../../../cluster/scripts_<master_job_name><tag>");


        f.write("############################################################################");
        f.write("#");
        f.write("#############################################################################");
        f.write("qsub_command:-q eecs,eecs1,eecs,share");
        f.write("#qsub_command:-M jedirv@gmail.com");
        f.write("qsub_command:-m beas");
        f.write("qsub_command:-cwd");

        f.write("############################################################################");
        f.write("#");
        f.write("############################################################################");
        f.write("#");
        f.write("command:_some_command_");


        f.close()