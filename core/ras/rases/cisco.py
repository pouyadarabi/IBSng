"""
    add rsh wrapper for non-blocking pipe
    snmp kill
"""
from core.script_launcher import launcher_main
from core.ras.ras import GeneralUpdateRas
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.lib.snmp import Snmp
from core.user import user_main
import time,re

def init():
    ras_main.getFactory().register(CiscoRas,"Cisco")

class CiscoRas(GeneralUpdateRas, VoIPRas):
    type_attrs={"cisco_rsh_command":"%scisco/rsh_wrapper -lroot"%defs.IBS_ADDONS,
                "cisco_update_accounting_interval":1,
                "cisco_snmp_community":"public",
                "cisco_update_inout_with_snmp":1,
                "cisco_snmp_version":"2c",
                "cisco_snmp_timeout":10,
                "cisco_snmp_retries":3,
                "cisco_kill_use_snmp":1,
                "cisco_voip_username_length":8,
                "cisco_credit_float_precision":0} #should we convert credit_amount float precision

    async_port_match=re.compile("(Async[0-9/]+)")
    DEBUG=False

    def init(self):
        self.port_inout_bytes={} #port => {in_bytes:,out_bytes:,in_rate:,out_rate:)
        self.internet_onlines={}#port => {"username":,"in_bytes":,"out_byte":,"last_update":,"start_in_bytes":,"start_out_bytes":}

        self.voip_onlines={}#h323 => {"username":,"last_update":}
	#h323 ids that authorization has been done but no voip leg accounting
	self.voip_auth_h323ids=[] #[h323_id, h323_id] 

        self.port_no_to_desc_mapping={} #port_no:port_desc
        self.port_desc_to_no_mapping={} #port_desc:port_no
        self.port_mapping_last_update=0
        self.last_inout_update = 0

        self.handle_reload=True
        self.snmp_client=self.__createSnmpClient()

    def __createSnmpClient(self):
        return Snmp(self.getRasIP(),
                    self.getAttribute("cisco_snmp_community"),
                    int(self.getAttribute("cisco_snmp_timeout")),
                    int(self.getAttribute("cisco_snmp_retries")),
                    161,
                    self.getAttribute("cisco_snmp_version"))


    def __parseAsyncPort(self,port):
        return self.async_port_match.match(port).groups()[0]

    ############################################ rsh handling, unused by default
    def __rcmd(self,command):
        """
            run "command" on cisco ras
        """
        return self.__doRcmd(self.getRasIP(),command)
    
    def __doRcmd(self,host,command):
        """
            run command "command" on "host" host
        """
        _in,out,err=launcher_main.getLauncher().popen3(self.getAttribute("cisco_rsh_command"),[host,command])
        err_str=self.__readAll(err)
        if not err_str:
            self.toLog("RCMD: %s"%err_str,LOG_DEBUG)
        out_str=self.__readAll(out)
        map(lambda fd:fd.close(),(_in,out,err))
        return out_str
            
    def __readAll(self,fd):
        ret=""
        tmp=fd.read()
        while tmp!="":
            ret+=tmp
            tmp=fd.read()
        return ret
################################################## kill user
    def killUser(self,user_msg):
        """
            kill user based on his port
        """
        try:
	    if user_msg.hasAttr("port"):
	        self.__killUserOnPort(user_msg["port"])
        except:
            logException(LOG_ERROR)

    def __killUserOnPort(self,port):
        if int(self.getAttribute("cisco_kill_use_snmp")):
            return self.__killBySnmp(port)
        else:
            return self.__killByRSH(port)

    def __killByRSH(self,port):
        if port.startswith("Async"):
            port=self.__parseAsyncPort(port)
            self.__rcmd("clear line %s"%port[5:])
        elif port.startswith("Serial"):
            self.__rcmd("clear interface %s"%port)
        else:
            self.toLog("rsh kill: Don't know how to kill port %s"%(self.getRasIP(),port),LOG_ERROR)
            return False
        return True
        
    def __killBySnmp(self,port):
        """
            kill a user on async port,  using snmp
            port should be in format AsyncX
        """
        try:
            self.__updatePortMapping()
            try:
                self.snmp_client.set(".1.3.6.1.4.1.9.2.1.76.0","i",self.port_desc_to_no_mapping[port])
            except KeyError:
                self.toLog("snmp kill: Don't know how to kill port %s"%port,LOG_ERROR)
                return False

        except SnmpException:
            logException(LOG_ERROR)
            return False        
            
        return True
