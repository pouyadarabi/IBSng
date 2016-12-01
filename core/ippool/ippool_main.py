from core.server import handlers_manager

def init():
    from core.ippool.ippool_loader import IPpoolLoader    
    global ippool_loader
    ippool_loader=IPpoolLoader()
    ippool_loader.loadAllIPpools()

    from core.ippool.ippool_actions import IPpoolActions
    global ippool_actions
    ippool_actions=IPpoolActions()

    from core.ippool.ippool_handler import IPpoolHandler
    handlers_manager.getManager().registerHandler(IPpoolHandler())

    

def getLoader():
    return ippool_loader

def getActionsManager():
    return ippool_actions
