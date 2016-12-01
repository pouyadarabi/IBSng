from core.ibs_exceptions import *
from core.lib.general import *
from core.charge import charge_main
from core.db import ibs_db,db_main
from core.db.ibs_query import IBSQuery
from core.errors import errorText
from core.admin import admin_main
from core.lib import password_lib,iplib,report_lib
from core.group import group_main
from core.user import user_main
from core.ras import ras_main
from core.ias import ias_main
import re,time

class UserActions:
#######################################################
    def getLoadedUsersByUserID(self,user_ids, keep_order=False):
        """
            return a list of LoadedUser instances for users with ids "user_ids"
        """
        user_ids=map(lambda x:to_int(x,"user id"),user_ids)
        loaded_users=user_main.getUserPool().getUsersByID(user_ids, keep_order)
        return loaded_users

    def getUserInfoByUserID(self,user_id,date_type):
        """
            return a list of user info dics with user_id in multi string user_id
            return dic is in format {user_id=>user_info dic}
        """
        loaded_users=self.getLoadedUsersByUserID(user_id)
        return self.getUserInfosFromLoadedUsers(loaded_users,date_type)
        
#######################################################
    def getLoadedUsersByNormalUsername(self,normal_usernames):
        """
            return a list of LoadedUser instances for users with normal_usernames "normal_usernames"
        """
        loaded_users=map(user_main.getUserPool().getUserByNormalUsername,normal_usernames)
        return loaded_users
    
    def getUserInfoByNormalUsername(self,normal_username,date_type):
        """
            return a list of user info dics with normal_username in multi string user_id
            return dic is in format {user_id=>user_info dic}
        """
        loaded_users=self.getLoadedUsersByUsername(normal_username)
        return self.getUserInfosFromLoadedUsers(loaded_users,date_type)

#######################################################
    def getLoadedUsersByVoIPUsername(self,voip_usernames):
        """
            return a list of LoadedUser instances for users with voip_usernames "voip_usernames"
        """
        loaded_users=map(user_main.getUserPool().getUserByVoIPUsername,voip_usernames)
        return loaded_users

########################################################

    def insertUserAttrQuery(self,user_id,attr_name,attr_value):
        return ibs_db.createFunctionCallQuery("insert_user_attr",[user_id,dbText(attr_name), dbText(attr_value)])
        
    def updateUserAttrQuery(self,user_id,attr_name,attr_value):
        return ibs_db.createFunctionCallQuery("update_user_attr",[user_id,dbText(attr_name), dbText(attr_value)])

    def deleteUserAttrQuery(self,user_id,attr_name):
        return ibs_db.createFunctionCallQuery("delete_user_attr",[user_id,dbText(attr_name)])