####################################    
    def updateInOutBytes(self):
        if int(self.getAttribute("cisco_update_inout_with_snmp")):
            self.updateInOutBytesBySNMP()

####################################
    def isOnline(self,user_msg):
        if user_msg.hasAttr("port"): #internet
            key = "port"
            dic = self.internet_onlines

        elif user_msg.hasAttr("h323_conf_id"): #voip
            key = "h323_conf_id"
            dic = self.voip_onlines

        return dic.has_key(user_msg[key]) and \
               dic[user_msg[key]]["last_update"]>=time.time()-int(self.getAttribute("cisco_update_accounting_interval"))*60

###################################
    def getInOutBytes(self, user_msg):
        try:
            port=user_msg["port"]
            if port in self.internet_onlines:
                if port in self.port_inout_bytes and "start_in_bytes" in self.internet_onlines[port]:
                    return (self.port_inout_bytes[port]["in_bytes"]-self.internet_onlines[port]["start_in_bytes"],
                            self.port_inout_bytes[port]["out_bytes"]-self.internet_onlines[port]["start_out_bytes"],
                            self.port_inout_bytes[port]["in_rate"],
                            self.port_inout_bytes[port]["out_rate"])
                else:
                    return (self.internet_onlines[port]["in_bytes"],self.internet_onlines[port]["out_bytes"],0,0)
            else:
                return (0,0,0,0)
        except:
            logException(LOG_ERROR)
            return (-1,-1,-1,-1)
###################################
    def __isInternetPacket(self, pkt):
        """
            return True if pkt belongs to an internet session
        """
        return pkt.has_key("Framed-Protocol") and pkt["Framed-Protocol"][0] == "PPP"
        
################################### internet helper methods
    def __getPortFromRadiusPacket(self,pkt):
        if pkt.has_key("Cisco-NAS-Port"):
            port=pkt["Cisco-NAS-Port"][0]
            if port.startswith("Async"):
                port=self.__parseAsyncPort(port)
        else:
            port="%s%s"%(pkt["NAS-Port-Type"][0],pkt["NAS-Port"][0])
        return port

    def __addInternetUniqueIDToRasMsg(self,ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"] = self.__getPortFromRadiusPacket( ras_msg.getRequestPacket() )
                                                      

#################################### some voip helper methods
    def __addVoIPUsernamePasswordToRasMsg(self, ras_msg):
        """
            split username/password from radius packet username
        """
        username_len = int(self.getAttribute("cisco_voip_username_length"))
        username = ras_msg.getRequestPacket()["User-Name"][0]

        ras_msg["voip_username"] = username[:username_len]
        ras_msg["voip_password"] = username[username_len:]

    def __isVoIPPreAuth(self, request_pkt):
        """
        """
	if not request_pkt.has_key("Cisco-AVPair") or not request_pkt.has_key("Calling-Station-Id"):
	    return False
	    
	for avpair in request_pkt["Cisco-AVPair"]:
	    if "ani_authorization" in avpair:
		return True
	
	return False

    def __getH323ConfID(self,ras_msg):
        return self.getH323AttrValue("H323-conf-id",ras_msg.getRequestPacket())

    def __addVoIPUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"] = "h323_conf_id"
        ras_msg["h323_conf_id"] = self.__getH323ConfID(ras_msg)

    def __getVoIPCallType(self, ras_msg):
        """
            return (call_type, call_origin) of ras_msg
        """
        pkt = ras_msg.getRequestPacket()
        call_type = self.getH323AttrValue("H323-call-type", pkt)
        call_origin = self.getH323AttrValue("H323-call-origin", pkt)
        return (call_type,call_origin)

####################################
    def handleRadAuthPacket(self,ras_msg):
        req_pkt = ras_msg.getRequestPacket()
        if self.__isInternetPacket(req_pkt):
            return self.internetHandleRadAuthPacket(ras_msg)
        else:
            return self.voipHandleRadAuthPacket(ras_msg)

    def internetHandleRadAuthPacket(self,ras_msg):
        self.__addInternetUniqueIDToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password",
                                    "CHAP-Password":"chap_password",
                                    "MS-CHAP-Response":"ms_chap_response",
                                    "MS-CHAP2-Response":"ms_chap2_response",
                                    "Calling-Station-Id":"caller_id",
                                    "Connect-Info":"connect_info"
                                    })

        ras_msg.getReplyPacket()["Service-Type"]="Framed-User"
        ras_msg.getReplyPacket()["Framed-Protocol"]="PPP"

        ras_msg.setAction("INTERNET_AUTHENTICATE")

    def voipHandleRadAuthPacket(self,ras_msg):
        self.__addVoIPUniqueIdToRasMsg(ras_msg)
        req = ras_msg.getRequestPacket()

        if req.has_key("Called-Station-Id"): #authorization
            self.__addVoIPUsernamePasswordToRasMsg(ras_msg)     
            
            ras_msg.setInAttrs({"Called-Station-Id":"called_number"})
            ras_msg["h323_authorization"] = True
            ras_msg["calc_remaining_time"] = True

            ras_msg.setAction("VOIP_AUTHORIZE")

        else:
            if self.__isVoIPPreAuth(req): #pre authentication
                ras_msg["h323_pre_authentication"] = True
                
            else: #authentication
                self.__addVoIPUsernamePasswordToRasMsg(ras_msg) 
                ras_msg["h323_authentication"] = True

            ras_msg.setAction("VOIP_AUTHENTICATE")

        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"caller_id"})

        ras_msg["multi_login"] = False
        ras_msg["single_session_h323"] = True
        

    def _postAuth(self,ras_msg, auth_success):
        GeneralUpdateRas._postAuth(self,ras_msg, auth_success)
	
	if ras_msg.hasAttr("h323_pre_authentication") and auth_success:
	    user_attrs = user_main.getUserPool().getUserByCallerID(ras_msg["caller_id"]).getUserAttrs()

	    username = user_attrs["voip_username"] + user_attrs["voip_password"]
	    ras_msg.getReplyPacket()["Cisco-AVPair"]="h323-ivr-in=%s"%username

	    if user_attrs.hasAttr("voip_preferred_language"):
		self.setH323PreferredLanguage(ras_msg.getReplyPacket(), user_attrs["voip_preferred_language"])

	elif ras_msg.hasAttr("h323_authorization") and auth_success:
	    self.__addToAuthH323IDs(ras_msg["h323_conf_id"])


