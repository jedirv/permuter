import unittest
from permute import cluster_spec

class TestClusterSpec(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)
        
    def test_load_permutes(self):
        permutations_as_string = "{0}".format(self.cspec.permutations)
        self.assertTrue(permutations_as_string == "{'number': ['1', '2', '3'], 'letter': ['AAA', 'BBB']}")
        
    def test_concise_print_map(self):
        concise_print_map_as_string = "{0}".format(self.cspec.concise_print_map)
        self.assertTrue(concise_print_map_as_string == "{'letter': 'l', 'month': 'm'}")
           
    def test_key_val_map(self):
        kvm = self.cspec.key_val_map
        self.assertTrue(kvm['config[AAA]']=='aaa')
        self.assertTrue(kvm['config[BBB]']=='bbb')
        self.assertTrue(kvm['pretty[1]']=='one')
        self.assertTrue(kvm['pretty[2]']=='two')
        self.assertTrue(kvm['pretty[3]']=='three')
        self.assertTrue(kvm['permutation_set_name']=='unittest')
        self.assertTrue(kvm['root']=='/nfs/foo/bar')
        self.assertTrue(kvm['x_dir']=='/nfs/foo/bar/(letter)/<config[(letter)]>/(number)')
        self.assertTrue(kvm['algs_dir']=='/nfs/algs')
        self.assertTrue(kvm['tools_dir']=='/nfs/algs/tools')
        self.assertTrue(kvm['results_root']=='/nfs/foo/results/unittest')
        self.assertTrue(kvm['results_dir']=='/nfs/foo/results/unittest/(number)/(letter)')
        self.assertTrue(kvm['outfile_root']=='<pretty[(number)]>__TEST')
        self.assertTrue(kvm['dir_script']=='./scripts_unittest')
        self.assertTrue(kvm['one_up_basis']=='100')
            
    def test_commands(self):
        commands_as_string = "{0}".format(self.cspec.commands)
        self.assertTrue(commands_as_string == "['ls -la /nfs/missing > <x_dir>/<pretty[(number)]>.txt']")
           
    def test__qsub_commands(self):
        qsub_commands_as_string = "{0}".format(self.cspec.qsub_commands)
        self.assertTrue(qsub_commands_as_string == "['-q eecs,eecs1,eecs,share', '-M someone@gmail.com', '-m beas']")
           

           
if __name__ == '__main__':
    unittest.main()
    
   