from core.user import user_main,normal_user,loading_user,user
from core.event import event,periodic_events
from core.ibs_exceptions import *
from core.errors import errorText
from core.ras.msgs import RasMsg
from core.ras import ras_main
from core.log_console.console_main import getLogConsole
import copy

class OnlineUsers:
    def __init__(self):
        self.user_onlines={}#user_id=>user_obj
        self.ras_onlines={}#(ras_id,unique_id)=>user_obj
        self.loading_user=loading_user.LoadingUser()

    def __loadUserObj(self,loaded_user,obj_type):
        return user.User(loaded_user,obj_type)

##############################################
    def __addToOnlines(self,user_obj):
        global_unique_id = user_obj.getGlobalUniqueID(user_obj.instances)
        self.user_onlines[user_obj.getUserID()]=user_obj
        self.ras_onlines[global_unique_id]=user_obj

    def __removeFromRasOnlines(self,global_unique_id):
        del(self.ras_onlines[global_unique_id])
    
    def __removeFromUserOnlines(self,user_obj):
        del(self.user_onlines[user_obj.getUserID()])
        
    def __checkDuplicateOnline(self,ras_msg):
        """
            check if there's any other user online, with this global unique id
        """
        global_unique_id = (ras_msg.getRasID(), ras_msg.getUniqueIDValue())
        
        if self.ras_onlines.has_key( global_unique_id ):
            current_online_user_obj = apply(self.getUserObjByUniqueID,global_unique_id)
            current_online_user_id = current_online_user_obj.getUserID()
            
            getLogConsole().log(current_online_user_obj.getUserRepr(), 
                                "Duplicate Login",
                                [("New User", ras_msg.getUserRepr()),
                                 ("Ras", ras_main.getLoader().getRasByID(global_unique_id[0]).getRasIP()),
                                 ("ID", global_unique_id[1])])

            toLog("User %s logged on %s, while user %s was on it, force logouting %s"%(
                                                                    ras_msg.getUserRepr(), 
                                                                    global_unique_id,
                                                                    current_online_user_id,
                                                                    current_online_user_id),LOG_ERROR)

            self.clearUser(current_online_user_id, global_unique_id[0], global_unique_id[1], \
                                   "Another user logged on this global unique id", False)
        
############################################
    def getOnlineUsers(self):
        return copy.copy(self.user_onlines)
    
    def getOnlineUsersByRas(self):
        return copy.copy(self.ras_onlines)

    def getOnlinesCount(self):
        return len(self.ras_onlines)

############################################
    def isUserOnline(self,user_id):
        """
            return True if user with "user_id" is online
            better called when self.loading_user lock held
        """
        return self.user_onlines.has_key(user_id)

    def getUserObj(self,user_id):
        """
            return User instance of online user, or None if no user is online
        """
        try:
            return self.user_onlines[user_id]
        except KeyError:
            return None

    def getUserObjByUniqueID(self, ras_id, unique_id_val):
        """
            return User instance of online user, or None if no user is online
        """
        try:
            return self.ras_onlines[(ras_id,unique_id_val)]
        except KeyError:
            return None

    def isAnyOneOnlineOnRas(self,ras_id):
        """
            return true if there's anyone online on ras with id "ras_id"
        """
        for online_ras_id,unique_id in self.getOnlineUsersByRas():
            if ras_id == online_ras_id:
                return True
        
        return False
        
############################################
    def reloadUser(self,user_id):
        self.loading_user.loadingStart(user_id)
        try:
            user_obj=self.getUserObj(user_id)
            if user_obj==None:
                toLog("Reload User called while user is not online for user_id: %s"%user_id,LOG_ERROR)
            else:
                user_obj._reload()
                if user_obj.accountingStarted(None):
                    self.recalcNextUserEvent(user_obj.getUserID(),True) 
        finally:                                                    
            self.loading_user.loadingEnd(user_id)

