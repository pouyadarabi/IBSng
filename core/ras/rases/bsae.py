from core.ras.ras import GeneralUpdateRas
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.lib.rsh import RSHClient

import os, time, re

def init():
    ras_main.getFactory().register(BSAERas, "BSAE")

class BSAERas(GeneralUpdateRas):
    type_attrs={"bsae_telnet_command":"%sbsae/telnet_wrapper"%defs.IBS_ADDONS, 
                "bsae_telnet_max_concurrent_connections":3, 
                "bsae_update_accounting_interval":1, 
                "bsae_telnet_username":"SuperManager", 
                "bsae_telnet_password":"bsae", 
                "general_update_interval":120}

    DEBUG=True

    def init(self):
        self.internet_onlines={}#port => {"username":,"in_bytes":,"out_byte":,"last_update":,"start_in_bytes":,"start_out_bytes":}

        self.ips={} #port => ip_address
        self.session_ids={} #port => acct_session_ids

        self.handle_reload=True
        self.rsh_client=self.__createRSHClient()

    def __createRSHClient(self):
        return RSHClient(self.getRasIP(), 
                         int(self.getAttribute("bsae_telnet_max_concurrent_connections")), 
                         self.getAttribute("bsae_telnet_command"))
                         

################################################## kill user

    def killUser(self, user_msg):
        """
            kill user based on his username
        """
        try:
            user_obj = user_msg["user_obj"]
            username = user_obj.getInstanceInfo(user_msg["instance"])["auth_ras_msg"]["username"]
            return self.__killUserByUsername(username)
        except:
            logException(LOG_ERROR)

    def __killUserByUsername(self, username):
        try:
            self.rsh_client.runCommand([self.getAttribute("bsae_telnet_username"), 
                                        self.getAttribute("bsae_telnet_password"), 
                                        "downuser username %s"%username])
        except:
            logException(LOG_ERROR)

####################################    
    def generalUpdate(self):
        """
            remove stale onlines here
        """
        for port in self.internet_onlines.keys():
            if self.internet_onlines[port]["last_update"] < time.time() - int(self.getAttribute("bsae_update_accounting_interval"))* 60 * 10:
                del(self.internet_onlines[port])
                
####################################
    def isOnline(self, user_msg):
        port=user_msg["port"]
        return self.internet_onlines.has_key(port) and \
               self.internet_onlines[port]["last_update"]>=time.time()-int(self.getAttribute("bsae_update_accounting_interval"))*60

###################################
    def getInOutBytes(self, user_msg):
        try:
            port = user_msg["port"]
            online_dic = self.internet_onlines[port]
            return (online_dic["in_bytes"] - online_dic["start_in_bytes"], 
                    online_dic["out_bytes"] - online_dic["start_out_bytes"], 
                    online_dic["in_rate"], 
                    online_dic["out_rate"])
        except:
            logException(LOG_ERROR)
            return (-1, -1, -1, -1)
        
####################################
    def __addUniqueIDToRasMsg(self, ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=ras_msg.getRequestPacket()["User-Name"][0]
        
####################################
    def _postAuth(self, ras_msg, auth_success):
        GeneralUpdateRas._postAuth(self, ras_msg, auth_success)

        if auth_success:
            try:
                remote_ip = ras_msg.getReplyPacket()["Framed-IP-Address"][0]
                self.ips[ras_msg["port"]] = remote_ip
            except KeyError:
                pass


    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password", 
                                    "CHAP-Password":"chap_password", 
                                    "MS-CHAP-Response":"ms_chap_response", 
                                    "MS-CHAP2-Response":"ms_chap2_response", 
                                    })

        ras_msg.getReplyPacket()["Service-Type"]="Framed-User"
        ras_msg.getReplyPacket()["Framed-Protocol"]="PPP"

        ras_msg.getReplyPacket()["Acct-Interim-Interval"] = self.getAttribute("bsae_update_accounting_interval")*60

        ras_msg["mac"] = self.__getMac(ras_msg.getRequestPacket())
        ras_msg["multi_login"] = False
        
        ras_msg.setAction("INTERNET_AUTHENTICATE")

    def __getMac(self, request_pkt):
        caller_id = request_pkt["Calling-Station-Id"][0]
        return ":".join((caller_id[0:2], caller_id[2:4], caller_id[4:6], caller_id[6:8], caller_id[8:10], caller_id[10:12]))

