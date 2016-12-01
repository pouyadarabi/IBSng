import threading
import time
import os
import sys

class Logger:
    PERMISSION=0600
    
    def __init__(self,file_name):
        self.re_open=False
        self.file_name=file_name
        self.open()
        self.tlock=threading.RLock()

    def open(self):     
        try:
            self.fd=open(self.file_name,"a+")
            self.__chmodFile()
        except IOError,(errno,errStr):
            sys.stderr.write("Warning: Can't open log file %s\n" % errStr)
            raise
        except Exception,e:
            sys.stderr.write("Warning: Can't open log file %s\n" % errStr)
            raise
    
    def __chmodFile(self):
        """
            chmod file to 0600
        """
        os.chmod(self.file_name,self.PERMISSION)
    
    def write(self,_str,add_stack=False):
        self.tlock.acquire()
        try:
            try:
                if self.re_open:
                    self.reOpenFD()

                self.fd.write("%s %s \n"%(self.timeStr() , _str)) 
                if add_stack:
                    self.fd.write("\n%s"%self.stackTrace())
        
                self.fd.flush()
            
            except IOError,(errNo,errStr):
                if not self.re_open:
                    self.re_open=True
                    self.write(str)
        
        finally:
            self.tlock.release()

    def stackTrace(self):
        retStr=""
        stackList=traceback.format_list(traceback.extract_stack())
        for tmp in stackList:
            retStr+=tmp
        return retStr

    def timeStr(self):
        return time.strftime("%Y/%m/%d-%H:%M:%S")

    def reOpenFD(self):
        self.fd.close()
        self.open()
        self.re_open = False
