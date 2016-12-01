from core.ras.ras import GeneralUpdateRas
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.lib.rsh import RSHClient

import os, time, re

def init():
    ras_main.getFactory().register(CiscoVPDNRas, "CiscoVPDN")

class CiscoVPDNRas(GeneralUpdateRas):
    type_attrs={"cisco_rsh_command":"%scisco/rsh_wrapper"%defs.IBS_ADDONS, 
                "cisco_rsh_max_concurrent_connections":3, 
                "cisco_update_accounting_interval":1, 
                "cisco_reonline_users":0, 
                "general_update_interval":120}

    show_callers_pattern=re.compile("User: (.+?), line (.+?), .+? remote (\d+\.\d+\.\d+\.\d+)", re.M|re.S)
    find_mac_pattern=re.compile("^client-mac-address=(..)(..)\.(..)(..)\.(..)(..)$")

    DEBUG=True

    def init(self):
        self.internet_onlines={}#port => {"username":,"in_bytes":,"out_byte":,"last_update":,"start_in_bytes":,"start_out_bytes":}

        self.handle_reload=True
        self.rsh_client=self.__createRSHClient()

    def __createRSHClient(self):
        return RSHClient(self.getRasIP(), 
                         int(self.getAttribute("cisco_rsh_max_concurrent_connections")), 
                         self.getAttribute("cisco_rsh_command"))
                         

################################################## find user interface
    def __getUsernameAndRemoteIPFromUserMsg(self, user_msg):
        """
            return (username, remote_ip) from logged on user
            remote_ip maybe empty string in case we don't have remote ip of user
        """
        instance_info = user_msg["user_obj"].getInstanceInfo(user_msg["instance"])
        try:
            remote_ip=instance_info["attrs"]["remote_ip"]
        except KeyError:
            remote_ip = ""
        
        return (instance_info["attrs"]["username"], remote_ip)

    def __findUserInterface(self, username, remote_ip):
        """
            return virtual access interface name of username with remote_ip
            if remote_ip is empty return the first instance that is found
        """
        output=self.rsh_client.getOutput("show caller user %s"%username)
        match_list=self.show_callers_pattern.findall(output)

        if self.DEBUG:
            self.toLog("findUserInterface Query for (%s,%s): %s"%(username, remote_ip, match_list))

        if remote_ip:
            for match in match_list:
                #[('root', 'Vi2', '192.168.2.100'), ('root', 'Vi3', '192.168.2.10')]
                if match[0] == username and match[2] == remote_ip:
                    return match[1] 

            raise GeneralException("Interface name not available for %s %s"%(username, remote_ip))

        else:
            try:
                return match_list[0][1]
            except IndexError:
                raise GeneralException("Interface name not available for %s %s"%(username, remote_ip))
        
################################################## kill user

    def killUser(self, user_msg):
        """
            kill user based on his username
        """
        try:
            username, remote_ip = self.__getUsernameAndRemoteIPFromUserMsg(user_msg)
            return self.__killUser(username, remote_ip)
        except:
            logException(LOG_ERROR)

    def __killUser(self, username, remote_ip):
        try:
            interface = self.__findUserInterface(username, remote_ip)
            self.__killUserOnPort(interface)
        except:
            logException(LOG_ERROR)

    def __killUserOnPort(self, port):
        return self.__killByRSH(port)

    def __killByRSH(self, port):
        self.rsh_client.runCommand("clear interface %s"%port)
        
####################################    
    def generalUpdate(self):
        """
            remove stale onlines here
        """
        for session_id in self.internet_onlines.keys():
            if self.internet_onlines[session_id]["last_update"] < time.time() - int(self.getAttribute("cisco_update_accounting_interval"))* 60 * 10:
                del(self.internet_onlines[session_id])
                
####################################
    def isOnline(self, user_msg):
        session_id=user_msg["acct_session_id"]
        return self.internet_onlines.has_key(session_id) and \
               self.internet_onlines[session_id]["last_update"]>=time.time()-int(self.getAttribute("cisco_update_accounting_interval"))*60

###################################
    def getInOutBytes(self, user_msg):
        try:
            session_id = user_msg["acct_session_id"]
            online_dic = self.internet_onlines[session_id]
            return (online_dic["in_bytes"] - online_dic["start_in_bytes"], 
                    online_dic["out_bytes"] - online_dic["start_out_bytes"], 
                    online_dic["in_rate"], 
                    online_dic["out_rate"])
        except:
            logException(LOG_ERROR)
            return (-1, -1, -1, -1)
        
####################################
    def __addUniqueIDToRasMsg(self, ras_msg):
        ras_msg["unique_id"]="acct_session_id"
        ras_msg.setInAttrs({"Acct-Session-Id":"acct_session_id"})

