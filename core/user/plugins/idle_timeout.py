from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.errors import *
from core.ibs_exceptions import *

attr_handler_name="idle_timeout"
def init():
    user_main.getUserPluginManager().register(attr_handler_name,IdleTimeoutUserPlugin)
    user_main.getAttributeManager().registerHandler(IdleTimeoutAttrHandler(),["idle_timeout"],["idle_timeout"],[])

class IdleTimeoutUserPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"idle_timeout")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.idle_timeout=long(self.user_obj.getUserAttrs()["idle_timeout"])
 
    def s_login(self,ras_msg):
        reply_pkt=ras_msg.getReplyPacket()

        if not reply_pkt: #null packet?
            return 
        
        reply_pkt["Idle-Timeout"]=self.idle_timeout

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
        
class IdleTimeoutAttrUpdater(AttrUpdater):

    def changeInit(self,idle_timeout):
        try:
            self.idle_timeout = long( idle_timeout )
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_IDLE_TIMEOUT"))

        self.useGenerateQuery({"idle_timeout":self.idle_timeout})

    def deleteInit(self):
        self.useGenerateQuery(["idle_timeout"])

class IdleTimeoutAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(IdleTimeoutAttrUpdater,["idle_timeout"])
