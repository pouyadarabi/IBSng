import time
import threading

from core import defs,db_handle
from core.ibs_exceptions import *
from core.event import event
from core import main
from core.lib.general import *

class DBPool:
    def __init__(self):
        self.tlock=threading.Lock()
        self.__pool=[]
        self.__in_use={}
        self.__total_handles=0
        self.__initializeHandles()

    def __initializeHandles(self):
        retry=3
        for i in range(defs.DB_POOL_DEFAULT_CONNECTIONS):
            while not main.isShuttingDown():
                try:
                    self.__addNewHandleToPool()
                except DBException:
                    if retry==0:
                        raise
                    elif i==0:
                        retry-=1
                        time.sleep(5)
                        continue
                break           

    def __addNewHandleToPool(self):
        handle=self.__createNewHandle()
        self.__pool.append(handle)
        self.__total_handles+=1
            
    def __createNewHandle(self):
        return db_handle.getDBHandle()

    ######################################
    def getHandle(self):
        """
            return a db handle, may raise an DBException on error
        """
        self.tlock.acquire()
        try:
            if len(self.__pool)==0:
                if self.__total_handles>defs.DB_POOL_MAX_CONNECTIONS:
                    raise DBException("Maximum number of %s handles already in use"%defs.DB_POOL_MAX_CONNECTIONS)
                else:
                    self.__addNewHandleToPool()
            handle=self.__useOneHandle()
            return handle
        finally:
            self.tlock.release()

    def __useOneHandle(self):
        """
            pop a handle from pool and add it to in_use
        """
        handle=self.__pool.pop()
        self.__in_use[handle]=time.time()
        return handle
        
    ######################################
    def release(self,handle):
        self.tlock.acquire()
        try:
            del(self.__in_use[handle])
            self.__pool.insert(0,handle)
        finally:
            self.tlock.release()
    ##########################
    def check(self):
        self.tlock.acquire()
        try:
            self.__checkInUse()
            self.__checkPool()
        finally:
            self.tlock.release()

    def __checkInUse(self):
        min_allocate_time=time.time()-defs.DB_POOL_MAX_RELEASE_TIME
        to_del=[]
        for handle in self.__in_use:
            if self.__in_use[handle]<min_allocate_time:
                toLog("Detected Stale DB Connection, allocate_time:%s min_allocate_time:%s"%(self.__in_use[handle],min_allocate_time),LOG_ERROR)
                to_del.append(handle)

#        for handle in to_del:
#Don't close the in-use handle. The result is unexpected
#            handle.close()
#            del(self.__in_use[handle])
            #self.__addNewHandleToPool()

    def __checkPool(self):
        to_del=[]
        for handle in self.__pool:
            try:
                handle.check() #ping and reset connection
            except DBException,e:
                logException(LOG_ERROR)
                to_del.append(handle)

        for handle in to_del:
            self.__pool.remove(handle)
            self.__addNewHandleToPool()
    ################################
    def close(self): 
        self.tlock.acquire()
        try:
            for handle in self.__pool:
                try:
                    handle.close()
                except:
                    logException(LOG_ERROR,"dbpool.close")

            for handle in self.__in_use:
                try:
                    toLog("In Use Database Handle while shutting down!!!",LOG_ERROR)
                    handle.close()
                except:
                    logException(LOG_ERROR,"dbpool.close")
        finally:
            self.tlock.release()

def initPool():
    global main_pool
    main_pool=DBPool()
    from core.db import db_check
    db_check.init()

def getPool():
    return main_pool

