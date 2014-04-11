'''
Created on Mar 14, 2014

@author: admin-jed
'''
import unittest
import getpass

from permute import user_usage

class TestUserUsage(unittest.TestCase):

    
        
    def test_append(self):
        uu = user_usage.UserUsage()
        uu.clear()
        uu.log_command("foo")
        username = getpass.getuser()
        log_dir = "user_usage"
        logfilename = "{0}/{1}_counts.txt".format(log_dir, username)
        f = open(logfilename, 'r')
        lines = f.readlines()
        f.close()
        self.assertTrue(len(lines) == 1)
        date, time, command = lines[0].rstrip().split(' ')
        self.assertTrue(command=="foo")
        
        uu.log_command("bar")
        uu.log_command("baz")
        f = open(logfilename, 'r')
        lines = f.readlines()
        f.close()
        self.assertTrue(len(lines) == 3)
        date, time, command = lines[0].rstrip().split(' ')
        self.assertTrue(command=="foo")
        date, time, command = lines[1].rstrip().split(' ')
        self.assertTrue(command=="bar")
        date, time, command = lines[2].rstrip().split(' ')
        self.assertTrue(command=="baz")
        
if __name__ == '__main__':
    unittest.main()
    
   