from core.ras.ras import GeneralUpdateRas
from core.ras import ras_main
from core.ibs_exceptions import *
from core.lib.snmp import Snmp
from core.lib.rsh import RSHClient

import os, time

def init():
    ras_main.getFactory().register(MikrotikRas, "Mikrotik")

class MikrotikRas(GeneralUpdateRas):
    type_attrs={"mikrotik_update_accounting_interval":1, 
                "mikrotik_snmp_community":"public", 
                "mikrotik_snmp_timeout":10, 
                "mikrotik_snmp_retries":3, 
                "mikrotik_snmp_enabled":1, 
                "mikrotik_ssh_wrapper":"%smikrotik/ssh_wrapper"%defs.IBS_ADDONS, 
                "mikrotik_ssh_username":"admin", 
                "mikrotik_ssh_password":"admin"
                }

    def init(self):

        self.inouts = {}# dic in format port=>{"in_bytes":,"out_bytes":,"in_rate":,"out_rate":}
        self.onlines = {}# dic of port=>{"username":,"in_bytes":,"out_bytes": "last_update":}

        self.handle_reload=True

        self.snmp_client=self.__createSnmpClient()
        self.rsh_client=self.__createRSHClient()

    def __createSnmpClient(self):
        return Snmp(self.getRasIP(), 
                    self.getAttribute("mikrotik_snmp_community"), 
                    int(self.getAttribute("mikrotik_snmp_timeout")), 
                    self.getAttribute("mikrotik_snmp_retries"), 
                    161, 
                    "1")

    def __createRSHClient(self):
        return RSHClient(self.getRasIP(), 
                         3, 
                         self.getAttribute("mikrotik_ssh_wrapper"))


####################################
    def killUser(self, user_msg):
        """
            kill user, this will call "kill_port_command" attribute, 
            with user ppp interface numbers as argument
        """
        try:
            user_ip=self.__getUserIP(user_msg)
            nas_port_type=self.__getNasPortType(user_msg)
            if nas_port_type == "Wireless-802.11":
                command="/ip hotspot active remove [/ip hotspot active find user=%s address=%s]"% \
                                            (user_msg["user_obj"].getUserAttrs()["normal_username"], user_ip)
            else:
                command="/ppp active remove [/ppp active find name=%s address=%s]"% \
                                            (user_msg["user_obj"].getUserAttrs()["normal_username"], user_ip)

            self.rsh_client.runCommand([self.getAttribute("mikrotik_ssh_username"), 
                                        self.getAttribute("mikrotik_ssh_password"), 
                                        command
                                        ])
        except:
            logException(LOG_ERROR)

    def __getUserIP(self, user_msg):
        return user_msg["user_obj"].getTypeObj().getClientAddr(user_msg["instance"])

    def __getNasPortType(self, user_msg):
        return user_msg["instance_info"]["attrs"]["nas_port_type"]

####################################    
    def __getInOuts(self):
        in_bytes_oid=".1.3.6.1.2.1.2.2.1.16" #IF-MIB::ifInOctets
        out_bytes_oid=".1.3.6.1.2.1.2.2.1.10" #IF-MIB::ifOutOctets
        snmp_in_bytes=self.snmp_client.walk(in_bytes_oid)
        snmp_out_bytes=self.snmp_client.walk(out_bytes_oid)

        if snmp_in_bytes.has_key(in_bytes_oid):
            del(snmp_in_bytes[in_bytes_oid])

        if snmp_out_bytes.has_key(out_bytes_oid):
            del(snmp_out_bytes[out_bytes_oid])

        inout_bytes={}
        for oid in snmp_in_bytes:
            port=oid[oid.rfind(".")+1:]
            try:
                inout_bytes[port]={"in_bytes":snmp_in_bytes[oid], "out_bytes":snmp_out_bytes["%s.%s"%(out_bytes_oid, port)]}
            except KeyError, key:
                self.toLog("Unable to update port inout bytes, key %s missing"%key)
        return inout_bytes

    def updateInOutBytes(self):
        if int(self.getAttribute("mikrotik_snmp_enabled")):
            try:
                inouts=self.__getInOuts()
            except:
                logException(LOG_ERROR, "Mikrotik Ras")
                return
            
            inouts=self._calcRates(self.inouts, inouts)
            self.inouts=inouts
####################################
    def isOnline(self, user_msg):
        return self.onlines.has_key(user_msg["port"]) and self.onlines[user_msg["port"]]["last_update"] >= \
                                    time.time() - int(self.getAttribute("mikrotik_update_accounting_interval"))*60
