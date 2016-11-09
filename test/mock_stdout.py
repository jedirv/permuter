'''
Created on Oct 29, 2016

@author: Jed Irvine
wrapper around stdout to support unit tests
'''

class MockStdout(object):
    line_without_newline = ''
    '''
    classdocs
    '''
    def println(self,s):
        string_with_newline = '{0}\n'.format(s)
        if self.line_without_newline != '':
            string_with_newline = '{0}{1}'.format(self.line_without_newline, string_with_newline)
        sublines = string_with_newline.split('\n')
        for subline in sublines:
            if subline != '':
                subline = "{0}\n".format(subline)
                self.lines.append(subline)
        self.line_without_newline = ''
        
    def print_without_newline(self,s):
        self.line_without_newline = "{0}{1}".format(self.line_without_newline,s)
        
    def clear(self):
        self.lines = []

    def __init__(self):
        '''
        Constructor
        '''
        self.lines = []