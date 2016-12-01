import threading
from core.threadpool import threadpool
from core.ibs_exceptions import *
import time, copy


class ThreadPoolWrapper:
    """
        Wrapper for threadpool
        it use a queue, to enqueue jobs that currently can't run due to our maximum 
        number of allocated threads limit.
        if we didn't get to the limit, we'll ask the mainThreadPool to get us a thread
    """

    DEBUG = False

    def __init__(self, usage_limit, name):
        """
            usage_limit(integer): maximum number of allocated threads for this object
            name(String): Object name, used for debugging
        """
        self.__tlock=threading.RLock()
        self.__usage=0 #thread usages
        self.__usage_limit=usage_limit #thread usage limit
        self.__name=name
        self.__queue=[]# [[method, arg, queue_time]]

    def getName(self):
        return self.__name
    
    def getQueue(self):
        return copy.copy(self.__queue)

    def __runInThreadPool(self,method,args):
        threadpool.getThreadPool().runThread(self,method,args)

    def runThread(self,method,args):
        """
            run a new thread whithin this wrapper
        """
        self.__tlock.acquire()
        try:
            if self.__usage>self.__usage_limit:
                self.__addToQueue(method, args)
            else:
                self.__runInThreadPool(method,args)     
                self.__usage += 1
        finally:
            self.__tlock.release()

    def __addToQueue(self, method, args):
        if self.DEBUG:
            toLog("ThreadWrapper %s: Queued job %s %s"%(self.getName(), method, args), LOG_DEBUG)
            threadpool.getThreadPool().logThreads()
    
        self.__queue.append([method,args, long(time.time())])
    
    def threadReleased(self):
        """
            called when main thread pool wants to signal us that one of our threads released
        """
        self.__tlock.acquire()
        try:
            if len(self.__queue)>0:
                (method,args,queue_time)=self.__queue.pop(0)
                self.__runInThreadPool(method,args)
            else:
                self.__usage -= 1
        finally:
            self.__tlock.release()
