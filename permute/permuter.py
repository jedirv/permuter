'''
Created on Nov 19, 2013

@author: admin-jed
'''
import sys, os
import cluster_spec
import cluster_runs_info
import logging
import permutation_driver
import spec_help
import user_usage
import stdout
import cluster

def main():
    if (len(sys.argv) == 2 and sys.argv[1] == "spec_help"):
        spechelp = spec_help.SpecHelp()
        spechelp.express()
        uu = user_usage.UserUsage()
        uu.log_command("spec_help", '')
        exit()
        
    if (len(sys.argv) < 3 or len(sys.argv) > 5):
        usage()
        exit()
    cspec_path = sys.argv[1]
    permute_command = sys.argv[2]
    if len(sys.argv) == 3:
        scope = ''
        debug = False
    elif len(sys.argv) == 4:
        if sys.argv[3] == '-debug':
            scope = ''
            debug = True
        else:
            scope = sys.argv[3]
            debug = False
    else:  #len(sys.argv) == 5
        if (sys.argv[4] != '-debug'):
            usage()
        else:
            scope = sys.argv[3]
            debug = True
        
    #real_cluster_system = cluster_system.ClusterSystem()
    if (permute_command == "new_spec"):
        cluster_spec.generate_new_spec(cspec_path)
        uu = user_usage.UserUsage()
        uu.log_command(permute_command,'')
        exit()
        
   
    # set up logging 
    home_dir_permuter = os.path.expanduser('~/permuter')
    logging_level = logging.INFO
    if (debug):
        logging_level = logging.DEBUG
    if (not(os.path.isdir(home_dir_permuter))):
        os.makedirs(home_dir_permuter)
    logging.basicConfig(filename='{0}/permuter.log'.format(home_dir_permuter), filemode='w', level=logging_level)
    
    validate_args(permute_command, scope)
    validate_cspec_is_cspec(cspec_path)
    
    f = open(cspec_path, 'r')
    cspec_lines = f.readlines()
    f.close()
    true_stdout = stdout.Stdout()
    if (not(cluster_spec.validate(cspec_lines, true_stdout))):
        exit()
    cspec = cluster_spec.ClusterSpec(cspec_path, cspec_lines, true_stdout)
    cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec, true_stdout)
    hp_cluster = cluster.Cluster(cluster_runs, true_stdout)
    pdriver = permutation_driver.PermutationDriver(cspec_lines, cspec_path, true_stdout, hp_cluster)
    uu = user_usage.UserUsage()
    uu.log_command(permute_command, scope)
    pdriver.run_command(permute_command, scope)


def validate_args(command, scope):
    if (command == 'count' or command == 'preview' or command == 'gen'):
        return
    if (command == 'test_launch' or command == 'launch' or command == 'retry'):
        return
    if (command == 'summary' or command == 'stat' or command == 'pending' or command == 'errors'):
        return
    if (command == 'stop' or command == 'clean_runs'):
        return
    #if (command == 'launch_job' or command == 'stat_job' or command == 'stop_job' or command == 'clean_job'):
    #    if is_plausible_job_number(scope):
    #        return
    #    else:
    #        print "scope must be a job number of the form 'j123'"
    #        usage()
    #        exit()
    if (command == 'clean_scripts' or command == 'clean_results'):
        return
    usage()
    exit()
    
def validate_cspec_is_cspec(cspec_path):
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
  
def usage():
    print "usage:  python permuter.py spec_help"
    print"               # prints documentation for the cspec file contents."  
    print ""
    print "or"
    print ""
    print "usage:  python permuter.py <path of cluster_spec> <command> [scope]  [-debug]"  # TODOadd [scope]
    print ""
    print "   where some_command can be..."
    print"        ...for generating a template cspec file" 
    print"               new_spec               # generate a template cspec file the user can fill out"  
    print""            
    print"        ...for actions to launch permutations"              
    print"               count                  # show the number of scripts that will be generated"                   
    print"               preview                # print to stdout what the first script generated will look like"     
    print"               gen                    # generate cluster scripts"                 
    print"               test_launch            # launch the first script to see if it runs successfully (cleans downstream files first)"            
    print"               launch                 # launch all the generated cluster scripts that aren't already running (cleans downstream files first)"
    print"               retry                  # retry any jobs that have not run cleanly (clean downstream files first)" 
    print""
    print"         ...for assessing the status of permutation runs that have been launched:"                      
    print"               summary                # show the summary counts of status of runs"                   
    print"               stat                   # show the status of each permutation run"                    
    print"               pending                # show the status of each permutation run that is still running"                
    print"               errors                 # show the runs that have issues"
    print""                
    print"        ...for actions to run after permutations have launched"               
    print"               stop                   # call qdel on any runs that are unfinished to abort them"   
    print"               clean_runs             # stop running jobs, clean everything but scripts" 
    #print"               collect                # created pooled results from results"  
    print""      
    print"        ...surgical commands that are normally handled in aggregate"
    print"               launch_job j<#>        # launch job by number"                    
    print"               stat_job j<#>          # show the status of desired permutation run"
    print"               stop_job j<#>          # call qdel on any runs that are unfinished to abort them"
    print"               clean_job j<#>         # clean downstream files for job"                    
    print"               clean_scripts          # clean the launch scripts and associated .out, .err, and .qil files"          
    print"               clean_results          # clean only the contents of <permutation_results_dir>" 
    #print"               clean_pooled_results   # clean only the pooled results"           
    print""
    print""
    print"  -debug will enable DEBUG level logging which is 'INFO' level by default.  Log sent to ~/permuter/permuter.log"                      
    #print"               stat_all               # show the summary status of all specs."                                     
    #print"               stat_full_all          # show the status of each permutation run for all specs."                                     
    #print"               stat_pending_all       # show the status of each permutation run that is not finished for all specs"   

    
if __name__ == '__main__':
    main()
    
