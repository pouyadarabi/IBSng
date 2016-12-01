from core.ibs_exceptions import *
from core.lib.general import *
from core.errors import errorText
from core.db import db_main,ibs_db
from core.user import normal_user,voip_user,user_main
from core.ras.msgs import UserMsg
from core import main
import operator


class User:
    """
        Base User Class, for online users
    """
    remove_ras_attrs=["pap_password", #ras attrs to be removed from user visible attributes
                      "chap_password",
                      "ms_chap_response",
                      "ms_chap2_response",
                      "start_accounting",
                      "multi_login",
                      "voip_chap_password",
                      "voip_password",
                      "voip_digest_response",
                      "h323_authorization",
                      "single_session_h323",
                      "try_single_session_h323",                      
                      "calc_remaining_time"]

    def __init__(self, loaded_user, _type):
        """
            loaded_user(LoadedUser instance): Loaded user instance
            o_type(string): type of user either "Normal" or "VoIP"
        """
        self.instances=0
        self.__instance_info=[]
        self.loaded_user=loaded_user
        self.__type=_type
        self.__type_obj=self.__loadTypeObj(_type)
        self.__setInitialVariables()
        
        user_main.getUserPluginManager().callHooks("USER_INIT",self)

    def __loadTypeObj(self,_type):
        if _type=="Normal":
            return normal_user.NormalUser(self)
        if _type=="VoIP":
            return voip_user.VoIPUser(self)

    def __setInitialVariables(self):
        self.__setInitialCredit()

    def __setInitialCredit(self):
        self.initial_credit=self.getLoadedUser().getBasicUser().getInitialCredit()

    def __str__(self):
        return "User with id %s"%self.getLoadedUser().getUserID()

    def getLoadedUser(self):
        return self.loaded_user

    def getUserID(self):
        return self.getLoadedUser().getUserID()

    def getUserAttrs(self):
        return self.getLoadedUser().getUserAttrs()      

    def getType(self):
        return self.__type

    def getTypeObj(self):
        return self.__type_obj
    
    def isNormalUser(self):
        return self.getType()=="Normal"

    def isVoIPUser(self):
        return self.getType()=="VoIP"

    def getUserRepr(self):
        """
            return username representation of this user_obj
        """
        if self.isNormalUser():
            if self.getUserAttrs().hasAttr("normal_username"):
                return self.getUserAttrs()["normal_username"]
            else:
                return "plan %s"%self.getUserID()

        elif self.isVoIPUser() and self.getUserAttrs().hasAttr("voip_username"):
            return self.getUserAttrs()["voip_username"]

        else:
            return "userid %s"%self.getUserID()

###################################################
    def getInstanceInfo(self,instance):
        return self.__instance_info[instance-1]

    def getRasID(self,instance):
        return self.getInstanceInfo(instance)["ras_id"]

    def getUniqueIDValue(self,instance):
        return self.getInstanceInfo(instance)["unique_id_val"]
        
    def getGlobalUniqueID(self,instance):
        return (self.getRasID(instance),self.getUniqueIDValue(instance))

    def accountingStarted(self, instance):
        """
            return true if accounting is started for instance
            if instance is None, check all instances
        """
        if instance:
            return self.getInstanceInfo(instance).has_key("start_accounting")
        else:
            for instance in xrange(1,self.instances+1):
                if self.getInstanceInfo(instance).has_key("start_accounting"):
                    return True
            return False

##################################################
    def getInstanceFromRasMsg(self,ras_msg):
        ras_id=ras_msg.getRasID()
        unique_id_val=ras_msg.getUniqueIDValue()
        return self.getInstanceFromUniqueID(ras_id,unique_id_val)
        
    def getInstanceFromUniqueID(self,ras_id,unique_id_val):
        for instance in range(1,self.instances+1):
            instance_info=self.getInstanceInfo(instance)
            if instance_info["ras_id"]==ras_id and instance_info["unique_id_val"]==unique_id_val:
                return instance
        return None
##################################################
    def calcCurrentCredit(self,round_result=True):
        return self.initial_credit - self.charge.calcCreditUsage(round_result)

    def calcInstanceCreditUsage(self,instance,round_result=True):
        return self.charge.calcInstanceCreditUsage(instance,round_result)
