from core.ibs_exceptions import *
from core.lib.general import *
from core.errors import errorText
from core.db import db_main
from core.group.group import Group

class GroupLoader:
    def __init__(self):
        self.groups_name={}
        self.groups_id={}

    def __getitem__(self,key):
        if isInt(key):
            return self.getGroupByID(key)
        else:
            return self.getGroupByName(key)
    
    def __iter__(self):
        return self.groups_id.iterkeys()

    def getGroupByID(self,group_id):
        try:
            return self.groups_id[group_id]
        except KeyError:
            raise GeneralException(errorText("GROUPS","GROUP_ID_INVALID")%group_id)
        
    def getGroupByName(self,group_name):
        try:
            return self.groups_name[group_name]
        except KeyError:
            raise GeneralException(errorText("GROUPS","GROUP_NAME_INVALID")%group_name)
        
    def checkGroupID(self,group_id):
        if not self.groups_id.has_key(group_id):
            raise GeneralException(errorText("GROUPS","GROUP_ID_INVALID")%group_id)

    def checkGroupName(self,group_name):
        if not self.groups_name.has_key(group_name):
            raise GeneralException(errorText("GROUPS","GROUP_NAME_INVALID")%group_name) 
        
    def getAllGroupNames(self):
        return self.groups_name.keys()
    
    def groupNameExists(self,group_name):
        return self.groups_name.has_key(group_name)

    def loadGroup(self,group_id):
        """
            load group with id "group_id"
        """
        (group_id,group_name,comment,owner_id)=self.__getGroupInfoDB(group_id)
        group_attrs=self.__getGroupAttrs(group_id)
        group_obj=self.__createGroupObj(group_id,group_name,comment,owner_id,group_attrs)
        self.__addInternal(group_obj)

    def loadGroupByName(self,group_name):
        """
            load group with name "group_name"
            "group_name" should be available in object
        """
        group_id=self.getGroupByName(group_name).getGroupID()
        self.loadGroup(group_id)


    def loadAllGroups(self):
        group_ids=self.__getAllGroupIDs()
        map(self.loadGroup,group_ids)

    def unloadGroup(self,group_id):
        """
            unload group with id "group_id"
        """
        group_obj=self.getGroupByID(group_id)
        del(self.groups_name[group_obj.getGroupName()])
        del(self.groups_id[group_id])

    def __getAllGroupIDs(self):
        group_ids=db_main.getHandle().get("groups","true",0,-1,"",["group_id"])
        return [m["group_id"] for m in group_ids]

    def __addInternal(self,group_obj):
        self.groups_name[group_obj.getGroupName()]=group_obj
        self.groups_id[group_obj.getGroupID()]=group_obj
    
    def __createGroupObj(self,group_id,group_name,comment,owner_id,group_attrs):
        return Group(group_id,group_name,comment,owner_id,group_attrs)

    def __getGroupInfoDB(self,group_id):
        """
            get group info of group with id "group_id" from "groups" table
            and return (group_id,group_name) tuple
        """
        group_info=db_main.getHandle().get("groups","group_id=%s"%to_int(group_id,"group id"))
        return (group_info[0]["group_id"],group_info[0]["group_name"],group_info[0]["comment"],group_info[0]["owner_id"])

    def __getGroupAttrs(self,group_id):
        """
            get attributes of group with id "group_id" from db, and return a dic of Attribute instances
            in format {attr_name:attr_value}
        """
        attr_list=self.__getGroupAttrsDB(group_id)
        return self.__attrListToDic(attr_list)

    def __attrListToDic(self,attr_list):
        """
            attr_list is a list of attribute dics return from db select query
            return a dic in format {attr_name:attr_value}
        """
        attr_dic={}
        for _dic in attr_list:
            attr_dic[_dic["attr_name"]]=_dic["attr_value"]
        return attr_dic
    
    def __getGroupAttrsDB(self,group_id):
        """
            return group attrs from db in a list of associative dics
        """
        return db_main.getHandle().get("group_attrs","group_id=%s"%group_id)
