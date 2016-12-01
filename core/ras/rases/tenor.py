from core.ibs_exceptions import *

from core.ras.ras import Ras
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main
from core.user import user_main
import time

def init():
    ras_main.getFactory().register(QuintumTenorRas,"Quintum Tenor")

DEBUG=False

class QuintumTenorRas(Ras, VoIPRas):
    type_attrs={"tenor_username_length":8,
                "tenor_currency_type":"USD",
                "tenor_language":"En",
                "online_check":0,
                "tenor_telephony_stop_wait_time":30}
    
    def init(self):
        
        self.pre_auth_usernames={} #h323_conf_id => voip_username
        self.onlines={} #voip_username => [h323_conf_ids]
        self.handle_reload=True

###################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"] = "h323_conf_id"
        ras_msg["h323_conf_id"] = self.__getH323ConfID(ras_msg)

    def __getH323ConfID(self,ras_msg):
        return self.getH323AttrValue("Quintum-h323-conf-id",ras_msg.getRequestPacket())


    def __addUsernamePasswordToRasMsg(self, ras_msg):
        """
            split username/password from radius packet username
        """
        if self.__isPreAuth(ras_msg.getRequestPacket()):
            h323_conf_id = ras_msg["h323_conf_id"]
            try:
                ras_msg["voip_username"] = self.pre_auth_usernames[h323_conf_id]
                return
            except KeyError:
                self.toLog("PreAuth Conf ID is not in list %s"%h323_conf_id)

        username_len = int(self.getAttribute("tenor_username_length"))
        username = ras_msg.getRequestPacket()["User-Name"][0]

        ras_msg["voip_username"] = username[:username_len]
        ras_msg["voip_password"] = username[username_len:]

    def __isPreAuth(self, request_pkt):
        return request_pkt.has_key("Calling-Station-Id") and \
               request_pkt["Calling-Station-Id"][0] == request_pkt["User-Name"][0]

