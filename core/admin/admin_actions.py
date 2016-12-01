import string
import re

from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main,ibs_db,ibs_query
from core.lib.general import *
from core.admin import admin_main
from core.lib import iplib
from core.ias import ias_main
from core.user import user_main
from core.group import group_main


class AdminActions:
    def addNewAdmin(self,username,password,name,comment,creator_id):


        self.__addNewAdminCheckInput(username,password,name,comment,creator_id)
        admin_id=self.__getNewAdminID()
        self.__addNewAdminDB(admin_id,username,password.getMd5Crypt(),name,comment,creator_id)
        self.__getAdminLoader().loadAdmin(admin_id)
        return admin_id
    
    
    def __getNewAdminID(self):
        """
            return a new unique admin id
        """
        return db_main.getHandle().seqNextVal("admins_id_seq")


    def __addNewAdminDB(self,admin_id,username,password,name,comment,creator_id):
        """
            insert the new admin information into admins table
        """
        query = self.__addNewAdminQuery(admin_id,username,password,name,comment,creator_id)
        query += self.__addNewAdminIASQuery(username, creator_id)
        db_main.getHandle().transactionQuery(query)

    def __addNewAdminIASQuery(self, username, creator_id):
        creator_username=admin_main.getLoader().getAdminByID(creator_id).getUsername()
        return ias_main.getActionsManager().logEvent("ADD_ADMIN",creator_username,0,username)
        
    def __addNewAdminQuery(self,admin_id,username,password,name,comment,creator_id):
        """
            return query to insert new admin
        """
        return ibs_db.createInsertQuery("admins",{"admin_id":admin_id,
                                                  "username":dbText(username),
                                                  "password":dbText(password),
                                                  "name":dbText(name.strip()),
                                                  "comment":dbText(comment.strip()),
                                                  "creator_id":dbText(creator_id),
                                                  "deposit":0,
                                                  "due":0
                                                  })

    def __addNewAdminCheckInput(self,username,password,name,comment,creator_id):
        if not self.__getAdminLoader().adminNameAvailable(username):
            raise GeneralException(errorText("ADMIN","ADMIN_USERNAME_TAKEN")%username)
            
        if self.__checkAdminUserChars(username) != 1:
            raise GeneralException(errorText("ADMIN","BAD_USERNAME")%username)

        if password.checkPasswordChars() != 1:
            raise GeneralException(errorText("ADMIN","BAD_PASSWORD"))
        
        self.__getAdminLoader().checkAdminID(creator_id)

    def __checkAdminUserChars(self,username):
        if not len(username) or username[0] not in string.letters:                 
            return 0
        if re.search("[^A-Za-z0-9_]",username) != None:                 
            return 0
        return 1



    ######################
    def changePassword(self,username,password):
        """
            change admin password
            username(string): admin username
            password(password instance): New Password instance
        """
        self.__changePasswordCheckInput(username,password)      
        self.__changePasswordDB(username,password.getMd5Crypt())
        self.__getAdminLoader().loadAdminByName(username)
    
    def __changePasswordCheckInput(self,username,password):
        self.__getAdminLoader().checkAdminName(username)

        if password.checkPasswordChars() != 1:
            raise GeneralException(errorText("ADMIN","BAD_PASSWORD"))

    def __changePasswordDB(self,username,password):
        db_main.getHandle().update("admins",
                      {"password":dbText(password)},
                      "username=%s"%dbText(username)
                     )
    
    
    #####################

    def __getAdminLoader(self):
        return admin_main.getLoader()

    ####################
    
    def updateInfo(self,admin_username,name,comment):
        self.__updateInfoCheckInput(admin_username,name,comment)
        admin_obj=self.__getAdminLoader().getAdminByName(admin_username)
        self.__updateInfoDB(admin_obj,name,comment)
        self.__getAdminLoader().loadAdmin(admin_obj.getAdminID())
    
    def __updateInfoDB(self,admin_obj,name,comment):
        query=self.__updateInfoQuery(admin_obj.getAdminID(),name,comment)
        db_main.getHandle().transactionQuery(query)

    def __updateInfoQuery(self,admin_id,name,comment):
        return ibs_db.createUpdateQuery("admins",{"name":dbText(name),
                                                  "comment":dbText(comment)},"admin_id=%s"%admin_id)

