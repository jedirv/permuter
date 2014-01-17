#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N unittest-j108_1_l_bb_number_2_s_300_1
#
# send stdout and stderror to this file
#$ -o j108_1_l_bb_number_2_s_300.out
#$ -e j108_1_l_bb_number_2_s_300.err
#
#see where the job is being run
hostname
echo BBB 2 300 > ./generated_results/unittest/trial1/l_bb_number_2_s_300/BBB_2_two.txt
touch ./generated_results/unittest/trial1/l_bb_number_2_s_300/permutation_done_marker.txt
