'''
Created on Oct 29, 2016

@author: Jed Irvine
wrapper around stdout to support unit tests
'''

class MockStdout(object):
    '''
    classdocs
    '''
    def println(self,s):
        string_with_newline = '{0}\n'.format(s)
        self.stdout.append(string_with_newline)
        
    def clear(self):
        self.stdout = []

    def __init__(self):
        '''
        Constructor
        '''
        self.stdout = []