'''
Created on Feb 23, 2014

@author: irvine
'''
import cluster_script
class SpecHelp(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def express(self):   
        print("#cspec")
        print("# The very first line of the file must start with #cspec")
        print("############################################################################")
        print("#  trials - specify the number of trials you want to run. Each permutation  ")
        print("#           will be run that many times.  Value must be integer.")
        print("############################################################################")
        print("trials:1")
        print("  ")
        print("  ")
        print("############################################################################")
        print("  command - one or more command lines specify which commands to run.  ")
        print("      - to enable concise command lines, <replace> declarations elsewhere ")
        print("        in the file can be used to enable cleaner command lines ")
        print("      - each command line can contain permuters (declared elsewhere ")
        print("        in this file) that control parameter choice")
        print("      - each permuter is contained in parenthesis, i.e. (t_val)")
        print("      - the algorithm must allow the output file path to be passed in as an")
        print("        argument, so that the <permutation_result_dir> can be the dir containing")
        print("        the result for that permutation.  This enables status commands to function")
        print("      - <permutation_results_dir> is computed automatically for each permutation")
        print("        using this scheme <root_dir>/<cspec_name>/results/<permCode>")
        print("        where permCode is built from the permute variables, values, and trial number")
        print("        NOTE : root_dir is defined by the user in the cspec (see below)")
        print("        NOTE : trial is the value of the specific trial from among the value of 'trials:'")
        print("        NOTE : <permCode> is a code representing a particular permutation.  It is")
        print("        computed by permuter (i.e. not specified by the user)")
        print("############################################################################")
        print("command:<alg_dir>/some_algorithm -i (year)/(month)/mydata.csv -o <permutation_result_dir>/rawresult.csv -t (t_val)")
        print("command:<alg_dir>/post_processor -i <permutation_result_dir>/rawresult.csv -o <permutation_result_dir>/finalresult.csv")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# one_up_basis - each permutation is assigned a one-up number to make it easier ")
        print("#       to keep track of them.  The number appears after the cspec_name. ")
        print("#       For example,  somename_j00_t_1_f_3.sh.")
        print("#       Since the remainder of the job name can become quite dense (denser the ")
        print("#       more permuters in play), the number can be an easier way to discriminate")
        print("#       job and file names.  The number series will start at the one_up_basis value, ")
        print("#       so if you have two cspecs in play, you might want to start the numbering ")
        print("#       for one of them at 0 and another at 1000.  Any integer is ok.")
        print("############################################################################")
        print("one_up_basis:0")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# permute - permute declarations specify variables that hold a range of one  ")
        print("#       or more values.  For each permutation, that variable will be replaced ")
        print("#       by the appropriate value from the list.")
        print("#")  
        print("#       In version 0.3, it is permute:, in version 1.0, is is (permute):")   
        print("#")     
        print("# examples:")
        print("#       permute:color=red,blue,green  # comma separated list of strings")
        print("#       permute:month=2010,2011,2012  # comma separated list - numbers are")
        print("#                                     # just treated as strings")
        print("#       permute:f_val= range(3,6)     # generates a range of integers - this")
        print("#                                     # would resolve to 3,4,5,6")
        print("#         (NOTE in version 0.3, this used to be expressed as permute:f_val=3 6)")
        print("#       permute:t_val= 7 # singletons ok")
        print("#")
        print("#       Elsewhere in the file, permute values are expressed inside ")
        print("#       parentheses:  (b_val)")
        print("# ")
        print("#       permute values can be used to pick which dataset to use, or which ")
        print("#       algorithm arguments to use.  In fact, permuters can be used anywhere")
        print("#       in the command line or in replace expressions.")
        print("############################################################################")
        print("permute:some_val=1,2,3")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# concise_print - permuters and permute values are used in filenames or as ")
        print("#       column names in collected results.  To help make these more readable, the ")
        print("#       concise_print declaration specifies a shorthand code for each value")
        print("############################################################################")
        print("concise_print:a_val,a")
        print("concise_print:b_val,b")
        print("concise_print:typeXYZ,xyz")
        print("concise_print:s_val,s")
        print("concise_print:t_val,t")
        print("concise_print:k_val,k")
        print("concise_print:AlUdRawCounts,Raw")
        print("concise_print:AlUdCoUq,CoUq")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# scores_permute - scores_permute is an optional special permuter.  It is used")
        print("#       when a single permutation run generates multiple output files. In other")
        print("#       words, there are more than one file which contain answer values that ")
        print("#       need to be collected by the 'collect' command.  It has no effect unless")
        print("#       the scores_permuter is referenced by the scores_from field, which must")
        print("#       replicate the output file path. See the scores_from for an example.")
        print("#  ")
        print("#  ")
        print("############################################################################")
        print("scores_permute:resolution=userDay,userMonth")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# scores_from - This field is not optional as it serves one primary purpose ")
        print("#       in addition to an optional one.  In order for the stat commands to ")
        print("#       work, they need to know where the output files are so they can see")
        print("#       if they have been created yet.  Since permuter.py is not smart enough")
        print("#       to deduce which 'command:' line's substring represents the output file, ")
        print("#       that information needs to be exactly replicated in the scores_from field.")
        print("#       ")
        print("#       The value of the scores_from field is a comma separated list.  This ")
        print("#       supports the optional purpose, which is the 'collect' command.  In order")
        print("#       for the collect command to find the numeric 'answer' for the run, it  ")
        print("#       needs to know the coordinates of that number, which is expressed like this:")
        print("#       ")
        print("#       pathname_of_the_file, column_name_of_answer, line_number_of_answer")
        print("#       ")
        print("#       Note that if you are not using collect, you need to put bogus values")
        print("#       in for column_name_of_answer, line_number_of_answer to keep the spec")
        print("#       parser from throwing an error.")
        print("#       ")
        print("#       If scores_permute: is in play, it would appear in the scores_from pathname.")
        print("#       We'll show two examples - one with and one without scores_permute")
        print("############################################################################")
        print("scores_from:file=<permutation_results_dir>/score_out_(resolution).csv,column_name=auc,row_number=1")
        print("scores_from:file=<permutation_results_dir>/score_out.csv,column_name=auc,row_number=1")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# scores_to - This field specifies the root dir of where the collected scores")
        print("#       will be put.  It is only needed if 'collect' is being used")
        print("############################################################################")
        print("scores_to:/nfs/guille/bugid/optimization/collected_scores")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# scores_y_axis:")
        print("# scores_x_axis: - these two fields work together to support the collect command.")
        print("#       They can be omitted if 'collect' will not be used.")
        print("#       ")
        print("#       Let's say you have four permuters in play: month, fv_type, f_val and t_val.")
        print("#       When collect runs, it will want to know how to combine scores that it finds.")
        print("#       Collect is currently rigged to ...   ADD MORE HERE")
        print("############################################################################")
        print("scores_y_axis:month,fv_type")
        print("scores_x_axis:f_val,t_val")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# replace:   (version 0.3)")
        print("# <replace>: (version 1.0)")
        print("#       - replace statements allow for long pathnames to be compressed. Consider")
        print("#       the pathname /one/two/three/four/five/six/seven/eight/nine/ten.")
        print("#       This pathname can be represented as <aaa>/four/five/six/seven/eight/nine/ten")
        print("#       if there is a replace:aaa=/one/two/three")
        print("#       ")
        print("#       Taking a step further, defining replace:bbb=aaa/four/five/six/seven")
        print("#       will evaluate to full path if you use <bbb>/eight/nine/ten")
        print("#       ")
        print("#       replace: statements can include permuters in addition to other replace ")
        print("#       statements.")
        print("############################################################################")
        print("<replace>:project_root=/nfs/guille/bugid/adams/prodigalNet")
        print("<replace>:fv_root=<project_root>/fv")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# complicated tricks with replace and permute - ")
        print("#       Let's say I have to match a directory pattern to reference input files")
        print("#       where the dir pattern looks like")
        print("#           /foo/2010/abc/input.csv")
        print("#           /foo/2011/abc/input.csv")
        print("#           /foo/2012/xyz/input.csv")
        print("#       ")
        print("#       Note how abc appears under both 2010 and 2011, but xyz appears under 2012")
        print("#       If we have:")
        print("#           (permute):year=2010,2011,2012")
        print("#           <replace>:config_for_year[2010]=abc")
        print("#           <replace>:config_for_year[2011]=abc")
        print("#           <replace>:config_for_year[2012]=xyz")
        print("#       ...then the following would resolve these correctly, since the permuter")
        print("#       would be resolved, then the replace would be resolved.")
        print("############################################################################")
        print("<replace>:input_file=/foo/(year)/<config_for_year[(year)]>/input.csv")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# root_dir - used to compute <permutation_results_dir as follows: ")
        print("#       ")
        print("      - <permutation_results_dir> is computed automatically for each permutation")
        print("        using this scheme <root_dir>/<cspec_name>/results/<permCode>")
        print("        where permCode is built from the permute variables, values, and trial #")
        print("        NOTE : root_dir is defined by the user in the cspec (see below)")
        print("        NOTE : trial is the value of the specific trial from among the value of 'trials:'")
        print("        NOTE : <permCode> is a code representing a particular permutation.  It is")
        print("        computed by permuter (i.e. not specified by the user)")
        print("#       ")
        print("#       So, as should be obvious, root_dir is the root directory for all")
        print("#       files generated by this spec")
        print("############################################################################")
        print("root_dir:/someDir/myRuns")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# script_dir - the location where scripts will be generated.  It will also be ")
        print("#       where .qil, .err, .out, .qacct files are put.   Here's what each of these is")
        print("#       ")
        print("#       *.err - file generated for each script that captures errors emitted by the script")
        print("#       *.out - receives stdout from the script and algorithm")
        print("#       *.qil - 'qsub invocation log' captures output of the qsub commands which includes")
        print("#                the cluster job number.  This allows permuter to tie its job numbers to")
        print("#                the job number known to the cluster")
        print("#       *.qacct - after a run is finished, 'collect' wants to know stats of the run such")
        print("#                as cpu time, maxvmem, etc.  the cluster command 'qacct run#' yields that ")
        print("#                info and it is captured in this file")
        print("#                NOTE - qacct takes a long time to run so collect can take a good while ")
        print("#                if the job count is high. ")
        print("############################################################################")
        print("script_dir:<project_root>/<cspec_name>/scripts")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# qsub_command: - these values are routed into each script file and wind up ")
        print("#       with the syntax: ")
        print("#       ")
        print("#       #$ some_value")
        print("#       ")
        print("#       For example, ")
        print("#       ")
        print("#       qsub_command:-q eecs,eecs2,share")
        print("#       ")
        print("#       ...specifies which queues are requested")
        print("#       ")
        print("#       ")
        print("#       NOTE - some script content is automatically generated, such as specifying ")
        print("#       a name for the run - it includes the one-up run number, the trial number ")
        print("#       and permutation code and t.")
        print("#       #$ -N runtest-j00_1_x_1_y_1_1")
        print("#       ")
        print("#       Also automatically generated are filenames for error and stdout content to ")
        print("#       be routed to:")
        print("#       ")
        print("#       #$ -o j00_1_x_1_y_1.out")
        print("#       #$ -e j00_1_x_1_y_1.err")
        print("#       ")
        print("#       NOTE - qsub_command:-cwd for now needs to be included in the spec to ensure that ")
        print("#       *.qil, *.err, *.out, *.acct files are routed to the appropriate dir (i.e.")
        print("#       the script dir) ")
        print("#       ")
        print("#       ")
        print("#############################################################################")
        print("qsub_command:-q eecs,eecs2,share")
        print("qsub_command:-cwd")
        print("  ")
        print("  ")
        print("############################################################################")
        print("# ASSUMPTIONS of permuter.py")
        print("############################################################################")
        print("#   - the output pathname of the run is exposed as an argument thus appears as ")
        print("#     a substring of one of the command: fields")
        print("#")
        print("#   - the output pathname of the run is replicated as the first field of the ")
        print("#     scores_from value")
        print("#")
        print("#   - for collect to function, it is assumed that the answer of interest (the")
        print("#     one that will be collected) is located in a csv file, which has a header")
        print("#     line where the column containing the answer has a name, and is in the 2nd or")
        print("#     later line of the file.")
        print("#")
        print("#   - qsub_command:-cwd for now needs to be included in the spec to ensure that ")
        print("#     *.qil, *.err, *.out, *.acct files are routed to the appropriate dir (i.e.")
        print("#      the script dir) ")
        print("#")
        print("############################################################################")
        print("# OTHER NOTES")
        print("############################################################################")
        print("#  permuter.py appends a command to each script that touches a file in the ")
        print("#  results dir for each run, with this name ")
        print("#  ")
        done_file = cluster_script.get_done_marker_filename()
        print("#  touch <permutation_results_dir>/{0}".format(done_file))
        print("#  ")
        print("#  This file is used to signal that the script has run through all of its commands.")
        print("#  It does not signify that all commands ran error-free.  it is used by the stat")
        print("#  commands to help assess the state of the runs")

