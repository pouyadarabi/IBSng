from core.snapshot.realtime_snapshot import SnapShot
from core.snapshot.onlines_loop import OnlinesLoopClient
from core.snapshot import snapshot_main, snapshot_defs
from core.user import user_main
from core.ibs_exceptions import *

def init():
    internet_bw_snapshot = InternetBWSnapShot()

    snapshot_main.getRealTimeManager().register(internet_bw_snapshot)
    snapshot_main.getOnlinesLoop().registerClient(internet_bw_snapshot)


class InternetBWSnapShot(SnapShot, OnlinesLoopClient):
    def __init__(self):
        SnapShot.__init__(self, "internet_bw", snapshot_defs.ONLINES_SNAPSHOT_COUNT)
        # we should obey onlines interval instead of bw
        OnlinesLoopClient.__init__(self, defs.REALTIME_ONLINES_SNAPSHOT_INTERVAL) 
    
        self.__resetValues()
    
    def __resetValues(self):
        self.in_sum = 0
        self.out_sum = 0
    

    def processInstance(self, user_obj, instance):
        if user_obj.isNormalUser():
            _in,out,in_rate,out_rate = user_obj.getTypeObj().getInOutBytes(instance)
            self.in_sum += in_rate
            self.out_sum += out_rate

    def loopEnd(self):
        self.add((self.in_sum,self.out_sum))

        self.__resetValues()    
