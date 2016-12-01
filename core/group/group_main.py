from core.server import handlers_manager

def init():
    from core.group.group_loader import GroupLoader
    global group_loader
    group_loader=GroupLoader()
    group_loader.loadAllGroups()

    from core.group.group_actions import GroupActions
    global group_actions
    group_actions=GroupActions()

    from core.group.group_handler import GroupHandler
    handlers_manager.getManager().registerHandler(GroupHandler())

def getLoader():
    return group_loader

def getActionManager():
    return group_actions
    