####################################################
    def addNewUsers(self,_count,credit,owner_name,creator_name,group_name,remote_address,credit_change_comment,user_ids=None):
        """
            add _count of users to system
            _count(int): postive integer
            credit(float): initial credit of users
            owner_name(str): valid admin name, that is owner of created users
            creator_name(str): valid admin name, that created users
            group_name(str): valid group name these users belongs to
            remote_address(str): ip address that admin used to create these users
            credit_change_comment(str): 
            user_ids(None or list of int): list of user_ids to use. if set to None
                                           generate new ids
                    
        """
        self.__addNewUsersCheckInput(_count,credit,owner_name,creator_name,group_name,remote_address,credit_change_comment,user_ids)
        admin_consumed_credit=credit*_count
        ibs_query=IBSQuery()
        ibs_query+=admin_main.getActionManager().consumeDeposit(creator_name,admin_consumed_credit)
        try:
            user_ids=self.addNewUsersQuery(_count,credit,owner_name,group_name,ibs_query,user_ids)
            creator_admin_obj=admin_main.getLoader().getAdminByName(creator_name)
            ibs_query+=user_main.getCreditChangeLogActions().logCreditChangeQuery("ADD_USER",creator_admin_obj.getAdminID(),user_ids,credit,\
                                        admin_consumed_credit,remote_address,credit_change_comment)
            self.__addNewUserIASQuery(ibs_query,creator_name,credit,user_ids)

            ibs_query.runQuery()
            return user_ids
        except:
            admin_main.getActionManager().consumeDeposit(creator_name,-1*admin_consumed_credit,False) #re-add deposit to admin
            raise

    

    def __addNewUsersCheckInput(self,_count,credit,owner_name,creator_name,group_name,remote_address,credit_change_comment,user_ids):
        if not isInt(_count) or _count<=0:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_USER_COUNT")%_count)
        
        if not isFloat(credit):
            raise GeneralException(errorText("USER_ACTIONS","CREDIT_NOT_FLOAT"))

        if credit<0:
            raise GeneralException(errorText("USER_ACTIONS","CREDIT_MUST_BE_POSITIVE"))
        
        admin_main.getLoader().checkAdminName(owner_name)
        admin_main.getLoader().checkAdminName(creator_name)
        group_main.getLoader().checkGroupName(group_name)

        if user_ids:
            if len(user_ids) != _count:
                raise GeneralException(errorText("USER_ACTIONS","USER_IDS_COUNT_NOT_MATCH"))
        
            for user_id in user_ids:
                if not isInt(user_id):
                    raise GeneralException(errorText("USER","INVALID_USER_ID")%user_id)

    def addNewUsersQuery(self,_count,credit,owner_name,group_name,ibs_query,user_ids=None):
        """
            _count(integer): count of users
            owner_name(string): name of owner admin
            credit(float): amount of credit users will have, 
            group_name(string): name of group string
            ibs_query(IBSQuery instance): IBSQuery instance we'll add query to
            user_ids(None or list of int): user_ids to use for created users.
                                           if set to None generate new ids
            
            XXX: add this: if credit is an empty string, group initial_credit
                is used, or an exception is raised if there's no initial_credit for user
            return a list of user ids of newly added users
        """

        owner_admin_obj=admin_main.getLoader().getAdminByName(owner_name)
        group_obj=group_main.getLoader().getGroupByName(group_name)

        if not user_ids:
            user_ids=self.__generateUserIDs(_count)

        self.__insertBasicUsersQueries(_count,user_ids,credit,owner_admin_obj.getAdminID(),group_obj.getGroupID(),ibs_query)
        return user_ids

    def __insertBasicUsersQueries(self,_count,user_ids,credit,owner_id,group_id,ibs_query):
        """
            add query to ibs_query for inserting "_count" of users with user ids in "user_ids" into users table
        """
        for user_id in user_ids:
            ibs_query+=self.__insertBasicUserQuery(user_id,credit,owner_id,group_id)

    
    def __insertBasicUserQuery(self,user_id,credit,owner_id,group_id):
        return ibs_db.createFunctionCallQuery("add_user",[user_id,credit,owner_id,group_id])
        
    def __generateUserIDs(self,_count):
        """
            generate "_count" number of user ids and return them in a list
            _count(integer): count of user ids that will be generated
        """
        return map(lambda x:self.__getNewUserID(),range(_count))
        
    def __getNewUserID(self):
        """
            return a new unique user_id from
        """
        return db_main.getHandle().seqNextVal("users_user_id_seq")

    def __addNewUserIASQuery(self,ibs_query,creator_name,credit,user_ids):
            destination=",".join(map(str,user_ids))
            ibs_query+=ias_main.getActionsManager().logEvent("ADD_USER",creator_name,0,destination)
            ibs_query+=ias_main.getActionsManager().logEvent("CHANGE_CREDIT",creator_name,credit,destination)

