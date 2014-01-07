'''
Created on Dec 12, 2013

@author: admin-jed
'''
import unittest, os
from permute import cluster_spec
from permute import permuter
from permute import cluster_runs_info

class TestPermuter(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)
        self.cluster_runs = cluster_runs_info.ClusterRunsInfo(self.cspec)

    def test_create_source_file_map(self):
        source_file_map = permuter.create_source_file_map(self.cspec)
        #print source_file_map
        #self.assertTrue(len(source_file_map.keys()) == 24)
        self.assertTrue(len(source_file_map.keys()) == 48)
        
        self.assertTrue(source_file_map['an_dog_l_aa_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_dog_l_bb_number_3_s_300/userMonth.csv')
        
        self.assertTrue(source_file_map['an_dog_l_aa_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_aa_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_dog_l_bb_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_dog_l_bb_number_3_s_300/userMonth.csv')
        
        
        self.assertTrue(source_file_map['an_cat_l_aa_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_1_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_2_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_3_res_userDay_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_1_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_2_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_3_res_userMonth_s_300_trials_1']== './sample_results/unittest/trial1/an_cat_l_bb_number_3_s_300/userMonth.csv')
        
        self.assertTrue(source_file_map['an_cat_l_aa_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_1_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_1_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_2_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_2_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_3_res_userDay_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_3_s_300/userDay.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_1_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_1_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_2_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_2_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_aa_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_aa_number_3_s_300/userMonth.csv')
        self.assertTrue(source_file_map['an_cat_l_bb_number_3_res_userMonth_s_300_trials_2']== './sample_results/unittest/trial2/an_cat_l_bb_number_3_s_300/userMonth.csv')
        
    def test_create_pooled_results_files(self):
        # delete everything in the results folder
        folder = './collected_results'
        self.clean_dir(folder)
        # generate 
        permuter.create_pooled_results_files(self.cluster_runs)
        f1 = open('./collected_results/unittest/res_userDay_s_300.csv','r')
        lines1 = f1.readlines()
        self.assertTrue(lines1[0] == '[\'letter\'],an_cat_number_1,an_cat_number_2,an_cat_number_3,an_dog_number_1,an_dog_number_2,an_dog_number_3\n')
        self.assertTrue(lines1[1] == 'l_aa,3111.0,3121.0,3131.0,4111.0,4121.0,4131.0\n')
        self.assertTrue(lines1[2] == 'l_bb,3211.0,3221.0,3231.0,4211.0,4221.0,4231.0\n')
        f1.close()
        
        f2 = open('./collected_results/unittest/res_userMonth_s_300.csv','r')
        lines2 = f2.readlines()
        self.assertTrue(lines2[0] == '[\'letter\'],an_cat_number_1,an_cat_number_2,an_cat_number_3,an_dog_number_1,an_dog_number_2,an_dog_number_3\n')
        self.assertTrue(lines2[1] == 'l_aa,5111.0,5121.0,5131.0,6111.0,6121.0,6131.0\n')
        self.assertTrue(lines2[2] == 'l_bb,5211.0,5221.0,5231.0,6211.0,6221.0,6231.0\n')
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
    
   