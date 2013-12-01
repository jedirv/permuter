import unittest
import test_cluster_spec
import test_permutations
import test_pooled_results
import test_collect_scores

def main():
    mySuite = suite()
    runner=unittest.TextTestRunner()
    runner.run(mySuite)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_cluster_spec.TestClusterSpec))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_permutations.TestPermuter))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_pooled_results.TestPooledResultsFile))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_collect_scores.TestCollectScores))
    return test_suite
    
if __name__ == '__main__':
    main()