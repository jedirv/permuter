import unittest, os
from permute import cluster_spec
from permute import permuter

class TestSystem(unittest.TestCase):

    def setUp(self):
        path = "./gentest.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)

    def test_generate(self):
        
        permuter.generate(self.cspec)
        
        self.assertTrue(os.path.isfile('./scripts_unittest/j100_1_l_aa_number_1_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j101_1_l_bb_number_1_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j102_1_l_aa_number_2_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j103_1_l_bb_number_2_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j104_1_l_aa_number_3_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j105_1_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(os.path.isfile('./scripts_unittest/j106_2_l_aa_number_1_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j107_2_l_bb_number_1_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j108_2_l_aa_number_2_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j109_2_l_bb_number_2_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j110_2_l_aa_number_3_s_300.sh'))
        self.assertTrue(os.path.isfile('./scripts_unittest/j111_2_l_bb_number_3_s_300.sh'))
        
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j100_1_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./generated_results/unittest/trial1/l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j101_1_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./generated_results/unittest/trial1/l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j102_1_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./generated_results/unittest/trial1/l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j103_1_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./generated_results/unittest/trial1/l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j104_1_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./generated_results/unittest/trial1/l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j105_1_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./generated_results/unittest/trial1/l_bb_number_3_s_300/BBB_3_three.txt'))
        
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j106_2_l_aa_number_1_s_300.sh','echo AAA 1 300 > ./generated_results/unittest/trial2/l_aa_number_1_s_300/AAA_1_one.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j107_2_l_bb_number_1_s_300.sh','echo BBB 1 300 > ./generated_results/unittest/trial2/l_bb_number_1_s_300/BBB_1_one.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j108_2_l_aa_number_2_s_300.sh','echo AAA 2 300 > ./generated_results/unittest/trial2/l_aa_number_2_s_300/AAA_2_two.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j109_2_l_bb_number_2_s_300.sh','echo BBB 2 300 > ./generated_results/unittest/trial2/l_bb_number_2_s_300/BBB_2_two.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j110_2_l_aa_number_3_s_300.sh','echo AAA 3 300 > ./generated_results/unittest/trial2/l_aa_number_3_s_300/AAA_3_three.txt'))
        self.assertTrue(self.is_echo_line_match('./scripts_unittest/j111_2_l_bb_number_3_s_300.sh','echo BBB 3 300 > ./generated_results/unittest/trial2/l_bb_number_3_s_300/BBB_3_three.txt'))
        
        
    def is_echo_line_match(self, path, expected_content):
        print expected_content
        result = False
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if (line.startswith('echo')):
                print line
                if (line == expected_content):
                    result = True
        f.close()
        return result
    
if __name__ == '__main__':
    unittest.main()
    
   