##############################################
    def updateUser(self,ras_msg):
        user_obj=self.getUserObjByUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
        if user_obj==None:
            toLog("Update User called while user is not online for ras_id: %s unique_id_value:%s"%(ras_msg.getRasID(),ras_msg.getUniqueIDValue()),LOG_ERROR)
            return None
        self.loading_user.loadingStart(user_obj.getUserID())
        try:
            recalc_event=user_obj.update(ras_msg)
            if recalc_event:
                self.recalcNextUserEvent(user_obj.getUserID(),user_obj.instances>1 or (user_obj.instances==1 and not ras_msg.hasAttr("start_accounting")))
        finally:
            self.loading_user.loadingEnd(user_obj.getUserID())

    
############################################
    def recalcNextUserEvent(self,user_id,remove_prev_event=False):
        """
            recalculates user next event.
            user_id(int): id of user we recalculate event
            remove_prev_event(bool): Remove user previous event. This flag should be set by reload method
        """
        self.loading_user.loadingStart(user_id)
        try:
            user_obj=self.getUserObj(user_id)
            if user_obj==None:
                toLog("recalcNextUserEvent Called for user id %s while he's not online"%user_id,LOG_DEBUG)
                return
            if remove_prev_event:
                self.__removePrevUserEvent(user_id)
            result=user_obj.canStayOnline()
            self.__killUsersInCanStayOnlineResult(user_obj,result)
            self.__setNextUserEvent(result,user_id)
        finally:
            self.loading_user.loadingEnd(user_id)

    def __removePrevUserEvent(self,user_id):
        event.removeEvent(self.recalcNextUserEvent,[user_id,False],False)

    def __setNextUserEvent(self,result,user_id):
        next_evt=result.getEventTime()
#       toLog("Next Evt:%s"%next_evt,LOG_DEBUG)
        if next_evt != 0: #no next event
            event.addEvent(next_evt,self.recalcNextUserEvent,[user_id,False])

    def __killUsersInCanStayOnlineResult(self,user_obj,result):
        kill_dic = result.getKillDic()
        instances = kill_dic.keys()

        instances.sort()
        instances.reverse() #kill downward, prevent from instance shift
        
        for instance in instances:
            user_obj.setKillReason(instance,kill_dic[instance])
            user_obj.getTypeObj().killInstance(instance)
