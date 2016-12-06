import sys
'''
Created on Oct 29, 2016

@author: Jed Irvine
wrapper around stdout so that we can have a MockStdout for catching output 
and checking it in unittests
'''
class Stdout(object):
    '''
    classdocs
    '''
    def println(self, s):
        print s

    def print_without_newline(self, s):
        sys.stdout.write(s)
        
    def __init__(self):
        '''
        Constructor
        '''
        