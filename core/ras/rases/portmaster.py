from core.ras.ras import UpdateUsersRas
from core.lib.snmp import Snmp
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
import os, time

def init():
    ras_main.getFactory().register(PortMasterRas,"PortMaster")

class PortMasterRas(UpdateUsersRas):
    type_attrs={"portmaster_snmp_community":"public",
                "portmaster_snmp_timeout":10,
                "portmaster_snmp_retries":3}

    def init(self):

        self.onlines = {} # port=>username
        self.inouts = {} # port => {"in_bytes":,"out_bytes":,"in_rate":,"out_rate":}
        self.snmp_client = self.__createSnmpClient()

    def __createSnmpClient(self):
        return Snmp(self.getRasIP(),
                    self.getAttribute("portmaster_snmp_community"),
                    int(self.getAttribute("portmaster_snmp_timeout")),
                    int(self.getAttribute("portmaster_snmp_retries")),
                    161,
                    "1")

####################################
    def killUser(self,user_msg):
        port = user_msg["port"]
        try:
            self.snmp_client.set(".1.3.6.1.2.1.2.2.1.7.%s"%(int(port)+2),"i",2)
        except:
            logException(LOG_ERROR)

####################################
    def updateUserList(self):
        self.onlines = self.getOnlineUsers()

    def getOnlineUsers(self):
        """
            return a dic of port=>username
        """
        LISTUSERS_OID = ".1.3.6.1.4.1.307.3.2.1.1.1.4"
        snmp_ret = self.snmp_client.walk(LISTUSERS_OID)

        onlines={}
        for oid in snmp_ret:
            port = self.__getPortFromOid(oid)
            username = snmp_ret[oid].strip()[1:-1]
            if username != "":
                onlines[port] = username
                
        return onlines

    def __getPortFromOID(self, oid):
        return str(int(oid[oid.rfind(".")+1:])-1) #magic!
####################################    
    def updateInOutBytes(self):
        inouts = self.__getInOutBySnmp()
        inouts = self._calcRates(self.inouts, inouts)
        self.inouts = inouts

    def __getInOutBySnmp(self):
        INBYTES_OID = ".1.3.6.1.4.1.307.3.2.1.1.1.17"
        OUTBYTES_OID = ".1.3.6.1.4.1.307.3.2.1.1.1.16"

        in_snmp_ret = self.snmp_client.walk(INBYTES_OID)
        out_snmp_ret = self.snmp_client.walk(OUTBYTES_OID)

        inouts={}
        for oid in in_snmp_ret:
            inouts[self.__getPortFromOid(oid)] = {"in_bytes":in_snmp_ret[oid]}

        for oid in out_snmp_ret:
            inouts[self.__getPortFromOid(oid)]["out_bytes"] = out_snmp_ret[oid]

        return inouts
        

####################################
    def isOnline(self,user_msg):
        return self.onlines.has_key(user_msg["port"])
####################################
    def getInOutBytes(self, user_msg):
        try:
            port = user_msg["port"]
            return (self.inouts[port]["in_bytes"],self.inouts[port]["out_bytes"],self.inouts[port]["in_rate"],self.inouts[port]["out_rate"])
        except KeyError:
            return (0,0,0,0)
####################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=str(ras_msg.getRequestPacket()["NAS-Port"][0])

    def handleRadAuthPacket(self,ras_msg):

        #we don't handle non-ppp sessions
        if ras_msg.getRequestPacket()["Service-Type"][0] != "Framed-User":
            return 

        self.__addUniqueIdToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password",
                                    "CHAP-Password":"chap_password",
                                    "MS-CHAP-Response":"ms_chap_response",
                                    "MS-CHAP2-Response":"ms_chap2_response",
                                    "Calling-Station-Id":"caller_id",
                                    })

        if self.inouts.has_key(ras_msg["port"]):
            self.inouts[ras_msg["port"]]["in_bytes"],self.inouts[ras_msg["port"]]["out_bytes"]=0,0

        ras_msg.setAction("INTERNET_AUTHENTICATE")

####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type=ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)
        if status_type=="Start":
            ras_msg.setInAttrs({"User-Name":"username","Framed-IP-Address":"remote_ip","Acct-Session-Id":"session_id"})
            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["remote_ip","start_accounting"]

            ras_msg.setAction("INTERNET_UPDATE")
        elif status_type=="Stop":
            ras_msg.setInAttrs({"User-Name":"username","Acct-Session-Id":"session_id","Acct-Output-Octets":"in_bytes","Acct-Input-Octets":"out_bytes"})
            try:
                self.inouts[ras_msg["port"]]["in_bytes"],self.inouts[ras_msg["port"]]["out_bytes"]=ras_msg["in_bytes"],ras_msg["out_bytes"]
            except KeyError:
                #logException(LOG_DEBUG)
                pass

            ras_msg.setAction("INTERNET_STOP")
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)
        
