'''
Created on Nov 1, 2016

@author: Jed Irvine
'''
import unittest
from permute import qstat_log

class TestQstatLog(unittest.TestCase):


    def testLoadXml(self):
        path = './qstat_out.xml'
        qstat = qstat_log.QStatLog("ignored_dir", "ignored_name")
        qstat.ingest_from_path(path)
        self.assertTrue(qstat.run_state['runtest-j08_1_x_3_y_3_1'] == 'r')
        self.assertTrue(qstat.run_number['runtest-j08_1_x_3_y_3_1'] == '5911601')
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()