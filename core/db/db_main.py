from core.db import dbpool

class DBHandleQuery:
    def __init__(self,dedicate_handle=False):
        """
            dedicate_handle(boolean): by default we allocate dbhandlers for each query, if this flag is true
                                      a dbhandle will be dedicated to this object. This is usefull if you
                                      want to ensure same db connection and session is used for multiple
                                      queries. If you use this flag , you should release the dbhandle
                                      manually by calling self.releaseHandle()
        
        """
        if dedicate_handle:
            self.allocateHandle()
            self.__dedicate_handle=True
        else:
            self.__handle=None
            self.__dedicate_handle=False

    def __getattr__(self,name):
        self.method_name=name
        return self.__runQuery

    def __runQuery(self,*args):
        if not self.hasDedicatedHandle():
            self.allocateHandle()
        try:
            return apply(getattr(self.__handle,self.method_name),args)
        finally:
            if not self.hasDedicatedHandle():
                self.releaseHandle()

    def hasHandle(self):
        return self.__handle!=None

    def hasDedicatedHandle(self):
        return self.__dedicate_handle

    def allocateHandle(self):
        self.__handle=dbpool.getPool().getHandle()

    def releaseHandle(self):
        dbpool.getPool().release(self.__handle)
        self.__handle=None
        
    
def init():
    dbpool.initPool()
    from core.event import daily_events
    daily_events.addLowLoadJob(vacuumDB,[])

def shutdown():
    dbpool.getPool().close()

def getHandle(dedicated=False):
    return DBHandleQuery(dedicated)

def vacuumDB():
    getHandle().query("vacuum analyze")
    