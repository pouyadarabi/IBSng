from core.db import ibs_db,db_main
from core.db.ibs_query import IBSQuery
from core.admin import admin_main
from core.group import group_main
from core.errors import errorText
from core.ibs_exceptions import *
from core.lib.general import *
from core.user import user_main

class GroupActions:
    def addGroup(self,group_name,comment,owner_id):
        """
            add a new group with name "group_name"
            group_name(string): name of a new group
            owner_id(integer): id of owner admin id
            comment(string): 
        """
        self.__addGroupCheckInput(group_name,comment,owner_id)
        group_id=self.__getNewGroupSeq()
        self.__addGroupDB(group_id,group_name,comment,owner_id)
        group_main.getLoader().loadGroup(group_id)
    
    def __addGroupCheckInput(self,group_name,comment,owner_id):
        if not isValidName(group_name):
            raise GeneralException(errorText("GROUPS","GROUP_NAME_INVALID")%group_name)

        if group_main.getLoader().groupNameExists(group_name):
            raise GeneralException(errorText("GROUPS","GROUP_NAME_TAKEN")%group_name)   
        
        admin_main.getLoader().checkAdminID(owner_id)
        
    def __getNewGroupSeq(self):
        return db_main.getHandle().seqNextVal("groups_group_id_seq")

    def __addGroupDB(self,group_id,group_name,comment,owner_id):
        db_main.getHandle().transactionQuery(self.__addGroupQuery(group_id,group_name,comment,owner_id))

    def __addGroupQuery(self,group_id,group_name,comment,owner_id):
        return ibs_db.createInsertQuery("groups",{"group_id":group_id,
                                                  "group_name":dbText(group_name),
                                                  "comment":dbText(comment),
                                                  "owner_id":owner_id
                                                 })

############################################
    def updateGroup(self,group_id,group_name,comment,owner_name):
        """
            update group information with id "group_id"
            notice that group_name is changable
        """
        self.__updateGroupCheckInput(group_id,group_name,comment,owner_name)
        admin_obj=admin_main.getLoader().getAdminByName(owner_name)
        self.__updateGroupDB(group_id,group_name,comment,admin_obj.getAdminID())
        group_main.getLoader().unloadGroup(group_id)
        group_main.getLoader().loadGroup(group_id)
        
    def __updateGroupCheckInput(self,group_id,group_name,comment,owner_name):
        group_obj=group_main.getLoader().getGroupByID(group_id)
        if group_obj.getGroupName()!=group_name:
            if group_main.getLoader().groupNameExists(group_name):
                raise GeneralException(errorText("GROUPS","GROUP_NAME_TAKEN")%group_name)       

            if not isValidName(group_name):
                raise GeneralException(errorText("GROUPS","GROUP_NAME_INVALID")%group_name)

        admin_main.getLoader().checkAdminName(owner_name)
    
    def __updateGroupDB(self,group_id,group_name,comment,owner_id):
        db_main.getHandle().transactionQuery(self.__updateGroupQuery(group_id,group_name,comment,owner_id))

    def __updateGroupQuery(self,group_id,group_name,comment,owner_id):
        return ibs_db.createUpdateQuery("groups",{"group_name":dbText(group_name),
                                                  "comment":dbText(comment),
                                                  "owner_id":owner_id
                                                 },"group_id=%s"%group_id)