######################################################
    def changeCredit(self,user_ids,credit,changer_admin_name,remote_address,credit_change_comment,loaded_users):
        """
            change credit of user(s) with user_id in "user_ids"
            user_ids(iterable object, list or multi_str): user_ids that credit will be changed
            credit(float): amount of credit change, can be negative
            changer_admin_name(string): username of admin that initiate the change. He should have enough deposit
            remote_address(string): changer client ip address 
            credit_change_comment(string): comment that will be stored in credit change log
            loaded_users(LoadedUser instance): list of loaded users of "user_ids"
        """
        self.__changeCreditCheckInput(user_ids,credit,changer_admin_name,remote_address,credit_change_comment,loaded_users)
        admin_consumed_credit=credit*len(user_ids)
        ibs_query=IBSQuery()
        ibs_query+=admin_main.getActionManager().consumeDeposit(changer_admin_name,admin_consumed_credit)
        try:
            changer_admin_obj=admin_main.getLoader().getAdminByName(changer_admin_name)
            ibs_query+=self.__changeCreditQuery(user_ids,credit)
            ibs_query+=user_main.getCreditChangeLogActions().logCreditChangeQuery("CHANGE_CREDIT",changer_admin_obj.getAdminID(),user_ids,credit,\
                                        admin_consumed_credit,remote_address,credit_change_comment)

            ibs_query+=ias_main.getActionsManager().logEvent("CHANGE_CREDIT",changer_admin_name,credit,",".join(user_ids))

            ibs_query.runQuery()
        except:
            admin_main.getActionManager().consumeDeposit(changer_admin_name,-1*admin_consumed_credit,False) #re-add deposit to admin
            raise
        self.broadcastChange(user_ids)

    def __changeCreditCheckInput(self,user_ids,credit,changer_admin_name,remote_address,credit_change_comment,loaded_users):
        if not isFloat(credit):
            raise GeneralException(errorText("USER_ACTIONS","CREDIT_NOT_FLOAT"))

        admin_main.getLoader().checkAdminName(changer_admin_name)

        if not iplib.checkIPAddr(remote_address):
            raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%remote_address)

        if len(user_ids)==0:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_USER_COUNT")%0)

        for loaded_user in loaded_users:
            if credit<0 and loaded_user.getBasicUser().getCredit()+credit<0:
                raise GeneralException(errorText("USER_ACTIONS","CAN_NOT_NEGATE_CREDIT")%(loaded_user.getUserID(),loaded_user.getBasicUser().getCredit()))
            
    def __changeCreditQuery(self,user_ids,credit):
        where_clause=" or ".join(map(lambda user_id:"user_id = %s"%user_id,user_ids))
        return ibs_db.createUpdateQuery("users",{"credit":"credit+%s"%credit},where_clause)

######################################################
    def updateUserAttrs(self,loaded_users,admin_obj,attrs,to_del_attrs):
        """
            loaded_users(list of LoadedUser instances):
            
        """
        (ibs_query, changed_attr_updaters, deleted_attr_updaters, users) = self.updateUserAttrsQuery(loaded_users,admin_obj,attrs,to_del_attrs)
        ibs_query.runQuery()
        self.broadcastChange(users.iterkeys())
        self.__callPostUpdates(changed_attr_updaters,deleted_attr_updaters)

    def updateUserAttrsQuery(self,loaded_users,admin_obj,attrs,to_del_attrs):
        """
            return query for update user attrs.
            Caller must runQuery, broadcastChange and callPostUpdates
        """
        self.__updateUserAttrsCheckInput(loaded_users,admin_obj,attrs,to_del_attrs)
        changed_attr_updaters=user_main.getAttributeManager().getAttrUpdaters(attrs,"change")
        deleted_attr_updaters=user_main.getAttributeManager().getAttrUpdaters(to_del_attrs,"delete")
        users=self.__createUsersDic(loaded_users)
        ibs_query=IBSQuery()
        ibs_query=self.__getChangedQuery(ibs_query,users,admin_obj,changed_attr_updaters)
        ibs_query=self.__getDeletedQuery(ibs_query,users,admin_obj,deleted_attr_updaters)
        return (ibs_query, changed_attr_updaters, deleted_attr_updaters, users)

    def __updateUserAttrsCheckInput(self,loaded_users,admin_obj,attrs,to_del_attrs):
        pass #nothing to check here for now, everything is checked or will be checked
    
    def __createUsersDic(self,loaded_users):
        """
            create a dic of {user_id:loaded_user,user_id:loaded_user,...} from loaded_users
        """
        users={}
        for loaded_user in loaded_users:
            users[loaded_user.getUserID()]=loaded_user
        return users

    def __getChangedQuery(self,ibs_query,users,admin_obj,changed_attr_updaters):
        return changed_attr_updaters.getQuery(ibs_query,"user","change",{"users":users,
                                                                         "admin_obj":admin_obj})
        
    def __getDeletedQuery(self,ibs_query,users,admin_obj,deleted_attr_updaters):
        return deleted_attr_updaters.getQuery(ibs_query,"user","delete",{"users":users,
                                                                         "admin_obj":admin_obj})

    def __callPostUpdates(self,changed_attr_updaters,deleted_attr_updaters):
        changed_attr_updaters.postUpdate("user","change")
        deleted_attr_updaters.postUpdate("user","delete")

    def broadcastChange(self,user_ids):
        """
            broadcast that users with id in "users" has been change
            normally user_pool should be told to refresh the user
        """
        userChanged=user_main.getUserPool().userChanged
        map(userChanged,user_ids)
