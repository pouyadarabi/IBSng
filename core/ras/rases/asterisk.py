from core.server import handlers_manager
from core.server import handler
from core.ibs_exceptions import *
from core.user import user_main
from core.ras.msgs import *
from core.lib.general import *
from core.lib import password_lib
from core.lib.asterisk import manager

from core.ras.ras import Ras
from core.ras.voip_ras import VoIPRas
from core.ras import ras_main

def init():
    if not handlers_manager.getManager().handlerRegistered("asterisk"):
        handlers_manager.getManager().registerHandler(AsteriskHandler())

    ras_main.getFactory().register(AsteriskRas,"Asterisk")
    

class AsteriskHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"asterisk")
        self.registerHandlerMethod("preAuthenticate")
        self.registerHandlerMethod("authenticate")
        self.registerHandlerMethod("authorize")
        self.registerHandlerMethod("callEnd")
        self.registerHandlerMethod("addDestinationToFastDial")
        self.registerHandlerMethod("getFastDialDestination")
        self.registerHandlerMethod("getLastDestination")
        self.registerHandlerMethod("addCallerIDAuthentication")
        self.registerHandlerMethod("deleteCallerIDAuthentication")
        self.registerHandlerMethod("getUserCredit")
        self.registerHandlerMethod("checkPassword")
        self.registerHandlerMethod("changePassword")


    def __getRasObj(self, request):
        """
            return ras_obj associated with request remote address
        """
        ras_ip=request.getRemoteAddr()
        return ras_main.getLoader().getRasByIP(ras_ip)
        
        
    def __checkAsteriskAuth(self, request):
        """
            Check if Request is done from valid asterisk ras
            Request itself should have anonymous auth type.
            Field asterisk_password should be available in request and
            should be equal to the password entered in asterisk ras attributes
        """
        request.checkArgs("asterisk_password")
        ras_obj=self.__getRasObj(request)
        if ras_obj.getType() != "Asterisk" or \
           ras_obj.getAttribute("asterisk_password")!=request["asterisk_password"]:
           request.raiseAccessDenied()

    def preAuthenticate(self, request):
        """
            Pre Authenticate user, check if he's able to log in
            just by authenticating the caller id

            return (username,credit,language) if user is successfully authenticated via caller id
            return an error otherwise
            
            caller_id(str): caller id of user
            channel(str): asterisk channel name
            unique_id(str): unique id of call
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("caller_id","channel","unique_id")
        return self.__getRasObj(request).preAuthenticate(request["caller_id"],request["channel"],request["unique_id"])

    def authenticate(self, request):
        """
            authenticate user, check if he can log in
            
            return credit of user if user is successfully authenticated
            return an error otherwise
            
            username(str): pin number entered by user
            password(str): password of user
            caller_id(str): caller id of user
            channel(str): asterisk channel name
            unique_id(str): unique id of call
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","password","caller_id","channel","unique_id")
        return self.__getRasObj(request).authenticate(request["username"],request["password"],request["caller_id"],request["channel"],request["unique_id"])

    
    def authorize(self, request):
        """
            authorize user, check if he's authorized to call destination.
            user should be guaranteed to authenticated before calling authorization.
            AGI script should handle this.
            
            return seconds that user can talk (or a negative number if unilimited) if user successfully authorized
            return and error otherwise
            
            username(str): pin number entered by user
            destination(str): number dialed by user
            caller_id(str): caller id of user
            channel(str): asterisk channel name
            unique_id(str): unique id of call

        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","destination","caller_id","channel","unique_id")
        return self.__getRasObj(request).authorize(request["username"],request["destination"],request["caller_id"],request["channel"],request["unique_id"])


    def callEnd(self, request):
        """
            inform end of call
            return (duration,consumed_credit)
            
            username(str): pin number entered by user
            channel(str): asterisk channel name
            unique_id(str): unique id of call
            duration(integer): duration of call in seconds
            dc_cause(str): cause of disconnection
            
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","duration","channel","unique_id","dc_cause")
        return self.__getRasObj(request).callEnd(request["username"],to_int(request["duration"],"duration"),request["channel"],request["unique_id"],request["dc_cause"])
        
    def addDestinationToFastDial(self, request):
        """
            assign a destination to fast dial index

            username(str): pin number of user
            destination(str): 
            index(integer): integer within 0 and 9 to assgin destination to
        
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","destination","index")
        return user_main.getUserPluginModules()["fast_dial"].getActionsManager().addDestinationToFastDial(request["username"],
                                                                                                          request["destination"],
                                                                                                          request["index"])

    def getFastDialDestination(self, request):
        """
            get destination for specified index
            
            return string of assigned destination or empty string if no
            number assigned to this index
            
            index(integer): integer within 0 and 9
            username(str): pin number of user
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","index")
        return user_main.getUserPluginModules()["fast_dial"].getActionsManager().getFastDialDestination(request["username"],
                                                                                                        request["index"])

    def getLastDestination(self, request):
        """
            get last destination dialed by user
            return string of last destination or empty string if
            there's no last number
            
            username(str): pin number of user
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username")
        try:
            return user_main.getActionManager().getLastDestination(request["username"])
        except IBSError,e:
            raise IBSError(e.getErrorKey())
        
        

    def addCallerIDAuthentication(self, request):
        """
            add caller id of user in voip caller id attribute
            
            username(str): pin number of user
            caller_id(str): caller_id to be added to voip caller ids
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","caller_id")
        try:
            return user_main.getActionManager().addCallerIDAuthentication(request["username"], request["caller_id"])
        except IBSError,e:
            raise IBSError(e.getErrorKey())

    def deleteCallerIDAuthentication(self, request):
        """
            remove caller id of user in voip caller id attribute
            
            username(str): pin number of user
            caller_id(str): caller_id to be added to voip caller ids
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","caller_id")
        try:
            return user_main.getActionManager().deleteCallerIDAuthentication(request["username"], request["caller_id"])
        except IBSError,e:
            raise IBSError(e.getErrorKey())

    def getUserCredit(self, request):
        """
            return credit amount of user
            username(str): pin number of user
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username")
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(request["username"])
        return loaded_user.getBasicUser().getCredit()

    def checkPassword(self, request):
        """
            return True if password of user is correct
            username(str): pin number of user
            password(str): password of user
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","password")
        return user_main.getUserPluginModules()["voip_user"].getActionsManager().checkPassword(request["username"],request["password"])

    def changePassword(self, request):
        """
            change password of user to "password"
            username(str): pin number of user
            password(str): password of user
        """
        self.__checkAsteriskAuth(request)
        request.checkArgs("username","password")
        return user_main.getUserPluginModules()["voip_user"].getActionsManager().changePasswordByUsername(request["username"],request["password"])


class AsteriskRas(Ras, VoIPRas):
    type_attrs={"asterisk_password":"asterisk",
                "asterisk_multi_login":0,
                "asterisk_use_manager":0,
                "asterisk_manager_timeout":30,
                "asterisk_manager_port":5038,
                "asterisk_manager_username":"asterisk",
                "asterisk_manager_secret":"asterisk"
                }

    def init(self):
        if self.getAttribute("asterisk_use_manager"):
            self.manager=self.__createManager()
    
    def __createManager(self):
        return manager.AsteriskManager(self.getRasIP(),
                             self.getAttribute("asterisk_manager_port"),
                             self.getAttribute("asterisk_manager_username"),
                             self.getAttribute("asterisk_manager_secret"),
                             self.getAttribute("asterisk_manager_timeout"))


    def __runCommandOnManager(self, action, dic_args):
        """
            run action with dictionary arguments on manager
            return message returned by manager or None if error happened
        """
        try:
            return self.manager.run(action, dic_args)
        except:
            logException(LOG_ERROR,"Running action %s, args %s"%(action,dic_args))
            return None


    def killUser(self, user_msg):
        if self.getAttribute("asterisk_use_manager"):
            channel,unique_id=user_msg["asterisk_channel"].split("||")
            self.__runCommandOnManager("Hangup",{"channel":channel})

    #################################################

    def __createRasMsg(self, channel, unique_id):
        ras_msg=RasMsg({},{},self)
        self.__setUniqueID(ras_msg, channel, unique_id)
        ras_msg["multi_login"]=self.getAttribute("asterisk_multi_login")!=0
        if not ras_msg["multi_login"]:
            ras_msg["single_session_voip"]=True
        return ras_msg
        
    def __setUniqueID(self,ras_msg, channel, unique_id):
        ras_msg["asterisk_channel"]="%s||%s"%(channel,unique_id)
        ras_msg["unique_id"]="asterisk_channel"

    def __getLanguageForUser(self, loaded_user):
        if loaded_user.hasAttr("voip_preferred_language"):
            return loaded_user.getUserAttrs()["voip_preferred_language"]
        else:
            return ""

    def preAuthenticate(self, caller_id, channel,unique_id):
        ras_msg=self.__createRasMsg(channel,unique_id)
        ras_msg["caller_id"]=caller_id
        ras_msg["pre_authentication"]=True
        ras_msg.setAction("VOIP_AUTHENTICATE")
        if ras_msg.send():
            loaded_user=user_main.getUserPool().getUserByCallerID(caller_id)
            return (loaded_user.getUserAttrs()["voip_username"],
                    loaded_user.getBasicUser().getCredit(),
                    self.__getLanguageForUser(loaded_user))
        else:
            raise GeneralException(ras_msg["error_key"])
        
    def authenticate(self, username, password, caller_id, channel, unique_id):
        ras_msg=self.__createRasMsg(channel,unique_id)
        ras_msg["caller_id"]=caller_id
        ras_msg["voip_username"]=username
        ras_msg["voip_password"]=password
        ras_msg.setAction("VOIP_AUTHENTICATE")

        if ras_msg.send():
            loaded_user=user_main.getUserPool().getUserByVoIPUsername(username)
            return loaded_user.getBasicUser().getCredit()
        else:
            raise GeneralException(ras_msg["error_key"])


    def authorize(self, username, destination, caller_id, channel, unique_id):
        ras_msg=self.__createRasMsg(channel,unique_id)
        ras_msg["caller_id"]=caller_id
        ras_msg["voip_username"]=username
        ras_msg["calc_remaining_time"]=True
        ras_msg["start_accounting"]=True
        ras_msg["called_number"]=destination
        ras_msg.setAction("VOIP_AUTHORIZE")

        if ras_msg.send():
            loaded_user=user_main.getUserPool().getUserByVoIPUsername(username)
            user_obj=user_main.getOnline().getUserObj(loaded_user.getUserID())
            return user_obj.getTypeObj().getRemainingTime(user_obj.getInstanceFromRasMsg(ras_msg))
        else:
            raise GeneralException(ras_msg["error_key"])
        
        
    def callEnd(self, username, duration, channel, unique_id, dc_cause):
        ras_msg=self.__createRasMsg(channel,unique_id)
        ras_msg["voip_username"]=username

        now=time.time()
        ras_msg["connect_time"]=now-duration
        ras_msg["disconnect_time"]=now

        ras_msg["disconnect_cause"]=dc_cause

        ras_msg.setAction("VOIP_STOP")
        
        used_credit = ras_msg.send()
    
        return (duration, used_credit)


    #############################################
    def isOnline(self,user_msg):
        return True     