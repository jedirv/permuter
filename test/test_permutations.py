import unittest
from permute import cluster_spec
from permute import permutations

class TestPermuter(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)
        
    def test_expand_permutations(self):
        permuters = self.cspec.permuters
        dict_list = permutations.expand_permutations(permuters)
        #print dict_list
        self.assertTrue(len(dict_list) == 6)
        dict1 = {'number': '1', 'letter': 'AAA', 'singleton_val': '300'}
        dict2 = {'number': '1', 'letter': 'BBB', 'singleton_val': '300'}
        dict3 = {'number': '2', 'letter': 'AAA', 'singleton_val': '300'}
        dict4 = {'number': '2', 'letter': 'BBB', 'singleton_val': '300'}
        dict5 = {'number': '3', 'letter': 'AAA', 'singleton_val': '300'}
        dict6 = {'number': '3', 'letter': 'BBB', 'singleton_val': '300'}
        self.assertTrue(dict1 in dict_list)
        self.assertTrue(dict2 in dict_list)
        self.assertTrue(dict3 in dict_list)
        self.assertTrue(dict4 in dict_list)
        self.assertTrue(dict5 in dict_list)
        self.assertTrue(dict6 in dict_list)
        
           
    def test_resolve_permutation(self):
        permute_dict = {'number': '1', 'letter': 'AAA'}
        commands = ['ls -la /nfs/(number)/(letter)/<pretty[(letter)]>']
        kv = {}
        kv['pretty[AAA]'] = 'aaa'
        kv['pretty[BBB]'] = 'bbb'
        resolved_commands = permutations.resolve_permutation(permute_dict, commands, kv)
        self.assertTrue(len(resolved_commands) == 1)
        self.assertTrue(resolved_commands[0] == 'ls -la /nfs/1/AAA/aaa')


    def test_generate_permutation_code(self):
        permute_dict = {'number': '1', 'letter': 'AAA', 'trials': '1'}
        concisePrintMap = { 'number': 'n', 'AAA':'A'}
        code = permutations.generate_permutation_code(permute_dict, concisePrintMap, False)
        self.assertTrue(code == 'letter_A_n_1')     
        code = permutations.generate_permutation_code(permute_dict, concisePrintMap, True)
        self.assertTrue(code == 'letter_A_n_1_trials_1')      
        
if __name__ == '__main__':
    unittest.main()
    
   