############################################
    def updateGroupAttrs(self,group_name,attrs,to_del_attrs,admin_obj):
        """
            update group attributes
            attrs(dic): a dic of attributes in format attr_name=>attr_value that tell "I want these attributes
                        have these values", so attrs may contain only a portion of attributes and not all of them
            to_del_attrs(list): list of attributes that should be deleted from group
            admin_obj(Admin instance): admin that request this update
        """    
        group_obj=group_main.getLoader().getGroupByName(group_name)
        changed_attr_updaters=user_main.getAttributeManager().getAttrUpdaters(attrs,"change")
        deleted_attr_updaters=user_main.getAttributeManager().getAttrUpdaters(to_del_attrs,"delete")
        ibs_query=IBSQuery()
        self.__getChangedQuery(ibs_query,group_obj,changed_attr_updaters,admin_obj)
        self.__getDeletedQuery(ibs_query,group_obj,deleted_attr_updaters,admin_obj)
        ibs_query.runQuery()
        
        group_main.getLoader().loadGroupByName(group_name)
        self.__broadcastChange()
        self.__callPostUpdates(changed_attr_updaters,deleted_attr_updaters)

    def __getChangedQuery(self,ibs_query,group_obj,changed_attr_updaters,admin_obj):
        """
            get query for changed attributes in changed_attr_updaters
            this method may raise an exception on error condition, because info holder checkInputs are called 
            within this method
            
            group_obj(Group Instance): group we're dealing with
            changed_attr_updaters(AttrUpdaterContainer Instance): Container of all info holders
        
        """
        return changed_attr_updaters.getQuery(ibs_query,"group","change",{"group_obj":group_obj,
                                                                         "admin_obj":admin_obj
                                                                         })

    def __getDeletedQuery(self,ibs_query,group_obj,deleted_attr_updaters,admin_obj):
        return deleted_attr_updaters.getQuery(ibs_query,"group","delete",{"group_obj":group_obj,
                                                                         "admin_obj":admin_obj
                                                                         })
    def __callPostUpdates(self,changed_attr_updaters,deleted_attr_updaters):
        changed_attr_updaters.postUpdate("group","change")
        deleted_attr_updaters.postUpdate("group","delete")

    def __broadcastChange(self):
        """
            TODO:XXX reload all users with this group
        """
        pass

    ########################################
    def insertGroupAttrQuery(self,group_id,attr_name,attr_value):
        return ibs_db.createFunctionCallQuery("insert_group_attr",[group_id,dbText(attr_name), dbText(attr_value)])
        
    def updateGroupAttrQuery(self,group_id,attr_name,attr_value):
        return ibs_db.createFunctionCallQuery("update_group_attr",[group_id,dbText(attr_name), dbText(attr_value)])

    def deleteGroupAttrQuery(self,group_id,attr_name):
        return ibs_db.createFunctionCallQuery("delete_group_attr",[group_id,dbText(attr_name)])

    #########################################
    def delGroup(self,group_name):
        """
            delete group with name "group_name"
        """    
        self.__delGroupCheckInput(group_name)
        group_obj=group_main.getLoader().getGroupByName(group_name)
        self.__checkGroupUsageInUsers(group_obj)
        self.__deleteGroupDB(group_obj.getGroupID())
        group_main.getLoader().unloadGroup(group_obj.getGroupID())
        
    def __delGroupCheckInput(self,group_name):
        group_main.getLoader().checkGroupName(group_name)

    def __checkGroupUsageInUsers(self,group_obj):
        user_ids=user_main.getActionManager().getUserIDsWithBasicAttr("group_id",group_obj.getGroupID())
        if len(user_ids)>0:
            raise GeneralException(errorText("GROUPS","GROUP_USED_IN_USER")%(group_obj.getGroupName(),
                                                            ",".join(map(str,user_ids))))
    
    def __deleteGroupDB(self,group_id):
        query=self.__deleteGroupAttrsQuery(group_id)
        query+=self.__deleteGroupQuery(group_id)
        db_main.getHandle().transactionQuery(query)
    
    def __deleteGroupQuery(self,group_id):
        return ibs_db.createDeleteQuery("groups","group_id=%s"%group_id)

    def __deleteGroupAttrsQuery(self,group_id):
        return ibs_db.createDeleteQuery("group_attrs","group_id=%s"%group_id)
    ############################################
    def getGroupIDsWithAttr(self,attr_name,attr_value):
        """
            return group_ids whom attr_name value is attr_value, of course group should have attr_name!
        """
        group_ids=db_main.getHandle().get("group_attrs","attr_name=%s and attr_value=%s"%(dbText(attr_name),dbText(attr_value)),
                                         0,-1,("group_id",True),["group_id"])
                
        return map(lambda dic:dic["group_id"],group_ids)
        