'''
Created on Dec 12, 2013

@author: admin-jed
'''
import unittest, os
from permute import cluster_spec
from permute import permuter
from permute import cluster_runs_info

class TestPermuter(unittest.TestCase):

    def test_create_source_file_map(self):
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("permute:number=1 3\n")
        lines.append("permute:letter=AAA,BBB\n")
        lines.append("permute:singleton_val=300\n")
        lines.append("permute:animal=dog,cat\n")
        lines.append("concise_print:animal,an\n")
        lines.append("concise_print:letter,l\n")
        lines.append("concise_print:singleton_val,s\n")
        lines.append("concise_print:resolution,res\n")
        lines.append("concise_print:AAA,aa\n")
        lines.append("concise_print:BBB,bb\n")

        lines.append("scores_permute:resolution=userDay,userMonth\n")
        lines.append("scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1\n")
        lines.append("scores_to:./collected_results\n")
        lines.append("scores_y_axis:letter\n")
        lines.append("scores_x_axis:number,animal\n")
        
        lines.append("root_results_dir:./sample_results\n")
        
        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines)
        source_file_map = cluster_runs_info.create_source_file_map(cspec)
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
        lines = []
        lines.append("#cspec\n")
        lines.append("master_job_name:unittest\n")
        lines.append("trials:2\n")
        lines.append("permute:number=1 3\n")
        lines.append("permute:letter=AAA,BBB\n")
        lines.append("permute:singleton_val=300\n")
        lines.append("permute:animal=dog,cat\n")
        lines.append("concise_print:animal,an\n")
        lines.append("concise_print:letter,l\n")
        lines.append("concise_print:singleton_val,s\n")
        lines.append("concise_print:resolution,res\n")
        lines.append("concise_print:AAA,aa\n")
        lines.append("concise_print:BBB,bb\n")

        lines.append("scores_permute:resolution=userDay,userMonth\n")
        lines.append("scores_from:file=<permutation_results_dir>/(resolution).csv,column_name=auc,row_number=1\n")
        lines.append("scores_to:./collected_results\n")
        lines.append("scores_y_axis:letter\n")
        lines.append("scores_x_axis:number,animal\n")
        lines.append("root_results_dir:./sample_results\n")

        cspec = cluster_spec.ClusterSpec("/foo/bar/baz.cspec", lines)
        
        cluster_runs = cluster_runs_info.ClusterRunsInfo(cspec)
        # delete everything in the results folder
        folder = './collected_results'
        self.clean_dir(folder)
        # generate 
        permuter.create_pooled_results_files(cluster_runs)
        f1 = open('./collected_results/unittest/res_userDay_s_300.csv','r')
        lines1 = f1.readlines()
        print lines1
        self.assertTrue(lines1[0] == 'letter,an_cat_number_1,an_cat_number_2,an_cat_number_3,an_dog_number_1,an_dog_number_2,an_dog_number_3\n')
        self.assertTrue(lines1[1] == 'l_aa,3111.0,3121.0,3131.0,4111.0,4121.0,4131.0\n')
        self.assertTrue(lines1[2] == 'l_bb,3211.0,3221.0,3231.0,4211.0,4221.0,4231.0\n')
        f1.close()
        
        f2 = open('./collected_results/unittest/res_userMonth_s_300.csv','r')
        lines2 = f2.readlines()
        self.assertTrue(lines2[0] == 'letter,an_cat_number_1,an_cat_number_2,an_cat_number_3,an_dog_number_1,an_dog_number_2,an_dog_number_3\n')
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
                
#    def test_create_dir_under_tilde(self):
#        dir = os.path.expanduser('~/permuter')
#        if (not(os.path.isdir(dir))):
#            os.makedirs(dir)
#        file_created = os.path.isdir(dir)
#        self.asserTrue(file_created)
if __name__ == '__main__':
    unittest.main()
    
   