import os, time

def main():
    months = ['2013-01', '2013-02', '2013-03', '2013-04']
    configs_for_month = {}
    configs_for_month['2012-09'] = "001_b1a2ec07893c7243"
    configs_for_month['2012-10'] = "001_b1a2ec07893c7243"
    configs_for_month['2012-11'] = "002_d1bb7a0133d13950"
    configs_for_month['2012-12'] = "002_d1bb7a0133d13950"
    configs_for_month['2013-01'] = "003_a54a12478c5efcf9"
    configs_for_month['2013-02'] = "003_a54a12478c5efcf9"
    configs_for_month['2013-03'] = "003_a54a12478c5efcf9"
    configs_for_month['2013-04'] = "003_a54a12478c5efcf9"
	
    perm_sets = ["ride_s_1_k_5_t_0.1_f_0.1"]
    #arg_sets = ["", "_ride_opt", "_ride_opt_k3_s0.1", "_ride_opt_k4_s0.9", "_ride_opt_k1_s1.0"]
    #arg_sets_pretty = {}
    #arg_sets_pretty[""] = "k=10_s=0.01"
    #arg_sets_pretty["_ride_opt"] = "k=3_s=0.9"
    #arg_sets_pretty["_ride_opt_k3_s0.1"] = "k=3_s=0.1"
    #arg_sets_pretty["_ride_opt_k4_s0.9"] = "k=4_s=0.9"
    #arg_sets_pretty["_ride_opt_k1_s1.0"] = "k=1_s=1.0"
    fvs = ['AlUdRawCounts', 'AlUdCoUq']
    resolutions = ['userDay', 'userMonth']
    count_total = 0
    count_present = 0
    for fv in fvs:
        for month in months:
            for perm_set in perm_sets:
                perm_set_dir = "/nfs/guille/bugid/adams/prodigalNet/cluster_perms/{0}".format(perm_set)
                perm_set_subdir_list = os.listdir(perm_set_dir)
                perm_set_subdir_list.sort()
                for perm_set_subdir in perm_set_subdir_list:
                    result_path = "/nfs/guille/bugid/adams/prodigalNet/cluster_perms/{0}/{1}/{2}/{3}RIDE/score_out_userDay.csv".format(perm_set, perm_set_subdir, month, fv)
                    count_total = count_total + 1
                    if (os.path.isfile(result_path)):
                        count_present = count_present + 1
                        print "...{0} {1} {2}  DONE".format(perm_set_subdir, month, fv)
                    else:
                        print "...{0} {1} {2}".format(perm_set_subdir, month, fv)
    print "{0} of {1} completed".format(count_present, count_total) 

if __name__ == '__main__':
    main()
	