#############################################
    def checkOnlines(self):
        """
            check ibs current list of online users, by asking ras to say if user is online or not
        """
        for user_id in self.user_onlines.keys():
            self.loading_user.loadingStart(user_id)
            try:
                try:
                    user_obj=self.user_onlines[user_id]
                except KeyError:
                    pass
                else:
                    self.__checkStaleOnlines(user_obj)
                    self.__negCreditCheck(user_obj)
                    self.__killedCheck(user_obj)

            except:
                logException(LOG_ERROR)
            self.loading_user.loadingEnd(user_id)

    def __checkStaleOnlines(self, user_obj):
        instance = user_obj.instances
        while instance > 0:
            instance_info=user_obj.getInstanceInfo(instance)
            user_msg=user_obj.createUserMsg(instance,"IS_ONLINE")

            if user_msg.send():
                instance_info["check_online_fails"] = 0
            else:
                instance_info["check_online_fails"] += 1
                if instance_info["check_online_fails"]==defs.CHECK_ONLINE_MAX_FAILS:

                    toLog("Maximum Check Online Fails Reached for user %s"%user_obj.getUserID(), LOG_DEBUG)

                    getLogConsole().log(user_obj.getUserRepr(), 
                                        "Check Online Fail",
                                        [("Ras", ras_main.getLoader().getRasByID(instance_info["ras_id"]).getRasIP()),
                                        ("ID", "(%s,%s)"%(instance_info["unique_id"], instance_info["unique_id_val"]))
                                        ])

                    self.__forceLogoutUser(user_obj,instance,errorText("USER_LOGIN","MAX_CHECK_ONLINE_FAILS_REACHED",False))
        
            instance -= 1


    def __negCreditCheck(self, user_obj):
        """
            check and kill users with negative credit
            
            WARNING: Will be Removed, killedCheck has better meaning and works with all plugins
        """
        credit = user_obj.calcCurrentCredit()
        if  credit < 0 : #neg credit checker
            toLog("Found User with negative credit %s:%s"%(user_obj.getUserID(), credit), LOG_ERROR)
            
            for instance in xrange(1,user_obj.instances+1):
                instance_info = user_obj.getInstanceInfo(instance)

                if not instance_info.has_key("neg_credit_killed"):
                    user_obj.setKillReason(instance,errorText("USER_LOGIN","KILLED_BY_NEG_CREDIT_CHECKER",False))
                    
                instance_info["neg_credit_killed"] = True                   
                user_obj.getTypeObj().killInstance(instance)
    
    
    def __killedCheck(self, user_obj):
        """
            check and re-kill users that has been killed previously
        """
        for instance in xrange(1,user_obj.instances+1):
            instance_info = user_obj.getInstanceInfo(instance)
            if instance_info.has_key("killed"):
                if instance_info.has_key("seen_by_killed_checker"):
                    toLog("Killed Checker Found User:Instance %s:%s Info:%s"%(user_obj.getUserID(), instance, instance_info), LOG_ERROR)
                    instance_info["seen_by_killed_checker"] += 1
                    user_obj.getTypeObj().killInstance(instance)
                else:
                    instance_info["seen_by_killed_checker"] = 0 
        
################################################
    def __forceLogoutUser(self,user_obj,instance,kill_reason,no_commit=False):
        """
            force logout "instance" of "user_obj"
            This is done by creating a fake ras_msg and send it to appropiate logout method
        """
        ras_msg=self.__createForceLogoutRasMsg(user_obj,instance)
        method=self.__populateRasMsg(user_obj,instance,ras_msg)
        if method==None:
            toLog("Don't know how to force logout user %s instance %s"%(self.user_obj.getUserID(),instance),LOG_ERROR|LOG_DEBUG)
            return
        user_obj.setKillReason(instance,kill_reason)
        
        if no_commit:
            ras_msg["no_commit"]=True
            
        return apply(method,[ras_msg])

    def __createForceLogoutRasMsg(self,user_obj,instance):
        instance_info=user_obj.getInstanceInfo(instance)
        ras_msg=RasMsg(None,None,ras_main.getLoader().getRasByID(instance_info["ras_id"]))
        return ras_msg
    
    def __populateRasMsg(self,user_obj,instance,ras_msg):
        """
            should set necessary ras_msg attribute and return the logout method
        """
        instance_info=user_obj.getInstanceInfo(instance)
        ras_msg["unique_id"]=instance_info["unique_id"]
        ras_msg[instance_info["unique_id"]]=instance_info["unique_id_val"]
        ras_msg["user_id"]=user_obj.getUserID()
        if user_obj.isNormalUser():
            
            if user_obj.getTypeObj().isPersistentLanClient(instance):
                ras_msg.setAction("PERSISTENT_LAN_STOP")
                return self.persistentLanStop
            else:
                ras_msg["username"]=user_obj.getInstanceInfo(instance)["attrs"]["username"]
                ras_msg.setAction("INTERNET_STOP")
                return self.internetStop

        elif user_obj.isVoIPUser():
            ras_msg["voip_username"]=user_obj.getInstanceInfo(instance)["attrs"]["voip_username"]
            ras_msg.setAction("VOIP_STOP")
            return self.voipStop
