
from core.ras.ras import GeneralUpdateRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from radius_server import rad_main
from radius_server.pyrad import client,packet
import os, time

def init():
    ras_main.getFactory().register(ChilliSpot,"ChilliSpot")
    
class ChilliSpot(GeneralUpdateRas):
    type_attrs = {
                    "chilli_update_accounting_interval":1,
                    "chilli_spot_disconnect_ip":"192.168.1.65",
                    "chilli_spot_disconnect_port":3799,
                    "chilli_spot_radius_timeout":5,
                    "chilli_reonline_users":1
                  }
                  
    def init(self):
        self.onlines = {} # dict, port => {"username":, "in_bytes":, "out_bytes":, "last_update":}
        
    def getInOutBytes(self, user_msg):
        try:
            port=user_msg["port"]
            if port in self.onlines:
                return (self.onlines[port]["in_bytes"],self.onlines[port]["out_bytes"],
                        self.onlines[port]["in_rate"],self.onlines[port]["out_rate"])
            else:
                return (0,0,0,0)
        except:
            logException(LOG_ERROR)
            return (-1,-1,-1,-1)

    def killUser(self, usr_msg):
           try:
               srv = client.Client(self.getAttribute("chilli_spot_disconnect_ip"),
                                   self.getAttribute("chilli_spot_disconnect_port"),
                                   self.getAttribute("chilli_spot_disconnect_port"),
                                   self.getRadiusSecret(),
                                   rad_main.getDictionary())
               req = srv.CreateAcctPacket(code=packet.DisconnectRequest)
               req["User-Name"] = self.__getUsernameFromUserMsg(usr_msg)
               srv.timeout = self.getAttribute("chilli_spot_radius_timeout")
               reply = srv.SendPacket(req)
               if reply.code() != packet.DisconnectAck:
                   self.toLog("chilli_spot, killuser: recived packet shows failure type:%s"%reply.code, LOG_ERROR)
           except:
               logException(LOG_ERROR)

    def __getUsernameFromUserMsg(self, user_msg):
        """
            return (username) from logged on user
        """
        instance_info = user_msg["user_obj"].getInstanceInfo(user_msg["instance"])
        return (instance_info["attrs"]["username"])


          
####################################
    def isOnline(self,user_msg):
        return self.onlines.has_key(user_msg["port"]) and self.onlines[user_msg["port"]]["last_update"] >= \
            time.time() - int(self.getAttribute("chilli_update_accounting_interval"))*60

#####################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=str(ras_msg.getRequestPacket()["NAS-Port"][0])


#####################################
    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({
                                    "User-Password":"pap_password",
                                    "CHAP-Password":"chap_password",
                                    "MS-CHAP-Response":"ms_chap_response",
                                    "MS-CHAP2-Response":"ms-chap2-response",
                                    "Calling-Station-Id":"mac",
                                    "Framed-IP-Address":"remote_ip"
                                    })
        if self.onlines.has_key(ras_msg["port"]):
            self.onlines[ras_msg["port"]]["in_bytes"], self.onlines[ras_msg["port"]]["out_bytes"]= 0,0
        
        ras_msg.getReplyPacket()["Acct-Interim-Interval"] = self.getAttribute("chilli_update_accounting_interval")*60
        
        ras_msg["ip_assignment"]=False
        ras_msg.setAction("INTERNET_AUTHENTICATE")
        
#######################################
    def handleRadAcctPacket(self, ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)
        
        if status_type == "Start":
            ras_msg.setInAttrs({"User-Name":"username", "Acct-Session-Id":"session_id"})
            ras_msg["start_accounting"] = True
            ras_msg["update_attrs"] = ["start_accounting"]
            
            self.__addInOnlines(ras_msg)
            
            ras_msg.setAction("INTERNET_UPDATE")
        
        elif status_type == "Stop":
            ras_msg.setInAttrs({"User-Name":"username",
                                "Framed-IP-Address":"remote_ip",
                                "Acct-Session-Id":"session_id",
                                "Acct-Output-Octets":"in_bytes",
                                "Acct-Input-Octets":"out_bytes",
                                "Acct-Terminate-Cause":"terminate_cause"})
            self.__updateInOnlines(ras_msg)    
            ras_msg.setAction("INTERNET_STOP")

        elif status_type == "Alive":
            if not self.isUserOnline(ras_msg) and int(self.getAttribute("chilli_reonline_users")):
                self.tryToReOnline(ras_msg)
                self.toLog("handleRadAcctPacket: Update Acct recieved, but user is not in Onlines", LOG_ERROR)
            else:
                self.__updateInOnlines(ras_msg)
    
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)
########################################
    def populateReOnlineRasMsg(self, ras_msg):
        GeneralUpdateRas.populateReOnlineRasMsg(self, ras_msg)        
        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"mac"})

    def tryToReOnlineResult(self, ras_msg, auth_success):
        if auth_success: 
            self.__addInOnlines(ras_msg)
        else:
            #auth failed
            self.killUser(ras_msg)
            self.toLog("tryToReOnlineResult: kill by username on unseccessful auth")

    def __addInOnlines(self, ras_msg):
    
        pkt = ras_msg.getRequestPacket()
        if pkt.has_key("Acct-Output-Octets"):
            start_in_bytes = pkt["Acct-Input-Octets"][0]
            start_out_bytes = pkt["Acct-Output-Octets"][0]
        else:
            start_in_bytes = 0
            start_out_bytes = 0
    
        self.onlines[ras_msg["port"]] = {"username":ras_msg["username"], 
                         "in_bytes":0, 
                         "out_bytes":0,
                         "in_rate":0, 
                         "out_rate":0,
                         "start_in_bytes":start_in_bytes,
                         "start_out_bytes":start_out_bytes,
                         "last_update":time.time()}



    def __updateInOnlines(self, ras_msg):
        if ras_msg["port"] in self.onlines:
            out_bytes=ras_msg.getRequestAttr("Acct-Input-Octets")[0]
            in_bytes=ras_msg.getRequestAttr("Acct-Input-Octets")[0]
            duration=time.time() - self.onlines[ras_msg["port"]]["last_update"]

            self.onlines[ras_msg["port"]]["in_rate"]=(in_bytes-self.onlines[ras_msg["port"]]["in_bytes"])/duration
            self.onlines[ras_msg["port"]]["out_rate"]=(out_bytes-self.onlines[ras_msg["port"]]["out_bytes"])/duration
    
            self.onlines[ras_msg["port"]]["in_bytes"]=in_bytes
            self.onlines[ras_msg["port"]]["out_bytes"]=out_bytes

            self.onlines[ras_msg["port"]]["last_update"] = time.time()
            
        else:
            self.toLog("Update accounting called for %s,%s while he's NOT on my online list"%(ras_msg.getRequestAttr("User-Name")[0],ras_msg["port"]))
