#!/bin/csh
#
#$ -q eecs,eecs1,eecs,share
#$ -M someone@gmail.com
#$ -m beas
#$ -N unittest-j103_2_l_aa_number_2_s_300_2
#
# send stdout and stderror to this file
#$ -o j103_2_l_aa_number_2_s_300.out
#$ -e j103_2_l_aa_number_2_s_300.err
#
#see where the job is being run
hostname
echo AAA 2 300 > ./generated_results/unittest/trial2/l_aa_number_2_s_300/AAA_2_two.txt
touch ./generated_results/unittest/trial2/l_aa_number_2_s_300/permutation_done_marker.txt
