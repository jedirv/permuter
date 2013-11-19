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
        self.assertTrue(len(dict_list) == 12)
        dict1 =  {'unused_vals': 'x', 'number': '1', 'letter': 'AAA', 'singleton_val': '300'}
        dict2 =  {'unused_vals': 'x', 'number': '1', 'letter': 'BBB', 'singleton_val': '300'}
        dict3 =  {'unused_vals': 'x', 'number': '2', 'letter': 'AAA', 'singleton_val': '300'}
        dict4 =  {'unused_vals': 'x', 'number': '2', 'letter': 'BBB', 'singleton_val': '300'}
        dict5 =  {'unused_vals': 'x', 'number': '3', 'letter': 'AAA', 'singleton_val': '300'}
        dict6 =  {'unused_vals': 'x', 'number': '3', 'letter': 'BBB', 'singleton_val': '300'}
        dict7 =  {'unused_vals': 'y', 'number': '1', 'letter': 'AAA', 'singleton_val': '300'}
        dict8 =  {'unused_vals': 'y', 'number': '1', 'letter': 'BBB', 'singleton_val': '300'}
        dict9 =  {'unused_vals': 'y', 'number': '2', 'letter': 'AAA', 'singleton_val': '300'}
        dict10 = {'unused_vals': 'y', 'number': '2', 'letter': 'BBB', 'singleton_val': '300'}
        dict11 = {'unused_vals': 'y', 'number': '3', 'letter': 'AAA', 'singleton_val': '300'}
        dict12 = {'unused_vals': 'y', 'number': '3', 'letter': 'BBB', 'singleton_val': '300'}
        self.assertTrue(dict1 in dict_list)
        self.assertTrue(dict2 in dict_list)
        self.assertTrue(dict3 in dict_list)
        self.assertTrue(dict4 in dict_list)
        self.assertTrue(dict5 in dict_list)
        self.assertTrue(dict6 in dict_list)
        self.assertTrue(dict7 in dict_list)
        self.assertTrue(dict8 in dict_list)
        self.assertTrue(dict9 in dict_list)
        self.assertTrue(dict10 in dict_list)
        self.assertTrue(dict11 in dict_list)
        self.assertTrue(dict12 in dict_list)
           
    def test_resolve_permutation(self):
        permuters = self.cspec.permuters
        permute_dict = {'unused_vals': 'x', 'number': '1', 'letter': 'AAA'}
        commands = ['ls -la /nfs/(number)/(letter)/<pretty[(letter)]>']
        kv = {}
        kv['pretty[AAA]'] = 'aaa'
        kv['pretty[BBB]'] = 'bbb'
        resolved_commands = permutations.resolve_permutation(permute_dict, commands, kv)
        self.assertTrue(len(resolved_commands) == 1)
        self.assertTrue(resolved_commands[0] == 'ls -la /nfs/1/AAA/aaa')


    def test_generate_permutation_code(self):
        permute_dict = {'unused_vals': 'x', 'number': '1', 'letter': 'AAA'}
        concisePrintMap = { 'number': 'n', 'unused_vals':'u', 'AAA':'A'}
        code = permutations.generate_permutation_code(permute_dict, concisePrintMap)
        self.assertTrue(code == 'letter_A_n_1_u_x')        
        
if __name__ == '__main__':
    unittest.main()
    
   