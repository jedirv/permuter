#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N unittest-j110_1_l_bb_number_3_s_300_1
#
# send stdout and stderror to this file
#$ -o j110_1_l_bb_number_3_s_300.out
#$ -e j110_1_l_bb_number_3_s_300.err
#
#see where the job is being run
hostname
echo BBB 3 300 > ./generated_results/unittest/trial1/l_bb_number_3_s_300/BBB_3_three.txt
touch ./generated_results/unittest/trial1/l_bb_number_3_s_300/permutation_done_marker.txt
