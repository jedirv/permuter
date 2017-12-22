# README for cluster project


Permuter is a tool for generating .sh files to run via qsub on an mpich cluster, running them, and keeping track of their status.  All permuter.py commands reference a cspec file (foo.cspec), which captures how to generate the different scripts.  The original intent was that each script would have  a different set of arguments for a command.

For example, if you want the .sh script to run a command with three arguments, such as:

foo color month f_val 

on a given cluster machine, but have the arguments varied in a particular way, in the cspec file you can say:

permute:color=red,blue,green 
permute:month=2010,2011,2012
permute:f_val= range(3,6)      # would resolve to 3,4,5,6
command:/home/me/foo (color) (month) (f_val)
 
...and 3 x 3 x 4, or 36 .sh files will be generated, each one having a particular set of values for the arguments, for example

/home/me/foo green 2010 5



Permuter is written in python 27.  To configure your environment, do the following:

1. run "python --version" to see if 2.7 in play, if not, create a virtual environment using virtualenv

1.a. if python version is not 2.7 and you wish to use virtualenv, then 

$ pip install virtualenv
$ cd my_project_folder
$ virtualenv env27
$ virtualenv -p /usr/bin/python2.7 env27
$ bash 
$ source pnv27/bin/activate

