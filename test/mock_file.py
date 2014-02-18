'''
Created on Feb 13, 2014

@author: irvine
'''
class MockFile(object):
    def __init__(self,pathname):
        self.pathname = pathname;
        self.lines = []
        self.nextReadIndex = 0
        self.nextWriteIndex = 0
        
    def readlines(self):
        result = []
        for line in self.lines:
            result.append(line)
        return result
    
    def readline(self):
        if (len(self.lines) == 0):
            raise IOError("tried to read line from empty file")
        if (self.nextReadIndex >= len(self.lines)):
            raise IOError("tried to read line beyond end of file")
        line = self.lines[self.nextReadIndex]
        self.nextReadIndex = self.nextReadIndex + 1
        return line
    
    def close(self):
        self.nextReadIndex = 0
        
    def write(self, s):
        if (self.nextWriteIndex == 0):
            self.lines.append(s)
            self.nextWriteIndex = self.nextWriteIndex + 1
        else:
            prevWriteIndex = self.nextWriteIndex - 1
            prev_write = self.lines[prevWriteIndex]
            if prev_write.endswith('\n'):
                self.lines.append(s)
                self.nextWriteIndex = self.nextWriteIndex + 1
            else:
                appended_line = "{0}{1}".format(prev_write,s)
                self.lines[prevWriteIndex] = appended_line
                # don't inc write index
        