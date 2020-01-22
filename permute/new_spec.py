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
        f.write("# A pspec can have one or more commands.  Here we have an algorithm run as the first ")
        f.write("# command and a post-processing step as the second. Note that in this case the final ")
        f.write("# output of this two-command sequence is the output filename specified in the second ") 
        f.write("# command: 'finalresult_technique1.csv'.  Therefore, the value of the ")
        f.write("# 'output_filename:' directive will be 'finalresult_technique1.csv'.  permuter will ")
        f.write("# consider presence of that file as indicating a successful completion of the command ")
        f.write("# sequence.  You may only have need for a single command. ")
        f.write("command:<alg_dir>/some_algorithm -i <project_root>/(year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)\n")
        f.write("command:<tools_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o -technique 1 <permutation_result_dir>/finalresult_technique1.csv\n")
        f.write("\n")
        f.write("# output_filename must match the filename (not the path) of the final result file.")
        f.write("# The path will be generated and replace the string '<permutation_result_dir>'.")
        f.write("output_filename:finalresult_technique1.csv")
        f.write("\n")
        f.write("# <replace> directives allow you to compress pathnames that appear in this file, to ")
        f.write("# simplify visual inspection.  In this cases, the following <replace> directives allow ")
        f.write("# the small strings 'alg_dir' and 'tools_dir' to appear in the commands above.")
        f.write("<replace>:project_root=/somedir/myproject\n")
        f.write("<replace>:alg_dir=<project_root>/R-algos\n")
        f.write("<replace>:tools_dir=<alg_dir>/tools\n")
        f.write("\n")
        f.write("# All script files and output files will appear underneath the root_dir. Underneath the ")
        f.write("# root dir will be another dir with the same name as this pspec file.this allows ")
        f.write("# multiple pspec files to share a common root.")
        f.write("root_dir:<project_root>\n")
        f.write("\n")
        f.write("# one-up job numbers start at 0 by default (j00, j01, etc), but this can be overridden")
        f.write("#  by specifying a different value for 'first_job_number'")
        f.write("first_job_number:0")
        f.write("\n")
        f.write("# specifying 'trials:' value greatere than 1  will cause each permutation of algorithms")
        f.write("# to be run that many times ")
        f.write("trials:1\n")
        f.write("\n")
        f.write("# 'permute:' directives control the values that will appear in the command line where ")
        f.write("# '(...)' appear.  So the following three '(permute):' directives will cause the first ")
        f.write("# command in the first permutation's script to resolve to : ")
        f.write("#         '<alg_dir>/some_algorithm -i <project_root>/2011/08/mydata.csv -o <permutation_result_dir>/rawresult.csv -t 1' ")
        f.write("# ...prior to when the replace directives are obeyed to fully resolve the string")
        f.write("(permute):year=2011,2012,2013\n")
        f.write("(permute):month=08,09,10\n")
        f.write("(permute):t_val=range(1,4)\n")
        f.write("\n")
        f.write("# the following concise_print directives allow the permutation id to look like ")
        f.write("#     'j00_t_1_m_08_y_2011_trial1'   rather than  'j00_t_val_1_month_08_year_2011_trial1'")
        f.write("concise_print:t_val,t\n")
        f.write("concise_print:month,m\n")
        f.write("concise_print:year,y\n")
        f.write("\n")
        f.write("'qsub_command:' directives cause their values to be copied verbatim into the script,")
        f.write("# preceded by '#$'")
        f.write("qsub_command:-q eecs,eecs1,eecs,share\n")
        f.write("qsub_command:-cwd\n")
        f.close() 
