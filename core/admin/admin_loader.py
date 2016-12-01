from core.db import db_main
from core.admin import admin_lock,admin,perm_loader
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

class AdminLoader:
    def __init__(self):
        self.admins_id={}
        self.admins_name={}
        
    def __getitem__(self,key):
        if isInt(key):
            return self.getAdminByID(key)
        else:
            return self.getAdminByName(key)
    
    def __iter__(self):
        return self.admins_id.iterkeys()

    def getAdminByID(self,admin_id):
        try:
            return self.admins_id[admin_id]
        except KeyError:
            raise GeneralException(errorText("ADMIN","ADMIN_ID_INVALID")%admin_id)

    def getAdminByName(self,admin_name):
        try:
            return self.admins_name[admin_name]
        except KeyError:
            raise GeneralException(errorText("ADMIN","ADMIN_USERNAME_INVALID")%admin_name)
    
    
    def checkAdminID(self,admin_id):
        if not isInt(admin_id):
            raise GeneralException(errorText("ADMIN","ADMIN_ID_INVALID")%admin_id)
        
        if not self.admins_id.has_key(admin_id):
            raise GeneralException(errorText("ADMIN","ADMIN_ID_INVALID")%admin_id)
    
    def checkAdminName(self,admin_name):
        if not self.admins_name.has_key(admin_name):
            raise GeneralException(errorText("ADMIN","ADMIN_USERNAME_INVALID")%admin_name)
    
    
    def adminNameAvailable(self,admin_name):
        """
            check if "admin_name" is available for adding.
            return 1 if it's available(no other admin has this name)
            return 0 if it's not available(another admin has this name)
        """
        return not self.admins_name.has_key(admin_name)


    def getAllUsernames(self):
        """
            return a list of all admin usernames
        """
        return self.admins_name.keys()
        
    def loadAdmin(self,admin_id):
        """
            load admin with id "admin_id" and put it in internally used dic
        """
        admin_obj=self.__loadAdminObj(admin_id)
        self.admins_id[admin_id]=admin_obj
        self.admins_name[admin_obj.username]=admin_obj
        
    def loadAdminByName(self,username):
        """
            load admin with username "username" by calling self.loadAdmin
            NOTE: admin must be previously loaded
        """
        admin_id=self.getAdminByName(username).getAdminID()
        self.loadAdmin(admin_id)
        
    def loadAllAdmins(self):
        """
            load all of admins available in "admin" table
        """
        admin_ids=self.__getAllAdminIDs()
        map(self.loadAdmin,admin_ids)
        
    def unLoadAdmin(self, admin_id):
        """
            unload admin with id "admin_id"     
        """
        admin_obj = self.getAdminByID(admin_id)
        del(self.admins_id[admin_id])
        del(self.admins_name[admin_obj.getUsername()])

    def __loadAdminObj(self,admin_id):
        """
            get admin information from db(including basic info,perms and locks), 
            Create an object of these information, and return the object
        """
        admin_info=self.__getAdminBasicInfoDB(admin_id)
        admin_obj=self.__createAdminObj(admin_info)
        admin_perms=perm_loader.getLoader().getPermsOfAdmin(admin_obj)
        admin_locks=self.__getAdminLocks(admin_id)
        admin_obj.setPerms(admin_perms)
        admin_obj.setLocks(admin_locks)
        return admin_obj
        
    def __getAdminBasicInfoDB(self,admin_id):
        """
            return dic of admin basic information from "admin" table
        """
        try:
            return db_main.getHandle().get("admins","admin_id=%s"%admin_id)[0]
        except:
            logException(LOG_ERROR,"AdminLoader.__getAdminBasicInfoDB")
            raise

    def __createAdminObj(self,admin_info):
        """
            create and return an admin object from "admin_info"
            "admin_info" is a dic that returned from db query
        """
        return admin.Admin(admin_info["username"],admin_info["password"],admin_info["name"],admin_info["comment"],
                           admin_info["admin_id"],admin_info["deposit"],admin_info["creator_id"],
                           admin_info["due"])
    
    def __getAdminLocks(self,admin_id):
        """
            retrieve locks of admin with id "admin_id" and return a list of AdminLock instances 
        """
        locks=self.__getAdminLocksDB(admin_id)
        return map(self.__createAdminLockObj,locks)

    def __createAdminLockObj(self,lock_dic):
        """
            create an AdminLock object from "lock_dic"
        """
        return admin_lock.AdminLock(lock_dic["lock_id"],lock_dic["locker_admin_id"],lock_dic["admin_id"],lock_dic["reason"])

    def __getAdminLocksDB(self,admin_id):
        """
            get admin locks from "admin_locks" table.
        """
        return db_main.getHandle().get("admin_locks","admin_id=%s"%admin_id)

    
    def __getAllAdminIDs(self):
        """
            return a list of all admin_ids from "admins" table
        """
        admin_ids=db_main.getHandle().get("admins","true",0,-1,"",["admin_id"])
        return [m["admin_id"] for m in admin_ids]
