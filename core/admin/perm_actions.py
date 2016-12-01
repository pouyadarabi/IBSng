from core.admin import admin_main,perm_loader
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import ibs_db,db_main
from core.lib.general import *


def init():
    global perm_actions
    perm_actions=PermActions()
    
def getActionManager():
    return perm_actions

class PermActions:

    def __checkAdminUsernameAndPerm(self,admin_username,perm_name):
        """
            check if admin_username and perm are valid
        """
        admin_main.getLoader().checkAdminName(admin_username)
        perm_loader.getLoader().checkPermName(perm_name)


    def __checkAdminPerm(self,admin_username,perm_name):
        """
            check if admin_username and perm_name is valid and also
            admin_usernams has permission perm_name
        """
        self.__checkAdminUsernameAndPerm(admin_username,perm_name)
        if admin_main.getLoader().getAdminByName(admin_username).hasPerm(perm_name)!=1:
            raise GeneralException(errorText("PERMISSION","DON_HAVE_PERMISSION"))
#########################################################    

    def changePermission(self,admin_username,perm_name,perm_value):
        """
            change permission of "admin_username" by setting "perm_name" value to "perm_value"
            if admin has this already this permission, value changes to "perm_value" or "perm_value"
            adds to other values regarding permission value type.
        """
        self.__changePermissionCheckInput(admin_username,perm_name,perm_value)
        admin_obj=admin_main.getLoader().getAdminByName(admin_username)
        if not admin_obj.hasPerm(perm_name):
            self.__addNewPerm(admin_obj,perm_name,perm_value)
        else:
            self.__changePermValue(admin_obj,perm_name,perm_value)
        admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
        
    def __addNewPerm(self,admin_obj,perm_name,perm_value):
        self.__checkPermDependencies(admin_obj,perm_name)
        self.__addPermToDB(admin_obj,perm_name,perm_value)
    
    def __addPermToDB(self,admin_obj,perm_name,perm_value):
        db_main.getHandle().transactionQuery(self.__addPermQuery(admin_obj.getAdminID(),perm_name,perm_value))
    
    def __addPermQuery(self,admin_id,perm_name,perm_value):
        return ibs_db.createInsertQuery("admin_perms",{"admin_id":admin_id,
                                                       "perm_name":dbText(perm_name),
                                                       "perm_value":dbText(perm_value)})

    def __checkPermDependencies(self,admin_obj,perm_name):
        dep_list=perm_loader.getLoader()[perm_name].getDependencies()
        for dep in dep_list:
            if not admin_obj.hasPerm(dep):
                raise GeneralException(errorText("PERMISSION","DEPENDENCY_NOT_SATISFIED")%(dep,perm_name))


    def __changePermissionCheckInput(self,admin_username,perm_name,perm_value):
        self.__checkAdminUsernameAndPerm(admin_username,perm_name)
        perm_loader.getLoader()[perm_name].checkNewValue(perm_value)

    def __changePermValue(self,admin_obj,perm_name,perm_value):
        perm_obj=perm_loader.getLoader()[perm_name]
        if perm_obj.getValueType()=="MULTIVALUE":
            admin_perm_obj=admin_obj.getPerms()[perm_name]
            if admin_perm_obj.multi_value.hasValue(perm_value):
                raise GeneralException(errorText("PERMISSION","PERMISSION_ALREADY_HAS_VALUE")%(perm_name,perm_value)) 
            perm_value=admin_perm_obj.multi_value.addNewValue(perm_value)
        elif perm_obj.getValueType()=="NOVALUE":
            raise GeneralException(errorText("PERMISSION","ALREADY_HAS_PERMISSION")%perm_name) #there's no value to change
            
        self.__changePermValueDB(admin_obj,perm_name,perm_value)

    def __changePermValueDB(self,admin_obj,perm_name,perm_value):
        db_main.getHandle().transactionQuery(self.__changePermValueQuery(admin_obj.getAdminID(),perm_name,perm_value))

    def __changePermValueQuery(self,admin_id,perm_name,perm_value):
        return ibs_db.createUpdateQuery("admin_perms",
                                  {"perm_value":dbText(perm_value)},
                                  "perm_name=%s and admin_id=%s"%(dbText(perm_name), admin_id) )
