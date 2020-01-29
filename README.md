# PERMUTER
--------
Permuter is a tool for:
- generating .sh files to run via qsub on a Sun Grid Engine cluster
- running them
- and keeping track of their status  

Written in python2.7 all permuter.py commands reference a pspec file (foo.pspec).  The pspec file captures how to generate multiple scripts, where each script has a command that has a certain set of parameters, and those parameters are drawn from a set of permutations.

For example, if you want the .sh script to run a command on a cluster machine, and pass it three arguments, such as:
```
/command_dir/my_command -c some_color -y some_year -fvalue f_val -o /output_dir/outfile.txt 
```
on a given cluster machine, but have the arguments varied in a particular way, in the pspec file you can say:
```
root_dir:/my_outputs
output_filename:outfile.txt
(permute):some_color=red,blue,green 
(permute):some_year=2010,2011,2012
(permute):f_val= range(3,6)      # would resolve to 3,4,5
command:/command_dir/my_command -c (some_color) -y (some_year) -fvalue (f_val) -o <permutation_output_dir>/outfile.txt
```
...and 3 x 3 x 3, or 27 .sh files will be generated, each one having a particular set of values for the arguments, for example
```
/command_dir/my_command -c green -y 2010 -fvalue 5 -o ... 
```
For a full explanation of the workings or permuter.py and the pspec file, watch the two videos referenced below.

Permuter is written in python 27.  To configure your environment, do the following:

1. run "python --version" to see if 2.7 in play, if not, create a virtual environment using virtualenv

1.a. if python version is not 2.7 and you wish to use virtualenv, then 
```bash
$ pip install virtualenv
$ cd my_project_folder
$ virtualenv env27
$ virtualenv -p /usr/bin/python2.7 env27
$ bash 
$ source pnv27/bin/activate
```
To intsall permuter, make sure you clone it into a directory visible from the submit-host:
```
$ mkdir cluster
$ cd cluster
$ git clone https://github.com/jedirv/permuter.git
$ cd permuter
$ git checkout v1.0
$ cd permute
$ python permuter.py   // to show usage statement
```
