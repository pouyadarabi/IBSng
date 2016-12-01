from core.server import handlers_manager
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main



def init():
    global admin_loader,admin_actions,deposit_change_log_actions

    import core.admin.perm_loader
    core.admin.perm_loader.init()

    from core.admin.admin_loader import AdminLoader
    admin_loader=AdminLoader()
    admin_loader.loadAllAdmins()

    from core.admin.admin_actions import AdminActions
    admin_actions=AdminActions()

    import core.admin.perm_actions
    core.admin.perm_actions.init()

    from core.admin.deposit_change_log import DepositChangeLogActions
    deposit_change_log_actions=DepositChangeLogActions()
    

    from core.admin.admin_handler import AdminHandler
    handlers_manager.getManager().registerHandler(AdminHandler())

    from core.admin.perm_handler import PermHandler
    handlers_manager.getManager().registerHandler(PermHandler())

def getActionManager():
    return admin_actions

def getLoader():
    return admin_loader

def getDepositChangeLogActions():
    return deposit_change_log_actions