####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
        is_internet = self.__isInternetPacket(ras_msg.getRequestPacket())
        
        if status_type=="Start":
            if is_internet:
                self.__internetAcctStart(ras_msg)
            else:
                self.__voipAcctStart(ras_msg)

        elif status_type=="Stop":
            if is_internet:
                self.__internetAcctStop(ras_msg)
            else:
                self.__voipAcctStop(ras_msg)

        elif status_type=="Alive":
            if is_internet:
                self.__internetAcctUpdate(ras_msg)
            else:
                self.__voipAcctUpdate(ras_msg)

        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)

###############################################
    def __internetAcctStart(self, ras_msg):
        self.__addInternetUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username","Acct-Session-Id":"session_id"})
        ras_msg["start_accounting"]=True
        ras_msg["update_attrs"]=["start_accounting"]
        ras_msg.setInAttrsIfExists({"Framed-IP-Address":"remote_ip"})
        if ras_msg.hasAttr("remote_ip"):
            ras_msg["update_attrs"].append("remote_ip")

        port = self.__getPortFromRadiusPacket(ras_msg.getRequestPacket())
        self.__addInInternetOnlines(ras_msg.getRequestPacket(),port)

        ras_msg.setAction("INTERNET_UPDATE")

    def __internetAcctStop(self, ras_msg):
        self.__addInternetUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username",
                            "Acct-Session-Id":"session_id",
                            "Acct-Output-Octets":"in_bytes",
                            "Acct-Input-Octets":"out_bytes"})
        ras_msg.setInAttrsIfExists({"Framed-IP-Address":"remote_ip", 
                                    "Acct-Terminate-Cause":"terminate_cause"})

        port = self.__getPortFromRadiusPacket(ras_msg.getRequestPacket())
        self.__updateInInternetOnlines(ras_msg.getRequestPacket(),port)

        ras_msg.setAction("INTERNET_STOP")

    def __internetAcctUpdate(self, ras_msg):
        port = self.__getPortFromRadiusPacket(ras_msg.getRequestPacket())
        self.__updateInInternetOnlines(ras_msg.getRequestPacket(),port)

