#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N j110_l_aa_number_3_s_300_2
#
# send stdout and stderror to this file
#$ -o ./scripts_unittest/j110_2_l_aa_number_3_s_300.out
#$ -e ./scripts_unittest/j110_2_l_aa_number_3_s_300.err
#
#see where the job is being run
hostname
echo AAA 3 300 > ./generated_results/unittest/trial2/l_aa_number_3_s_300/AAA_3_three.txt