##################################################
    def createUserMsg(self,instance,action):
        """
            create a UserMsg ready to send to a ras.
            Information necessary for ras will be set from user "instance" information
        """
        instance_info=self.getInstanceInfo(instance)
        msg=UserMsg()
        msg["ras_id"]=instance_info["ras_id"]
        msg["unique_id"]=instance_info["unique_id"]
        msg[instance_info["unique_id"]]=instance_info["unique_id_val"]
        msg["user_obj"]=self
        msg["instance"]=instance
        msg["instance_info"]=self.getInstanceInfo(instance)
        msg.setAction(action)
        return msg

##################################################
    def setKillReason(self,instance,reason):
        instance_info=self.getInstanceInfo(instance)
        if instance_info["attrs"].has_key("kill_reason"):
            instance_info["attrs"]["kill_reason"]+=", %s"%reason
        else:
            instance_info["attrs"]["kill_reason"]=reason

##################################################
    def __filterRasAttrs(self,attrs):
        cattrs=attrs.copy()
        for attr_name in self.remove_ras_attrs:
            if cattrs.has_key(attr_name):
                del(cattrs[attr_name])
        return cattrs
##################################################
    def login(self,ras_msg):
        self.instances += 1
        self.__instance_info.append({})

        instance_info=self.getInstanceInfo(self.instances)
        instance_info["auth_ras_msg"]=ras_msg
        instance_info["unique_id"]=ras_msg["unique_id"]
        instance_info["unique_id_val"]=ras_msg.getUniqueIDValue()
        instance_info["attrs"]=self.__filterRasAttrs(ras_msg.getAttrs())
        instance_info["ras_id"]=ras_msg.getRasID()
        instance_info["check_online_fails"]=0
        instance_info["login_time"]=time.time()
        instance_info["successful_auth"]=False

        try:
            self.__checkNoLoginFlag()
            user_main.getUserPluginManager().callHooks("USER_LOGIN",self,[ras_msg])
        except Exception,e:
            if isinstance(e,IBSError):
                self.setKillReason(self.instances,e.getErrorText())
            else:
                self.setKillReason(self.instances,str(e))

            self.logout(self.instances,ras_msg)
            raise

        instance_info["successful_auth"]=True

    def __checkNoLoginFlag(self):
        """
            check if main no_login flag is set
        """
        if main.noLoginSet():
            raise LoginException(errorText("USER_LOGIN","LOGIN_NOT_ALLOWED"))
        
    def logout(self,instance,ras_msg):
        """
            this method calls before user logout process start
            we call plugins now, so they'll see the correct user object
            that not changed for logout
        """

        self.getInstanceInfo(instance)["logout_ras_msg"]=ras_msg
        (query,used_credit)=self.getTypeObj().logout(instance,ras_msg)
        user_main.getUserPluginManager().callHooks("USER_LOGOUT",self,[instance,ras_msg])
        if not ras_msg.hasAttr("no_connection_log"):
            query += self.getTypeObj().logToConnectionLog(instance)
        query.runQuery()
        self.instances-=1
        del(self.__instance_info[instance-1])
        return used_credit

    def update(self,ras_msg):
        """
            plugins can update themeselves whenever we recieved an update packet, with updated info 
            from radius server
            They can return True to cause a recalcEvent for user
        """
        ret=user_main.getUserPluginManager().callHooks("UPDATE",self,[ras_msg])
        return True in ret

    def canStayOnline(self):
        results=filter(lambda x:x!=None,user_main.getUserPluginManager().callHooks("USER_CAN_STAY_ONLINE",self))
        return reduce(operator.add,results)

    def commit(self,used_credit):
        """
            saves all changed user info from memory into DB
            commit is called before logout of each instance
        """
        query=reduce(operator.add,filter(lambda x:x!=None,user_main.getUserPluginManager().callHooks("USER_COMMIT",self)))
        query+=self.__commitCreditQuery(used_credit)
        return query
        
    def __commitCreditQuery(self,used_credit):
        return ibs_db.createFunctionCallQuery("change_user_credit",[self.getUserID(), -1*used_credit])

    
    def _reload(self):
        self.__setInitialCredit()
        user_main.getUserPluginManager().callHooks("USER_RELOAD",self)

