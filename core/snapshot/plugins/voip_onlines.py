from core.snapshot.realtime_snapshot import SnapShot
from core.snapshot.onlines_loop import OnlinesLoopClient
from core.snapshot import snapshot_main, snapshot_defs
from core import defs

def init():
    voip_onlines_snapshot = VoIPOnlinesSnapShot()
    snapshot_main.getRealTimeManager().register(voip_onlines_snapshot)
    snapshot_main.getOnlinesLoop().registerClient(voip_onlines_snapshot)


class VoIPOnlinesSnapShot(SnapShot, OnlinesLoopClient):
    def __init__(self):
        SnapShot.__init__(self, "voip_onlines", snapshot_defs.ONLINES_SNAPSHOT_COUNT)
        OnlinesLoopClient.__init__(self, defs.REALTIME_ONLINES_SNAPSHOT_INTERVAL) 
        
        self.__resetValues()
        
    def __resetValues(self):
        self.count = 0
    
    def processInstance(self, user_obj, instance):
        if user_obj.isVoIPUser():
            self.count += 1

    def loopEnd(self):
        self.add(self.count)
        
        self.__resetValues()    