#############################################
    def clearUser(self,user_id, ras_id, unique_id, kill_reason, no_commit = True):
        """
            clear instance of user from online
            if no_commit is true no credit is deducted from user
        """
        user_obj = None

        self.loading_user.loadingStart(user_id)
        try:
            user_obj, instance = self.__getUserAndInstance(user_id, ras_id, unique_id)
            self.__forceLogoutUser(user_obj,instance,kill_reason,no_commit)
        finally:
            self.loading_user.loadingEnd(user_id)

        if user_obj != None:
            getLogConsole().log(user_obj.getUserRepr(), 
                                "Clear User",
                                [("Ras", ras_main.getLoader().getRasByID(ras_id).getRasIP()),
                                ("ID", unique_id),
                                ("Kill Reason", kill_reason)
                                ])


    def killUser(self,user_id, ras_id, unique_id, kill_reason):
        user_obj = None

        self.loading_user.loadingStart(user_id)
        try:
            user_obj, instance = self.__getUserAndInstance(user_id, ras_id, unique_id)
            user_obj.setKillReason(instance,kill_reason)
            user_obj.getTypeObj().killInstance(instance)
        finally:
            self.loading_user.loadingEnd(user_id)


        if user_obj != None:
            getLogConsole().log(user_obj.getUserRepr(), 
                                "Kill User",
                                [("Ras", ras_main.getLoader().getRasByID(ras_id).getRasIP()),
                                ("ID", unique_id),
                                ("Kill Reason", kill_reason)
                                ])

    def killAllUsers(self, kill_or_clear, kill_reason):
        """
            Kill all online users
            kill_or_clear(boolean): if set to true, kill the users, else, clear the users
        """
        for user_id in self.user_onlines.keys():
            self.loading_user.loadingStart(user_id)
            try:
                try:
                    user_obj=self.user_onlines[user_id]
                except KeyError: #he's no longer online
                    continue
                    
                for instance in xrange(user_obj.instances, 0, -1): #prevent from instance shifts
                    try:
                        if kill_or_clear:
                            user_obj.setKillReason(instance,kill_reason)
                            user_obj.getTypeObj().killInstance(instance)
                        else:
                            self.__forceLogoutUser(user_obj,instance,kill_reason,False)
                    except:
                        logException(LOG_DEBUG)
            finally:
                self.loading_user.loadingEnd(user_id)

    def __getUserAndInstance(self, user_id, ras_id, unique_id):
        user_obj=user_main.getOnline().getUserObjByUniqueID(ras_id,unique_id)
        if user_obj==None or user_obj.getUserID()!=user_id:
            raise GeneralException(errorText("GENERAL","NOT_ONLINE")%(user_id,ras_id,unique_id))

        instance=user_obj.getInstanceFromUniqueID(ras_id,unique_id)
        return (user_obj, instance)
    
#############################################
    def internetAuthenticate(self,ras_msg):
        self.__checkDuplicateOnline(ras_msg)

        loaded_user=user_main.getUserPool().getUserByNormalUsername(ras_msg["username"],True)
        self.loading_user.loadingStart(loaded_user.getUserID())
        try:
            user_obj=None
            try:
                user_obj=self.getUserObj(loaded_user.getUserID())

                if user_obj==None:
                    user_obj=self.__loadUserObj(loaded_user,"Normal")
                elif not user_obj.isNormalUser():
                    raise GeneralException(errorText("USER_LOGIN","CANT_USE_MORE_THAN_ONE_SERVICE"))
                    
                user_obj.login(ras_msg)
                self.__authSuccessfull(user_obj,ras_msg)
            except:
                if user_obj==None or user_obj.instances==0:
                    loaded_user.setOnlineFlag(False)
                raise
        finally:
            self.loading_user.loadingEnd(loaded_user.getUserID())
            
    def __authSuccessfull(self,user_obj,ras_msg):
        """
            add user to online dic      
        """
        self.__addToOnlines(user_obj)
        if ras_msg.hasAttr("start_accounting"):
            self.recalcNextUserEvent(user_obj.getUserID(),user_obj.instances>1)
