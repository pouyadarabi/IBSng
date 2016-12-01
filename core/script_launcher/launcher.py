from core.ibs_exceptions import toLog, LOG_DEBUG
import os
from core import defs

class ScriptLauncher:
    """
        Script Launcher is a tool for calling external scripts and setting special timeout
        on run time of scripts.
        The problem Script Launcher is going to solve is sometimes external scripts hang and don't exit. So
        the coresponding thread in IBSng can't be freed.
    """
    
    DEBUG=False
    
    def system(self, script, args, timeout=20):
        """
            run "script" with "args" with timeout of "timeout"
            args(list of str): A List of arguments.
            WARNING: Do now pass multiple arguments as a single string
        """
        return self.__launchWithScriptWrapper(os.system, script, args, timeout, ">/dev/null 2>/dev/null")
    
    def popen(self, script, args, timeout=20):
        return self.__launchWithScriptWrapper(os.popen, script, args, timeout, "2>&1")

    def popen3(self, script, args, timeout=20):
        return self.__launchWithScriptWrapper(os.popen3, script, args, timeout)

    def __launchWithScriptWrapper(self, method, script, args, timeout, shell_pipes=""):
        #script may contain extra arguments. ex. ssh cache tc
        sp = script.split()
        real_script, script_args = sp[0], sp[1:]
        
        cmd = "%s/script_wrapper/script_wrapper.py -t %s -- '%s' %s %s"%(defs.IBS_ADDONS, 
                                                                                timeout, 
                                                                                real_script, 
                                                                                self.__prepareScriptArgs(script_args + args),
                                                                                shell_pipes)
        if self.DEBUG:
            toLog("Script Launcher is running %s"%cmd, LOG_DEBUG)
        
        return method(cmd)
    
    def __prepareScriptArgs(self, args):
        """
            args(list of str): list of command line argument
            return a string of escaped command line arguments ready to be passed to system or popen call
        """
        prepared_args = []
        for arg in args:
            prepared_args.append("'%s'"%self.__escapeArg(arg))
        
        return " ".join(prepared_args)

    def __escapeArg(self, arg):
        """
            backslashify special bash characters
        """
        return str(arg).replace("'","\\'").replace("`","\\`")
