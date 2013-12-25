'''
Created on Dec 23, 2013

@author: admin-jed
'''
import sys, os
# <input_root>/(y1) <permutation_results_dir>  (x1) (x2) 
# arg1 directory
# arg2 permutation_results_dir
# arg3 x1 value
# arg4 x2 value

def main():
    if (len(sys.argv) < 5):
        usage()
        exit()
    input_dir = sys.argv[1]
    result_dir = sys.argv[2]
    if (not(os.path.isdir(result_dir))):
        os.makedirs(result_dir)
    x1 = sys.argv[3]
    x2 = sys.argv[4]
    red_count_path = "{0}/red_count_{1}_{2}.txt".format(input_dir, x1, x2)
    red_command = "ls {0} | grep red | grep {1} | grep {2} | wc > {3}".format(input_dir, x1, x2, red_count_path)
    print red_command
    os.system(red_command) 
    f = open(red_count_path, 'r')
    line = f.readline()
    line = ' '.join(line.split())
    red_count = line.split(" ")[0]
    f.close()
    
    blue_count_path = "{0}/blue_count_{1}_{2}.txt".format(input_dir, x1, x2)
    blue_command = "ls {0} | grep blue | grep {1} | grep {2} | wc > {3}".format(input_dir, x1, x2, blue_count_path)
    print blue_command
    os.system(blue_command) 
    f = open(blue_count_path, 'r')
    line = f.readline()
    line = ' '.join(line.split())
    blue_count = line.split(" ")[0]
    f.close()
    
    red_csv_file = "{0}/score_out_red.csv".format(result_dir)
    f = open(red_csv_file, 'w')
    f.write("auc\n")
    f.write("{0}\n".format(red_count))
    print "red_count {0}".format(red_count)
    f.close()

    blue_csv_file = "{0}/score_out_blue.csv".format(result_dir)
    f = open(blue_csv_file, 'w')
    f.write("auc\n")
    f.write("{0}\n".format(blue_count))
    print "blue_count {0}".format(blue_count)
    f.close()
def usage():
    print "usage:  python test_alg.py  <input_dir> <permutation_results_dir> <x1> <x2>"
    
     
if __name__ == '__main__':
    main()
    