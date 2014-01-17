#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N unittest-j104_1_l_aa_number_3_s_300_1
#
# send stdout and stderror to this file
#$ -o j104_1_l_aa_number_3_s_300.out
#$ -e j104_1_l_aa_number_3_s_300.err
#
#see where the job is being run
hostname
echo AAA 3 300 > ./generated_results/unittest/trial1/l_aa_number_3_s_300/AAA_3_three.txt
touch ./generated_results/unittest/trial1/l_aa_number_3_s_300/permutation_done_marker.txt
