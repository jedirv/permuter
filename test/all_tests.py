import unittest
from permute import cluster_spec
import test_cluster_spec
import test_permutations
import test_pooled_results

def main():
    mySuite = suite()
    runner=unittest.TextTestRunner()
    runner.run(mySuite)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_cluster_spec.TestClusterSpec))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_permutations.TestPermuter))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_pooled_results.TestPooledResultsFile))
    return test_suite
    
if __name__ == '__main__':
    main()