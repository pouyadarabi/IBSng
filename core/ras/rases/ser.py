from core.ras.ras import Ras
from core.ras import ras_main
from core.ibs_exceptions import *
from core.user import user_main
import re

from core.ras.voip_ras import VoIPRas


def init():
    ras_main.getFactory().register(SerRas,"Ser")

class SerRas(Ras, VoIPRas):
    type_attrs={}
    strip_called_number_pattern = re.compile("sip:([^@]+)@.+")
    
    

    def init(self):
	self.call_ids = [] #call ids that accounting has been started for

####################################
    def killUser(self,user_msg):
	pass

####################################
    def isOnline(self,user_msg):
	"""
	    We keep call id of calls that accounting has been started in self.call_ids list.
	    This Help to recover from timeout situation that ser doesn't send start and stop accounting 
	    after authorization request
	"""
	return user_msg["call_id"] in self.call_ids
	
###################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"] = "call_id"
	if ras_msg.getRequestPacket().has_key("Acct-Session-Id"):
	    ras_msg.setInAttrs({"Acct-Session-Id":"call_id"})
	    
	elif ras_msg.getRequestPacket().has_key("Cisco-AVPair"):
	    for avpair in ras_msg.getRequestPacket()["Cisco-AVPair"]:
		if avpair.startswith("call-id"):
		    ras_msg["call_id"] = avpair[8:]
	
	if not ras_msg.hasAttr("call_id"):
	    raise IBSException("No CallID in Packet %s"%ras_msg.getRequestPacket())
	
###################################
    def handleRadAuthPacket(self,ras_msg):
	
        if ras_msg.getRequestPacket()["Digest-Method"][0] == "INVITE": #Authorization
            return self.authInvite(ras_msg)
            
        else: #Register, Authentication Request
            return self.authRegister(ras_msg)


    def authRegister(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)

        ras_msg.setInAttrs({"Digest-User-Name":"voip_username",
			    "Digest-Response":"voip_digest_response",
			    "User-Name":"user_uri"})

        ras_msg.setAction("VOIP_AUTHENTICATE")

                            
    def authInvite(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)

        ras_msg.setInAttrs({"Digest-User-Name":"voip_username",
			    "Digest-Response":"voip_digest_response",
                            "Digest-URI":"called_number",
			    "User-Name":"user_uri"})

	ras_msg["called_number"] = self.strip_called_number_pattern.match(ras_msg["called_number"]).groups()[0]

        ras_msg.setAction("VOIP_AUTHORIZE")

####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
	sip_method = ras_msg.getRequestAttr("Sip-Method")[0]
	
        self.__addUniqueIdToRasMsg(ras_msg)

        if status_type=="Start" and sip_method == "Invite":
	    
	    self.call_ids.append(ras_msg["call_id"])

            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["start_accounting"]
            ras_msg.setAction("VOIP_UPDATE")
            
        elif status_type=="Stop":
	    try:
	        self.call_ids.remove(ras_msg["call_id"])
	    except ValueError:
		logException(LOG_DEBUG, "CallID:%s"%ras_msg["call_id"])
	    
            ras_msg.setAction("VOIP_STOP")

        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)
                