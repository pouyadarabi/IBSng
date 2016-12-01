import time
import re

from core.user import user_main
from core.ras import ras_main
from core.ibs_exceptions import *

class Msg:

    username_filter_sub_pattern = re.compile("[^a-zA-Z0-9#_\-]")

    def __init__(self):
        self.action=None
        self.attrs={}
        self.time=time.time()
        
    def __getitem__(self,key):
        return self.attrs[key]

    def __setitem__(self,key,value):
        self.attrs[key]=value    

    def hasAttr(self,attr_name):
        return self.attrs.has_key(attr_name)
        
    def getAttrs(self):
        return self.attrs

    def setAction(self,action):
        self.action=action

    def getAction(self):
        return self.action

    def getTime(self):
        return self.time

    def getUniqueIDValue(self):
        """
            WARNING: unique_id values must be string!
        """
        return self[self["unique_id"]]

    def send(self):
        assert(self.action!=None)

    ###############################

    def getUserRepr(self):
        """
            Produce a representation of user in this message by trying different attributes.
            return "N/A" if no reperesentation can be produced
        """
    
        if self.hasAttr("username"):
            return self.__filterUsername(self["username"])

        elif self.hasAttr("voip_username"):
            return self.__filterUsername(self["voip_username"])

        elif self.hasAttr("user_id"):
            return "user_id %s"%self["user_id"]

        elif self.hasAttr("caller_id"):
            return "caller_id %s"%self["caller_id"]

        else:
            return "N/A"

    def __filterUsername(self, username):
        """
            filter username from non-alpha numberic #_- characters and
            replace bad characters with ?
        """
        return self.username_filter_sub_pattern.sub("?", username)


caller_id_filter_sub = re.compile("[^a-zA-Z0-9+]")

class RasMsg(Msg):
    """
        Ras Msg is a message from ras, to user subsystem
    """

    """
        conversion map is list of attr_name=>callable_object
        when we ask to assign a attribute from request, the conversion callable object will be called with value as argument
        and return value will be replaced with value
    """
    conversion_map = {"caller_id":lambda caller_id: caller_id_filter_sub.sub("", caller_id)}

    def __init__(self,request_pkt,reply_pkt,ras_obj):
        Msg.__init__(self)
        self.request_pkt=request_pkt
        self.reply_pkt=reply_pkt
        self.ras_obj=ras_obj
    
    def getRequestPacket(self):
        return self.request_pkt

    def getReplyPacket(self):
        return self.reply_pkt

    def getRequestAttr(self,attr_name):
        return self.request_pkt[attr_name]

    def getRasID(self):
        return self.ras_obj.getRasID()

    def getRasObj(self):
        return self.ras_obj

    def createNew(self,request_pkt,reply_pkt,ras_obj):
        """
            create a new RasMsg with unique_id and unique_id_value attributes set
        """
        new_ras_msg=RasMsg(request_pkt,reply_pkt,ras_obj)
        new_ras_msg["unique_id"]=self["unique_id"]
        new_ras_msg[self["unique_id"]]=self.getUniqueIDValue()
        return new_ras_msg

    
    def setRequestToAttr(self,request_key,attr_name):
        """
            request_key(string): Request Attribute Name
            attr_name(string): Attribute Name that value will be assigned
            
            set Request packet attribute value to packet attribute with key "attr_name"
            if request attribute has multiple values, you shouldn't use this
        """
        try:
            value = self.getRequestAttr(request_key)[0]
            
            if self.conversion_map.has_key(attr_name):
                value = self.conversion_map[attr_name](value)
            
            self[attr_name] = value
        except KeyError:
            raise IBSException("Attribute %s not found in request packet"%request_key)

    def setRequestToAttrIfExists(self,request_key,attr_name):
        """
            request_key(string): Request Attribute Name
            attr_name(string): Attribute Name that value will be assigned
            
            set Request packet attribute value to packet attribute with key "attr_name" if it exists
            if request attribute has multiple values, you shouldn't use this
            
            return True if request_key exists in request or False if it doesn't exists
        """
        if self.request_pkt.has_key(request_key):
            self.setRequestToAttr(request_key, attr_name)
            return True
        else:
            return False

    def setInAttrs(self,key_dics):
        """
            key_dic(dic): dictionary in format {request_key:attr_key}
            set request keys into attributes, this is done, by calling self.setRequestToAttr multiple times
        """
        for request_key in key_dics:
            self.setRequestToAttr(request_key, key_dics[request_key])

    def setInAttrsIfExists(self,key_dics):
        """
            key_dic(dic): dictionary in format {request_key:attr_key}
            set request keys into attributes, this is done, by calling self.setRequestToAttrIfExists multiple times
        """
        for request_key in key_dics:
            self.setRequestToAttrIfExists(request_key, key_dics[request_key])

    def send(self):
        """
            Send this Message to Ras Message Dispatcher
        """
        Msg.send(self)
        return user_main.getRasMsgDispatcher().dispatch(self)

class UserMsg(Msg):
    def __init__(self):
        """
        """
        Msg.__init__(self)

    def send(self):
        """
            send this message to User Message Dispatcher
        """
        Msg.send(self)
        return ras_main.getUserMsgDispatcher().dispatch(self)
        
