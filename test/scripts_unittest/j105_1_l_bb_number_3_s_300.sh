#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N j105_1_l_bb_number_3_s_300_1
#
# send stdout and stderror to this file
#$ -o ./scripts_unittest/j105_1_l_bb_number_3_s_300.out
#$ -e ./scripts_unittest/j105_1_l_bb_number_3_s_300.err
#
#see where the job is being run
hostname
echo BBB 3 300 > ./generated_results/unittest/trial1/l_bb_number_3_s_300/BBB_3_three.txt
