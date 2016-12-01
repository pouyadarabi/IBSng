import time

class SnapShot:
    def __init__(self, name, _count):
        self.name = name
        self._count = _count

        self.dates = []
        self.values = []
        
    def getName(self):
        return self.name
    
    def add(self, value, date=None):
        """
            add new value to snapshot
            if date is not specified, current timestamp is used
        """
        if date == None:
            date=int(time.time())
    
        if len(self.dates)>self._count:
            self.dates.pop(0)
            self.values.pop(0)
        
        self.dates.append(date)
        self.values.append(value)

    def getDates(self):
        """
            we may need to copy the list before returning
        """
        return self.dates

    def getValues(self):
        return self.values
    
    def update(self):
        """
            children should overide this to update themselves
        """
        pass


######################################
#               UN-USED CODE
######################################
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/

class GenericSnapShotManager(SnapShot):
    """
        Generic snapshots has generic loops and run other snapshot updaters in inner loop
    """
    def __init__(self, name, _count):
        SnapShot.__init__(self, name, _count)
        self.__generic_snapshots = []

    def registerMethods(self, generic_snapshot):
        """
            register a generic snapshot client
            generic_snapshot(GenericSnapshot Instance):
        """
        self.__update_methods.append(update_method)
        self.__end_methods.append(end_method)

    def callUpdateMethods(self, *args):
        self.__callMethods("genericUpdate", *args)

    def callEndMethods(self, *args):
        self.__callMethods("genericEnd", *args)

    def __callMethods(self, method_name, *args):
        for generic_snapshot in self.__generid_snapshots:
            getattr(generic_snapshot, method_name)(*args)

class BWGenericSnapShotManager(GenericSnapShotManager):
    def update(self):
        onlines = user_main.getOnline().getOnlineUsers()
        state = {}
        for user_obj in onlines.itervalues():
            if user_obj.isNormalUser():
                for instance in xrange(1,user_obj.instances+1):
                        try:
                            _in,out,in_rate,out_rate = user_obj.getTypeObj().getInOutBytes(instance)
                            self.callUpdateMethods(user_obj, instance, _in, out, in_rate, out_rate)
                        except:
                            logException(LOG_DEBUG)
        
        self.callEndMethods()

class OnlineSnapShotManager(GenericSnapShotManager):
    def update(self):
        onlines = user_main.getOnline().getOnlineUsers()
        state = {}
        for user_obj in onlines.itervalues():
            if user_obj.isNormalUser():
                for instance in xrange(1,user_obj.instances+1):
                        try:
                            _in,out,in_rate,out_rate = user_obj.getTypeObj().getInOutBytes(instance)
                            self.callUpdateMethods(user_obj, instance, _in, out, in_rate, out_rate)
                        except:
                            logException(LOG_DEBUG)
        
        self.callEndMethods()