import threading
import time
import traceback
import sys
from core import defs
from core.threadpool import thread_main
from core.ibs_exceptions import *

#priority 100 is for shutdown process

class Scheduler:
    def __init__(self):
        self.tlock=threading.RLock()
        self.event_obj=threading.Event()
        self.event_obj.clear()
        self.__events=[]
    
    def loop(self):
        while True:
            next_evt=self.nextEvent()
            if next_evt <= 0:
                self.doEvent()
                continue
            self.event_obj.wait(next_evt)
            self.event_obj.clear()

    def __getEventIndex(self, time_to_run, priority):
        i = 0
        for i in xrange(len(self.__events)): #sequential search, list is sorted, so there are better 
            if self.__events[i]["timeToRun"] == time_to_run:
                if priority > self.__events[i]["priority"]:
                    i -= 1
                    break
                else:
                    break
            elif self.__events[i]["timeToRun"] > time_to_run:
                break
        else:
            i += 1 #append to end of list
        
        return max( i, 0 )

    def addEvent(self, secs_from_now, method, args, priority):
        """
            add a new event to event schedueler
            secs_from_now(integer): seconds from now that the event will be run
            method(Callable object): method that will be called
            args(list): list of arguments passed to method
            priority(integer): priority of job. Greater numbers favored more. it should be less than 20
                               jobs with priority number more than 10 in run in main thread pool wrapper
                               while under 10 priorities run in event thread pool wrapper
                               priority 100 is reserved for shutdown method
        """
        time_to_run = self.now() + secs_from_now
        
        self.tlock.acquire() 
        try:
            if priority == 100:
                new_event_index = 0
            else:
                new_event_index = self.__getEventIndex(time_to_run,priority)

            self.__events.insert(new_event_index, {"timeToRun":time_to_run,
                                                   "method":method,
                                                   "args":args,
                                                   "priority":priority})
        finally:
            self.tlock.release()
            if new_event_index == 0:
                self.event_obj.set() 

    def nextEvent(self): #no locking, return time to next event
        t=30
        self.tlock.acquire()
        try:
            if len(self.__events):
                t=self.__events[0]["timeToRun"]-self.now()
        finally:
            self.tlock.release()
                
        return t

    def removeEvent(self,method,args,suppress_error=False): #inefficient way
        self.tlock.acquire()
        entry_found=False
        try:
            for evt in self.__events:
                if evt["method"]==method and evt["args"]==args:
                    self.__events.remove(evt)
                    entry_found=True
                    break
        finally:
            self.tlock.release()
        
        if not entry_found and not suppress_error:
            toLog("event.removeEvent: Can't find event to delete %s %s"%(method,args),LOG_DEBUG,defs.DEBUG_ALL)
        
    def doEvent(self):
        self.tlock.acquire()
        try:
                job=self.__events.pop(0)
        finally:
            self.tlock.release()
        
        if defs.LOG_EVENTS:
            toLog("Event Scheduler: Running Method:%s Arguments: %s"%(job["method"],job["args"]),LOG_DEBUG)
        
        if job["priority"]==100: #run shutdown method in main thread, not a new thread
            apply(job["method"],job["args"])
        else:

            if job["priority"] < 10:
                twrapper = "event"
            else:
                twrapper = "main"
                    
            try:
                thread_main.runThread(job["method"],job["args"],twrapper)
            except:
                logException(LOG_ERROR,"Unhandled exception on event loop")
        
    def now(self):
        return long(time.time())

    def printMe(self):
        for evt in self.__events:
            print "%s %s is going to run on %s"%(evt["method"],evt["args"],evt["timeToRun"] - time.time())

def initSched():
    global sched
    sched=Scheduler()

def addEvent(secsFromNow,method,args,priority=0):
    sched.addEvent(secsFromNow,method,args,priority)

def removeEvent(method,args,suppress_error=False):
    sched.removeEvent(method,args,suppress_error)

def startLoop():
    while True:
        try:
            sched.loop()
        except SystemExit:
            raise
        except:
            logException(LOG_ERROR, "Event Loop Exited Abnormally !!!")

