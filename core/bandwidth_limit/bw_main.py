from core.server import handlers_manager
from core.event import periodic_events
import signal


def init():
    global bw_loader
    from core.bandwidth_limit.bw_loader import BWLoader
    bw_loader=BWLoader()
    bw_loader.loadAll()
    registerInParents()

    global tc
    from core.bandwidth_limit.tc import TC
    tc=TC()

    global mark_id_pool
    from core.bandwidth_limit.idpool import IDPool
    mark_id_pool=IDPool([10000,4294967295],"iptables mark")
    
    global iptables
    from core.bandwidth_limit.iptables import IPTables
    iptables=IPTables()
    
    initTree()

    global manager
    from core.bandwidth_limit.bw_manager import BWManager,UpdateCounters
    manager=BWManager()
    periodic_events.getManager().register(UpdateCounters())    
    
    global actions
    from core.bandwidth_limit.bw_actions import BWActions
    actions=BWActions()
    
    from core.bandwidth_limit.bw_handler import BWHandler
    handlers_manager.getManager().registerHandler(BWHandler())

    applyStatics()


    setReCreateTreeSignalHandler()
    
#################    
    
def getLoader():
    return bw_loader

def getTCRunner():
    return tc
    
def getMarkIDPool():
    return mark_id_pool

def getIPTablesRunner():
    return iptables

def getManager():
    return manager
    
def getActionsManager():
    return actions

#################
def registerInParents():
    list([getLoader().getNodeByID(node_id).registerInParent() for node_id in getLoader().getAllNodeIDs()])

    list([getLoader().getLeafByName(leaf_name).registerInParent() for leaf_name in getLoader().getAllLeafNames()])

def initTree():
    list([getLoader().getInterfaceByName(interface_name).createTree() for interface_name in getLoader().getAllInterfaceNames()])

def applyStatics():
    list([getLoader().getStaticIPByIP(ip).apply() for ip in getLoader().getAllStaticIPs()])

####################
def setReCreateTreeSignalHandler():
    """
        set signal handler for recreating signal handler
    """
    signal.signal(signal.SIGUSR2,reCreateTreeSignalHandler)

def reCreateTreeSignalHandler(signum,frame):
    """
        reinit tree, and apply static 
    """
    initTree()
    applyStatics()
    return