############################################
    def internetStop(self,ras_msg):
        pre_user_obj=self.getUserObjByUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
        if pre_user_obj==None:
            toLog("Internet Stop called while user %s is not online for ras_id: %s unique_id_value: %s"%(ras_msg["username"],ras_msg.getRasID(),ras_msg.getUniqueIDValue()),LOG_ERROR)
            return

        self.loading_user.loadingStart(pre_user_obj.getUserID())
        try:
            user_obj=self.getUserObj(pre_user_obj.getUserID()) #make sure he didn't log out yet, inside lock
            if user_obj==None:
                toLog("Got internet stop for user %s, but he's not online"%ras_msg["username"],LOG_DEBUG)
                return
                
            instance=user_obj.getInstanceFromRasMsg(ras_msg)
            if instance==None:
                toLog(errorText("USER","CANT_FIND_INSTANCE")%(user_obj.getUserID(),ras_msg.getRasID(),ras_msg.getUniqueIDValue()),LOG_DEBUG)
                return

            accounting_started = user_obj.accountingStarted(instance)
            global_unique_id = user_obj.getGlobalUniqueID(instance)

            used_credit=user_obj.logout(instance,ras_msg)
            self.__logoutRecalcEvent(user_obj, global_unique_id, accounting_started)
        finally:
            self.loading_user.loadingEnd(pre_user_obj.getUserID())


    def __logoutRecalcEvent(self,user_obj, global_unique_id, accounting_started):
        """
            accounting_started(bool): is start accounting received for this instance of this user?
        """
        self.__removeFromRasOnlines(global_unique_id)
        
        if user_obj.instances==0:
            self.__removeFromUserOnlines(user_obj)
            if accounting_started:
                self.__removePrevUserEvent(user_obj.getUserID())

            user_obj.getLoadedUser().setOnlineFlag(False)
            user_main.getUserPool().userChanged(user_obj.getUserID()) 
                
        else:
            if accounting_started:
                self.recalcNextUserEvent(user_obj.getUserID(),True)

#########################################################
    def persistentLanAuthenticate(self,ras_msg):
        self.__checkDuplicateOnline(ras_msg)
                
        loaded_user=user_main.getUserPool().getUserByID(ras_msg["user_id"],True)
        self.loading_user.loadingStart(loaded_user.getUserID())
        try:
            user_obj=None
            try:
                user_obj=self.getUserObj(loaded_user.getUserID())
                if user_obj==None:
                    user_obj=self.__loadUserObj(loaded_user,"Normal")
                elif not user_obj.isNormalUser():
                    raise GeneralException(errorText("USER_LOGIN","CANT_USE_MORE_THAN_ONE_SERVICE"))

                user_obj.login(ras_msg)
                self.__authSuccessfull(user_obj,ras_msg)
            except:
                if user_obj==None or user_obj.instances==0:
                    loaded_user.setOnlineFlag(False)
                raise
        finally:
            self.loading_user.loadingEnd(loaded_user.getUserID())

    def persistentLanStop(self,ras_msg):
        loaded_user=user_main.getUserPool().getUserByID(ras_msg["user_id"])
        self.loading_user.loadingStart(loaded_user.getUserID())
        try:
            user_obj=self.getUserObj(loaded_user.getUserID())
            if user_obj==None:
                toLog("Got persistent lan stop for user %s, but he's not online"%ras_msg["user_id"],LOG_DEBUG)
                return
            instance=user_obj.getInstanceFromRasMsg(ras_msg)
            if instance==None:
                toLog(errorText("USER","CANT_FIND_INSTANCE")%(loaded_user.getUserID(),ras_msg.getRasID(),ras_msg.getUniqueIDValue()))
                return

            global_unique_id = user_obj.getGlobalUniqueID(instance)
            accounting_started = user_obj.accountingStarted(instance)

            user_credit=user_obj.logout(instance,ras_msg)
            self.__logoutRecalcEvent(user_obj, global_unique_id, accounting_started)
        finally:
            self.loading_user.loadingEnd(loaded_user.getUserID())
