from core.server import handlers_manager

def init():
    from core.stats.stat_handler import StatHandler
    handlers_manager.getManager().registerHandler(StatHandler())

    from core.stats.stat_keeper import StatKeeper
    global stat_keeper
    stat_keeper = StatKeeper()

def getStatKeeper():
    return stat_keeper
