from core.group import group_main
from core.db import db_main,ibs_db
from core.lib import password_lib
from core.ibs_exceptions import *
from core.lib.general import *
from core.charge import charge_main
from core.admin import admin_main
from core.lib.date import *
import re
import threading
import copy
import time

class Admin:
    def __init__(self,username,password,name,comment,admin_id,deposit,creator_id,due):
        self.username=username
        self.password=password_lib.Password(password.strip())
        self.name=name
        self.comment=comment
        self.admin_id=integer(admin_id)
        self.deposit=integer(deposit)
        self.creator_id=integer(creator_id)
        self.due=due
        self.deposit_lock=threading.RLock()
        self.activity_status = {"last_request_ip":"--", "last_activity":0.0}

    def getAdminActivity(self):
        return self.activity_status

    def getAdminID(self):
        return self.admin_id

    def getUsername(self):
        return self.username

    def getAdminInfo(self,date_type):
        """
            return a dictionary of admin properties
            normally contains username,name,comment,admin_id,deposit,creator_id
        """
        return {"username":self.username,
                "name":self.name,
                "comment":self.comment,
                "admin_id":self.admin_id,
                "deposit":self.deposit,
                "creator_id":self.creator_id,
                "creator":admin_main.getLoader().getAdminByID(self.creator_id).getUsername(),
                "locks":map(lambda lock_obj:lock_obj.getLockInfo(),self.locks),
                "last_request_ip":self.activity_status["last_request_ip"],
                "last_activity":self.__getAdminLastActivity(date_type),
                "online_status":self.__getOnlineStatus()
                }
    
    def __getOnlineStatus(self):
	"""
	    return True if admin had an activity in last 15 minutes
	"""
        if time.time() - self.activity_status["last_activity"] > 900: # more than 15 min
            return False
	    
        return True
    
    def __getAdminLastActivity(self,date_type):
	"""
	    return admin last activity in epoch time
	    0 if admin hadn't any request from start of IBSng
	"""
        if self.activity_status["last_activity"]:
            return AbsDateFromEpoch(self.activity_status["last_activity"]).getDate(date_type)
        
        return 0

    def setLocks(self,locks):
        """
            locks is a list of admin_lock instances
        """
        self.locks=locks

    def getLocks(self):
        return self.locks
        
    def setPerms(self,perms):
        """
            calls when loading an admin to set its perms
            perms is a dic of {perm_name:perm_obj}
        """
        self.perms=perms

    def getPerms(self):
        return self.perms

    def checkPerm(self,perm_name,*args):
        """
            check if this admin has permission with name "perm_name" and it's acceptable with
            "args", permissions raise a PermissionException on access denied conditions
        """
        try:
            return apply(self.perms[perm_name].check,args)
        except KeyError:
            raise PermissionException(errorText("PERMISSION","DONT_HAVE_PERMISSION"))
        except IndexError:
            raise PermissionException(errorText("PERMISSION","DONT_HAVE_PERMISSION"))


    def hasPerm(self,perm_name):
        """
            check if this admin --JUST HAS-- permission "perm_name" regardless of enviroment and 
            permission values. To check a permission use checkPerm instead.
        """
        return self.perms.has_key(perm_name)

    def canDo(self,perm_name,*args):
        """
            check if this admin can do "perm_name"
            "can do" is a positive statement, so "perm_name" can't be a negative (restrictive) 
            permission such as LIMIT_LOGIN_ADDR.
            raise a PermissionException if admin can't do it
        """
        if self.isGod():
            return 
        apply(self.checkPerm,[perm_name]+list(args))
        

    def isGod(self):
        return self.hasPerm("GOD")
        
    ##########################
    def consumeDeposit(self,credit): 
        """
            consume admin deposit in loaded instance
        """
        return self.changeDeposit(credit*-1)
    
    def changeDeposit(self,deposit_change):
        """
            change deposit in amount of deposit_change
        """
        self.deposit_lock.acquire()
        try:
            self.deposit+=deposit_change
        finally:
            self.deposit_lock.release()
        return self.deposit

    #############################

    def checkPass(self,password):
        """
            check if "password" is correct for this admin 
            password(Password instance): password to check
        """
        if not self.__checkPass(password):
            raise GeneralException(errorText("ADMIN_LOGIN","INCORRECT_PASSWORD"))

    def __checkPass(self,password):
        """
            check if "password" is correct for this admin 
            password(Password instance): password to check
            return 1 if it's correct and 0 if it's not
        """
        if password == self.password:
            return 1
        else:
            return 0


    def isAuthorizedFromAddr(self,remote_addr):
        if self.hasPerm("LIMIT LOGIN ADDR"):
            self.checkPerm("LIMIT LOGIN ADDR",remote_addr)


    def canLogin(self,remote_addr): 
        """
            check if this admin can login to server from remote address "remoteaddr"
        """
        self.isAuthorizedFromAddr(remote_addr)
        self.__checkIfLocked()
        
    def isLocked(self):
        """
            return False if admin is not locked
            return True if this admin is locked
        """
        return len(self.locks)!=0
        
    def __checkIfLocked(self):
        """
            check if this admin is locked, raise a LoginException if it's locked
            so admin can't login to IBS
        """
        if self.isLocked():
            raise LoginException(errorText("ADMIN_LOGIN","ADMIN_LOCKED"))

    #############################
    def checkServerAuth(self, auth_pass, remote_addr):
        self.__updateActivity(remote_addr, long(time.time()))
	self.checkAuth(auth_pass, remote_addr)

    def __updateActivity(self, last_ip, last_update):
        self.activity_status["last_request_ip"], self.activity_status["last_activity"] = last_ip, last_update

    ##############################

    def checkAuth(self,auth_pass,remote_addr):
        """
            authenticate admin, raise an exception if access is denied
        """
        self.checkPass(auth_pass)
        self.canLogin(remote_addr)

    def canUseCharge(self,charge_name):
        """
            return True if admin can use charge with name "charge_name"
        """
        if charge_main.getLoader().getChargeByName(charge_name).isVisibleToAll() or self.isGod() or self.hasPerm("ACCESS ALL CHARGES"):
            return True

        if self.hasPerm("CHARGE ACCESS"):
            try:
                self.checkPerm("CHARGE ACCESS",charge_name)
                return True
            except PermissionException:
                return False

        return False

    def canUseGroup(self,group_name):
        """
            return True if admin can use group with name "group_name"
        """
        if self.isGod() or self.hasPerm("ACCESS ALL GROUPS"):
            return True
        
        if group_main.getLoader().getGroupByName(group_name).getOwnerID() == self.getAdminID():
            return True

        if self.hasPerm("GROUP ACCESS"):
            try:
                self.checkPerm("GROUP ACCESS",group_name)
                return True
            except PermissionException:
                return False
        return False

    def canAccessUser(self,loaded_user):
        """
            raise an PermissionException if admin can not access and get information of  user loaded in "loaded_user"
            or return if admin has access to the user. Checking is done with admin permission GET USER INFORMATION
        """
        
        self.canDo("GET USER INFORMATION",loaded_user)

    def canChangeUser(self,loaded_user):
        """
            raise an PermissionException if admin can not change user loaded in "loaded_user"
            Admin should have CHANGE_USER_ATTRS permission to be able to change users
        """
        self.canDo("CHANGE USER ATTRIBUTES",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())

    def canChangeNormalAttrs(self,loaded_user):
        """
            raise an PermissionException if admin can not change normal attributes of user loaded in "loaded_user"
            if loaded_user is None, it will check if admin have enough permissions, useful for checking group attribute chnges
            Admin should have CHANGE_NORMAL_USER_ATTRS permission to be able to change users
        """
        if loaded_user==None:
            self.canDo("CHANGE NORMAL USER ATTRIBUTES",None,None)
        else:
            self.canDo("CHANGE NORMAL USER ATTRIBUTES",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())

    def canChangeVoIPAttrs(self,loaded_user):
        """
            raise an PermissionException if admin can not change voip attributes of user loaded in "loaded_user"
            if loaded_user is None, it will check if admin have enough permissions, useful for checking group attribute chnges
            Admin should have CHANGE_VOIP_USER_ATTRS permission to be able to change users
        """
        if loaded_user==None:
            self.canDo("CHANGE VOIP USER ATTRIBUTES",None,None)
        else:
            self.canDo("CHANGE VOIP USER ATTRIBUTES",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())

