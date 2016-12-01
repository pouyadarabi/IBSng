from core.plugins import plugin_loader
from core import defs
from core.server import handlers_manager
from core.event import periodic_events
from core import main

def init():
    global user_audit_log_manager
    from core.user.user_audit_log import UserAuditLog
    user_audit_log_manager = UserAuditLog()

    from core.user import user_actions,user_plugin,attribute_manager
    global attr_manager
    attr_manager = attribute_manager.AttributeManager()
    
    global user_loader
    from core.user.user_loader import UserLoader
    user_loader = UserLoader()

    global user_pool
    from core.user.user_pool import UserPool
    user_pool = UserPool()
    
    global mail_actions
    from core.user.mail_actions import MailActions
    mail_actions=MailActions()

    global user_action_manager
    user_action_manager = user_actions.UserActions()

    global user_plugin_manager
    user_plugin_manager = user_plugin.UserPluginManager()

    global credit_change_log_actions
    from core.user.credit_change_log import CreditChangeLogActions
    credit_change_log_actions = CreditChangeLogActions()

    global connection_log_manager
    from core.user.connection_log import ConnectionLogActions
    connection_log_manager = ConnectionLogActions()


    global add_user_save_actions
    from core.user.add_user_save import AddUserSaveActions,AddUserSaveHandler
    add_user_save_actions = AddUserSaveActions()
    handlers_manager.getManager().registerHandler(AddUserSaveHandler())

    global ras_msg_dispatcher
    from core.user.ras_msg_dispatcher import RasMsgDispatcher
    ras_msg_dispatcher = RasMsgDispatcher()
    
    global online
    from core.user.online import OnlineUsers,OnlineCheckPeriodicEvent
    online = OnlineUsers()
    periodic_events.getManager().register(OnlineCheckPeriodicEvent())
    
    global user_server_auth
    from core.user.server_auth import UserServerAuth
    user_server_auth = UserServerAuth()
    
    global dialer_errors
    from core.user.dialer_errors import DialerErrors
    dialer_errors = DialerErrors()

    global voip_errors
    from core.user.voip_errors import VoIPErrors
    voip_errors = VoIPErrors()

    global ip_map
    from core.user.ip_map import IPMap
    ip_map=IPMap()

    global user_plugin_modules
    user_plugin_modules=plugin_loader.loadPlugins(defs.IBS_CORE+"/user/plugins")

    from core.user.user_handler import UserHandler
    handlers_manager.getManager().registerHandler(UserHandler())

def shutdown():
    if main.isSuccessfullyStarted():
        getActionManager().shutdownUsers()

def getActionManager():
    return user_action_manager

def getUserPluginManager():
    return user_plugin_manager

def getAttributeManager():
    return attr_manager

def getUserLoader():
    return user_loader

def getUserPool():
    return user_pool

def getCreditChangeLogActions():
    return credit_change_log_actions

def getConnectionLogManager():
    return connection_log_manager

def getAddUserSaveActions():
    return add_user_save_actions

def getRasMsgDispatcher():
    return ras_msg_dispatcher

def getOnline():
    return online

def getServerAuth():
    return user_server_auth

def getDialerErrors():
    return dialer_errors

def getVoIPErrors():
    return voip_errors
    
def getUserAuditLogManager():
    return user_audit_log_manager

def getMailActions():
    return mail_actions 

def getUserPluginModules():
    return user_plugin_modules

def getIPMap():
    return ip_map