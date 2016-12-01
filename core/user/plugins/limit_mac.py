"""
    Limit Mac Address Plugin: This plugin limit mac address that user can login from
"""
from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.lib import maclib

attr_handler_name="limit_mac_address"
def init():
    user_main.getUserPluginManager().register("limit_mac",LimitMacPlugin,1)
    user_main.getAttributeManager().registerHandler(LimitMacAttrHandler(),["limit_mac"],["limit_mac"],[])

class LimitMacPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"limit_mac")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.macs=self.user_obj.getUserAttrs()["limit_mac"].split(",")

    def s_login(self,ras_msg):
        if ras_msg.hasAttr("mac") and ras_msg["mac"] not in self.macs:
            raise LoginException(errorText("USER_LOGIN","LOGIN_FROM_THIS_MAC_DENIED"))

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()

        
class LimitMacAttrUpdater(AttrUpdater):

    def changeInit(self,macs):
        mac_list=map(lambda mac:mac.strip(),MultiStr(macs))

        for mac in mac_list:
            if not maclib.checkMacAddress(mac):
                raise GeneralException(errorText("GENERAL","INVALID_MAC_ADDRESS")%mac)

        self.useGenerateQuery({"limit_mac":",".join(mac_list)})

    def deleteInit(self):
        self.useGenerateQuery(["limit_mac"])

class LimitMacAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.likeStrSearch(search_helper,"limit_mac","limit_mac_op","limit_mac",MultiStr)


class LimitMacAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(LimitMacAttrUpdater,["limit_mac"])
        self.registerAttrSearcherClass(LimitMacAttrSearcher)
