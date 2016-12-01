from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from radius_server import rad_main
from core.errors import *
from core.ibs_exceptions import *
import pickle
import re

attr_handler_name="radius_attrs"
def init():
    user_main.getUserPluginManager().register(attr_handler_name,RadiusAttrsUserPlugin)
    user_main.getAttributeManager().registerHandler(RadiusAttrsAttrHandler(),["radius_attrs"],["radius_attrs"],["radius_attrs"])

class RadiusAttrsUserPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"radius_attrs")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.rad_attrs=pickle.loads(self.user_obj.getUserAttrs()["radius_attrs"])
 
    def s_login(self,ras_msg):
        reply_pkt=ras_msg.getReplyPacket()
        if reply_pkt == None: #null packet?
            return 
            
        for attr_name in self.rad_attrs:
            reply_pkt[attr_name]=self.rad_attrs[attr_name]

    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()
        
class RadiusAttrsAttrUpdater(AttrUpdater):
    def changeInit(self,radius_attrs):
        groups=re.findall("(.+)=\"(.*)\"",radius_attrs)
        attrs={}
        for group in groups:
            if not rad_main.getDictionary().has_key(group[0]):
                raise GeneralException(errorText("USER_ACTIONS","INVALID_RADIUS_ATTRIBUTE")%group[0])
            attrs[group[0]]=group[1]
        self.useGenerateQuery({"radius_attrs":pickle.dumps(attrs)})

    def deleteInit(self):
        self.useGenerateQuery(["radius_attrs"])

    def checkInput(self,src,action,dargs):
        dargs["admin_obj"].checkPerm("GOD")


class RadiusAttrsAttrHolder(AttrHolder):
    def __init__(self,radius_attrs):
        self.attr_dic=pickle.loads(radius_attrs)
        self.attr_str="\n".join(map(lambda attr:"%s=\"%s\""%(attr,self.attr_dic[attr]),self.attr_dic))

    def getParsedDic(self):
        return {"radius_attrs":self.attr_str}

class RadiusAttrsAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(RadiusAttrsAttrUpdater,["radius_attrs"])
        self.registerAttrHolderClass(RadiusAttrsAttrHolder,["radius_attrs"])
