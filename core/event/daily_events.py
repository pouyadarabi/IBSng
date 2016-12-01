"""
    these module handles events that should be run daily 
    there are two defined daily jobs, one LowLoadJobs that will be run when system is in low load
    (normally 4:30 AM) and midnoght jobs that will be run each midnight. 
    The diffrence between daily events and periodic events are: time of last daily event run is kept in
    database, and the event will be runned at ibs startup if it's more than 24 hours 
    after its last run
"""

from core.ibs_exceptions import *
from core.event import event
from core.lib import ibs_states
from core.lib.time_lib import *
from core import main

def init():
    global lowload,midnight
    lowload=DailyEvents("lowload","LOWLOAD_JOBS",4,1)
    midnight=DailyEvents("midnight","MIDNIGHT_JOBS",0,1)
    main.registerPostInitMethod(postInit)

def postInit():
    lowload.checkLastRun()
    midnight.checkLastRun()

    lowload.setNextDayEvent()
    midnight.setNextDayEvent()
    
def addLowLoadJob(function,args):
    lowload.addJob(function,args)

def addMidnightJob(function,args):
    midnight.addJob(function,args)

class DailyEvents:
    def __init__(self, name, state_name, hour, minute):
        """
            name(string): name of event, just used for debugings
            state_name(string): name of state, that is load and saved into db
        """
        self.__jobs=[]
        self.name=name
        self.__state_name=state_name
        self.hour=hour
        self.minute=minute

    def __repr__(self):
	return str(self)

    def __str__(self):
	return "Daily Events %s"%self.name

    def checkLastRun(self):
        """
            check last time that jobs done
            if it's more than 24 hours then do it now
        """
        state_obj=ibs_states.State(self.__state_name)
        last_run=long(state_obj.getCurVal())
        if last_run < time.time() - secondsFromMorning():
            self.__doJobs()
            self.__updateLastRun()

    def __updateLastRun(self):
        """
            update state value of last run
        """
        state_obj=ibs_states.State(self.__state_name)
        state_obj.setValue(long(time.time()))
                                                  
    def setNextDayEvent(self):
        """
            set event for next run
        """
        next_run=getEpochTimeFromHourOfDay(self.hour,self.minute,5,0)
        now=time.time()
        if next_run<now:
            next_run=getEpochTimeFromHourOfDay(self.hour,self.minute,5,1)
        next_run -= now
        event.addEvent(next_run,self.eventCall,[])

    def addJob(self,function,args):
        """
            add a job to do on doJobs
        """
        self.__jobs.append((function,args))
    
    def eventCall(self):
        """
            this method called by event sched
        """
        self.setNextDayEvent()
        self.__doJobs()
        self.__updateLastRun()

    def __doJobs(self):
        """
            do all jobs
        """
        if defs.DEBUG_LEVEL>=defs.DEBUG_ALL:
            toLog("do jobs done for %s @ %s"%(self.name,time.time()),LOG_DEBUG)
        
        for (function,args) in self.__jobs:
            try:
                apply(function,args)
            except:
                logException(LOG_ERROR,"dailyEvents: %s"%self.name)
        

    
