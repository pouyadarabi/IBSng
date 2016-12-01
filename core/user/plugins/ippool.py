from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ippool import ippool_main
from core.errors import *
from core.ibs_exceptions import *


attr_handler_name="ippool"
def init():
    user_main.getUserPluginManager().register("ippool",IPpoolUserPlugin,4)
    user_main.getUserPluginManager().register("remote_ip",RemoteIPUserPlugin,3)
    user_main.getAttributeManager().registerHandler(IPpoolAttrHandler(),["ippool"],["ippool"],["ippool"])

class RemoteIPUserPlugin(user_plugin.UserPlugin):
    def login(self,ras_msg):
        if ras_msg.hasAttr("remote_ip"):
            self.__setRemoteIP(ras_msg)
        
    def update(self,ras_msg):
        if "remote_ip" in ras_msg["update_attrs"]:
            self.__setRemoteIP(ras_msg)

        if "mac" in ras_msg["update_attrs"]:
            self.__setMac(ras_msg)

    

    def __setRemoteIP(self,ras_msg):
        instance=self.user_obj.getInstanceFromUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
        self.user_obj.getInstanceInfo(instance)["attrs"]["remote_ip"]=ras_msg["remote_ip"]
        
        user_main.getIPMap().addIP(ras_msg["remote_ip"], self.user_obj.getUserID())
        

    def __setMac(self,ras_msg):
        instance=self.user_obj.getInstanceFromUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
        self.user_obj.getInstanceInfo(instance)["attrs"]["mac"]=ras_msg["mac"]


class IPpoolUserPlugin(user_plugin.UserPlugin):
 
    def getIPpoolID(self):    
        return int(self.user_obj.getUserAttrs()["ippool"])

    def getIPpoolObj(self):
        ippool_id = self.getIPpoolID()
        return ippool_main.getLoader().getIPpoolByID(ippool_id)

    def login(self,ras_msg):
        if not self.user_obj.getUserAttrs().hasAttr("ippool"):
            return
    
        if ras_msg.hasAttr("re_onlined") and \
           not ras_msg.getReplyPacket().has_key("Framed-IP-Address"):

            #Re Onlined user

            if ras_msg.hasAttr("remote_ip") and self.getIPpoolObj().hasIP(ras_msg["remote_ip"]):
                try:
                    self.getIPpoolObj().useIP(ras_msg["remote_ip"])
                except IPpoolFullException:
                    raise LoginException(errorText("USER_LOGIN", "REMOTE_IP_CONFLICT"))

                self.__updateInstanceInfo(self.user_obj.instances, self.getIPpoolID(), ras_msg["remote_ip"])
            

        elif self.user_obj.isNormalUser() and \
           (not ras_msg.hasAttr("ip_assignment") or ras_msg["ip_assignment"]==True) and \
           not ras_msg.getReplyPacket().has_key("Framed-IP-Address"):
           
            #Normal Login User
            
            ip = None
            try:
                ip=self.getIPpoolObj().setIPInPacket(ras_msg.getReplyPacket())
            except GeneralException: #ippool deleted?
                logException(LOG_DEBUG)
            except IPpoolFullException:
                pass

            if ip != None:
                self.__updateInstanceInfo(self.user_obj.instances, self.getIPpoolID(), ip)


    def logout(self,instance,ras_msg):
        if self.user_obj.getInstanceInfo(instance).has_key("ippool_id"):
            try:
                ippool_main.getLoader().getIPpoolByID(self.user_obj.getInstanceInfo(instance)["ippool_id"]).freeIP(self.user_obj.getInstanceInfo(instance)["attrs"]["ippool_assigned_ip"])
            except GeneralException:
                logException(LOG_DEBUG)
        
    def update(self,ras_msg):
        if "ippool_id" in ras_msg["update_attrs"]:
            instance=self.user_obj.getInstanceFromUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
            if instance==None:
                raise IBSError("Got Update ippool info for user %s while he has no instance online on %s %s"%
                                                                                                (self.user_obj.getUserID(),
                                                                                                ras_msg.getRasID(),
                                                                                                ras_msg.getUniqueIDValue()))

            self.__updateInstanceInfo(instance,ras_msg["ippool_id"],ras_msg["ippool_assigned_ip"])


    def __updateInstanceInfo(self,instance,ippool_id,ip):
        instance_info=self.user_obj.getInstanceInfo(instance)
        instance_info["ippool_id"]=ippool_id
        instance_info["attrs"]["ippool"]=ippool_main.getLoader().getIPpoolByID(ippool_id).getIPpoolName()
        instance_info["attrs"]["ippool_assigned_ip"]=ip
        

class IPpoolAttrUpdater(AttrUpdater):
    def changeInit(self,ippool_name):
        self.ippool_name = ippool_name
        self.ippool_obj = ippool_main.getLoader().getIPpoolByName(self.ippool_name)
        self.useGenerateQuery({"ippool":self.ippool_obj.getIPpoolID()})

    def deleteInit(self):
        self.useGenerateQuery(["ippool"])

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return ippool_main.getLoader().getIPpoolByID(int(old_value)).getIPpoolName()

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return self.ippool_name


class IPpoolAttrHolder(AttrHolder):
    def __init__(self,ippool_id):
        self.ippool_id=int(ippool_id)

    def getParsedDic(self):
        try:
            return {"ippool":ippool_main.getLoader().getIPpoolByID(self.ippool_id).getIPpoolName()}
        except GeneralException:
            logException(LOG_DEBUG)
            return {}

class IPpoolAttrSearcher(AttrSearcher):
    def run(self):
        self.exactSearchOnUserAndGroupAttrs("ippool","ippool",lambda x:ippool_main.getLoader().getIPpoolByName(x).getIPpoolID())

class IPpoolAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(IPpoolAttrUpdater,["ippool"])
        self.registerAttrHolderClass(IPpoolAttrHolder,["ippool"])
        self.registerAttrSearcherClass(IPpoolAttrSearcher)
