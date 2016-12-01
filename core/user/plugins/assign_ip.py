from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.lib import iplib
from core.lib.multi_strs import MultiStr
from core.errors import *
from core.ibs_exceptions import *
from core.ippool import ippool

def init():
    user_main.getUserPluginManager().register("assign_ip",AssignIPUserPlugin,3)
    user_main.getAttributeManager().registerHandler(AssignIPAttrHandler(),["assign_ip"],["assign_ip"],[])

class AssignIPUserPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self, user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self, user_obj, "assign_ip")
        if self.hasAttr():
            self.__initIPContainer()

    ############################################# IP Container methods
    def __initIPContainer(self):
        self.ip_container = ippool.IPPoolContainer(\
                                self.user_obj.getUserAttrs()["assign_ip"].split(","), "user_ip_container %s"%self.user_obj.getUserID())

    def __reloadIPContainer(self):
        self.ip_container._reload(self.user_obj.getUserAttrs()["assign_ip"].split(","))
                            
    def getIPContainer(self):
        return self.ip_container
    #############################################
 
    def s_login(self,ras_msg):
        if ras_msg.hasAttr("re_onlined"):
        
            #re onlined user    
        
            if ras_msg.hasAttr("remote_ip") and self.getIPContainer().hasIP(ras_msg["remote_ip"]):
                try:
                    self.getIPContainer().useIP(ras_msg["remote_ip"])
                except IPpoolFullException:
                    raise LoginException(errorText("USER_LOGIN", "REMOTE_IP_CONFLICT"))

                self.__updateInstanceInfo(self.user_obj.instances, ras_msg["remote_ip"])

        elif self.user_obj.getUserAttrs().hasAttr("assign_ip") and \
           self.user_obj.isNormalUser() and \
           (not ras_msg.hasAttr("ip_assignment") or ras_msg["ip_assignment"]==True):
           
                #normal authentication  
           
                ip = None
                try:
                    ip=self.getIPContainer().setIPInPacket(ras_msg.getReplyPacket())
                except IPpoolFullException:
                    pass

                if ip != None:
                    self.__updateInstanceInfo(self.user_obj.instances,ip)


    def s_logout(self,instance,ras_msg):
        if self.user_obj.getInstanceInfo(instance)["attrs"].has_key("assigned_ip"):
            try:
                self.getIPContainer().freeIP(self.user_obj.getInstanceInfo(instance)["attrs"]["assigned_ip"])
            except GeneralException:
                logException(LOG_DEBUG)
        

    def __updateInstanceInfo(self,instance,ip):
        instance_info=self.user_obj.getInstanceInfo(instance)
        instance_info["attrs"]["assigned_ip"]=ip

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        if self.hasAttr():
            if hasattr(self,"ip_container") and self.ip_container:
                self.__reloadIPContainer()
            else:
                self.__initIPContainer() 


class AssignIPAttrUpdater(AttrUpdater):
    """
        get a multi string ip as argument
    """
    def changeInit(self,ips):
        self.ips = MultiStr(ips)
        self.checkIPs(self.ips)
        self.useGenerateQuery({"assign_ip":",".join(map(lambda x:x,self.ips))})

    def checkIPs(self, ips):
        for ip in ips:
            if not iplib.checkIPAddrWithoutMask(ip):
                raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%ip)

    def deleteInit(self):
        self.useGenerateQuery(["assign_ip"])


class AssignIPAttrSearcher(AttrSearcher):
    def run(self):
        self.likeStrSearchOnUserAndGroupAttrs("assign_ip","assign_ip_op","assign_ip")

class AssignIPAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"assign_ip")
        self.registerAttrUpdaterClass(AssignIPAttrUpdater,["assign_ip"])
        self.registerAttrSearcherClass(AssignIPAttrSearcher)
