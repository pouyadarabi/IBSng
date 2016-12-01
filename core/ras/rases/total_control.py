from core.ras.ras import GeneralUpdateRas
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.lib.snmp import Snmp

import time

def init():
    ras_main.getFactory().register(TotalControlRas,"Total Control")

class TotalControlRas(GeneralUpdateRas):
    type_attrs={"tc_snmp_community":"public",
                "tc_snmp_timeout":10,
                "tc_snmp_retries":3,
                "tc_inout_use_snmp":1,
                "tc_update_accounting_interval":1}

    DEBUG=True

    def init(self):

        self.onlines={}#port => {"username":,"in_bytes":,"out_byte":,"last_update":}
        self.inouts={}#port => {"in_bytes":,"out_bytes":,"in_rate":,"out_rate":}

        self.handle_reload=True
        self.snmp_client=self.__createSnmpClient()

    def __createSnmpClient(self):
        return Snmp(self.getRasIP(),
                    self.getAttribute("tc_snmp_community"),
                    self.getAttribute("tc_snmp_timeout"),
                    self.getAttribute("tc_snmp_retries"),
                    161,
                    1)

################################################## kill user
    def killUser(self,user_msg):
        """
            kill user based on his interface_index
        """
        try:
            self.snmp_client.set(".1.3.6.1.2.1.2.2.1.7.%s"%user_msg["interface_index"],"i",2) #down
            self.snmp_client.set(".1.3.6.1.2.1.2.2.1.7.%s"%user_msg["interface_index"],"i",1) #up
        except:
            logException(LOG_ERROR)

####################################    
    def isOnline(self,user_msg):
        iface_idx = user_msg["interface_index"]
        return self.onlines.has_key(iface_idx) and \
               self.onlines[iface_idx]["last_update"]>=time.time()-int(self.getAttribute("tc_update_accounting_interval"))*60

###################################

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
                inout_bytes[port]={"in_bytes":snmp_in_bytes[oid],"out_bytes":snmp_out_bytes["%s.%s"%(out_bytes_oid,port)]}
            except KeyError,key:
                self.toLog("Unable to update port inout bytes, key %s missing"%key)
        return inout_bytes

    def updateInOutBytes(self):
        if not int(self.getAttribute("tc_inout_use_snmp")):
            return
        
        try:
            inouts=self.__getInOuts()
        except:
            logException(LOG_ERROR,"Total Control Ras")
            return
            
        inouts=self._calcRates(self.inouts, inouts)
        self.inouts=inouts

    def getInOutBytes(self, user_msg):
        try:
            iface_idx=user_msg["interface_index"]
            if iface_idx in self.inouts and "start_out_bytes" in self.onlines[iface_idx]:
                return (self.inouts[iface_idx]["in_bytes"] - self.onlines[iface_idx]["start_in_bytes"],
                        self.inouts[iface_idx]["out_bytes"] - self.onlines[iface_idx]["start_out_bytes"],
                        self.inouts[iface_idx]["in_rate"],
                        self.inouts[iface_idx]["out_rate"])
            elif iface_idx in self.onlines:
                return (self.onlines[iface_idx]["in_bytes"],self.onlines[iface_idx]["out_bytes"],self.onlines[iface_idx]["in_rate"],self.onlines[iface_idx]["out_rate"])
            else:
                return (0,0,0,0)
        except:
            logException(LOG_ERROR)
            return (-1,-1,-1,-1)

####################################
    def __addUniqueIDToRasMsg(self,ras_msg):
        ras_msg["unique_id"]="interface_index"
        ras_msg["interface_index"]=str(ras_msg.getRequestPacket()["USR-Interface-Index"][0])

####################################
    def handleRadAuthPacket(self,ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password",
                                    "CHAP-Password":"chap_password",
                                    "MS-CHAP-Response":"ms_chap_response",
                                    "MS-CHAP2-Response":"ms_chap2_response",
                                    "Calling-Station-Id":"caller_id",
                                    "Called-Station-Id":"called_id",
                                    "NAS-Port":"port"
                                    })

        ras_msg.setAction("INTERNET_AUTHENTICATE")

####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
        
        if status_type=="Start":
            self.__internetAcctStart(ras_msg)

        elif status_type=="Stop":
            self.__internetAcctStop(ras_msg)

        elif status_type=="Alive":
            self.__internetAcctUpdate(ras_msg)

        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)

###############################################
    def __internetAcctStart(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username","Framed-IP-Address":"remote_ip"})
        ras_msg["start_accounting"]=True
        ras_msg["update_attrs"]=["start_accounting","remote_ip"]
        
        self.__addInInternetOnlines(ras_msg)

        ras_msg.setAction("INTERNET_UPDATE")

    def __internetAcctStop(self, ras_msg):
        self.__addUniqueIDToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"username"})
        self.__updateInInternetOnlines(ras_msg)

        ras_msg.setAction("INTERNET_STOP")

    def __internetAcctUpdate(self, ras_msg):
        if ras_msg.getRequestPacket().has_key("USR-Interface-Index"):
           self.__addUniqueIDToRasMsg(ras_msg)
           self.__updateInInternetOnlines(ras_msg)

############################################
    def __addInInternetOnlines(self, ras_msg):
        iface_idx = ras_msg["interface_index"]
        self.onlines[iface_idx]={}
        self.onlines[iface_idx]["username"]=ras_msg["username"]
        self.onlines[iface_idx]["last_update"]=time.time()
        self.onlines[iface_idx]["in_bytes"]=0
        self.onlines[iface_idx]["out_bytes"]=0
        self.onlines[iface_idx]["in_rate"]=0
        self.onlines[iface_idx]["out_rate"]=0

        try:
            self.onlines[iface_idx]["start_in_bytes"] = self.inouts[iface_idx]["in_bytes"]
            self.onlines[iface_idx]["start_out_bytes"] = self.inouts[iface_idx]["out_bytes"]
        except KeyError:
            self.toLog("In/Out Byte is not available for interface index %s"%iface_idx)
            

    def __updateInInternetOnlines(self, ras_msg):
        """
            update user in internal online list. Update in/out bytes, and last_update time
        """
        iface_idx = ras_msg["interface_index"]
        update_pkt = ras_msg.getRequestPacket()

        if not update_pkt.has_key("User-Name"):
            return

        if iface_idx in self.onlines and update_pkt["User-Name"][0]==self.onlines[iface_idx]["username"]:
            if update_pkt.has_key("Acct-Output-Octets"):
                out_bytes=update_pkt["Acct-Output-Octets"][0]
                in_bytes=update_pkt["Acct-Input-Octets"][0]
                duration=time.time() - self.onlines[iface_idx]["last_update"]

                self.onlines[iface_idx]["in_rate"]=(in_bytes-self.onlines[iface_idx]["in_bytes"])/duration
                self.onlines[iface_idx]["out_rate"]=(out_bytes-self.onlines[iface_idx]["out_bytes"])/duration

                self.onlines[iface_idx]["in_bytes"]=in_bytes
                self.onlines[iface_idx]["out_bytes"]=out_bytes

            self.onlines[iface_idx]["last_update"]=time.time()
        else:
            self.toLog("Received Alive/Logout packet for user %s, while he's not in my online list"%update_pkt["User-Name"][0])

####################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.inouts = {}
        self.snmp_client = self.__createSnmpClient()
