#!/usr/bin/python
import time

from analyze_conf import *
from analyze_exceptions import *

class SquidLogWatcher:
    """
        Log Wrapper: takes a file path and a sleep interval in secs
        watchs for new lines available in the file specified
        external interfaces: getNextLines
    """
    def __init__(self):
        self.file_path = getConf("SQUID_LOG_PATH")
        
        try:
            self.fd = open(self.file_path,"r")
            if getConf('IGNORE_OLD'):
                self.fd.seek(0,2)

                if getConf('DEBUG'):
                    toLog("LogWatcher: going to position %s"%self.fd.tell())
        except:
            logException()
            raise
            
        self.cache = []
        self.cont = True #would we continue?
        self.max_cache_fill = getConf("MAX_CACHE_FILL")

        if getConf('DEBUG'):
            toLog("LogWatcher, Initiated on %s"%self.file_path)
    
    def __fill_cache(self, no_of_lines =  None):
        """
            try to read next available lines from log file
            no_of_lines (int): if is neg, read till end_of_file,
                                otherwise read this amount of lines
        """
        if no_of_lines == None:
            no_of_lines = self.max_cache_fill

        if getConf('DEBUG') == 2:
            toLog('Fill Cache, starting ...')
      
        l = 0
        line = 'non-empty'
        while line and self.cont and (no_of_lines < 0 or l < no_of_lines):# it's not good, but works :|
            line = self.fd.readline()
            if line:
                l += 1
                self.cache.append(line)

        if getConf('DEBUG') == 2:
            toLog("cache filled, up to %s line(s)"%l)

        return l

    def getNextLines(self,no_of_lines= None):
        """
            External calls upon this method on demand:
            next available lines or nothing
        """
        tmp = []
        if not len(self.cache):
            self.__fill_cache() # try to get available lines
        
        if not no_of_lines:
            tmp = self.cache
            self.cache = []
        else:
            tmp=self.cache[:no_of_lines]
            self.cache=self.cache[no_of_lines:]
        return tmp
    
    def __reset(self):
        self.cont = False
        self.fd.close()
        self.fd = open(self.file_path,"r")
        self.cont = True
        if getConf('DEBUG'):
            toLog('logWatcher, resetted')
    
    def rotateHandler(self):
        if getConf('DEBUG'):
            toLog('squid log file got rotated, so ...')
        self.__fill_cache(-1)
        self.__reset()

    def quitMonitor(self, discard = True):
        self.cont = False
        if not discard:
            return self.cache
        else:
            self.cache = []
        if getConf('DEBUG'):
            toLog('LogWatcher, Closed')
