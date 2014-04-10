'''
Created on Mar 14, 2014

@author: admin-jed
'''
import getpass
import os
from time import strftime

class UserUsage(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def clear(self):
        username = getpass.getuser()
        log_dir = "user_usage"
        if (not os.path.exists(log_dir)):
            pass
        else:
            logfilename = "{0}/{1}_counts.txt".format(log_dir, username)
            if (os.path.exists(logfilename)):
                os.remove(logfilename)
                
    # override this
    def log_command(self, command):
        timestamp = strftime("%Y-%m-%d %H:%M:%S")
        logline = "{0} {1}\n".format(timestamp, command)
        username = getpass.getuser()
        log_dir = "user_usage"
        if (not os.path.exists(log_dir)):
            os.mkdir(log_dir)
        logfilename = "{0}/{1}_counts.txt".format(log_dir, username)
        if (os.path.exists(logfilename)):
            f = open(logfilename, 'a')
            f.write(logline)
            f.close()
        else:
            f = open(logfilename, 'w')
            f.write(logline)
            f.close()
            