from core.server import handlers_manager


def init():    
    from core.defs_lib.defs_handler import DefsHandler
    handlers_manager.getManager().registerHandler(DefsHandler())
    global actions_manager
    from core.defs_lib.defs_actions import DefsActions
    actions_manager=DefsActions()

def getActionManager():
    return actions_manager