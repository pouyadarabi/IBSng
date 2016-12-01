from core.ibs_exceptions import *
from core.event import event
from core.user import user_main

import time, sys

class OnlinesLoop:
    DEBUG = False

    def __init__(self):
        self.__clients = []
        
    def registerClient(self, client_obj):
        """
            Register a client object
            client_obj processInstance in runned each run_interval for each instance of each user
        """
        if not isinstance(client_obj, OnlinesLoopClient):
            raise IBSError("Onlines Loop Registered client is invalid") 
    
        self.__clients.append(client_obj)

    def __prepareLoop(self):
        """
            prepare loop by finding this loop clients
            and update last_runs of all clients
        """
        now = int(time.time()) + 1
        min_next_run = sys.maxint
        loop_clients = [] #clients that will be runned in this loop
        
        for client in self.__clients:
            last_run = client.getLastRun()
            
            if last_run == 0:
                next_run = now
            else:
                next_run = last_run + client.getRunInterval()
            
            if next_run <= now:

                loop_clients.append(client)

                client.updateLastRun(next_run) #update client last run
                next_run = now + client.getRunInterval()
        
            min_next_run = min(next_run, min_next_run)
        
        return min_next_run - now, loop_clients
            
    def __setEventForNextRun(self, time_to_next_run):
        event.addEvent(time_to_next_run, self.doLoop, [])

    def doLoop(self):
        start = time.time()
    
        time_to_next_run, loop_clients = self.__prepareLoop()
        
        if self.DEBUG:
            toLog("OnlinesLoop: time_to_next_run: %s loop_clients: %s"%(time_to_next_run, loop_clients), LOG_DEBUG)
        
        self.__doLoop(loop_clients)

        #set event after the loop prevents from double runs
        self.__setEventForNextRun(time_to_next_run) 

        if self.DEBUG:
            toLog("OnlinesLoop: Loop took %s seconds"%(time.time() - start), LOG_DEBUG)
            

    def __doLoop(self, loop_clients):
        """
            actually run the loop on online users
        """
        onlines = user_main.getOnline().getOnlineUsers()
        for user_obj in onlines.itervalues():
            for instance in xrange(1,user_obj.instances+1):
                self.__runMethod(loop_clients, "processInstance", user_obj, instance)
        
        self.__runMethod(loop_clients, "loopEnd")

    def __runMethod(self, loop_clients, method_name, *args):
        for client in loop_clients:
            try:
                getattr(client, method_name)(*args)
            except:
                logException(LOG_ERROR, "Snapshots OnlinesLoop")
        

class OnlinesLoopClient:
    def __init__(self, run_interval):
        self.__run_interval = run_interval
        self.__last_run = 0
        
    def getRunInterval(self):
        return self.__run_interval

    def updateLastRun(self, last_run_epoch):
        self.__last_run = last_run_epoch

    def getLastRun(self):
        return self.__last_run
    
    ######################## these functions should be overriden by children
    def processInstance(self, user_obj, instance):
        """
            process "instance" of "user_obj"
            all raised Exceptions are catched and logged
        """
        pass

    def loopEnd(self):
        """
            announce end of loop. 
            client may do insert/update and cleanups here
        """
        pass
    
