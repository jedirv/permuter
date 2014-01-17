'''
Created on Jan 10, 2014

@author: admin-jed
'''
#import permutations
import pooled_results_file
#import permutation_score_timing
from operator import itemgetter

class RankedResultsFile(object):
    '''
    classdocs
    '''


    def __init__(self,filename_permutation_info, cluster_runs):
        '''
        Constructor
        '''
        self.cluster_runs = cluster_runs
        self.cspec = cluster_runs.cspec
        self.target_dir = pooled_results_file.generate_target_dirname(self.cspec)
        self.perm_code_for_filename  = pooled_results_file.build_code_using_dictionary(filename_permutation_info, self.cspec)
        self.target_path = "{0}/{1}_score_list.txt".format(self.target_dir, self.perm_code_for_filename)
        self.scores_source_path = "{0}/{1}.csv".format(self.target_dir, self.perm_code_for_filename)
        self.timings_source_path = "{0}/{1}_timings.csv".format(self.target_dir, self.perm_code_for_filename)
        
       
    def persist(self):
        f_scores = open(self.scores_source_path, 'r')
        f_timings = open(self.timings_source_path, 'r')
        print "writing {0}".format(self.target_path)
        lines_scores = f_scores.readlines()
        lines_timings = f_timings.readlines()
        f_scores.close()
        f_timings.close()
        # verify headers match
        header_scores = lines_scores[0].rstrip('\n')
        header_timings = lines_timings[0].rstrip('\n')
        if (not(header_timings == header_scores)):
            raise Exception("headers don't match in scores and timings file: {0} ; {1}".format(header_scores, header_timings))
        
        # get averages line in each - should be last line
        index_scores_averages = len(lines_scores) - 1
        index_timings_averages = len(lines_timings) - 1
        averages_scores = lines_scores[index_scores_averages].rstrip('\n')
        #print "averages_scores {0}".format(averages_scores)
        averages_timings = lines_timings[index_timings_averages].rstrip('\n')
        #print "averages_timings {0}".format(averages_timings)
        
        if (not(averages_scores.startswith("averages"))):
            raise Exception("missing averages line in scores file {0}".format(self.scores_source_path))
        if (not(averages_timings.startswith("averages"))):
            raise Exception("missing averages line in timings file {0}".format(self.timings_source_path))
        
        header_parts = header_scores.split(",")
        scores_parts = averages_scores.split(",")
        timings_parts = averages_timings.split(",")
        
        if (len(header_parts) != len(scores_parts)):
            raise Exception("column mismatch between scores_header and scores_averages")
        if (len(header_parts) != len(timings_parts)):
            raise Exception("column mismatch between scores_header and timings_averages")
        
        perm_tuples = []
        
        for i in range(1, len(header_parts)):
            header_val = header_parts[i]
            scores_val = scores_parts[i]
            score_float = pooled_results_file.get_float_from_median_expression(scores_val)
            score_Xs = pooled_results_file.get_Xs_from_median_expression(scores_val)
            timings_val = timings_parts[i]
            timing_int = int(pooled_results_file.get_float_from_median_expression(timings_val))
            #print "timing_val {0} timing_int {1}".format(timings_val, timing_int)
            timings_Xs = pooled_results_file.get_Xs_from_median_expression(timings_val)
            perm_tuple = (header_val, score_float, score_Xs, timing_int, timings_Xs)
            perm_tuples.append(perm_tuple)
            #perm_score_timing = permutation_score_timing.PermutationScoreTiming(header_val, scores_val, timings_val)
            
        
        sorted_perm_tuples = sort_by_higher_score_then_lower_timing(perm_tuples)
        f = open(self.target_path, 'w')
        f.write("score\tcpu time(min)\tpermutation\tx=missing run\n")
        for perm_tuple in sorted_perm_tuples:
            minutes = int(int(perm_tuple[3]) / 60)
            #print "perm_tuple[3] {0} minutes {1}".format(perm_tuple[3], minutes)
            #print "0th {0}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            #print "1th {1}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            #print "2th {2}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            #print "3th {3}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            #print "4th {4}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            #print "5th {5}".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes)
            f.write("{1}\t{5}\t\t{0}\t{2}\n".format(perm_tuple[0], perm_tuple[1], perm_tuple[2], perm_tuple[3], perm_tuple[4], minutes))
        f.close()



def sort_by_higher_score_then_lower_timing(perm_tuples):
    s = sorted(perm_tuples, key=itemgetter(3))     # sort on secondary key , want lower timings first
    return sorted(s, key=itemgetter(1), reverse=True) # now sort on primary key, - want highest scores first