#########################################################
    def getUserInfosFromLoadedUsers(self,loaded_users,date_type):
        """
            return a list of user info dics, from loaded_users list
            return dic is in format {user_id=>user_info dic}
            loaded_users(list of LoadedUser instances): users that we want info for
        """
        user_infos={}
        def addToUserInfo(loaded_user):
            user_infos[str(loaded_user.getUserID())]=loaded_user.getUserInfo(date_type) #python xmlrpc required keys not to be integers
            
        map(addToUserInfo,loaded_users)
        return user_infos

##########################################################
    def searchUsers(self,conds,_from,to,order_by,desc,admin_obj):
        """
            search in users based on conditions in "conds" and return user_ids result from "_from" to "to"
            admin_obj(Admin Instance): requester admin object
        """
        self.__searchUsersCheckInput(conds,_from,to,order_by,desc,admin_obj)
        search_helper=user_main.getAttributeManager().runAttrSearchers(conds,admin_obj)
        return search_helper.getUserIDs(_from,to,order_by,desc)

    def __searchUsersCheckInput(self,conds,_from,to,order_by,desc,admin_obj):
        report_lib.checkFromTo(_from,to)
###########################################################
    def delUser(self,user_ids,comment,del_connections,del_audit_logs,admin_name,remote_address):
        """
            delete users with ids in user_ids
            comment: comment when deleting users
            del_connection tells if we should delete user(s) connection logs too
        """
        self.__delUserCheckInput(user_ids,comment,del_connections,del_audit_logs,admin_name,remote_address)
        admin_obj=admin_main.getLoader().getAdminByName(admin_name)
        map(lambda user_id:user_main.getUserPool().addToBlackList,user_ids)
        try:
            loaded_users=self.getLoadedUsersByUserID(user_ids)
            total_credit=self.__delUserCheckUsers(loaded_users)
            admin_deposit=total_credit*-1
            ibs_query=IBSQuery()
            ibs_query+=user_main.getCreditChangeLogActions().logCreditChangeQuery("DEL_USER",
                                                                              admin_obj.getAdminID(),
                                                                              user_ids,
                                                                              0,
                                                                              admin_deposit,
                                                                              remote_address,
                                                                              comment)
            ibs_query+=admin_main.getActionManager().consumeDepositQuery(admin_obj.getAdminID(),admin_deposit)
            ibs_query+=ias_main.getActionsManager().logEvent("DELETE_USER",admin_name,0,",".join(user_ids))

            self.__delUserQuery(ibs_query,user_ids,del_connections,del_audit_logs)
            ibs_query.runQuery()
            admin_obj.consumeDeposit(admin_deposit)
            map(user_main.getUserPool().userChanged,user_ids)
        finally:
            map(lambda user_id:user_main.getUserPool().removeFromBlackList,user_ids)

        self.__postDelUser(loaded_users)


    def __postDelUser(self, loaded_users):
        for loaded_user in loaded_users:
            if loaded_user.getUserAttrs().hasAttr("mail_quota") and loaded_user.getUserAttrs().hasAttr("normal_username"):
                user_main.getMailActions().deleteMailbox(loaded_user.getUserAttrs()["normal_username"])
    
    
    def __delUserCheckInput(self,user_ids,comment,del_connections,del_audit_logs,admin_name,remote_address):
        admin_main.getLoader().checkAdminName(admin_name)
        if not iplib.checkIPAddr(remote_address):
            raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%remote_address)
        if len(user_ids)==0:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_USER_COUNT")%0)


    def __delUserCheckUsers(self,loaded_users):
        """
            check users and return their total credit
            WARNING: XXX this is not safe, checking online, and unloading there! to be fixed
        """
        total_credit=0
        for loaded_user in loaded_users:
            if loaded_user.isOnline():
                raise GeneralException(errorText("USER_ACTIONS","DELETE_USER_IS_ONLINE")%loaded_user.getUserID())
            total_credit += max( 0 , loaded_user.getBasicUser().getCredit() )
        return total_credit

    def __delUserQuery(self,ibs_query,user_ids,del_connections,del_audit_logs):

        user_id_conds = self.__delUserCreateCondition(user_ids)
        
        ibs_query += self.__delUserAttrsQuery(user_id_conds)
        ibs_query += self.__delUserNormalAttrsQuery(user_id_conds)
        ibs_query += self.__delUserPLanAttrsQuery(user_id_conds)
        ibs_query += self.__delUserCallerIDAttrsQuery(user_id_conds)
        ibs_query += self.__delUserVoIPAttrsQuery(user_id_conds)
        ibs_query += self.__delUserMessagesQuery(user_id_conds)
        ibs_query += self.__delUserWebAnalyzerLogsQuery(user_id_conds)
        ibs_query += self.__delUserBwSnapshotsQuery(user_id_conds)
        
        if del_connections:
            ibs_query += user_main.getConnectionLogManager().deleteConnectionLogsForUsersQuery(user_ids)
        
        if del_audit_logs:
            ibs_query += user_main.getUserAuditLogManager().deleteAuditLogsForUsersQuery(user_ids)

        ibs_query += self.__delUserFromUsersTableQuery(user_id_conds)


    def __delUserCreateCondition(self, user_ids):
        conds = []
        
        for user_id in user_ids:
            conds.append("%s::bigint"%user_id)

        return "user_id in (%s)" % ",".join(conds)


    def __delUserAttrsQuery(self,user_id_conds):
        """
            user_ids_conds: condition of user_ids
        """
        return ibs_db.createDeleteQuery("user_attrs",user_id_conds)

    def __delUserNormalAttrsQuery(self,user_id_conds):
        return ibs_db.createDeleteQuery("normal_users",user_id_conds)

    def __delUserVoIPAttrsQuery(self,user_id_conds):
        return ibs_db.createDeleteQuery("voip_users",user_id_conds)

    def __delUserPLanAttrsQuery(self,user_id_conds):
        return ibs_db.createDeleteQuery("persistent_lan_users",user_id_conds)

    def __delUserCallerIDAttrsQuery(self,user_id_conds):
        return ibs_db.createDeleteQuery("caller_id_users",user_id_conds)

    def __delUserFromUsersTableQuery(self,user_id_conds):
        return ibs_db.createDeleteQuery("users",user_id_conds)

    def __delUserMessagesQuery(self, user_id_conds):
        return ibs_db.createDeleteQuery("user_messages",user_id_conds) + \
               ibs_db.createDeleteQuery("admin_messages",user_id_conds)

    def __delUserWebAnalyzerLogsQuery(self, user_id_conds):
        return ibs_db.createDeleteQuery("web_analyzer_log",user_id_conds)

    def __delUserBwSnapshotsQuery(self, user_id_conds):
        return ibs_db.createDeleteQuery("internet_bw_snapshot",user_id_conds)
    