####################################
    def getInOutBytes(self, user_msg):
        try:
            port=user_msg["port"]
            if port in self.inouts:
                return (self.inouts[port]["in_bytes"], 
                        self.inouts[port]["out_bytes"], 
                        self.inouts[port]["in_rate"], 
                        self.inouts[port]["out_rate"])

            elif port in self.onlines:

                return (self.onlines[port]["in_bytes"], 
                        self.onlines[port]["out_bytes"], 
                        self.onlines[port]["in_rate"], 
                        self.onlines[port]["out_rate"])
            else:
                return (0, 0, 0, 0)
        except:
            logException(LOG_ERROR)
            return (-1, -1, -1, -1)
####################################
    def __addUniqueIdToRasMsg(self, ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=str(ras_msg.getRequestPacket()["NAS-Port"][0])

    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username", 
                            "NAS-Port-Type":"nas_port_type"})

        ras_msg.setInAttrsIfExists({"User-Password":"pap_password", 
                                    "CHAP-Password":"chap_password", 
                                    "MS-CHAP-Response":"ms_chap_response", 
                                    "MS-CHAP2-Response":"ms_chap2_response", 
                                    "Host-IP":"remote_ip"
                                    })
        if ras_msg["nas_port_type"]=="Ethernet": #PPPoE
            ras_msg.setInAttrsIfExists({"Calling-Station-Id":"mac"})

        elif ras_msg["nas_port_type"]=="Virtual": #PPTP
            ras_msg.setInAttrsIfExists({"Calling-Station-Id":"station_ip"})

        elif ras_msg["nas_port_type"]=="Wireless-802.11": #HotSpot
            ras_msg["ip_assignment"]=False      
            ras_msg.setInAttrsIfExists({"Calling-Station-Id":"mac"})

        if self.onlines.has_key(ras_msg["port"]):
                self.onlines[ras_msg["port"]]["in_bytes"], self.onlines[ras_msg["port"]]["out_bytes"]=0, 0

        ras_msg.setAction("INTERNET_AUTHENTICATE")

####################################
    def handleRadAcctPacket(self, ras_msg):
        status_type=ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)
        if status_type=="Start":
            ras_msg.setInAttrs({"User-Name":"username", "Framed-IP-Address":"remote_ip", "Acct-Session-Id":"session_id"})
            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["remote_ip", "start_accounting"]

            self.onlines[ras_msg["port"]] = {"username":ras_msg["username"], "in_bytes":0, "out_bytes":0 , "in_rate":0, "out_rate":0, "last_update":time.time()}
            if self.inouts.has_key(ras_msg["port"]):
                del(self.inouts[ras_msg["port"]])

            ras_msg.setAction("INTERNET_UPDATE")
        elif status_type=="Stop":
            ras_msg.setInAttrs({"User-Name":"username", 
                                "Framed-IP-Address":"remote_ip", 
                                "Acct-Session-Id":"session_id", 
                                "Acct-Output-Octets":"in_bytes", 
                                "Acct-Input-Octets":"out_bytes", 
                                "Acct-Terminate-Cause":"terminate_cause"})
            try:
                self.inouts[ras_msg["port"]]["in_bytes"], self.inouts[ras_msg["port"]]["out_bytes"]=ras_msg["in_bytes"], ras_msg["out_bytes"]
            except KeyError:
                logException(LOG_DEBUG)
            ras_msg.setAction("INTERNET_STOP")
            
        elif status_type == "Alive":
            if ras_msg["port"] in self.onlines:

                now = long(time.time())
                
                in_bytes = ras_msg.getRequestAttr("Acct-Output-Octets")[0] 
                out_bytes = ras_msg.getRequestAttr("Acct-Input-Octets")[0] 

                if ras_msg.getRequestPacket().has_key("Acct-Output-Gigawords"):
                    in_bytes += 2**32 * ras_msg.getRequestAttr("Acct-Output-Gigawords")[0]
                    out_bytes += 2**32 * ras_msg.getRequestAttr("Acct-Input-Gigawords")[0]

                duration = now - self.onlines[ras_msg["port"]]["last_update"]
                self.onlines[ras_msg["port"]]["last_update"] = now

                self.onlines[ras_msg["port"]]["in_rate"] = (in_bytes - self.onlines[ras_msg["port"]]["in_bytes"])/duration
                self.onlines[ras_msg["port"]]["out_rate"] = (out_bytes - self.onlines[ras_msg["port"]]["out_bytes"])/duration

                self.onlines[ras_msg["port"]]["in_bytes"] = in_bytes
                self.onlines[ras_msg["port"]]["out_bytes"] = out_bytes

            else:
                self.toLog("Update accounting called for %s,%s while he's on my online list"%(ras_msg.getRequestAttr("User-Name")[0], ras_msg["port"]))
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type, LOG_ERROR)

####################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.snmp_client=self.__createSnmpClient()
        self.rsh_client=self.__createRSHClient()
        
