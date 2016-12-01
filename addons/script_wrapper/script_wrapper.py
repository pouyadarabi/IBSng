#!/usr/bin/python
import os
import sys
import script_timeout
from optparse import OptionParser

timeout=20

    
def parseOptions():
    global timeout
    
    usage = """usage: %prog [options] <SCRIPT PATH> arg1 arg2 ... 
    
               script_wrapper is a wrapper to set a timeout for running an script. 
               If timeout reaches the script process will be killed.
               Exit code will be 255 if timeout occures or 254 if error occures.
               Otherwise exit code will be the same as script exit code
    """
               
    
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--timeout", type="int", dest="timeout", default=20, help="Script Run Timeout in seconds")
    options, args = parser.parse_args()
    
    if len(args) < 1:
        parser.error("Script Path is missing")
    
    timeout = options.timeout
    
    return args[0], args[1:]
    
def main():
    script , args = parseOptions()

    pid = os.fork()
    if pid == 0:
        str_args = " ".join(map(quote, args))
        os.execl("/bin/sh","sh","-c", "'%s' %s"%(script,str_args))
    else:
        script_timeout.shouldExitIn(timeout)
        child_status = os.wait()[1]
    
    if os.WIFEXITED(child_status):
        exit_code = os.WEXITSTATUS(child_status)
    else:
        exit_code = -2
    
    sys.exit(exit_code)

def quote(_str):
    return "'%s'"%_str

if __name__ == "__main__":
    main()