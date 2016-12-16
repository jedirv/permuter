'''
Created on Feb 13, 2014

@author: irvine
'''
import unittest
import mock_cluster_system
from permute import cluster_spec
class TestMockClusterSystem(unittest.TestCase):


    '''
   
    def test_is_cluster_job_still_running(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        mc_system.set_unittest_answers({})
        # set bogus cspec to satisfy method signature
        bogus_cspec_lines = []
        bogus_cspec_lines.append("#pspec\n")
        cspec = cluster_spec.ClusterSpec("/foo.cspec",bogus_cspec_lines,mc_system)
        mc_system.set_cluster_spec(cspec)
        self.assertTrue(mc_system.is_cluster_job_still_running("1", "na", "na") == False)
        self.assertTrue(mc_system.is_cluster_job_still_running("2", "na", "na") == False)
        mc_system.execute_command("qsub foo.sh")
        mc_system.execute_command("qsub bar.sh")
        self.assertTrue(mc_system.is_cluster_job_still_running("1", "na", "na") == True)
        self.assertTrue(mc_system.is_cluster_job_still_running("2", "na", "na") == True)
        mc_system.execute_command("qdel 1")
        self.assertTrue(mc_system.is_cluster_job_still_running("1", "na", "na") == False)
        self.assertTrue(mc_system.is_cluster_job_still_running("2", "na", "na") == True)
        mc_system.execute_command("qdel 2")
        self.assertTrue(mc_system.is_cluster_job_still_running("1", "na", "na") == False)
        self.assertTrue(mc_system.is_cluster_job_still_running("2", "na", "na") == False)
    '''
    '''    
        
    def test_execute_qsub_command(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        mc_system.set_unittest_answers({})
        # set bogus cspec to satisfy method signature
        bogus_cspec_lines = []
        bogus_cspec_lines.append("#pspec\n")
        cspec = cluster_spec.ClusterSpec("/foo.cspec",bogus_cspec_lines,mc_system)
        mc_system.set_cluster_spec(cspec)
        mc_system.execute_command("foo")
        mc_system.execute_command("bar")
        self.assertTrue(mc_system.commands[0] == "foo")
        self.assertTrue(mc_system.commands[1] == "bar")
        mc_system.execute_command("qsub foo.sh")
        mc_system.execute_command("qsub bar.sh")
        self.assertTrue(len(mc_system.running_jobs) == 2)
        self.assertTrue(mc_system.running_jobs["1"] == "foo.sh")
        self.assertTrue(mc_system.running_jobs["2"] == "bar.sh")
        mc_system.execute_command("qdel 1")
        self.assertTrue(len(mc_system.running_jobs) == 1)
        self.assertTrue(mc_system.running_jobs["2"] == "bar.sh")
        mc_system.execute_command("qdel 2")
        self.assertTrue(len(mc_system.running_jobs) == 0)
        
    '''    
        
    
    def test_delete_file(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertTrue(len(mc_system.files) == 0)
        mc_system.delete_file("deleting non existent file should be noop", "/foo/bar.txt")
        self.assertTrue(len(mc_system.files) == 0)
        f = mc_system.open_file("/foo/bar.txt",'w')
        f.write("line1\n")
        f.close() 
        self.assertTrue(len(mc_system.files) == 1)
        f = mc_system.open_file("/foo/baz.txt",'w')
        f.write("line1\n")
        f.close() 
        self.assertTrue(len(mc_system.files) == 2) 
        mc_system.delete_file("deleting existing file should work", "/foo/bar.txt")
        self.assertTrue(len(mc_system.files) == 1)
        self.assertTrue(mc_system.files.has_key("/foo/baz.txt"))
        mc_system.delete_file("deleting existinf file should work", "/foo/baz.txt")
        self.assertTrue(len(mc_system.files) == 0)
       
    def test_getcwd_chdir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertTrue(mc_system.getcwd() == '.')
        mc_system.chdir("/foo/bar")
        self.assertTrue(mc_system.getcwd() == "/foo/bar")
    
    def test_get_par_dir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        mc_system.make_dirs("/foo/bar/baz")
        self.assertTrue(mc_system.get_par_dir("/foo/bar/baz") == "/foo/bar")
        self.assertTrue(mc_system.get_par_dir("/foo/bar") == "/foo")
        self.assertTrue(mc_system.get_par_dir("/foo") == "/")
        self.assertTrue(mc_system.get_par_dir("/") == "/")
    def test_make_dirs(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        mc_system.make_dirs("/foo/bar/baz")
        self.assertTrue(mc_system.isdir("/foo/bar/baz"))
        self.assertTrue(mc_system.isdir("/foo/bar"))
        self.assertTrue(mc_system.isdir("/foo"))
      
    def test_mkdir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertFalse(mc_system.isdir("/foo/bar"))
        mc_system.mkdir("/foo/bar")
        self.assertTrue(mc_system.isdir("/foo/bar"))
              
    def test_listdir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        f = mc_system.open_file("/foo/bar.txt",'w')
        f.write("line1\n")
        f.close() 
        f = mc_system.open_file("/foo/baz.txt",'w')
        f.write("line1\n")
        f.close() 
        filenames = mc_system.listdir("/foo")
        self.assertTrue("bar.txt" in filenames)    
        self.assertTrue("baz.txt" in filenames) 
        
    def test_isfile(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertFalse(mc_system.isfile("/foo/bar.txt"))
        f = mc_system.open_file("/foo/bar.txt", 'w')
        f.write("hello world\n")
        f.close()
        self.assertTrue(mc_system.isfile("/foo/bar.txt"))
        
    def test_exists(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertFalse(mc_system.exists("/foo/bar"))
        mc_system.mkdir("/foo/bar")
        self.assertTrue(mc_system.exists("/foo/bar"))
        mc_system.rmdir("/foo/bar")
        self.assertFalse(mc_system.exists("/foo/bar"))
        
        self.assertFalse(mc_system.exists("/foo/bar.txt"))
        f = mc_system.open_file("/foo/bar.txt",'w')
        f.close()
        self.assertTrue(mc_system.exists("/foo/bar.txt"))
        mc_system.delete_file("some_message","/foo/bar.txt")
        self.assertFalse(mc_system.exists("/foo/bar.txt"))
        
    def test_isdir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        self.assertFalse(mc_system.isdir("/foo/bar"))
        mc_system.mkdir("/foo/bar")
        self.assertTrue(mc_system.isdir("/foo/bar"))
        mc_system.rmdir("/foo/bar")
        self.assertFalse(mc_system.isdir("/foo/bar"))
    
    def test_clean_out_dir(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        f = mc_system.open_file("/foo/bar.txt",'w')
        f.write("line1\n")
        f.close() 
        f = mc_system.open_file("/foo/baz.txt",'w')
        f.write("line1\n")
        f.close() 
        filenames = mc_system.listdir("/foo")
        self.assertTrue("bar.txt" in filenames)    
        self.assertTrue("baz.txt" in filenames) 
        mc_system.clean_out_dir("/foo")   
        filenames = mc_system.listdir("/foo")
        self.assertTrue(len(filenames) == 0)

    def test_open_file(self):
        mc_system = mock_cluster_system.MockClusterSystem()
        f = mc_system.open_file("/foo/bar.txt",'w')
        f.write("line1\n")
        f.write("line2\n")
        f.write("line3start_")
        f.write("line3end\n")
        f.close()
        f = mc_system.open_file("/foo/bar.txt",'r')
        self.assertTrue("line1\n" == f.readline())
        self.assertTrue("line2\n" == f.readline())
        self.assertTrue("line3start_line3end\n" == f.readline())
        try:
            line4 = f.readline()
            self.fail("should have had error calling readline beyond end of file")
        except:
            self.assertTrue(True)
        f.close()
        f = mc_system.open_file("/foo/bar.txt",'r')
        lines = f.readlines()
        f.close()
        
        self.assertTrue("line1\n" == lines[0])
        self.assertTrue("line2\n" == lines[1])
        self.assertTrue("line3start_line3end\n" == lines[2])
        
    def test_assert_job_done(self):
        print "agagagagag"
        mc_system = mock_cluster_system.MockClusterSystem()
        mc_system.running_jobs['1'] = "foo1.sh"
        mc_system.running_jobs['2'] = "foo2.sh"
        mc_system.running_jobs['3'] = "foo3.sh"
        mc_system.running_jobs['4'] = "foo4.sh"
        mc_system.running_jobs['5'] = "foo5.sh"
        mc_system.running_jobs['6'] = "foo6.sh"
        self.assertTrue(len(mc_system.running_jobs) == 6)
        mc_system.assert_job_done("foo5.sh")
        self.assertTrue(len(mc_system.running_jobs) == 5)
        self.assertTrue(mc_system.running_jobs['1'] == "foo1.sh")
        self.assertTrue(mc_system.running_jobs['2'] == "foo2.sh")
        self.assertTrue(mc_system.running_jobs['3'] == "foo3.sh")
        self.assertTrue(mc_system.running_jobs['4'] == "foo4.sh")
        self.assertTrue(mc_system.running_jobs['6'] == "foo6.sh")
        mc_system.assert_job_done("foo1.sh")
        self.assertTrue(len(mc_system.running_jobs) == 4)
        self.assertTrue(mc_system.running_jobs['2'] == "foo2.sh")
        self.assertTrue(mc_system.running_jobs['3'] == "foo3.sh")
        self.assertTrue(mc_system.running_jobs['4'] == "foo4.sh")
        self.assertTrue(mc_system.running_jobs['6'] == "foo6.sh")
        mc_system.assert_job_done("foo16.sh")
        self.assertTrue(len(mc_system.running_jobs) == 4)
        self.assertTrue(mc_system.running_jobs['2'] == "foo2.sh")
        self.assertTrue(mc_system.running_jobs['3'] == "foo3.sh")
        self.assertTrue(mc_system.running_jobs['4'] == "foo4.sh")
        self.assertTrue(mc_system.running_jobs['6'] == "foo6.sh")
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()