########################################################
    def deletePermission(self,admin_username,perm_name):
        """
            delete permission "perm_name" from admin "admin_username"
        """
        self.__deletePermissionCheckInput(admin_username,perm_name)
        admin_obj=admin_main.getLoader().getAdminByName(admin_username)
        self.__checkDependenciesOfPerm(admin_obj,perm_name)
        self.__deletePermissionDB(admin_obj,perm_name)
        admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
    
    def __deletePermissionCheckInput(self,admin_username,perm_name):
        self.__checkAdminPerm(admin_username,perm_name) 

    def __checkDependenciesOfPerm(self,admin_obj,perm_name):
        """
            check if there "admin_obj" has a perm that is dependent on "perm_name"
            it means we can not delete "perm_name" until we delete perms that are dependent on it
        """
        all_perms=admin_obj.getPerms()
        for perm in all_perms:
            if perm_name in all_perms[perm].getPermObj().getDependencies():
                raise GeneralException(errorText("PERMISSION","DEPENDENT_PERMISSION")%(perm_name,perm))

    def __deletePermissionDB(self,admin_obj,perm_name):
        db_main.getHandle().transactionQuery(self.__deletePermissionQuery(admin_obj.getAdminID(),perm_name))    
    
    def __deletePermissionQuery(self,admin_id,perm_name):
        return ibs_db.createDeleteQuery("admin_perms","admin_id=%s and perm_name=%s"%
                                                          (admin_id,dbText(perm_name)))

############################################################
    def deleteFromPermValues(self,admin_username,perm_name,perm_value):
        self.__deleteFromPermValuesCheckInput(admin_username,perm_name,perm_value)
        admin_obj=admin_main.getLoader().getAdminByName(admin_username)
        admin_perm_obj=admin_obj.getPerms()[perm_name]
        self.__checkDeleteValue(admin_obj,admin_perm_obj,perm_value)
        new_value=admin_perm_obj.multi_value.delValue(perm_value)
        self.__updatePermValueDB(admin_obj,perm_name,new_value)
        admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
        
    def __updatePermValueDB(self,admin_obj,perm_name,new_value):
        db_main.getHandle().transactionQuery(self.__updatePermValueQuery(admin_obj.getAdminID(),perm_name,new_value))
    
    def __updatePermValueQuery(self,admin_id,perm_name,perm_value):
        return ibs_db.createUpdateQuery("admin_perms",{"perm_value":dbText(perm_value)}
                                                     ,"perm_name=%s"%dbText(perm_name))
        
    def __deleteFromPermValuesCheckInput(self,admin_username,perm_name,perm_value):
        self.__checkAdminPerm(admin_username,perm_name) 

    def __checkDeleteValue(self,admin_obj,admin_perm_obj,perm_value):
        perm_obj=admin_perm_obj.getPermObj()
        if perm_obj.getValueType()!="MULTIVALUE":
            raise GeneralException(errorText("PERMISSION","NO_VALUE_TO_DELETE"))
        if perm_value not in admin_perm_obj.getValue():
            raise GeneralException(errorText("PERMISSION","PERMISSION_NOT_HAVE_THIS_VALUE")%perm_value)
###############################################################
    def savePermsOfAdminToTemplate(self,admin_username,template_name):
        """
            save permissions of "admin_username" to template with name "template_name"
        """
        self.__savePermsOfAdminToTemplateCheckInput(admin_username,template_name)
        admin_obj=admin_main.getLoader().getAdminByName(admin_username)
        template_id=self.__getNewTemplateID()
        self.__savePermsToTemplateDB(admin_obj,template_name,template_id)
        
    def __savePermsOfAdminToTemplateCheckInput(self,admin_username,template_name):
        admin_main.getLoader().checkAdminName(admin_username)

        if not len(template_name) or not template_name.isalnum():
            raise GeneralException(errorText("PERMISSION","INVALID_PERM_TEMPLATE_NAME")%template_name)

        self.__checkDuplicateTemplateName(template_name)

    def __checkDuplicateTemplateName(self,template_name):
        if self.__templateNameExists(template_name):
            raise GeneralException(errorText("PERMISSION","DUPLICATE_TEMPLATE_NAME")%template_name)
        
    def __templateNameExists(self,template_name):
        return db_main.getHandle().getCount("admin_perm_templates","template_name=%s"%
                                                dbText(template_name))

    def __getNewTemplateID(self):
        return db_main.getHandle().seqNextVal("admin_perm_template_id")

    def __savePermsToTemplateDB(self,admin_obj,template_name,template_id):
        query=self.__addNewPermTemplateQuery(template_name,template_id)
        query+=self.__savePermsTemplateDetailsFromAdminQuery(admin_obj.getAdminID(),template_id)
        db_main.getHandle().transactionQuery(query)
                        
    def __addNewPermTemplateQuery(self,template_name,template_id):
        return ibs_db.createInsertQuery("admin_perm_templates",{"template_id":template_id,
                                                                "template_name":dbText(template_name)
                                                                })

    def __savePermsTemplateDetailsFromAdminQuery(self,admin_id,template_id):
        return "insert into admin_perm_templates_detail (select %s,perm_name,perm_value from admin_perms \
                where admin_id=%s);"%(template_id,admin_id)
                    
