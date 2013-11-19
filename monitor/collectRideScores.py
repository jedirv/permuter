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
	
    #perm_sets = ["ride_s_1_k_1-10_a", "ride_s_0.9_k_4", "ride_s_0.9_k_3", "ride_s_0.1_k_3","ride_s_0.1_k_10"]
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
    for fv in fvs:
        for resolution in resolutions:
            createResultFile(months, perm_sets, fv, resolution)
		
def createResultFile(months, perm_sets, fv, resolution):
    parent = "./ride_scores_c"
    if (not(os.path.isdir(parent))):
        os.makedirs(parent)
    output_path = "{0}/rideScores_{1}_{2}.csv".format(parent,resolution, fv)
    print("creating output {0}".format(output_path))
    f = open(output_path, 'w')
    # write header
    header = "month,"
    for perm_set in perm_sets:
        perm_set_dir = "/nfs/guille/bugid/adams/prodigalNet/cluster_perms/{0}".format(perm_set)
        perm_set_subdir_list = os.listdir(perm_set_dir)
        sorted_perm_set_subdir_list = alphanum_sort(perm_set_subdir_list)
        for perm_set_subdir in sorted_perm_set_subdir_list:
            header = "{0}{1},".format(header,perm_set_subdir)
    header = header.rstrip(',')
    f.write("{0}\n".format(header))
    
    #write each month
    for month in months:
        aucs = []
        line = "{0},".format(month)
        for perm_set in perm_sets:
            perm_set_dir = "/nfs/guille/bugid/adams/prodigalNet/cluster_perms/{0}".format(perm_set)
            perm_set_subdir_list = os.listdir(perm_set_dir)
            sorted_perm_set_subdir_list = alphanum_sort(perm_set_subdir_list)
            for perm_set_subdir in sorted_perm_set_subdir_list:
                print "...{0} {1} {2}".format(perm_set_subdir, perm_set, month)
                result_path = "/nfs/guille/bugid/adams/prodigalNet/cluster_perms/{0}/{1}/{2}/{3}RIDE/score_out_{4}.csv".format(perm_set, perm_set_subdir, month, fv, resolution)
                if (os.path.isfile(result_path)):
                    print "load result from {0}".format(result_path)
                    result_file = open(result_path, 'r')
                    header = result_file.readline()
                    line_of_interest = result_file.readline()
                    parts = line_of_interest.split(",")
                    auc = parts[4]
                    line = "{0}{1},".format(line,auc)
                    result_file.close()
                else:
                    line = "{0}{1},".format(line,"NA")
        line = line.rstrip(',')
        line = "{0}\n".format(line)
        f.write(line)
    f.close
    
#def find_longest_value(alphanum_list, index):
#    max_len = 0
#    for entry in alphanum_list:
#        parts = entry.split("_")
#        val = parts[index]
#        cur_len = len(val)
#       if (cur_len > max_len):
#            max_len = cur_len
#    return max_len

def find_longest_integer_portion(alphanum_list, index):
    max_len = 0
    for entry in alphanum_list:
        parts = entry.split("_")
        val = parts[index]
        # number could be float or integer, isolate the integer portion
        number_as_integer_string = str(int(float(val)))
        cur_len = len(number_as_integer_string)
        if (cur_len > max_len):
            max_len = cur_len
    return max_len
    
def alphanum_sort(alphanum_list):
    sample_entry = alphanum_list[0]
    parts = sample_entry.split("_")
    column_natures = []
    index = 0
    for part in parts:
        if (part.isalpha()):
            column_natures.append("alpha")
        else:
            column_natures.append("number")
        index = index + 1
    #print "column_natures {0}".format(column_natures)
        
    # for each column, find the one with the most digits
    index = 0
    column_widths = []
    for column_nature in column_natures:
        if (column_nature == "alpha"):
            column_widths.append("NA")
        else:
            # must be number
            column_widths.append(find_longest_integer_portion(alphanum_list, index))
        index = index + 1
       
    #print "column_widths {0}".format(column_widths)       
    # for each entry, expand the relevant_columns to form a sortable string
    result_map = {}
    sortable_list = []
    for entry in alphanum_list:
        parts = entry.split("_")
        index = 0
        result = ""
        for part in parts:
            #print "part is {0}".format(part)
            #print "column_natures[index] is {0}".format(column_natures[index])
            if (column_natures[index] == "alpha"):
                result = "{0}{1}_".format(result,part)
            #elif (column_natures[index] == "integer"):
            #    zero_padded_integer_string = part.zfill(column_widths[index])
            #    result = "{0}{1}_".format(result,zero_padded_integer_string)
            else:
                # must be number
                integer_portion = int(float(part))
                integer_portion_as_string = str(integer_portion)
                decimal_portion = float(part) - float(integer_portion)
                decimal_portion_as_string = str(decimal_portion)
                decimal_portion_as_string_sans_leading_zero = decimal_portion_as_string.lstrip("0")
                zero_padded_integer_string = integer_portion_as_string.zfill(column_widths[index])
                #print "zero_padded_integer_string {0}".format(zero_padded_integer_string)
                if (decimal_portion_as_string_sans_leading_zero == ".0"):
                    # leave out the decimal portion
                    result = "{0}{1}_".format(result,zero_padded_integer_string)
                else:
                    result = "{0}{1}{2}_".format(result,zero_padded_integer_string,decimal_portion_as_string_sans_leading_zero)
            index = index + 1
        result = result.rstrip("_") 
        result_map[result] = entry     
        sortable_list.append(result)   
        
    # then sort the sortable list and generate the sorted original list
    final_sorted_list = []
    sortable_list.sort()
    #print "sortable_list sorted {0}".format(sortable_list)
    for entry in sortable_list:
        final_sorted_list.append(result_map[entry])
        
    return final_sorted_list
      
def main2():
    foo = [ 's_1_k_231', 's_3_k_3','s_1_k_2','s_1_k_1','s_15_k_11','s_1_k_10.234',]   
    print foo
    bar = alphanum_sort(foo)   
    print bar
if __name__ == '__main__':
    main()
	