####################################
    def handleRadAcctPacket(self, ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
        
        if status_type=="Start":
            self.__internetAcctStart(ras_msg)

        elif status_type=="Stop":
            self.__internetAcctStop(ras_msg)

        elif status_type=="Alive":
            self.__internetAcctUpdate(ras_msg)
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type, LOG_ERROR)

###############################################
    def __internetAcctStart(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg["start_accounting"]=True
        ras_msg["update_attrs"]=["start_accounting"]
        
        try:
            remote_ip = self.ips[ras_msg["port"]]
            ras_msg["remote_ip"] = remote_ip
            ras_msg["update_attrs"].append("remote_ip")
        except KeyError:
            pass
        
        self.__addInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["port"])

        ras_msg.setAction("INTERNET_UPDATE")

    def __internetAcctStop(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"Framed-IP-Address":"remote_ip", 
                                    "Acct-Terminate-Cause":"terminate_cause"})

        self.__updateInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["port"])

        ras_msg.setAction("INTERNET_STOP")

    def __internetAcctUpdate(self, ras_msg):
        req_pkt = ras_msg.getRequestPacket()

        if not req_pkt.has_key("User-Name"):
            return
        
        self.__addUniqueIDToRasMsg(ras_msg)

        self.__updateInInternetOnlines(req_pkt, ras_msg["port"])
############################################
    def populateReOnlineRasMsg(self, ras_msg):
        GeneralUpdateRas.populateReOnlineRasMsg(self, ras_msg)

        mac=self.__getMacAddressFromPacket(ras_msg.getRequestPacket())
        if mac:
            ras_msg["mac"]=mac
    
    def tryToReOnlineResult(self, ras_msg, auth_success):
        if auth_success: 
            self.__addInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["session_id"])
        else:
            #auth failed
            self.__killUser(ras_msg["username"], ras_msg["remote_ip"])
                
############################################
    def __addInInternetOnlines(self, pkt, port):

        self.internet_onlines[port] = {}
        self.internet_onlines[port]["username"] = pkt["User-Name"][0]
        self.internet_onlines[port]["last_update"] = time.time()

        self.internet_onlines[port]["in_bytes"] = 0
        self.internet_onlines[port]["out_bytes"] = 0

        self.internet_onlines[port]["in_rate"]=0
        self.internet_onlines[port]["out_rate"]=0

        if pkt.has_key("Acct-Output-Octets"):
            start_in_bytes = pkt["Acct-Output-Octets"][0]
            start_out_bytes = pkt["Acct-Input-Octets"][0]
        else:
            start_in_bytes = 0
            start_out_bytes = 0
        
        self.internet_onlines[port]["start_in_bytes"] = start_in_bytes
        self.internet_onlines[port]["start_out_bytes"] = start_out_bytes


    def __updateInInternetOnlines(self, update_pkt, port):
        """
            update user in internal online list. Update in/out bytes, and last_update time
        """

        if port in self.internet_onlines and update_pkt["User-Name"][0]==self.internet_onlines[port]["username"]:
            now = time.time()

            if update_pkt.has_key("Acct-Output-Octets"):
                
                out_bytes = update_pkt["Acct-Input-Octets"][0] + 2**32 * update_pkt["Acct-Input-Gigawords"][0]
                in_bytes = update_pkt["Acct-Output-Octets"][0] + 2**32 * update_pkt["Acct-Output-Gigawords"][0]
                duration = now - self.internet_onlines[port]["last_update"]

                self.internet_onlines[port]["in_rate"] = (in_bytes-self.internet_onlines[port]["in_bytes"])/duration
                self.internet_onlines[port]["out_rate"] = (out_bytes-self.internet_onlines[port]["out_bytes"])/duration

                self.internet_onlines[port]["in_bytes"] = in_bytes
                self.internet_onlines[port]["out_bytes"] = out_bytes

            self.internet_onlines[port]["last_update"] = now
        else:
            self.toLog("Received Alive/Logout packet for user %s, while he's not in my online list"%update_pkt["User-Name"][0])

####################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.rsh_client=self.__createRSHClient()
        
    
