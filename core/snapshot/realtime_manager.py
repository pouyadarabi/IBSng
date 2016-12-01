from core.event import periodic_events
from core.errors import errorText
from core.ibs_exceptions import *
from core.snapshot import snapshot_main,snapshot_defs

    
class RealTimeManager:
    def __init__(self):
        self.snapshots = {} #name:obj

    def register(self, snapshot_obj):
        """
            register snapshot object, so it would be updates every REALTIME_SNAPSHOT_INTERVAL
        """
        self.snapshots[snapshot_obj.getName()]=snapshot_obj
        
    def updateAll(self):
        for snapshot in self.snapshots.values():
            try:
                snapshot.update()
            except:
                logException(LOG_ERROR)
    
    def getSnapShot(self, name):
        try:
            return self.snapshots[name]
        except KeyError:
            raise GeneralException(errorText("REPORTS","INVALID_SNAPSHOT_NAME")%name)
    
class RealTimePeriodicEvent(periodic_events.PeriodicEvent):
    def __init__(self):
        periodic_events.PeriodicEvent.__init__(self,"RealTime Snapshot", defs.REALTIME_ONLINES_SNAPSHOT_INTERVAL, [], 0)

    def run(self):
        snapshot_main.getRealTimeManager().updateAll()