#########################################################
    def voipAuthenticate(self,ras_msg):
        if ras_msg.hasAttr("h323_pre_authentication") or ras_msg.hasAttr("pre_authentication"):
            loaded_user=user_main.getUserPool().getUserByCallerID(ras_msg["caller_id"])
        else:
            loaded_user=user_main.getUserPool().getUserByVoIPUsername(ras_msg["voip_username"])
            
        self.loading_user.loadingStart(loaded_user.getUserID())
        try:
            user_obj=self.getUserObj(loaded_user.getUserID())
            if user_obj!=None and not user_obj.isVoIPUser():
                raise GeneralException(errorText("USER_LOGIN","CANT_USE_MORE_THAN_ONE_SERVICE"))

        finally:
            self.loading_user.loadingEnd(loaded_user.getUserID())
            
        user_obj=self.__loadUserObj(loaded_user,"VoIP") #always test login on new user_obj, 
                                                        #and trash it after test
        ras_msg["no_commit"] = True
        user_obj.login(ras_msg) #test login

        return True

    def voipAuthorize(self, ras_msg):
        self.__checkDuplicateOnline(ras_msg)

        loaded_user=user_main.getUserPool().getUserByVoIPUsername(ras_msg["voip_username"], True)

        self.loading_user.loadingStart(loaded_user.getUserID())
        try:
            user_obj=None
            try:
                user_obj=self.getUserObj(loaded_user.getUserID())

                if user_obj==None:
                    user_obj=self.__loadUserObj(loaded_user,"VoIP")
                elif not user_obj.isVoIPUser():
                    raise GeneralException(errorText("USER_LOGIN","CANT_USE_MORE_THAN_ONE_SERVICE"))
                    
                user_obj.login(ras_msg)
                self.__authSuccessfull(user_obj,ras_msg)
            except:
                if user_obj==None or user_obj.instances==0:
                    loaded_user.setOnlineFlag(False)
                raise
        finally:
            self.loading_user.loadingEnd(loaded_user.getUserID())


    def voipStop(self,ras_msg):
        pre_user_obj=self.getUserObjByUniqueID(ras_msg.getRasID(),ras_msg.getUniqueIDValue())
        if pre_user_obj==None:
            toLog("VoIP Stop called while user %s is not online for ras_id: %s unique_id_value: %s"%(ras_msg["voip_username"],ras_msg.getRasID(),ras_msg.getUniqueIDValue()),LOG_ERROR)
            return -1

        self.loading_user.loadingStart(pre_user_obj.getUserID())
        try:
            user_obj=self.getUserObj(pre_user_obj.getUserID())
            if user_obj==None:
                toLog("Got VoIP stop for user %s, but he's not online"%ras_msg["voip_username"],LOG_DEBUG)
                return -1
            instance=user_obj.getInstanceFromRasMsg(ras_msg)
            if instance==None:
                toLog(errorText("USER","CANT_FIND_INSTANCE")%(user_obj.getUserID(),ras_msg.getRasID(),ras_msg.getUniqueIDValue()),LOG_DEBUG)
                return -1

            global_unique_id = user_obj.getGlobalUniqueID(instance)
            accounting_started = user_obj.accountingStarted(instance)

            used_credit=user_obj.logout(instance,ras_msg)
            self.__logoutRecalcEvent(user_obj, global_unique_id, accounting_started)
        finally:
            self.loading_user.loadingEnd(pre_user_obj.getUserID())
        
        return used_credit
        
class OnlineCheckPeriodicEvent(periodic_events.PeriodicEvent):
    def __init__(self):
        periodic_events.PeriodicEvent.__init__(self,"Online Check",defs.CHECK_ONLINE_INTERVAL,[],0)

    def run(self):
        user_main.getOnline().checkOnlines()

        
