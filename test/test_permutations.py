import unittest
import cluster_spec
import permutations
import mock_stdout

class TestPermuter(unittest.TestCase):
        
    def test_expand_permutations(self):
        stdout = mock_stdout.MockStdout()
        lines = []
        lines.append("#pspec\n")
        lines.append("(permute):number=range(1,4)\n")
        lines.append("(permute):letter=AAA,BBB\n")
        lines.append("(permute):singleton_val=300\n")
        lines.append("(permute):animal=dog,cat\n")
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines, stdout, [], False, False)
        
        permuters = cspec.permuters
        dict_list = permutations.expand_permutations(permuters)
        #print dict_list
        self.assertTrue(len(dict_list) == 12)
        dict1 = {'animal': 'cat', 'number': '1', 'letter': 'AAA', 'singleton_val': '300'}
        dict2 = {'animal': 'cat', 'number': '1', 'letter': 'BBB', 'singleton_val': '300'}
        dict3 = {'animal': 'cat', 'number': '2', 'letter': 'AAA', 'singleton_val': '300'}
        dict4 = {'animal': 'cat', 'number': '2', 'letter': 'BBB', 'singleton_val': '300'}
        dict5 = {'animal': 'cat', 'number': '3', 'letter': 'AAA', 'singleton_val': '300'}
        dict6 = {'animal': 'cat', 'number': '3', 'letter': 'BBB', 'singleton_val': '300'}
        
        dict7 = {'animal': 'dog', 'number': '1', 'letter': 'AAA', 'singleton_val': '300'}
        dict8 = {'animal': 'dog', 'number': '1', 'letter': 'BBB', 'singleton_val': '300'}
        dict9 = {'animal': 'dog', 'number': '2', 'letter': 'AAA', 'singleton_val': '300'}
        dict10 = {'animal': 'dog', 'number': '2', 'letter': 'BBB', 'singleton_val': '300'}
        dict11 = {'animal': 'dog', 'number': '3', 'letter': 'AAA', 'singleton_val': '300'}
        dict12 = {'animal': 'dog', 'number': '3', 'letter': 'BBB', 'singleton_val': '300'}
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
        permutation_info = {'number': '1', 'letter': 'AAA'}
        commands = ['ls -la /nfs/(number)/(letter)/<pretty[(letter)]>']
        kv = {}
        kv['pretty[AAA]'] = 'aaa'
        kv['pretty[BBB]'] = 'bbb'
        resolved_commands = permutations.resolve_list_for_permutation(permutation_info, commands, kv)
        self.assertTrue(len(resolved_commands) == 1)
        self.assertTrue(resolved_commands[0] == 'ls -la /nfs/1/AAA/aaa')


    def test_generate_perm_code(self):
        permutation_info = {'number': '1', 'letter': 'AAA', 'trial': '1'}
        concisePrintMap = { 'number': 'n', 'AAA':'A'}
        code = permutations.generate_perm_code(permutation_info, concisePrintMap, permutations.IGNORE_TRIALS)
        self.assertTrue(code == 'letter_A_n_1')     
        code = permutations.generate_perm_code(permutation_info, concisePrintMap, permutations.INCLUDE_TRIALS)
        self.assertTrue(code == 'letter_A_n_1_trial_1')      
        
if __name__ == '__main__':
    unittest.main()
    
   
