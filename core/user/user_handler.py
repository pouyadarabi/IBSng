from core.server import handler
from core.user import user_main
from core.group import group_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.multi_strs import MultiStr
from core.lib.general import *
from core.lib import report_lib
import string
import itertools

class UserHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"user")
        self.registerHandlerMethod("addNewUsers")
        self.registerHandlerMethod("getUserInfo")
        self.registerHandlerMethod("updateUserAttrs")
        self.registerHandlerMethod("changeCredit")
        self.registerHandlerMethod("searchUser")
        self.registerHandlerMethod("delUser")
        self.registerHandlerMethod("killUser")
        self.registerHandlerMethod("calcApproxDuration")
                
    def addNewUsers(self,request):
        """
            Add "count" number of raw users. Created users has no attribute assigned to them.
            Later you should assign attribute by updateUserAttrs
            
            return a list of created user_id s
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("count","credit","owner_name","group_name","credit_comment")
        requester=request.getAuthNameObj()
        requester.canDo("ADD NEW USER")
        if request["owner_name"]!=requester.getUsername():
            requester.canDo("CHANGE USERS OWNER")
        try:
            _count=int(request["count"])
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","COUNT_NOT_INTEGER"))

        try:
            credit=float(request["credit"])
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","CREDIT_NOT_FLOAT"))
            
        return user_main.getActionManager().addNewUsers(_count,credit,request["owner_name"],requester.getUsername(),
                                                        request["group_name"],request.getRemoteAddr(),
                                                        request["credit_comment"])

##########################################################
    def getUserInfo(self,request):
        """
            return user information in a list of dics in format
            [{"basic_info":{basic_user_info},"attrs":{user_attributes}},{"basic_info":{basic_user_info},"attrs":{user_attributes}},...]
            basic_user_info and user_attributes are dictionaries contain name=>values

            if requester is admin, he can specify user_id or normal_username or voip_username. All can be multistrings
            if requirter is user, no argument will be parsed and auth_name is used
        """
        if request.hasAuthType(request.ADMIN):
            if request.has_key("user_id"):
                loaded_users=user_main.getActionManager().getLoadedUsersByUserID(MultiStr(request["user_id"]))
            elif request.has_key("normal_username"):
                loaded_users=user_main.getActionManager().getLoadedUsersByNormalUsername(MultiStr(request["normal_username"]))
            elif request.has_key("voip_username"):
                loaded_users=user_main.getActionManager().getLoadedUsersByVoIPUsername(MultiStr(request["voip_username"]))
            else:
                raise request.raiseIncompleteRequest("user_id")

            admin_obj=request.getAuthNameObj()
            map(admin_obj.canAccessUser,loaded_users)
            
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            loaded_users=[request.getAuthNameObj()]
        else:
            raise request.raiseIncompleteRequest("auth_type")
        
        user_infos=user_main.getActionManager().getUserInfosFromLoadedUsers(loaded_users,request.getDateType())

        if request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            user_info=self.__filterAttrsForUser(user_infos.values()[0])
            return self.__addGroupAttrsForUser(user_info, request.getDateType())

        return user_infos
    
    def __filterAttrsForUser(self,user_info):
        """
            filter unnecessary informations of user, like password and raw_attrs so the informations
            are safe to be passed to a user type authenticated client.
            user_info(dic): dictionary of ONE user info, like what's returned by loaded_user.getInfo
        """
#       del(user_info["raw_attrs"])

        for attr_name in ["normal_password","voip_password","owner"]:
            if user_info["attrs"].has_key(attr_name):
                del(user_info["attrs"][attr_name])

        return user_info

    def __addGroupAttrsForUser(self,user_info, date_type):
        """
            add group attributes to attr dic, if user doesn't have the attr. Users don't have 
            access to groups, and they doesn't know about user/group logic.
        """
        group_obj=group_main.getLoader().getGroupByID(user_info["basic_info"]["group_id"])
        group_attrs = group_obj.getParsedAttrs(date_type)
        for attr_name in group_attrs:
            
            #if it's not set in user
            if attr_name not in user_info["attrs"]:
                user_info["attrs"][attr_name] = group_attrs[attr_name]

        return user_info
#########################################################
    def updateUserAttrs(self,request):
        """
            update user attributes
            
            user_id(string): user ids that should be updated, can be multi strings
            attrs(dic): dictionary of attr_name:attr_value. We say we want attr_name value to be attr_value
            to_del_attrs(dic): dic of attributes that should be deleted 
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_id","attrs","to_del_attrs")
        loaded_users=user_main.getActionManager().getLoadedUsersByUserID(MultiStr(request["user_id"]))
        admin_obj=request.getAuthNameObj()
        map(admin_obj.canChangeUser,loaded_users)

        to_del_attrs=requestDicToList(request["to_del_attrs"])
        return user_main.getActionManager().updateUserAttrs(loaded_users,
                                                            request.getAuthNameObj(),
                                                            request["attrs"],
                                                            to_del_attrs
                                                            )
