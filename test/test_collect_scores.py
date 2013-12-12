import unittest, os
from permute import cluster_spec
from monitor import collectScores

class TestCollectScores(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)
        
    
        
    def test_create_source_file_map(self):
        source_file_map = collectScores.create_source_file_map(self.cspec)
        #print source_file_map
        self.assertTrue(len(source_file_map.keys()) == 24)
        self.assertTrue(source_file_map['l_aa_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/l_bb_number_3_s_300/userMonth.csv')
        
        self.assertTrue(source_file_map['l_aa_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/l_bb_number_3_s_300/userMonth.csv')
        
    def test_create_pooled_results_files(self):
        # delete everything in the results folder
        folder = './collected_results'
        self.clean_dir(folder)
        # generate 
        collectScores.create_pooled_results_files(self.cspec)
        f1 = open('./collected_results/unittest/res_userDay_s_300.csv','r')
        lines1 = f1.readlines()
        self.assertTrue(lines1[0] == 'letter,number_1,number_2,number_3\n')
        self.assertTrue(lines1[1] == 'AAA,0.312,0.322,0.332\n')
        self.assertTrue(lines1[2] == 'BBB,0.412,0.422,0.432\n')
        f1.close()
        
        f2 = open('./collected_results/unittest/res_userMonth_s_300.csv','r')
        lines2 = f2.readlines()
        self.assertTrue(lines2[0] == 'letter,number_1,number_2,number_3\n')
        self.assertTrue(lines2[1] == 'AAA,0.311,0.321,0.331\n')
        self.assertTrue(lines2[2] == 'BBB,0.411,0.421,0.431\n')
        f2.close()
        # clean the folder again
        #self.clean_dir(folder)
       
    def clean_dir(self, folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
if __name__ == '__main__':
    unittest.main()
    
   