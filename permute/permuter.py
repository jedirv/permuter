'''
Created on Nov 19, 2013

@author: admin-jed
'''
import sys, os
import cluster_spec
import logging
import cluster_system
import permutation_driver
import spec_help
import user_usage

def main():
    if (len(sys.argv) == 2 and sys.argv[1] == "spec_help"):
        spechelp = spec_help.SpecHelp()
        spechelp.express()
        uu = user_usage.UserUsage()
        uu.log_command("spec_help")
        exit()
        
    if (len(sys.argv) < 3):
        usage()
        exit()
    permute_command = sys.argv[1]
    cspec_path = sys.argv[2]
        
    real_cluster_system = cluster_system.ClusterSystem()
    if (permute_command == "new_spec"):
        cluster_spec.generate_new_spec(real_cluster_system, cspec_path)
        uu = user_usage.UserUsage()
        uu.log_command(permute_command)
        exit()
        
    flags = ""
    if (len(sys.argv) == 4):
        flags = sys.argv[3]
        
    # set up logging 
    home_dir_permuter = os.path.expanduser('~/permuter')
    logging_level = logging.INFO
    if (flags == '-debug'):
        logging_level = logging.DEBUG
    if (not(os.path.isdir(home_dir_permuter))):
        os.makedirs(home_dir_permuter)
    logging.basicConfig(filename='{0}/permuter.log'.format(home_dir_permuter), filemode='w', level=logging_level)
    
    validate_args(permute_command, cspec_path, flags)
    
    f = open(cspec_path, 'r')
    cspec_lines = f.readlines()
    f.close()
    
    if (not(cluster_spec.validate(cspec_lines, real_cluster_system))):
        exit()
        
    pdriver = permutation_driver.PermutationDriver(cspec_lines, cspec_path, real_cluster_system)
    uu = user_usage.UserUsage()
    uu.log_command(permute_command)
    pdriver.run_command(permute_command)

 
def validate_args(permute_command, cspec_path, flags):
    if (not(permute_command == "collect" or 
            permute_command == "count" or 
            permute_command == "stat" or 
            permute_command == "stat_full" or 
            permute_command == "stat_pending" or 
            permute_command == "stat_all" or 
            permute_command == "stat_full_all" or 
            permute_command == "stat_pending_all" or 
            permute_command == "gen" or 
            permute_command == "launch" or 
            permute_command == "auto" or 
            permute_command == "preview" or 
            permute_command == "retry" or 
            permute_command == "stop" or 
            permute_command == "clean_scripts" or 
            permute_command == "clean_results" or 
            permute_command == "clean_pooled_results" or 
            permute_command == "clean_all" or 
            permute_command == "test_launch")):
        usage()
        exit()
    # verify spec path exists
    try:
        f = open(cspec_path, 'r')
        # verify first line has cspec flag
        header = f.readline()
        if (header != "#cspec\n"):
            print "cspec file must have this header:  '#cspec', {0} does not. Exiting.".format(cspec_path)
            f.close()
            exit()
        f.close()
    except IOError:
        print "An error occurred trying to open {0}".format(cspec_path)
        exit()
    if (flags != "-debug" and flags != ""):
        print "Invalid flag {0}. -debug is only flag supported".format(flags)
        exit()
  
def usage():
    print "usage:  python permuter.py  some_command <path of cluster_spec>  [-debug]"
    print ""
    print "   where some_command can be..."
    print"        ...for generating a template cspec file" 
    print"               new_spec               # generate a template cspec file the user can fill out"  
    print"               spec_help              # prints documentation for the cspec file contents."  
    print""            
    print"        ...for actions to launch permutations"              
    print"               count                  # show the number of permutations that will be generated"                   
    print"               preview                # print to stdout what the first script generated will look like"     
    print"               gen                    # generate cluster scripts"              
    print"               test_launch            # launch the first script to see if it runs successfully"            
    print"               launch                 # launch all the generated cluster scripts"                   
    print"               auto                   # runs gen and then launch in sequence - only use if very confident"                   
    print"               retry                  # launch any jobs that have not generated all output files (calls stop first)" 
    print""
    print"         ...for assessing the status of permutation runs that have been launched:"                      
    print"               stat                   # show the summary counts of status of runs"                   
    print"               stat_full              # show the status of each permutation run"                   
    print"               stat_pending           # show the status of each permutation run that is not finished"                    
    print"               stat_all               # show the summary status of all specs."                                     
    print"               stat_full_all          # show the status of each permutation run for all specs."                                     
    print"               stat_pending_all       # show the status of each permutation run that is not finished for all specs"   
    print""                
    print"        ...for actions to run after permutations have launched"               
    print"               stop                   # call qdel on any runs that are unfinished to abort them"                    
    print"               clean_scripts          # clean the launch scripts and associated .out, .err, and .qil files"                   
    print"               clean_results          # clean only the contents of <permutation_results_dir>" 
    print"               clean_pooled_results   # clean only the pooled results"           
    print"               clean_all              # clean scripts, results, pooled results, and stop running jobs" 
    print"               collect                # created pooled results from results"  
    print""
    print""
    print"  -debug will enable DEBUG level logging which is 'INFO' level by default.  Log sent to ~/permuter/permuter.log"  

    
if __name__ == '__main__':
    main()
    
