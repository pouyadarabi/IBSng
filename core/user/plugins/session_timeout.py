from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.errors import *
from core.ibs_exceptions import *

attr_handler_name="session_timeout"
def init():
    user_main.getUserPluginManager().register(attr_handler_name,SessionTimeoutUserPlugin)
    user_main.getAttributeManager().registerHandler(SessionTimeoutAttrHandler(),["session_timeout"],["session_timeout"],[])

class SessionTimeoutUserPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"session_timeout")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.session_timeout=long(self.user_obj.getUserAttrs()["session_timeout"])
 
    def s_login(self,ras_msg):
        reply_pkt=ras_msg.getReplyPacket()
        if not reply_pkt: #null packet?
            return 
            
        reply_pkt["Session-Timeout"]=self.session_timeout

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
        
class SessionTimeoutAttrUpdater(AttrUpdater):

    def changeInit(self,session_timeout):
        try:
            self.session_timeout = long( session_timeout )
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_SESSION_TIMEOUT"))

        self.useGenerateQuery({"session_timeout":self.session_timeout})

    def deleteInit(self):
        self.useGenerateQuery(["session_timeout"])

class SessionTimeoutAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(SessionTimeoutAttrUpdater,["session_timeout"])
