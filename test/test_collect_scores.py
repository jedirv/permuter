import unittest, os
from permute import cluster_spec
from monitor import collectScores

class TestCollectScores(unittest.TestCase):

    def setUp(self):
        path = "./test.cspec"
        self.cspec = cluster_spec.ClusterSpec(path)
        
    def test_create_delta_line(self):
        number_line = "2013-04,0.82333,0.92333,0.72222"
        delta_line = collectScores.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.10,-0.10")
        
        number_line = "2013-04,0.082333,0.092333,0.072222"
        delta_line = collectScores.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.01,-0.01")
        
        number_line = "2013-04,0.0082333,0.0092333,0.0072222"
        delta_line = collectScores.create_delta_line(number_line)
        self.assertTrue(delta_line == "2013-04,0,0.00,-0.00")
        
    def test_create_source_file_map(self):
        source_file_map = collectScores.create_source_file_map(self.cspec)
        #print source_file_map
        self.assertTrue(len(source_file_map.keys()) == 12)
        self.assertTrue(source_file_map['l_aa_number_1_res_userDay_s_300']== './sample_results/l_aa_number_1_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userDay_s_300']== './sample_results/l_bb_number_1_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userDay_s_300']== './sample_results/l_aa_number_2_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userDay_s_300']== './sample_results/l_bb_number_2_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userDay_s_300']== './sample_results/l_aa_number_3_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userDay_s_300']== './sample_results/l_bb_number_3_s_300_FOO_300/userDay.csv')
        self.assertTrue(source_file_map['l_aa_number_1_res_userMonth_s_300']== './sample_results/l_aa_number_1_s_300_FOO_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_1_res_userMonth_s_300']== './sample_results/l_bb_number_1_s_300_FOO_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_2_res_userMonth_s_300']== './sample_results/l_aa_number_2_s_300_FOO_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_2_res_userMonth_s_300']== './sample_results/l_bb_number_2_s_300_FOO_300/userMonth.csv')
        self.assertTrue(source_file_map['l_aa_number_3_res_userMonth_s_300']== './sample_results/l_aa_number_3_s_300_FOO_300/userMonth.csv')
        self.assertTrue(source_file_map['l_bb_number_3_res_userMonth_s_300']== './sample_results/l_bb_number_3_s_300_FOO_300/userMonth.csv')
        
    def test_create_pooled_results_files(self):
        # delete everything in the results folder
        folder = './collected_results'
        self.clean_dir(folder)
        # generate 
        collectScores.create_pooled_results_files(self.cspec)
        f1 = open('./collected_results/unittest/res_userDay_s_300.csv','r')
        lines1 = f1.readlines()
        self.assertTrue(lines1[0] == 'letter,number_1,number_2,number_3\n')
        self.assertTrue(lines1[1] == 'AAA,AAA1ud,AAA2ud,AAA3ud\n')
        self.assertTrue(lines1[2] == 'BBB,BBB1ud,BBB2ud,BBB3ud\n')
        f1.close()
        
        f2 = open('./collected_results/unittest/res_userMonth_s_300.csv','r')
        lines2 = f2.readlines()
        self.assertTrue(lines2[0] == 'letter,number_1,number_2,number_3\n')
        self.assertTrue(lines2[1] == 'AAA,AAA1um,AAA2um,AAA3um\n')
        self.assertTrue(lines2[2] == 'BBB,BBB1um,BBB2um,BBB3um\n')
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
    
   