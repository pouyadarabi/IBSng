from core.ibs_exceptions import *
from core.server import handler
from core.lib.multi_strs import MultiStr
import sys
import os
import traceback
import imp

class UtilHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"util")
        self.registerHandlerMethod("multiStrGetAll")
        self.registerHandlerMethod("runDebugCode")


    def multiStrGetAll(self,request):
        request.checkArgs("str","left_pad")
        return map(lambda x:x,MultiStr(request["str"],request["left_pad"]))

    def runDebugCode(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("command")
        requester=request.getAuthNameObj()
        if not requester.isGod():
            return "Access Denied"

        if request.has_key("no_output"):
            self.__execCode(request)
            return True
        else:
            return self.__grabOutput(request)


    def __grabOutput(self, request):
        import pty
        out=""
        (pid, fd) = pty.fork()
        if pid == 0:
            try:
                self.__execCode(request)
            except:
                (_type,value,tback)=sys.exc_info()
                print "".join(traceback.format_exception(_type, value, tback))
            
            sys.stdout.flush()
            os._exit(0)
        else:
            out = ""

            while True:
                (exit_pid, exit_status) = os.waitpid(pid, os.WNOHANG)

                try:
                    out += os.read(fd, 1024*1024)
                except OSError:
                    logException(LOG_DEBUG,"Debug Code Read:")

                if exit_pid == pid:
                    break

            return out



    def __execCode(self, request):
        if request.has_key("read_from_file"):
            module_name = os.path.basename(request["command"])[:-3]
            directory = os.path.dirname(request["command"])
            (file,pathname,desc)=imp.find_module(module_name,[directory])
            imp.load_module(module_name,file,pathname,desc)

#           __import__(request["command"])
#           exec( open(request["command"]).read(os.stat(request["command"])[6]) )
        else:
            exec( request["command"] )

