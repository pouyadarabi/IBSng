from core.plugins import plugin_loader
from core.event import periodic_events
from core.server import handlers_manager
from core import defs

def init():
    global onlines_loop
    from core.snapshot.onlines_loop import OnlinesLoop
    onlines_loop = OnlinesLoop()

    global realtime_manager
    from core.snapshot.realtime_manager import RealTimeManager
    realtime_manager = RealTimeManager()

    from core.snapshot.realtime_manager import RealTimePeriodicEvent
    periodic_events.getManager().register(RealTimePeriodicEvent())

    plugin_loader.loadPlugins(defs.IBS_CORE+"/snapshot/plugins")

    from core.snapshot.snapshot_handler import SnapShotHandler
    handlers_manager.getManager().registerHandler(SnapShotHandler())

    from core.snapshot.bw_snapshot import BWSnapShotOnlinesLoopClient
    getOnlinesLoop().registerClient(BWSnapShotOnlinesLoopClient())

    from core.snapshot.onlines_snapshot import OnlinesSnapShotOnlinesLoopClient
    getOnlinesLoop().registerClient(OnlinesSnapShotOnlinesLoopClient())

    getOnlinesLoop().doLoop() #do loop for first time
    
def getRealTimeManager():
    return realtime_manager

def getOnlinesLoop():
    return onlines_loop