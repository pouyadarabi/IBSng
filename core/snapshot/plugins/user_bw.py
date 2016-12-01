from core.snapshot.realtime_snapshot import SnapShot
from core.snapshot.onlines_loop import OnlinesLoopClient
from core.snapshot import snapshot_main, snapshot_defs
from core.ibs_exceptions import *
from core import defs

def init():
    user_bw_snapshot = UserBWSnapShot()

    snapshot_main.getRealTimeManager().register(user_bw_snapshot)
    snapshot_main.getOnlinesLoop().registerClient(user_bw_snapshot)

class UserBWSnapShot(SnapShot, OnlinesLoopClient):
    def __init__(self):
        SnapShot.__init__(self, "user_bw", snapshot_defs.USER_BW_SNAPSHOT_COUNT)
        OnlinesLoopClient.__init__(self, defs.REALTIME_BW_SNAPSHOT_INTERVAL)
        
        self.__resetValues()

    def __resetValues(self):
        self.state = {}
    
    def processInstance(self, user_obj, instance):
        if user_obj.isNormalUser():
            _in,out,in_rate,out_rate = user_obj.getTypeObj().getInOutBytes(instance)
            ras_id,unique_id_val = user_obj.getGlobalUniqueID(instance)
            self.state[",".join(map(str,(user_obj.getUserID(), ras_id, unique_id_val)))] = (in_rate, out_rate)
        
    def loopEnd(self):
        self.add(self.state)
        self.__resetValues()