##################################################################
    def getListOfPermTemplates(self):
        """
            return a list of all perm template names
        """
        templates=db_main.getHandle().get("admin_perm_templates","true")
        return [dic["template_name"] for dic in templates]

#################################################################

    def __templateNameToIDQuery(self,template_name):
        return "select template_id from admin_perm_templates where template_name=%s"%dbText(template_name)

##################################################################
    def getPermsOfTemplate(self,template_name):
        return db_main.getHandle().get("admin_perm_templates_detail",
                                 "template_id = (%s)"%self.__templateNameToIDQuery(template_name))
##################################################################
    def loadPermTemplateToAdmin(self,template_name,admin_username):
        """
            load permissions in template into admin permissions.
            WARNING: This will delete all of admin permissions
        """
        self.__loadPermTemplateToAdminCheckInput(template_name,admin_username)
        admin_obj=admin_main.getLoader().getAdminByName(admin_username)
        self.__loadPermTemplateToAdminDB(template_name,admin_obj)
        admin_main.getLoader().loadAdmin(admin_obj.getAdminID())
        
    def __loadPermTemplateToAdminDB(self,template_name,admin_obj):
        query=self.__delAllAdminPermsQuery(admin_obj.getAdminID())
        query+=self.__loadPermTemplateIntoAdminQuery(template_name,admin_obj.getAdminID())
        db_main.getHandle().transactionQuery(query)
    
    def __loadPermTemplateToAdminCheckInput(self,template_name,admin_username):
        admin_main.getLoader().checkAdminName(admin_username)
        self.__checkTemplateName(template_name)
        
    def __checkTemplateName(self,template_name):
        if not self.__templateNameExists(template_name):
            raise GeneralException(errorText("PERMISSION","INVALID_PERM_TEMPLATE_NAME")%template_name)

    def __delAllAdminPermsQuery(self,admin_id):
        return ibs_db.createDeleteQuery("admin_perms","admin_id=%s"%admin_id)

    def __loadPermTemplateIntoAdminQuery(self,template_name,admin_id):
        return "insert into admin_perms (admin_id,perm_name,perm_value) (select %s,perm_name,perm_value from \
                admin_perm_templates_detail where template_id=(%s));"%(admin_id,self.__templateNameToIDQuery(template_name))

#####################################################################
    def deletePermTemplate(self,template_name):
        self.__deletePermTemplateCheckInput(template_name)
        self.__deletePermTemplateDB(template_name)
        
    def __deletePermTemplateDB(self,template_name):
        query=self.__deletePermTemplateDetailsQuery(template_name)
        query+=self.__deletePermTemplateQuery(template_name)
        db_main.getHandle().transactionQuery(query)
    
    def __deletePermTemplateDetailsQuery(self,template_name):
        return ibs_db.createDeleteQuery("admin_perm_templates_detail","template_id = (%s)"%(self.__templateNameToIDQuery(template_name)))

    def __deletePermTemplateQuery(self,template_name):
        return ibs_db.createDeleteQuery("admin_perm_templates","template_name=%s"%dbText(template_name))
        
    def __deletePermTemplateCheckInput(self,template_name):
        self.__checkTemplateName(template_name)
