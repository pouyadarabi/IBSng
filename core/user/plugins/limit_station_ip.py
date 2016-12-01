"""
    Limit Station IP Address Plugin: This plugin limit ip address that user can login from
"""
from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.lib import iplib

attr_handler_name="limit_ip_station_ip_address"
def init():
    user_main.getUserPluginManager().register("limit_station_ip",LimitStationIPPlugin,1)
    user_main.getAttributeManager().registerHandler(LimitStationIPAttrHandler(),["limit_station_ip"],["limit_station_ip"],[])

class LimitStationIPPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"limit_station_ip")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.ips=self.user_obj.getUserAttrs()["limit_station_ip"].split(",")

    def s_login(self,ras_msg):
        if ras_msg.hasAttr("station_ip"):
            for ip_range in self.ips:
                if iplib.isIPAddrIn(ras_msg["station_ip"], ip_range):
                    return

            raise LoginException(errorText("USER_LOGIN","LOGIN_FROM_THIS_IP_DENIED"))

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
        
class LimitStationIPAttrUpdater(AttrUpdater):

    def changeInit(self,ips):
        ip_list=map(lambda ip:ip.strip(),MultiStr(ips))

        for ip in ip_list:
            if not iplib.checkIPAddr(ip):
                raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%ip)

        self.useGenerateQuery({"limit_station_ip":",".join(ip_list)})

    def deleteInit(self):
        self.useGenerateQuery(["limit_station_ip"])

class LimitStationIPAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.likeStrSearch(search_helper,"limit_station_ip","limit_station_ip_op","limit_station_ip",MultiStr)


class LimitStationIPAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(LimitStationIPAttrUpdater,["limit_station_ip"])
        self.registerAttrSearcherClass(LimitStationIPAttrSearcher)
