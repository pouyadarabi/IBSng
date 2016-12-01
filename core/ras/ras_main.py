from core.server import handlers_manager
from core.plugins.plugin_loader import loadPlugins
from core import defs

RAS_IMPLEMENTIONS="%s/ras/rases"%defs.IBS_CORE

def init():
    from core.ras.ras_factory import RasFactory
    global ras_factory
    ras_factory=RasFactory()

    loadPlugins(RAS_IMPLEMENTIONS)
    
    from core.ras.ras_actions import RasActions
    global ras_actions
    ras_actions=RasActions()

    from core.ras.user_msg_dispatcher import UserMsgDispatcher
    global user_msg_dispatcher
    user_msg_dispatcher=UserMsgDispatcher()

    from core.ras.ras_loader import RasLoader
    global ras_loader
    ras_loader=RasLoader()
    ras_loader.loadAllRases()

    from core.ras.ras_handler import RasHandler
    handlers_manager.getManager().registerHandler(RasHandler())

    
def getFactory():
    return ras_factory

def getLoader():
    return ras_loader

def getActionManager():
    return ras_actions

def getUserMsgDispatcher():
    return user_msg_dispatcher
    