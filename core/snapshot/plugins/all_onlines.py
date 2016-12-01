from core.snapshot.realtime_snapshot import SnapShot
from core.snapshot import snapshot_main,snapshot_defs
from core.user import user_main

def init():
    snapshot_main.getRealTimeManager().register(AllOnlinesSnapShot())

class AllOnlinesSnapShot(SnapShot):
    def __init__(self):
        SnapShot.__init__(self, "all_onlines", snapshot_defs.ONLINES_SNAPSHOT_COUNT)
    
    def update(self):
        self.add(user_main.getOnline().getOnlinesCount())