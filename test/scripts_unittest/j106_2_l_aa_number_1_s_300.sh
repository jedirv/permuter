#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N j106_2_l_aa_number_1_s_300_2
#
# send stdout and stderror to this file
#$ -o ./scripts_unittest/j106_2_l_aa_number_1_s_300.out
#$ -e ./scripts_unittest/j106_2_l_aa_number_1_s_300.err
#
#see where the job is being run
hostname
echo AAA 1 300 > ./generated_results/unittest/trial2/l_aa_number_1_s_300/AAA_1_one.txt
