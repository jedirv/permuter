import unittest
import test_cluster_spec
import test_permutations
import test_pooled_results
import test_permuter
import test_system
import test_ranked_results_file
import test_mock_cluster_system
import test_user_usage

def main():
    mySuite = suite()
    runner=unittest.TextTestRunner()
    runner.run(mySuite)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_cluster_spec.TestClusterSpec))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_permutations.TestPermuter))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_pooled_results.TestPooledResultsFile))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_permuter.TestPermuter))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_system.TestSystem))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_ranked_results_file.TestRankedResultsFile))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_mock_cluster_system.TestMockClusterSystem))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_user_usage.TestUserUsage))
    return test_suite
    
if __name__ == '__main__':
    main()