############################################################
    def changeCredit(self,request):
        """
            change credit of user
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_id","credit","credit_comment")
        requester=request.getAuthNameObj()
        user_id_multi=MultiStr(request["user_id"])
        loaded_users=user_main.getActionManager().getLoadedUsersByUserID(user_id_multi)
        map(self.__canChangeCredit,loaded_users,itertools.repeat(requester,len(loaded_users)))
        return user_main.getActionManager().changeCredit(user_id_multi,
                                                         to_float(request["credit"],"credit"),
                                                         requester.getUsername(),
                                                         request.getRemoteAddr(),
                                                         request["credit_comment"],
                                                         loaded_users)

    def __canChangeCredit(self,loaded_user,requester):
        requester.canDo("CHANGE USER CREDIT",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())
############################################################
    def searchUser(self,request):
        """
            return (count_of_result,user_id_lists)
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("conds","from","to","order_by","desc")
        admin_obj=request.getAuthNameObj()
        conds=self.__searchUserFixConds(request["conds"])

        if admin_obj.isGod(): pass
        elif admin_obj.hasPerm("GET USER INFORMATION"):
            if admin_obj.getPerms()["GET USER INFORMATION"].isRestricted():
                conds["owner_name"]=[admin_obj.getUsername()]
        else:
            raise PermissionException(errorText("GENERAL","ACCESS_DENIED"))
                
        return user_main.getActionManager().searchUsers(conds,request["from"],request["to"],request["order_by"],request["desc"],admin_obj)

    def __searchUserFixConds(self,conds):
        """
            convert integer key dictionaries to lists. It takes care of other dics so it won't convert 
            other dics
        """
        return report_lib.fixConditionsDic(conds)
##########################################################
    def delUser(self,request):
        """
            delete users
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_id","delete_comment","del_connection_logs","del_audit_logs")
        requester=request.getAuthNameObj()
        user_id_multi=MultiStr(request["user_id"])
        loaded_users=user_main.getActionManager().getLoadedUsersByUserID(user_id_multi)
        map(self.__canDeleteUser,loaded_users,itertools.repeat(requester,len(loaded_users)))
        return user_main.getActionManager().delUser(user_id_multi,
                                                    request["delete_comment"],
                                                    request["del_connection_logs"],
                                                    request["del_audit_logs"],
                                                    requester.getUsername(),
                                                    request.getRemoteAddr()
                                                    )

    def __canDeleteUser(self,loaded_user,requester):
        requester.canDo("DELETE USER",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())
##############################################################
    def killUser(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("user_id","ras_ip","unique_id_val","kill")
        requester=request.getAuthNameObj()
        loaded_users=user_main.getActionManager().getLoadedUsersByUserID(MultiStr(request["user_id"]), True)
        if request["kill"]:
            map(lambda loaded_user:self.__canKillUser(loaded_user,requester),loaded_users)
        else:
            map(lambda loaded_user:self.__canClearUser(loaded_user,requester),loaded_users)

        ras_ips=MultiStr(request["ras_ip"])
        unique_id_vals=MultiStr(request["unique_id_val"])

        for i in xrange(len(loaded_users)):
            user_main.getActionManager().killUser(loaded_users[i].getUserID(),
                                                  ras_ips[i],
                                                  unique_id_vals[i],
                                                  request["kill"],
                                                  requester.getUsername())

    def __canKillUser(self,loaded_user,requester):
        requester.canDo("KILL USER",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())

    def __canClearUser(self,loaded_user,requester):
        requester.canDo("CLEAR USER",loaded_user.getUserID(),loaded_user.getBasicUser().getOwnerObj().getAdminID())
################################################################
    def calcApproxDuration(self,request):
        if request.hasAuthType(request.ADMIN):
            request.checkArgs("user_id")
            loaded_user=user_main.getUserPool().getUserByID(request["user_id"])

            admin_obj=request.getAuthNameObj()
            admin_obj.canAccessUser(loaded_user)
            
        elif request.hasAuthType(request.NORMAL_USER) or request.hasAuthType(request.VOIP_USER):
            loaded_user=request.getAuthNameObj()
        else:
            raise request.raiseIncompleteRequest("auth_type")
        
        return user_main.getActionManager().calcApproxDuration(loaded_user)
    