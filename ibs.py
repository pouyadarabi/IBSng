#! /usr/bin/python -W ignore::: -OO 
print "importing required files ..."
import signal
import sys
import os
import syslog
import traceback
from core.debug import thread_debug
from core.event import event
from core import ibs_exceptions
import core.main


RUN_PROFILER=False
PROFILER_STAT_FILENAME="/tmp/profile"

if RUN_PROFILER:
    import profile

def termSigHandler(signum,frame):
    event.addEvent(0,core.main.mainThreadShutdown,[],100)
    
def childWaitSigHandler(signum,frame):
    if signum==signal.SIGUSR1: #successfully started
        print "IBSng started successfully!"
        sys.exit(0)
    else:
        print "IBSng Failed to start!"
        sys.exit(1)
        
def handleUserDefinedSignals(handler):
    signal.signal(signal.SIGUSR1,handler)
    signal.signal(signal.SIGUSR2,handler)

def mainThreadInitialize():
    mainThreadSignalHandlers()
    print "Calling Initializer routins"
    thread_debug.debug_me()

    core.main.init()

def mainThreadSignalHandlers():
    handleUserDefinedSignals(signal.SIG_IGN)
    signal.signal(signal.SIGTERM,termSigHandler)
    signal.signal(signal.SIGHUP,signal.SIG_IGN)

def logToSysLog(err_text):
    syslog.openlog("IBSng",syslog.LOG_DAEMON)
    syslog.syslog(syslog.LOG_ERR,err_text)
    syslog.closelog()

def writePID(pid):
    fp = open('/var/run/IBSng.pid','w+')
    fp.write(str(pid))
    fp.close()

def start():
    handleUserDefinedSignals(childWaitSigHandler)
    print "forking ..."
    pid=os.fork()
    print "IBSng started with pid=%d"%pid
    if pid == 0:
        try:
            try:
                mainThreadInitialize()
                os.kill(os.getppid(),signal.SIGUSR1)
            except:
                print "Shutting down on error"
                os.kill(os.getppid(),signal.SIGUSR2)
                raise
        except:
            err_text=ibs_exceptions.getExceptionText()
            sys.stderr.write(err_text)
            logToSysLog(err_text)
            core.main.mainThreadShutdown()

        print "Successfully initialized, entering event loop ..."
        writePID(os.getpid())

        sys.setcheckinterval(500)
        event.startLoop()
    
    else:
        signal.pause()

if RUN_PROFILER:
    profile.run('start()',PROFILER_STAT_FILENAME)
else:
    start()
