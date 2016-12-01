from core.ras.ras import UpdateUsersRas
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core.ibs_exceptions import *
from core.user import user_main
from radius_server import rad_server
from radius_server.pyrad import client,packet

import os,time,copy

def init():
    ras_main.getFactory().register(MVTSRas,"MVTS")

class MVTSRas(UpdateUsersRas,VoIPRas):
    type_attrs={"mvts_acct_update_interval":1,
                "mvts_enable_kill_user":1,
                "mvts_radius_auth_port":1812,
                "mvts_radius_timeout":5,
                "mvts_cdr_user":"cdr"}

    def init(self):
        self.onlines={}

####################################
    def killUser(self,user_msg):
        try:
            srv=client.Client(self.getRasIP(),
                              self.getAttribute("mvts_radius_auth_port"),
                              1813,
                              self.getRadiusSecret(),
                              rad_server.getDictionary())
            req=srv.CreateAuthPacket(code=packet.DisconnectRequest)
            req["User-Name"]=user_msg["user_obj"].getUserAttrs()["voip_username"]
            req["H323-conf-id"]="h323-conf-id=%s"%user_msg["h323_conf_id"]
            req.VerifyReply=lambda pkt,raw_reply:True #fool mvts always zero fill authenticator
            srv.timeout=self.getAttribute("mvts_radius_timeout")
            reply=srv.SendPacket(req)
            if reply.code!=packet.DisconnectAck:
                self.toLog("killUser: received packet shows failure, type: %s"%reply.code,LOG_ERROR)
        except:
            logException(LOG_ERROR)
        
####################################
    def getOnlines(self):
        pass
####################################    
    def generalUpdate(self):
        pass
    
    def updateUserList(self):
        min_last_update=time.time()-int(self.getAttribute("mvts_acct_update_interval"))*60
        for h323_conf_id in self.onlines.keys():
            if self.onlines[h323_conf_id]<min_last_update:
                del(self.onlines[h323_conf_id])
####################################
    def isOnline(self,user_msg):
        return self.onlines.has_key(user_msg["h323_conf_id"])

    def __updateOnlines(self,ras_msg):
        self.onlines[self.getH323AttrValue("H323-conf-id",ras_msg.getRequestPacket())]=time.time()

####################################
    def __addToAuthCalls(self, request_pkt):
        self.auth_users.append(self.getH323AttrValue("H323-conf-id",request_pkt))

    def __removeFromAuthCalls(self, pkt):
        self.auth_users.append(self.getH323AttrValue("H323-conf-id",pkt))

    def __isAuthCallByConfID(self, h323_conf_id):
        return h323_conf_id in self.auth_users
        
####################################
    def _handleRadAuthPacket(self,request,reply):
        if request.has_key("H323-conf-id"): #ARQ, Authorization Request
            return UpdateUsersRas._handleRadAuthPacket(self, request, reply)
        else: #RRQ, Authentication Request
            return self.__rrqAuth(request ,reply)
            
###################################
    def __rrqAuth(self,request,reply):
        """
            do the RRQ Auth. We do it by just checking the username and password
            other checkings will be done in authorization request.
        """
        try:
            loaded_user=user_main.getUserPool().getUserByVoIPUsername(request["User-Name"][0])
        except GeneralException:
            return False

        if not request.checkChapPassword(loaded_user.getUserAttrs()["voip_password"]):
            return False

        return True


###################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"] = "h323_conf_id"
        ras_msg["h323_conf_id"] = self.__getH323ConfID(ras_msg)

    def __getH323ConfID(self,ras_msg):
        return self.getH323AttrValue("H323-conf-id",ras_msg.getRequestPacket())

    def __getVoIPCallType(self, ras_msg):
        """
            return (call_type, call_origin) of ras_msg
        """
        pkt = ras_msg.getRequestPacket()
        call_type = self.getH323AttrValue("H323-call-type", pkt)
        call_origin = self.getH323AttrValue("H323-call-origin", pkt)
        return (call_type,call_origin)

###################################
    def handleRadAuthPacket(self,ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)

        ras_msg.setInAttrs({"User-Name":"voip_username",
                            "Called-Station-Id":"called_number",
                            
                            })
                            
        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"caller_id",
                                    "CHAP-Password":"voip_chap_password"})

        ras_msg["try_single_session_h323"] = True
        ras_msg["h323_authorization"] = True

        ras_msg["calc_remaining_time"] = True

        ras_msg["called_ip"]=self.getH323AttrValue("H323-remote-address",ras_msg.getRequestPacket())
        ras_msg["caller_ip"]=self.getAttrInCiscoAVPair("h323-gw-address",ras_msg.getRequestPacket())

        ras_msg.setAction("VOIP_AUTHORIZE")

####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]

        if status_type=="Start":
            self.__handleStartAccounting(ras_msg)
        elif status_type=="Stop":
            self.__handleStopAccounting(ras_msg)
        elif status_type=="Alive":
            self.__updateOnlines(ras_msg)
        elif status_type in ("Accounting-On","Accounting-Off"):
            pass
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)


    def __handleStartAccounting(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        (call_type, call_origin) = self.__getVoIPCallType(ras_msg)

        if (call_type,call_origin) == ("VoIP","originate"):
            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["start_accounting"]
            self.__updateOnlines(ras_msg)
            ras_msg.setAction("VOIP_UPDATE")

    def __handleStopAccounting(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        (call_type, call_origin) = self.__getVoIPCallType(ras_msg)

        if (call_type,call_origin) == ("VoIP","originate"):
            ras_msg.setInAttrs({"User-Name":"voip_username",
                                "Acct-Session-Time":"duration",
                                "Acct-Session-Id":"session_id"})
                                
            self.setH323TimeInAttrs(ras_msg,{"H323-disconnect-time":"disconnect_time"})
            
            if ras_msg.getRequestPacket().has_key("H323-connect-time"):
                self.setH323TimeInAttrs(ras_msg,{"H323-connect-time":"connect_time"})
            else:
                ras_msg["connect_time"]=ras_msg["disconnect_time"]
        
            ras_msg["disconnect_cause"]=self.getH323AttrValue("H323-disconnect-cause",ras_msg.getRequestPacket())
            
            ras_msg.setAction("VOIP_STOP")

########################################
    def setSingleH323CreditTime(self,reply_pkt,credit_time):
        VoIPRas.setSingleH323CreditTime(self,reply_pkt,credit_time, True)

    def setSingleH323CreditAmount(self,reply_pkt,credit_amount):
        VoIPRas.setSingleH323CreditAmount(self,reply_pkt,credit_amount, True)
                