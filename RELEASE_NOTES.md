permuter.py v0.2
================

New Features
------------
* python permuter.py stop <cspec_path>                  # stops all runs that are still running
* python permuter.py clean_scripts <cspec_path>         # erases **ALL** contents of the scripts dir
* python permuter.py clean_results <cspec_path>         # erases **ALL** contents of the results dir
* python permuter.py clean_pooled_results <cspec_path>  # erases **ALL** contents of the pooled_results dir
* python permuter.py clean_all <cspec_path>             # runs all four of the prior four, for when you want to start from scratch
* log file is now sent to ~/permuter/permuter.log
* adding -debug at the end of the permuter.py invocation line will put the log into verbose mode

Bugs fixed
----------
* running stat after test_launch no longer crashes
* running stop deletes .qil files so that stat no longer reports stopped jobs as running
* running launch or test_launch will first delete results and pooled results so new results won't mix with old
