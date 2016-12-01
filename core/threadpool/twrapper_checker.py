from core.lib.time_lib import formatDuration
from core.event import periodic_events
from core.threadpool import thread_main
from core.ibs_exceptions import *

import time

class TWrapperChecker(periodic_events.PeriodicEvent):
    def __init__(self):
        periodic_events.PeriodicEvent.__init__(self, "TWrapperChecker", 5*60, [], False, 10)
    
    def run(self):
        now = long(time.time())
        logged_threadpool = False
        
        for twrapper in thread_main.getTWrappers():
            for method, args, queue_time in twrapper.getQueue():
                if now - queue_time > 60:

                    if not logged_threadpool: #do not log threadpool multiple times
                        thread_main.getThreadPool().logThreads(LOG_ERROR)
                        logged_threadpool = True
                    
                    toLog("Found Long Queued Thread %s:%s:%s queue time: %s"%(twrapper.getName(), 
                                                                            method, 
                                                                            args, 
                                                                            formatDuration(now-queue_time)), LOG_ERROR)
