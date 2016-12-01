from core.errors import errorText
from core.ibs_exceptions import *
from core.lib.general import *
from core.db import db_main
from core.user.loaded_user import LoadedUser
from core.user.basic_user import BasicUser
from core.user.attribute import UserAttributes

def init():
    global user_loader
    user_loader=UserLoader()
    
def getLoader():
    return user_loader

class UserLoader:
    DEBUG=False

    def normalUsername2UserID(self,normal_username):
        """
            return user_id of user with normal username "normal_username"
        """
        normal_attrs=self.__fetchNormalUserAttrsByNormalUsername(normal_username)
        if normal_attrs==None:
            raise GeneralException(errorText("USER","NORMAL_USERNAME_DOESNT_EXISTS")%normal_username)
        else:
            return normal_attrs["user_id"]

    def voipUsername2UserID(self,voip_username):
        """
            return user_id of user with voip username "voip_username"
        """
        voip_attrs=self.__fetchVoIPUserAttrsByVoIPUsername(voip_username)
        if voip_attrs==None:
            raise GeneralException(errorText("USER","VOIP_USERNAME_DOESNT_EXISTS")%voip_username)
        else:
            return voip_attrs["user_id"]

    def callerID2UserID(self, caller_id):
        """
            return user_id of user with caller_id "caller_id"
        """
        user_id=self.__fetchUserIDByCallerID(caller_id)
        if user_id==None:
            raise GeneralException(errorText("USER","CALLER_ID_DOESNT_EXISTS")%caller_id)
        else:
            return user_id

    #####################################
        
    def getLoadedUserByUserIDs(self,user_ids):
        """
            return a list of LoadedUser instances of user with ids "user_ids"
        """
        length = len(user_ids)
        singles = user_ids[length-length%35:]
        massives = user_ids[:length-length%35]

        if self.DEBUG:
            toLog("UserLoader: Loading %s massives and %s singles"%(len(massives),len(singles)),LOG_DEBUG)
    
        loaded_users = map(self.__loadSingle,singles)
        loaded_users += self.__loadMassives(massives)
        return loaded_users
        
    def __loadSingle(self, user_id):
        """
            load a single user_id and return a LoadedUser
        """
        basic_user=self.getBasicUser(user_id) #should be first
        user_attrs_dic=self.getUserAttrsByUserID(user_id)
        user_attrs=self.__createUserAttrs(user_attrs_dic,basic_user)
        return self.__createLoadedUser(basic_user,user_attrs)

    def __loadMassives(self, user_ids):
        """
            load multiple user_ids and return a list of loaded_users
            user_ids length should be dividable by defs.POSTGRES_MAGIC_NUMBER
        """
        loaded_users = []
        for i in range(0,len(user_ids),defs.POSTGRES_MAGIC_NUMBER):
            cur_ids = user_ids[i:i+defs.POSTGRES_MAGIC_NUMBER]
            basic_users = self.getBasicUsers(cur_ids)
            user_attrs_dic=self.getUserAttrsByUserIDs(cur_ids)
            user_attrs=self.__createUsersAttrs(user_attrs_dic,basic_users)
            loaded_users += map(self.__createLoadedUser,basic_users,user_attrs)
        return loaded_users

    ######################################

    def getUserAttrsByUserID(self,user_id):
        """
            return complete user attributes containing voip and normal user attributes
        """
        attrs=self.__fetchUserAttrs(user_id)
        attrs.update(self.__fetchNormalUserAttrsByUserID(user_id))
        attrs.update(self.__fetchVoIPUserAttrsByUserID(user_id))
        attrs.update(self.__fetchPersistentLanAttrs(user_id))
        attrs.update(self.__fetchCallerIDAttrsByUserID(user_id))
        return attrs

    def getUserAttrsByUserIDs(self, user_ids):
        """
            return a dic of user attribute if format {user_id:attrs}
        """
        attrs = self.__fetchUsersAttrs(user_ids)
        normal_attrs = self.__fetchNormalUsersAttrsByUserID(user_ids)
        voip_attrs = self.__fetchVoIPUsersAttrsByUserID(user_ids)
        plan_attrs = self.__fetchPersistentLansAttrs(user_ids)
        callerid_attrs = self.__fetchCallerIDsAttrsByUserID(user_ids)
        
        all_attrs = {}
        for user_id in user_ids:
            all_attrs[user_id] = {}
            
            for attrs_dic in [attrs, normal_attrs, voip_attrs, plan_attrs, callerid_attrs]:
                if attrs_dic.has_key(user_id):
                    all_attrs[user_id].update(attrs_dic[user_id])
                    
        return all_attrs
            
        
    def getBasicUser(self,user_id):
        """
            return BasicUser instance of user_id
            raise a GeneralException if user with user_id doesn't exists
        """
        basic_user_info=self.__fetchBasicUserInfo(user_id)
        if basic_user_info==None:
            raise GeneralException(errorText("USER","USERID_DOESNT_EXISTS")%user_id)
        return self.__createBasicUser(basic_user_info)

    def getBasicUsers(self,user_ids):
        basic_infos = self.__fetchMassiveBasicInfo(user_ids)
        return map(self.__createBasicUser,basic_infos)

    #########################################
    def __createUserAttrs(self,user_attrs_dic,basic_user):
        """
            create UserAttributes Instance from user_attrs_dic and basic_user
            user_attrs_dic(dic): dic of {attr_name:attr_value}
            basic_user(BasicUser instance): basic user informations
        """
        return UserAttributes(user_attrs_dic,basic_user.getGroupID())

    def __createUsersAttrs(self,user_attrs_dic,basic_users):
        """
            create UserAttributes Instances for multiple users
        """
        user_attrs=[]
        for basic_user in basic_users:
            user_attrs.append(self.__createUserAttrs(user_attrs_dic[basic_user.getUserID()],basic_user))
        return user_attrs

    def __createLoadedUser(self,basic_user,user_attrs):
        """
            create and return an instance of LoadedUser
        """
        return LoadedUser(basic_user,user_attrs)

    ###################################################
    def __createBasicUser(self,basic_user_info):
        """
            create BasicUser instance from basic_user_info
            basic_user_info(dic): dic of user infos, normally returned by __fetchBasicUserInfo
        """
        return BasicUser(basic_user_info["user_id"],
                         basic_user_info["owner_id"],
                         basic_user_info["credit"],
                         basic_user_info["group_id"],
                         basic_user_info["creation_date"])
                         
                         
    def __fetchBasicUserInfo(self,user_id):
        """
            fetch basic user info by user id and return a dic of user informations or None if 
            there's no such id
        """
        basic_user_info=db_main.getHandle().executePrepared("load_users",(user_id,))
        if len(basic_user_info)==0:
            return None
        return basic_user_info[0]
        
    def __fetchMassiveBasicInfo(self, user_ids):
        return db_main.getHandle().executePrepared("bulk_load_users",user_ids)

    ##################################################
    def __fetchNormalUserAttrsByUserID(self,user_id):
        """
            fetch normal user info from "normal_users" table, using user_id of user
            return a dic of attributes in format {attr_name:attr_value}
        """
        normal_db_attrs=db_main.getHandle().executePrepared("load_normal_users",(user_id,))

        if len(normal_db_attrs)==1:
            return normal_db_attrs[0]
        else:
            return {}

    def __fetchNormalUsersAttrsByUserID(self,user_ids):
        users = {}
        normal_db_attrs = db_main.getHandle().executePrepared("bulk_load_normal_users",user_ids)
        for _dic in normal_db_attrs:
            users[_dic["user_id"]] = _dic
        return users

    def __fetchNormalUserAttrsByNormalUsername(self,normal_username):
        """
            fetch normal user info from "normal_users" table, using normal username of user
            return a dic of attributes in format {attr_name:attr_value} or None if normal_username
            doesn't exists
        """
        normal_db_attrs=db_main.getHandle().executePrepared("load_normal_users_username",[dbText(normal_username)])
        if len(normal_db_attrs)==1:
            return normal_db_attrs[0]
        else:
            return None

    ##############################################
    def __fetchVoIPUserAttrsByUserID(self,user_id):
        """
            fetch voip user info from "voip_users" table, using user_id of user
            return a dic of attributes in format {attr_name:attr_value}
        """
        voip_db_attrs=db_main.getHandle().executePrepared("load_voip_users",(user_id,))
        if len(voip_db_attrs)==1:
            return voip_db_attrs[0]
        else:
            return {}

    def __fetchVoIPUsersAttrsByUserID(self,user_ids):
        users = {}
        voip_db_attrs = db_main.getHandle().executePrepared("bulk_load_voip_users",user_ids)
        for _dic in voip_db_attrs:
            users[_dic["user_id"]] = _dic
        return users
        

    def __fetchVoIPUserAttrsByVoIPUsername(self,voip_username):
        """
            fetch voip user info from "voip_users" table, using voip username of user
            return a dic of attributes in format {attr_name:attr_value} or None if voip_username
            doesn't exists
        """
        voip_db_attrs=db_main.getHandle().executePrepared("load_voip_users_username",[dbText(voip_username)])
        if len(voip_db_attrs)==1:
            return voip_db_attrs[0]
        else:
            return None

    ##################################
    def __fetchUserAttrs(self,user_id):
        """
            return a dictionary of user attributes in format {attr_name:attr_value}
        """
        user_attrs={}
        db_user_attrs=db_main.getHandle().executePrepared("load_user_attrs",(user_id,))
        for user_dic in db_user_attrs:
            user_attrs[user_dic["attr_name"]]=user_dic["attr_value"]
        return user_attrs

    def __fetchUsersAttrs(self,user_ids):
        users = {} #user:dic of attrs
        db_user_attrs = db_main.getHandle().executePrepared("bulk_load_user_attrs",user_ids)
        for _dic in db_user_attrs:
            try:
                users[_dic["user_id"]][_dic["attr_name"]]=_dic["attr_value"]
            except KeyError:
                users[_dic["user_id"]]={_dic["attr_name"]:_dic["attr_value"]}
        return users

    ###################################
    def __fetchPersistentLanAttrs(self,user_id):
        """
            return a dictionary of persistent_lan_users table attributes in format {attr_name:attr_value}
        """
        plan_db_attrs=db_main.getHandle().executePrepared("load_persistent_lan_users",(user_id,))
        if len(plan_db_attrs)==1:
            return plan_db_attrs[0]
        else:
            return {}

    def __fetchPersistentLansAttrs(self,user_ids):
        users = {}
        plan_db_attrs = db_main.getHandle().executePrepared("bulk_load_persistent_lan_users",user_ids)
        for _dic in plan_db_attrs:
            users[_dic["user_id"]]=_dic
        return users

    ######################################
    def __fetchCallerIDAttrsByUserID(self,user_id):
        """
            return a dictionary of caller_id_users table attributes in format {attr_name:attr_value}
        """
        cid_db_attrs=db_main.getHandle().executePrepared("load_caller_id_users",(user_id,))
        if len(cid_db_attrs) > 0:
            cids=[]
            for row in cid_db_attrs:
                cids.append(row["caller_id"])   

            return {"caller_id":cids}
        return {}

    def __fetchCallerIDsAttrsByUserID(self,user_ids):
        users={}
        cid_db_attrs = db_main.getHandle().executePrepared("bulk_load_caller_id_users",user_ids)
        for _dic in cid_db_attrs:
            if users.has_key(_dic["user_id"]):
                users[_dic["user_id"]]["caller_id"].append(_dic["caller_id"])
            else:
                users[_dic["user_id"]]={"caller_id":[_dic["caller_id"]]}
        return users

    def __fetchUserIDByCallerID(self, caller_id):
        cid_db_attrs=db_main.getHandle().executePrepared("load_caller_id_users_caller_id",[dbText(caller_id)])
        if len(cid_db_attrs):
            return cid_db_attrs[0]["user_id"]
        return None
