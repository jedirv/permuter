'''
Created on Jan 22, 2014

@author: irvine
'''
import sys, os
import time

def main():
    if (len(sys.argv) < 5):
        usage()
        exit()
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    delay = int(sys.argv[3])
    outpath = sys.argv[4]
    product = x * y
    for i in range(0,product):
        time.sleep(delay)
        print "sleeping at i: {0}".format(i)
    dir = os.path.dirname(outpath)
    if not(os.path.exists(dir)):
        os.makedirs(dir);
    f = open(outpath, 'w')
    f.write("foo,auc,bar\n")
    f.write("NA,{0},NA\n".format(product))
    f.close()

def usage():
    print "python run_test <x> <y> <delay> <outfile>.csv "  
    print "    # where x and y are integers.  They will be multiplied together and "
    print "    # to yield a count of how many times the sleep-for-30-sec is called"
    print "    # also delivers that product to result file."
if __name__ == '__main__':
    main()
    