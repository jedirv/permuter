#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N j109_2_l_bb_number_1_s_300_2
#
# send stdout and stderror to this file
#$ -o ./scripts_unittest/j109_2_l_bb_number_1_s_300.out
#$ -e ./scripts_unittest/j109_2_l_bb_number_1_s_300.err
#
#see where the job is being run
hostname
echo BBB 1 300 > ./generated_results/unittest/trial2/l_bb_number_1_s_300/BBB_1_one.txt