####################################
    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password", 
                                    "CHAP-Password":"chap_password", 
                                    "MS-CHAP-Response":"ms_chap_response", 
                                    "MS-CHAP2-Response":"ms_chap2_response", 
                                    "Calling-Station-Id":"caller_id", 
                                    "Cisco-NAS-Port":"port", 
                                    "Connect-Info":"connect_info"
                                    })

        ras_msg.getReplyPacket()["Service-Type"]="Framed-User"
        ras_msg.getReplyPacket()["Framed-Protocol"]="PPP"

        ras_msg.setAction("INTERNET_AUTHENTICATE")

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

        ras_msg.setInAttrs({"User-Name":"username", "Framed-IP-Address":"remote_ip"})
        ras_msg["start_accounting"]=True
        ras_msg["update_attrs"]=["start_accounting", "remote_ip"]
        
        mac=self.__getMacAddressFromPacket(ras_msg.getRequestPacket())
        if mac:
            ras_msg["mac"]=mac
            ras_msg["update_attrs"].append("mac")

        self.__addInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["acct_session_id"])

        ras_msg.setAction("INTERNET_UPDATE")

    def __getMacAddressFromPacket(self, pkt):
        if pkt.has_key("Cisco-AVPair"):
            for item in pkt["Cisco-AVPair"]:
                match=self.find_mac_pattern.match(item)
                if match:
                    return ":".join(match.groups())
        
        return None
        

    def __internetAcctStop(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"Framed-IP-Address":"remote_ip", 
                                    "Acct-Terminate-Cause":"terminate_cause"})

        self.__updateInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["acct_session_id"])

        ras_msg.setAction("INTERNET_STOP")

    def __internetAcctUpdate(self, ras_msg):
        req_pkt = ras_msg.getRequestPacket()

        if not req_pkt.has_key("User-Name"):
            return
        
        self.__addUniqueIDToRasMsg(ras_msg)

        if not self.isUserOnline(ras_msg) and int(self.getAttribute("cisco_reonline_users")):
            self.tryToReOnline(ras_msg)
        else:
            self.__updateInInternetOnlines(req_pkt, ras_msg["acct_session_id"])
############################################
    def populateReOnlineRasMsg(self, ras_msg):
        GeneralUpdateRas.populateReOnlineRasMsg(self, ras_msg)

        mac=self.__getMacAddressFromPacket(ras_msg.getRequestPacket())
        if mac:
            ras_msg["mac"]=mac
    
    def tryToReOnlineResult(self, ras_msg, auth_success):
        if auth_success: 
            self.__addInInternetOnlines(ras_msg.getRequestPacket(), ras_msg["acct_session_id"])
        else:
            #auth failed
            self.__killUser(ras_msg["username"], ras_msg["remote_ip"])
                
############################################
    def __addInInternetOnlines(self, pkt, session_id):

        self.internet_onlines[session_id] = {}
        self.internet_onlines[session_id]["username"] = pkt["User-Name"][0]
        self.internet_onlines[session_id]["last_update"] = time.time()

        if pkt.has_key("Acct-Output-Octets"):
            start_in_bytes = pkt["Acct-Output-Octets"][0]
            start_out_bytes = pkt["Acct-Input-Octets"][0]
        else:
            start_in_bytes = 0
            start_out_bytes = 0

        self.internet_onlines[session_id]["in_bytes"] = start_in_bytes
        self.internet_onlines[session_id]["out_bytes"] = start_out_bytes

        self.internet_onlines[session_id]["start_in_bytes"] = start_in_bytes
        self.internet_onlines[session_id]["start_out_bytes"] = start_out_bytes

        self.internet_onlines[session_id]["in_rate"]=0
        self.internet_onlines[session_id]["out_rate"]=0



    def __updateInInternetOnlines(self, update_pkt, session_id):
        """
            update user in internal online list. Update in/out bytes, and last_update time
        """

        if session_id in self.internet_onlines and update_pkt["User-Name"][0]==self.internet_onlines[session_id]["username"]:
            now = long(time.time())

            if update_pkt.has_key("Acct-Output-Octets"):
                in_bytes=update_pkt["Acct-Output-Octets"][0]
                out_bytes=update_pkt["Acct-Input-Octets"][0]
                  
                duration= now - self.internet_onlines[session_id]["last_update"]

                self.internet_onlines[session_id]["in_rate"] = (in_bytes-self.internet_onlines[session_id]["in_bytes"])/duration
                self.internet_onlines[session_id]["out_rate"] = (out_bytes-self.internet_onlines[session_id]["out_bytes"])/duration

                self.internet_onlines[session_id]["in_bytes"] = in_bytes
                self.internet_onlines[session_id]["out_bytes"] = out_bytes

            self.internet_onlines[session_id]["last_update"] = now
        else:
            self.toLog("Received Alive/Logout packet for user %s, while he's not in my online list"%update_pkt["User-Name"][0])

####################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.rsh_client=self.__createRSHClient()
        
    
