import unittest
from permute import cluster_spec
import test_cluster_spec
import test_permuter

def main():
    mySuite = suite()
    runner=unittest.TextTestRunner()
    runner.run(mySuite)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_cluster_spec.TestClusterSpec))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_permuter.TestPermuter))
    return test_suite
    
if __name__ == '__main__':
    main()