################################################################
    def getUserIDsWithBasicAttr(self,attr_name,attr_value):
        """
            return user_ids whom attr_name value in basic attrs is attr_value
        """
        user_ids=db_main.getHandle().get("users","%s=%s"%(attr_name,attr_value),
                                         0,-1,("user_id",True),["user_id"])
        return map(lambda dic:dic["user_id"],user_ids)
################################################################
    def getUserIDsWithAttr(self,attr_name,attr_value):
        """
            return user_ids whom attr_name value is attr_value, of course user should have attr_name!
        """
        user_ids=db_main.getHandle().get("user_attrs","attr_name=%s and attr_value=%s"%(dbText(attr_name),dbText(attr_value)),
                                         0,-1,("user_id",True),["user_id"])
                
        return map(lambda dic:dic["user_id"],user_ids)
#################################################################
    def getPersistentLanUsers(self,ras_id):
        """
            return a list of dics, containin
        """
        return db_main.getHandle().get("persistent_lan_users","persistent_lan_ras_id=%s"%ras_id)

##################################################################
    def killUser(self,user_id,ras_ip,unique_id_val,kill,admin_name):
        """
            kill user on "ras_ip" and "unique_id_val" and check that user is "user_id"
            kill(boolean): either kill, or just clear the user from onlines
        """
        ras_id=ras_main.getLoader().getRasByIP(ras_ip).getRasID()
        if kill:
            user_main.getOnline().killUser(user_id,ras_id,unique_id_val,errorText("USER_LOGIN","KILLED_BY_ADMIN",False)%admin_name)
        else:
            user_main.getOnline().clearUser(user_id,ras_id,unique_id_val,errorText("USER_LOGIN","CLEARED_BY_ADMIN",False)%admin_name)
            
