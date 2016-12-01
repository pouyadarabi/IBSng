from core.server import handlers_manager

def init():
    from core.ias.ias_actions import IASActions
    global ias_actions
    ias_actions = IASActions()

    from core.ias.ias_handler import IASHandler
    handlers_manager.getManager().registerHandler(IASHandler())
    

def getActionsManager():
    return ias_actions

