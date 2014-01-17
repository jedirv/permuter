#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N unittest-j111_2_l_bb_number_3_s_300_2
#
# send stdout and stderror to this file
#$ -o j111_2_l_bb_number_3_s_300.out
#$ -e j111_2_l_bb_number_3_s_300.err
#
#see where the job is being run
hostname
echo BBB 3 300 > ./generated_results/unittest/trial2/l_bb_number_3_s_300/BBB_3_three.txt
touch ./generated_results/unittest/trial2/l_bb_number_3_s_300/permutation_done_marker.txt