####################################################################
    def killAllUsers(self, kill, kill_reason):
        """
            kill all online users
            kill(boolean): if set to true, kill the users, else, clear the users
            kill_reason(str): kill reason that will be submitted for user kill
        """
        user_main.getOnline().killAllUsers(kill, kill_reason)
##################################################################
    def shutdownUsers(self):
        kill_reason = errorText("USER_LOGIN","SYSTEM_SHUTTING_DOWN",False)

        if defs.KILL_USERS_ON_SHUTDOWN:
            self.killAllUsers(True, kill_reason)
            c = 0
            while user_main.getOnline().getOnlinesCount():
                toLog("shutdownUsers: Loop %s, %s users online"%(c, user_main.getOnline().getOnlinesCount()) , LOG_DEBUG)

                if c == defs.KILL_USERS_SHUTDOWN_WAIT_TIME:
                    toLog("shutdownUsers: Clearing %s online users"%user_main.getOnline().getOnlinesCount() , LOG_DEBUG)
                    self.killAllUsers(False, kill_reason)
                    break

                time.sleep(1)
                c += 1
        else:
            self.killAllUsers(False, kill_reason)
            
####################################################################
    def getUsernameReprForUserID(self, user_id):
        """
            return text representation of any available username for user_id
            this function tries to find user_id username and return that in format type:username
            first the normal username and then voip username is tried. If user doesn't have either of these
            N/A is returned
        """                         
        try:
            loaded_user = user_main.getUserPool().getUserByID(user_id)
        except GeneralException: #user not found
            return "N/A"
        
        return self.__getUsernameReprForLoadedUser(loaded_user)

    def __getUsernameReprForLoadedUser(self, loaded_user):
        if loaded_user.userHasAttr("normal_username"):
            return "I: %s"%loaded_user.getUserAttrs()["normal_username"]
        elif loaded_user.userHasAttr("voip_username"):
            return "V: %s"%loaded_user.getUserAttrs()["voip_username"]
        else:
            return "ID: %s"%loaded_user.getUserID()