#    def __updateDepositRatioQuery(self,admin_id,deposit_ratio):
#       return ibs_db.createUpdateQuery("admins",{"deposit_ratio":integer(deposit_ratio)},"admin_id=%s"%admin_id)

    def __updateInfoCheckInput(self,admin_username,name,comment):
        self.__getAdminLoader().checkAdminName(admin_username)

    ######################
    def consumeDeposit(self,admin_username,deposit,need_query=True):
        """
            consume "deposit" amount of deposit from admin with username "admin_username" and return 
            the query to commit it into database. 
            The caller must take care of readding deposit, if commit of query into database failed.
            This method may raise exception in case of admin doesn't have enough deposit. In such cases caller
            doesn't need to readd deposit!
            need_query(boolean): tell if we need query to be returned, useful when query failed and we want to readd
                                 deposit to in memory object
        """
        admin_obj=self.__getAdminLoader().getAdminByName(admin_username)
        new_deposit=admin_obj.consumeDeposit(deposit)
        try:
            if new_deposit<0:
                admin_obj.canDo("NO DEPOSIT LIMIT")
        except PermissionException: #negative deposit not allowed!
            admin_obj.consumeDeposit(-1*deposit) 
            raise GeneralException(errorText("ADMIN","NEGATIVE_DEPOSIT_NOT_ALLOWED")%deposit)
        
        if need_query:
            return self.consumeDepositQuery(admin_obj.getAdminID(),deposit)
        
    def consumeDepositQuery(self,admin_id,deposit):
        return ibs_db.createUpdateQuery("admins",
                                        {"deposit":"deposit - %s"%deposit},
                                        "admin_id=%s"%admin_id)

        
    ##############################
    def changeDeposit(self,changer_admin_name,admin_name,deposit_change,comment,remote_addr):
        """
            change deposit of admin "admin_name"
            
            changer_admin_name(str): name of admin, changing the deposit
            admin_name(str): name of admin that deposit changes
            deposit_change(float): amount of change
            comment(str):
            remote_addr(str): remote ip address of deposit changer
        """         
        self.__changeDepositCheckInput(changer_admin_name,admin_name,deposit_change,comment,remote_addr)
        changer_admin_obj=self.__getAdminLoader().getAdminByName(changer_admin_name)
        admin_obj=self.__getAdminLoader().getAdminByName(admin_name)
        query=""
        query+=admin_main.getDepositChangeLogActions().logDepositChangeQuery(changer_admin_obj.getAdminID(),
                                                                                 admin_obj.getAdminID(),
                                                                                 deposit_change,
                                                                                 comment,
                                                                                 remote_addr)
        query+=self.__changeDepositQuery(admin_obj.getAdminID(),deposit_change)
        query+=ias_main.getActionsManager().logEvent("CHANGE_DEPOSIT",changer_admin_name,deposit_change,admin_name)
        db_main.getHandle().transactionQuery(query)
        admin_obj.changeDeposit(deposit_change)


    def __changeDepositCheckInput(self,changer_admin_name,admin_name,deposit_change,comment,remote_addr):
        self.__getAdminLoader().checkAdminName(changer_admin_name)
        self.__getAdminLoader().checkAdminName(admin_name)
        
        if not isFloat(deposit_change):
            raise GeneralException(errorText("ADMIN","DEPOSIT_SHOULD_BE_FLOAT"))
        
        if not iplib.checkIPAddr(remote_addr):
            raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%remote_addr)

    
    def __changeDepositQuery(self,admin_id,deposit_change):
        return "update admins set deposit = deposit + %s where admin_id = %s ; "%(deposit_change,admin_id)

    ############################################
    def deleteAdmin(self, deleter_admin, admin_name):
        self.__deleteAdminCheckInput(deleter_admin, admin_name)
        admin_obj = self.__getAdminLoader().getAdminByName(admin_name)
        self.__deleteAdminDB(deleter_admin, admin_obj)
        self.__doPostDeleteAdmin(admin_obj)
        self.__getAdminLoader().unLoadAdmin(admin_obj.getAdminID())

    def __doPostDeleteAdmin(self, admin_obj):
        self.__reloadGroups(admin_obj.getAdminID())
        self.__reloadUsers(admin_obj.getAdminID())
        self.__reloadAdmins(admin_obj.getAdminID())
        
    def __reloadUsers(self, admin_id):
        """
            reload users whom owner is deleted admin
        """
        user_main.getUserPool().reloadUsersWithFilter(lambda loaded_user:loaded_user.getBasicUser().getOwnerObj().getAdminID()==admin_id)

    def __reloadGroups(self, admin_id):
        """
            reload groups with owner of deleted admin
        """
        all_groups=group_main.getLoader().getAllGroupNames()
        for group_name in all_groups:
            try:
                group_obj=group_main.getLoader().getGroupByName(group_name)
            except GeneralException:
                pass

            if group_obj.getOwnerID()==admin_id:        
                group_main.getLoader().loadGroupByName(group_name)

    def __reloadAdmins(self, admin_id):
        """
            reload admins whom creator or locker is deleted admin
        """
        for admin_username in admin_main.getLoader().getAllUsernames():
            try:
                admin_obj=admin_main.getLoader().getAdminByName(admin_username)
                if admin_obj.creator_id == admin_id:
                    admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
                else:
                    for lock_obj in admin_obj.getLocks():
                        if lock_obj.getLockerID()==admin_id:
                            admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
                            break
            except:
                logException(LOG_DEBUG)
                
    

    def __deleteAdminCheckInput(self, deleter_admin, admin_name):
        self.__getAdminLoader().checkAdminName(admin_name)
        if admin_name == "system":
            raise GeneralException(errorText("ADMIN","CANNOT_DELETE_SYSTEM"))

    def __deleteAdminDB(self, deleter_admin, admin_obj):
        admin_id=admin_obj.getAdminID()
        query_funcs = (self.__deleteAdminLocksQuery, self.__deleteAdminDepositChangesQuery,
                       self.__deleteAdminPermsQuery, self.__deleteAddUserSavesQuery, self.__delAdminUpdateUserOwnersQuery,
                       self.__delAdminUpdateGroupOwnersQuery, self.__delAdminUpdateAdminLockersQuery, self.__delAdminUpdateCreditChangersQuery,
                       self.__delAdminUpdateAdminDepositChangersQuery, self.__delAdminUpdateUserAuditLogAdmins, self.__deleteAdminQuery,
                       self.__delAdminUpdateAdminCreatorsQuery)
        query = ibs_query.IBSQuery()
        for func in query_funcs:
            query += apply(func,(admin_id,))
        query += self.__deleteAdminIASQuery(deleter_admin, admin_obj)
        query.runQuery()

    def __deleteAdminIASQuery(self, deleter_admin, admin_obj):
        return ias_main.getActionsManager().logEvent("DELETE_ADMIN",deleter_admin,admin_obj.deposit,admin_obj.getUsername())
        
    def __deleteAdminQuery(self, admin_id):
        return ibs_db.createDeleteQuery("admins","admin_id = %s"%admin_id)

    def __deleteAdminLocksQuery(self, admin_id):
        return ibs_db.createDeleteQuery("admin_locks","admin_id = %s"%admin_id)

    def __deleteAdminDepositChangesQuery(self, admin_id):
        return ibs_db.createDeleteQuery("admin_deposit_change","to_admin_id = %s"%admin_id)

    def __deleteAdminPermsQuery(self, admin_id):
        return ibs_db.createDeleteQuery("admin_perms","admin_id = %s"%admin_id)

    def __deleteAddUserSavesQuery(self, admin_id):
        return   ibs_db.createDeleteQuery("add_user_save_details","add_user_save_id in \
                    (select add_user_save_id from add_user_saves where admin_id = %s)"%admin_id) + \
                 ibs_db.createDeleteQuery("add_user_saves","admin_id = %s"%admin_id)


    def __delAdminUpdateUserOwnersQuery(self, admin_id):
        return ibs_db.createUpdateQuery("users",{"owner_id":0},"owner_id = %s"%admin_id)        

    def __delAdminUpdateGroupOwnersQuery(self, admin_id):
        return ibs_db.createUpdateQuery("groups",{"owner_id":0},"owner_id = %s"%admin_id)       

    def __delAdminUpdateAdminLockersQuery(self, admin_id):
        return ibs_db.createUpdateQuery("admin_locks",{"locker_admin_id":0},"locker_admin_id = %s"%admin_id)

    def __delAdminUpdateAdminCreatorsQuery(self, admin_id):
        return ibs_db.createUpdateQuery("admins",{"creator_id":0},"creator_id = %s"%admin_id)

    def __delAdminUpdateCreditChangersQuery(self, admin_id):
        return ibs_db.createUpdateQuery("credit_change",{"admin_id":0},"admin_id = %s"%admin_id)

    def __delAdminUpdateAdminDepositChangersQuery(self, admin_id):
        return ibs_db.createUpdateQuery("admin_deposit_change",{"admin_id":0},"admin_id = %s"%admin_id)

    def __delAdminUpdateUserAuditLogAdmins(self, admin_id):
        return ibs_db.createUpdateQuery("user_audit_log",{"admin_id":0},"admin_id = %s"%admin_id)

    ################################################
    def lockAdmin(self, admin_name, reason, locker_admin_name):
        self.__lockAdminCheckInput(admin_name, reason, locker_admin_name)
        admin_obj=self.__getAdminLoader().getAdminByName(admin_name)
        locaker_admin_obj=self.__getAdminLoader().getAdminByName(locker_admin_name)
        self.__lockAdminDB(admin_obj.getAdminID(),reason,locaker_admin_obj.getAdminID())
        self.__getAdminLoader().loadAdmin(admin_obj.getAdminID())

    def __lockAdminCheckInput(self, admin_name, reason, locker_admin_name):
        self.__getAdminLoader().checkAdminName(admin_name)
        self.__getAdminLoader().checkAdminName(locker_admin_name)

    def __lockAdminDB(self, admin_id, reason, locker_admin_id):
        db_main.getHandle().transactionQuery(self.__lockAdminQuery(admin_id, reason, locker_admin_id))
        
    def __lockAdminQuery(self, admin_id, reason, locker_admin_id):
        return ibs_db.createInsertQuery("admin_locks",{"admin_id":admin_id,
                                                       "reason":dbText(reason),
                                                       "locker_admin_id":locker_admin_id,
                                                       "lock_id":"nextval('admin_locks_lock_id_seq')"})
        
    ##################################################
    def unlockAdmin(self, admin_name, lock_id):
        self.__unlockAdminCheckInput(admin_name, lock_id)
        admin_obj=self.__getAdminLoader().getAdminByName(admin_name)
        self.__unlockAdminDB(admin_obj.getAdminID(),lock_id)
        self.__getAdminLoader().loadAdmin(admin_obj.getAdminID())

    def __unlockAdminCheckInput(self, admin_name, lock_id):
        self.__getAdminLoader().checkAdminName(admin_name)
        if not isInt(lock_id):
            raise GeneralException(errorText("ADMIN_ACTIONS","LOCK_ID_SHOULD_BE_INTEGER"))

    def __unlockAdminDB(self, admin_id, lock_id):
        db_main.getHandle().transactionQuery(self.__unlockAdminQuery(admin_id, lock_id))
        
    def __unlockAdminQuery(self, admin_id, lock_id):
        return ibs_db.createDeleteQuery("admin_locks","admin_id=%s and lock_id=%s"%(admin_id,lock_id))
        