####################################
    def _postAuth(self,ras_msg, auth_success):
        Ras._postAuth(self,ras_msg, auth_success)

        if self.__authSuccess(ras_msg, auth_success, "h323_pre_authentication"):
            voip_username = user_main.getUserPool().getUserByCallerID(ras_msg["caller_id"]).getUserAttrs()["voip_username"]
            self.pre_auth_usernames[ ras_msg["h323_conf_id"] ] = voip_username

        elif self.__authSuccess(ras_msg, auth_success, "h323_authorization"):
            self.__addToOnlines(ras_msg["voip_username"], ras_msg["h323_conf_id"])

    def __addToOnlines(self, voip_username, h323_conf_id):
        """
            add h323_conf_id to list of current online conf ids of voip_username
        """
        if self.onlines.has_key(voip_username):
            if h323_conf_id not in self.onlines[voip_username]:
                self.onlines[voip_username].append(h323_conf_id)
        else:
            self.onlines[voip_username] = [h323_conf_id] #list of h323 ids
        
    def __authSuccess(self, ras_msg, auth_success, attr_name):
        """
            return true if auth of ras_msg was successful and attr_name is available in ras_msg
        """
        if DEBUG:
            self.toLog("postAuth: auth_success: %s attr_name: %s has_attr_name: %s return_code: %s"%(auth_success, attr_name, ras_msg.hasAttr(attr_name), ras_msg.getReplyPacket()["Quintum-h323-return-code"]))

        success = auth_success and ras_msg.hasAttr(attr_name) \
                and ras_msg.getReplyPacket()["Quintum-h323-return-code"][0] == "h323-return-code=0"    

        if DEBUG:
            self.toLog("__authSuccess: return value is %s"%success)
        
        return success

    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)

        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"caller_id"})

        req = ras_msg.getRequestPacket()
        if req.has_key("Called-Station-Id"): #authorization
            self.__addUsernamePasswordToRasMsg(ras_msg) 
            ras_msg.setInAttrs({"Called-Station-Id":"called_number"})
            ras_msg["h323_authorization"] = True
            ras_msg["start_accounting"] = True
            ras_msg["calc_remaining_time"] = True

            ras_msg.setAction("VOIP_AUTHORIZE")

        else:
            if self.__isPreAuth(req): #pre authentication
                ras_msg["h323_pre_authentication"] = True
                
                
            else: #authentication
                self.__addUsernamePasswordToRasMsg(ras_msg)     
                ras_msg["h323_authentication"] = True

            self.setSingleH323Language(ras_msg.getReplyPacket(), self.getAttribute("tenor_language"))
            self.setSingleH323Currency(ras_msg.getReplyPacket(), self.getAttribute("tenor_currency_type"))
            ras_msg.setAction("VOIP_AUTHENTICATE")

        

        ras_msg["multi_login"] = False
        ras_msg["single_session_h323"] = True


    def handleRadAcctPacket(self,ras_msg):
        status_type = ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)

        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"caller_id"})

        self.__addUsernamePasswordToRasMsg(ras_msg)

        voip_username = ras_msg["voip_username"]
        h323_conf_id = ras_msg["h323_conf_id"]
                
        if status_type=="Stop":
            call_type = self.getH323AttrValue("Quintum-h323-call-type",ras_msg.getRequestPacket())
            call_origin = self.getH323AttrValue("Quintum-h323-call-origin",ras_msg.getRequestPacket())
            
            self.setH323TimeInAttrs(ras_msg,{"Quintum-h323-disconnect-time":"disconnect_time"})
            self.setH323TimeInAttrs(ras_msg,{"Quintum-h323-connect-time":"connect_time"})
            ras_msg["disconnect_cause"]=self.getH323AttrValue("Quintum-h323-disconnect-cause",ras_msg.getRequestPacket())

            if call_type == "VoIP" and call_origin == "originate":

                try:
                    self.onlines[voip_username].remove(h323_conf_id)
                except (KeyError, ValueError):
                    logException(LOG_ERROR, "Quintum %s: voip_username :%s conf_id:%s"%(self.getRasIP(), voip_username, h323_conf_id))
                
                ras_msg.setAction("VOIP_STOP")

            ######################
            #NOTE: SOME TIMES TELEPHONY STOP COMES BEFORE VOIP STOP
            ######################
            elif call_type == "Telephony" and call_origin == "answer":

                if not self.onlines.has_key(voip_username): #no authorization has been done
                    return    
                
                if h323_conf_id in self.onlines[voip_username]: #eh? no voip stop yet?
                    wait_time = int(self.getAttribute("tenor_telephony_stop_wait_time"))

                    while h323_conf_id in self.onlines[voip_username]:
                        if wait_time <= 0: #Logout user by telephony stop
                            self.toLog("handleRadAcctPacket: Logouting user %s by telephony stop"%voip_username)
                            ras_msg.setAction("VOIP_STOP") #let's suppose voip stop won't come
                            break
            
                        time.sleep(5)
                        wait_time -= 5
                

                if self.__isPreAuth(ras_msg.getRequestPacket()):
                    del(self.pre_auth_usernames[h323_conf_id])

                try:
                    self.onlines[voip_username].remove(h323_conf_id)
                except (KeyError, ValueError):
                    pass
                
                #####
                #TODO: self.onlines should be locked?
                #####
                if not self.onlines[voip_username]: #no more instances
                    del(self.onlines[voip_username])
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)
            
    


    def setSingleH323CreditTime(self,reply_pkt,credit_time):
        """
            set H323-Credit-Time or other attribute in reply_pkt
            this is only for rases that support pre-paid calling card type of auth          
        """
        reply_pkt["Quintum-h323-credit-time"]="h323-credit-time=%s"%credit_time

    def setSingleH323CreditAmount(self,reply_pkt,credit_amount):
        reply_pkt["Quintum-h323-credit-amount"]="h323-credit-amount=%s"%credit_amount

    def setSingleH323ReturnCode(self,reply_pkt,return_code):
        reply_pkt["Quintum-h323-return-code"]="h323-return-code=%s"%return_code

    def setSingleH323Currency(self, reply_pkt, currency):
        reply_pkt["Quintum-h323-currency-type"]="h323-currency-type=%s"%currency

    def setSingleH323Language(self, reply_pkt, language):
        reply_pkt["Quintum-h323-preferred-lang"]="h323-preferred-lang=%s"%language
        