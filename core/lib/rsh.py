from core.script_launcher import launcher_main
from core.lib.general import *
from core.ibs_exceptions import *
from core import defs
import threading
import types

class RSHClient:
    def __init__(self, host, max_concurrent_connections=3, rsh_wrapper="/usr/bin/rsh"):
        self.host=host
        self.max_concurrent_connections=max_concurrent_connections
        self.rsh_wrapper=rsh_wrapper
        self.lock=threading.Semaphore(max_concurrent_connections)


    def runCommand(self, command):
        """
            run command on remote host
        """
        self.getOutput(command)

    def getOutput(self, command):
        """
            run command and return output
        """
        self.lock.acquire()
        try:
            return self.__rcmd(self.host, command)
        finally:
            self.lock.release()
        
    def __rcmd(self, host, command):
        """
            command(str or list): if it's a list all list argument will be passed as arguments
        """
        args=self.__prepareCommandAsArgument(command)
        _in,out,err=launcher_main.getLauncher().popen3(self.rsh_wrapper,[host]+args)
        err_str=self.__readAll(err)
        if err_str:
            raise RSHException("Host: %s Command %s: %s"%(host,command,err_str))
        out_str=self.__readAll(out)
        map(lambda fd:fd.close(),(_in,out,err))
        return out_str

    def __prepareCommandAsArgument(self, command):
        """
            make sure arguments passed to rsh wrapper is a list
        """
        if type(command)==types.ListType:
            return command
        else: #str
            return [command]
        
            
    def __readAll(self,fd):
        ret=""
        tmp=fd.read()
        while tmp!="":
            ret+=tmp
            tmp=fd.read()
        return ret

