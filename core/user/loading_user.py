import threading
from core.ibs_exceptions import *

class LoadingUser:
        """
            This class prevent from double parallel load of a same user
            second loader will sleep until first one finishes
        """
        DEBUG=False

        def __init__(self):
            self.lock=threading.Lock()
            self.__loading={} #currently loading users
        
        def isLoading(self,user):
            return user in self.__loading

        def loadingStart(self,user):
            """
                called when we start loading a user
                caller may sleep here until load of previous instance of user finishes
            """
            self.__debugLog("start",user)
            
            wait=None
            self.lock.acquire()
            try:
                if user in self.__loading:
                    self.__debugLog("queue",user)
                
                    if self.__loading[user][0]==None:
                        self.__loading[user][0]=UserEvent(self.__loading[user][1])
                    wait=self.__loading[user][0].requestWait()
                else:
                    self.__loading[user]=[None,threading.currentThread()]
            finally:
                self.lock.release()

            if wait!=None:
                self.__loading[user][0].wait(wait)
                self.__debugLog("release after wait",user)
            else:
                self.__debugLog("release without wait",user)
                
        def loadingEnd(self,user):
            """
                called when we end loading a user
                this method wake waiter of user if any
            """
            self.__debugLog("end",user)

            self.lock.acquire()
            try:
                user_event,thread=self.__loading[user]
                if user_event!=None and user_event.getWaitingCount():
                    user_event.notify()
                else:
                    del(self.__loading[user])
            finally:
                self.lock.release()

        def __debugLog(self, action, user):
            if self.DEBUG:
                toLog("Thread: %s Action: %s User: %s"%(threading.currentThread().getName(), action, user),LOG_DEBUG)
        
class UserEvent:
    def __init__(self,running_thread):
        """
            object of this class would be created when two threads wants to enter critical
            section of same user
        """
        self.waiting=[]
        self.running_thread=running_thread
        self.recursive_calls=0
        
    def __setRunningThread(self):
        self.running_thread=threading.currentThread()
    
    def requestWait(self):
        if threading.currentThread()!=self.running_thread:
            evt=threading.Event()
            evt.clear()
            self.waiting.append((evt,threading.currentThread()))
            return evt
        else:
            self.recursive_calls+=1
            return None
    
    def wait(self,evt):
        evt.wait()
        self.__setRunningThread()

    def notify(self):
        if self.recursive_calls>0:
            self.recursive_calls-=1
        elif len(self.waiting):
            evt,thread=self.waiting.pop(0)
            self.running_thread=None
            evt.set()

    def getWaitingCount(self):
        return len(self.waiting)+self.recursive_calls
        