'''
Created on Mar 14, 2014

@author: admin-jed
'''
import unittest
import getpass
import os

import user_usage

class TestUserUsage(unittest.TestCase):

    
    def test_append(self):
        uu = user_usage.UserUsage()
        uu.clear()
        uu.log_command("foo", 'j123')
        username = getpass.getuser()
        log_dir = "user_usage"
        logfilename = "{0}/{1}_counts.txt".format(log_dir, username)
        f = open(logfilename, 'r')
        lines = f.readlines()
        f.close()
        self.assertTrue(len(lines) == 1)
        date, time, command, scope = lines[0].rstrip().split(' ')
        self.assertTrue(command=="foo")
        self.assertTrue(scope == 'j123')
        
        uu.log_command("bar", 'j123')
        uu.log_command("baz", '')
        f = open(logfilename, 'r')
        lines = f.readlines()
        f.close()
        self.assertTrue(len(lines) == 3)
        date, time, command, scope = lines[0].rstrip().split(' ')
        self.assertTrue(command=="foo")
        self.assertTrue(scope=="j123")
        date, time, command, scope = lines[1].rstrip().split(' ')
        self.assertTrue(command=="bar")
        self.assertTrue(scope == 'j123')
        date, time, command = lines[2].rstrip().split(' ')
        self.assertTrue(command=="baz")
        
if __name__ == '__main__':
    unittest.main()
    
   