############################################
    def __addInInternetOnlines(self,pkt,port):
        self.internet_onlines[port]={}
        self.internet_onlines[port]["username"]=pkt["User-Name"][0]
        self.internet_onlines[port]["last_update"]=time.time()
        self.internet_onlines[port]["in_bytes"]=0
        self.internet_onlines[port]["out_bytes"]=0
        try:
            self.internet_onlines[port]["start_in_bytes"]=self.port_inout_bytes[port]["in_bytes"]
            self.internet_onlines[port]["start_out_bytes"]=self.port_inout_bytes[port]["out_bytes"]
        except KeyError:
            self.toLog("In/Out Byte is not available for port %s"%port)
    
    def __updateInInternetOnlines(self,update_pkt,port):
        """
            update user in internal online list. Update in/out bytes, and last_update time
        """
        if not update_pkt.has_key("User-Name"):
            return

        if port in self.internet_onlines and update_pkt["User-Name"][0]==self.internet_onlines[port]["username"]:
            self.internet_onlines[port]["last_update"]=time.time()
            if update_pkt.has_key("Acct-Output-Octets"):
                self.internet_onlines[port]["in_bytes"]=update_pkt["Acct-Output-Octets"][0]
                self.internet_onlines[port]["out_bytes"]=update_pkt["Acct-Input-Octets"][0]
        else:
            self.toLog("Received Alive/Logout packet for user %s, while he's not in my online list"%update_pkt["User-Name"][0])

##############################################
    def __voipAcctStart(self, ras_msg):
        (call_type, call_origin) = self.__getVoIPCallType(ras_msg)
        if call_type == "VoIP" and call_origin == "originate":
            self.__addVoIPUniqueIdToRasMsg(ras_msg)
            self.__addVoIPUsernamePasswordToRasMsg(ras_msg)     

            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["start_accounting"]

            self.__addInVoIPOnlines(ras_msg)
	    #remove h323_conf_id from authorized but no accounting started list
	    self.__removeFromAuthH323IDs(ras_msg["h323_conf_id"])

            ras_msg.setAction("VOIP_UPDATE")
            
    def __voipAcctStop(self, ras_msg):
        (call_type, call_origin) = self.__getVoIPCallType(ras_msg)
        if call_type == "VoIP" and call_origin == "originate":
            self.__addVoIPUniqueIdToRasMsg(ras_msg)
            self.__addVoIPUsernamePasswordToRasMsg(ras_msg)     

            pkt = ras_msg.getRequestPacket()
            
            self.setH323TimeInAttrs(ras_msg,{"H323-disconnect-time":"disconnect_time"})
            self.setH323TimeInAttrs(ras_msg,{"H323-connect-time":"connect_time"})
            ras_msg["disconnect_cause"]=self.getH323AttrValue("H323-disconnect-cause",pkt)
            if pkt.has_key("H323-remote-address"):
                ras_msg["called_ip"]=self.getH323AttrValue("H323-remote-address",pkt)

            self.__deleteFromVoIPOnlines(ras_msg)

            ras_msg.setAction("VOIP_STOP")
	    
	elif call_type == "Telephony" and call_origin == "answer":
	    if ras_msg.getRequestPacket().has_key("H323-conf-id"):
    	  	self.__addVoIPUniqueIdToRasMsg(ras_msg)
                self.__addVoIPUsernamePasswordToRasMsg(ras_msg)     

		if self.__isInAuthH323IDs(ras_msg["h323_conf_id"]):

		    now=long(time.time())
		    ras_msg["connect_time"]=now
		    ras_msg["disconnect_time"]=now

		    ras_msg.setAction("VOIP_STOP")
        
        
    def __voipAcctUpdate(self, ras_msg):
        (call_type, call_origin) = self.__getVoIPCallType(ras_msg)
        if call_type == "VoIP" and call_origin == "originate":
            self.__addVoIPUniqueIdToRasMsg(ras_msg)
            self.__addVoIPUsernamePasswordToRasMsg(ras_msg)     
            self.__updateInVoIPOnlines(ras_msg)
        
