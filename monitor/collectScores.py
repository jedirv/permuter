import os, sys
from permute import cluster_spec
from permute import permutations
import pooled_results_file
import pooled_results_delta_file

def main():
    if (len(sys.argv) < 1):
        usage()
        exit()
    cspec_path = sys.argv[1]
    if (not(cluster_spec.validate(cspec_path))):
        exit()
    cspec = cluster_spec.ClusterSpec(cspec_path)
    
    

        

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

def usage():
    print "usage:  countScores <path of cluster_spec>"
    
def main2():
    foo = [ 's_1_k_231', 's_3_k_3','s_1_k_2','s_1_k_1','s_15_k_11','s_1_k_10.234',]   
    print foo
    bar = alphanum_sort(foo)   
    print bar
if __name__ == '__main__':
    main()
	
