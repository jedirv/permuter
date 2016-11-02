import getpass
import os
from xml.dom import minidom
import xml.etree.ElementTree

class QStatLog(object):
    '''
    Wraps the qstat result
    '''
    def __init__(self, script_dir):
        self.run_state = {}
        self.run_number = {}
        self.job_names = []
        self.logpath = "{0}/{1}".format(script_dir,'qstat.txt')
       
    def delete(self):
        if os.path.exists(self.logpath):
            os.unlink(self.logpath)
            
    def ingestOld(self):
        f = open(self.logpath, 'r')
        lines = f.readlines()
        for line in lines:
            if (line.startswith('job-ID')):
                pass
            elif(line.startswith('--')):
                pass
            else:
                self.qstat_lines.append(line)
        f.close()
        
    '''
    <job_list state="running">
      <JB_job_number>5911595</JB_job_number>
      <JAT_prio>0.50476</JAT_prio>
      <JB_name>runtest-j02_1_x_1_y_3_1</JB_name>
      <JB_owner>irvineje</JB_owner>
      <state>r</state>
      <JAT_start_time>2016-11-01T16:40:15.092</JAT_start_time>
      <queue_name>eecs@compute-0-8.hpc.engr.oregonstate.edu</queue_name>
      <jclass_name></jclass_name>
      <slots>1</slots>
    </job_list>
    '''    
    def ingest(self):
        self.ingest_from_path(self.logpath)
    
    '''
    <foo>
   <bar>
      <type foobar="1"/>
      <type foobar="2"/>
   </bar>
</foo>
    '''
    def ingest_from_path(self, path):
        e = xml.etree.ElementTree.parse(path).getroot()
        for job_list in e.findall('./queue_info/job_list'):
            for child in job_list:
                if child.tag == 'state':
                    job_state = child.text
                elif child.tag == 'JB_job_number':
                    job_number = child.text
                elif child.tag == 'JB_name':
                    job_name = child.text
                else:
                    pass
            self.run_state[job_name] = job_state
            self.run_number[job_name] = job_number
            self.job_names.append(job_name)    
        '''
        xmldoc = minidom.parse(path)
        job_infos =xmldoc.getElementsByTagName('job_info')
        for job_info in job_infos:
            queue_infos = job_info.getElementByTagName('queue_info')
            for queue_info in queue_infos:
                jobs = queue_info.getElementByTagName('joblist')
                for job in jobs:
                    job_state = self.getText(job.getElementsByTagName('state')[0].childNodes)
                    job_number = self.getText(job.getElementsByTagName('JB_job_number')[0].childNodes)
                    job_name = self.getText(job.getElementsByTagName('JB_name')[0].childNodes)
                    self.run_state[job_name] = job_state
                    self.run_number[job_name] = job_number
                    self.job_names.append(job_name)
        '''
    def getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def is_running(self, job_name):
        if self.job_state.has_key(job_name):
            if self.job_state[job_name] == 'r':
                return True
        return False
        
    def is_waiting(self, job_name):
        if self.job_state.has_key(job_name):
            if self.job_state[job_name] == 'qw':
                return True
        return False
        
    
    '''        
    def is_cluster_job_still_running(self, cluster_job_number):
        return self.cluster_system.is_cluster_job_still_running(cluster_job_number, self.script_dir, self.qstat_log)
    '''
        
        

 
    
        