###################################
    def __addInVoIPOnlines(self, ras_msg):
        self.voip_onlines[ras_msg["h323_conf_id"]]={"username":ras_msg["voip_username"],"last_update":time.time()}

    def __updateInVoIPOnlines(self, ras_msg):
        try:
            self.voip_onlines[ras_msg["h323_conf_id"]]["last_update"] = time.time()
        except KeyError:
            self.toLog("updateInVoIPOnlines: user %s wasn't online with conf_id %s"%(ras_msg["voip_username"],ras_msg["h323_conf_id"]))

    def __deleteFromVoIPOnlines(self, ras_msg):
        try:
            del(self.voip_onlines[ras_msg["h323_conf_id"]])
        except KeyError:
            self.toLog("deleteFromVoIPOnlines: user %s wasn't online with conf_id %s"%(ras_msg["voip_username"],ras_msg["h323_conf_id"]))

#################################### VoIP Auth H323 ID Mechanism
#######################This mechanism protect from authorization request with not
#######################VoIP Accounting Leg Start.
    def __addToAuthH323IDs(self, h323_conf_id):
        self.voip_auth_h323ids.append(h323_conf_id)
	
    def __removeFromAuthH323IDs(self, h323_conf_id):
	"""
	    Warning: Silently discard exception if value isn't in dic
	"""
	try:
	    self.voip_auth_h323ids.remove(h323_conf_id)
	except ValueError:
	    pass
    
    def __isInAuthH323IDs(self, h323_conf_id):
	return h323_conf_id in self.voip_auth_h323ids

########################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.snmp_client=self.__createSnmpClient()
        self.port_mapping_last_update=0
        
########################################
    def updateInOutBytesBySNMP(self):
        try:
            self.__updatePortMapping()
            port_inout_bytes=self.__createPortInOutBytesDic()
            port_inout_bytes=self._calcRates(self.port_inout_bytes, port_inout_bytes)
            self.port_inout_bytes = port_inout_bytes
        except SnmpException:
            if self.DEBUG:
                logException(LOG_DEBUG)

    def __createPortInOutBytesDic(self):
        in_bytes_oid=".1.3.6.1.2.1.2.2.1.16"
        out_bytes_oid=".1.3.6.1.2.1.2.2.1.10"
        snmp_in_bytes=self.snmp_client.walk(in_bytes_oid)
        snmp_out_bytes=self.snmp_client.walk(out_bytes_oid)

        if snmp_in_bytes.has_key(in_bytes_oid):
            del(snmp_in_bytes[in_bytes_oid])

        if snmp_out_bytes.has_key(out_bytes_oid):
            del(snmp_out_bytes[out_bytes_oid])

        inout_bytes={}
        for oid in snmp_in_bytes:
            port_no=oid[oid.rfind(".")+1:]
            try:
                inout_bytes[self.port_no_to_desc_mapping[port_no]]={"in_bytes":snmp_in_bytes[oid],"out_bytes":snmp_out_bytes["%s.%s"%(out_bytes_oid,port_no)]}
            except KeyError,key:
                if self.DEBUG:
                    self.toLog("Unable to update port inout bytes, key %s missing"%key)
        return inout_bytes

############################################
    def __updatePortMapping(self):
        if self.port_mapping_last_update>time.time()-60*60*5:#5 hours
            return
            
        snmp_mapping=self.snmp_client.walk(".1.3.6.1.2.1.2.2.1.2")
        if snmp_mapping:
            (self.port_no_to_desc_mapping,self.port_desc_to_no_mapping)=self.__createPortMappingDic(snmp_mapping)
            self.port_mapping_last_update=time.time()
    
    def __createPortMappingDic(self,snmp_dic):
        no_mapping={} #number to desc mapping
        desc_mapping={} #desc to number mapping

        for oid in snmp_dic:
            if_no = oid[ oid.rfind(".")+1: ]
            no_mapping[ if_no ] = snmp_dic[oid]
            desc_mapping[ snmp_dic[oid] ] = if_no

        return no_mapping, desc_mapping

#############################################
    def setSingleH323CreditTime(self,reply_pkt,credit_time):
        return VoIPRas.setSingleH323CreditTime(self,reply_pkt,credit_time, True)

    def setSingleH323CreditAmount(self,reply_pkt,credit_amount):
        return VoIPRas.setSingleH323CreditAmount(self,reply_pkt,credit_amount, int(self.getAttribute("cisco_credit_float_precision")))
    