#####################################################################
    def calcApproxDuration(self, loaded_user):
        """
            return approximate available duration when using normal charge for loaded_user
            return value is in seconds
        """
        if not loaded_user.getUserAttrs().hasAttr("normal_charge"):
            return []
            
        charge_obj=charge_main.getLoader().getChargeByID(int(loaded_user.getUserAttrs()["normal_charge"]))
        credit=loaded_user.getBasicUser().getCredit()
        approx=[]
    
        for rule_obj in charge_obj.getRules().itervalues():
            cpm=0
            if rule_obj.cpm:
                cpm += rule_obj.cpm
        
            if rule_obj.cpk:
                cpm += rule_obj.assumed_kps/rule_obj.cpk
            
            if rule_obj.ras_id!=rule_obj.ALL:
                ras_ip=ras_main.getLoader().getRasByID(rule_obj.ras_id).getRasIP()
            else:
                ras_ip=rule_obj.ALL

            if cpm:
                duration=credit/cpm*60
            else:
                duration="Infinite"
            approx.append([duration, ras_ip, rule_obj.day_of_weeks.getDayNames(), rule_obj.start_time, rule_obj.end_time])
        
        return approx
    
    ############################################################
    def getLastDestination(self, voip_username):
        """
            return last destination dialed by user or empty string if
            no number was dialed yet
        """
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(voip_username)
        ret=db_main.getHandle().selectQuery("""select 
                                    value 
                                 from 
                                    connection_log,connection_log_details 
                                 where 
                                    connection_log.connection_log_id=connection_log_details.connection_log_id 
                                 and 
                                    service=2 
                                 and 
                                    user_id=%s
                                 and 
                                    name='called_number' 
                                 order by 
                                    login_time 
                                 limit 1"""%loaded_user.getUserID())
        try:
            return ret[0]["value"]
        except IndexError:
            return ""

    ###################################################
    def addCallerIDAuthentication(self, voip_username, caller_id):
        """
            add caller_id to voip_username list of voip caller_ids
        """
        self.__addCallerIDAuthenticationCheckInput(voip_username, caller_id)
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(voip_username)
        if loaded_user.userHasAttr("caller_id"):
            caller_ids=loaded_user.getUserAttrs()["caller_id"]
        else:
            caller_ids=[]
        
        if caller_id not in caller_ids:
            caller_ids.append(caller_id)
        
        self.updateUserAttrs([loaded_user],
                             admin_main.getLoader().getAdminByName("system"),
                             {"caller_id":",".join(caller_ids)},
                             [])
        


    def __addCallerIDAuthenticationCheckInput(self, voip_username, caller_id):  
        if not caller_id:
            raise GeneralException(errorText("USER_ACTIONS","BAD_CALLER_ID")%caller_id)

    def deleteCallerIDAuthentication(self, voip_username, caller_id):
        """
            remove caller_id from voip_username list of voip caller_ids
            raise an exception if caller id doesn't exists in voip caller ids
        """
        self.__addCallerIDAuthenticationCheckInput(voip_username, caller_id)
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(voip_username)
        if loaded_user.userHasAttr("caller_id"):
            caller_ids=loaded_user.getUserAttrs()["caller_id"]
            try:
                caller_ids.remove(caller_id)
            except ValueError:
                raise GeneralException(errorText("USER_ACTIONS","CALLER_ID_NOT_EXISTS")%caller_id)
        
            self.updateUserAttrs([loaded_user],
                                 admin_main.getLoader().getAdminByName("system"),
                                 {"caller_id":",".join(caller_ids)},
                                 [])
        else:
            raise GeneralException(errorText("USER_ACTIONS","CALLER_ID_NOT_EXISTS")%caller_id)