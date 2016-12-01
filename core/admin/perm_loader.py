from core.db import db_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.admin import admin_perm
from core.plugins import plugin_loader
from core import defs

PERMS_DIRECTORY="%s/admin/perms"%defs.IBS_CORE

def init():
    global perm_loader
    perm_loader=PermLoader()
    plugin_loader.loadPlugins(PERMS_DIRECTORY)

def getLoader():
    return perm_loader

class PermLoader:
    def __init__(self):
        self.perm_objs={} #dic of {perm_name:perm_obj}
        
    def __getitem__(self,_index):
        return self.perm_objs[_index]

    def getAllPerms(self):
        return self.perm_objs

    def checkPermName(self,perm_name):
        """
            check perm name and raise a general exception on invalid name
        """
        if not self.permNameValid(perm_name):
            raise GeneralException(errorText("PERMISSION","NO_SUCH_PERMISSION"))


    def permNameValid(self,perm_name):
        """
            check if there's already registered permission with name "perm_name"
            return 1 if perm_name is valid and else 0
        """
        return self.perm_objs.has_key(perm_name)

        

    def registerPerm(self,perm_name,perm_class):
        """
            register "perm_class" with name "perm_name".
            Put the name and an instance of perm_class into internal dic
        """
        self.__checkDuplicateName(perm_name)
        self.perm_objs[perm_name]=self.__createPermObj(perm_name,perm_class)


    def __checkDuplicateName(self,perm_name):
        if self.perm_objs.has_key(perm_name):
            raise IBSException(errorText("PERMISSION","DUPLICATE_PERM_NAME")%perm_name)    


    def __createPermObj(self,perm_name,perm_class):
        """
            return initialized object of perm_class
        """
        perm_obj=perm_class(perm_name)
        perm_obj.init()
        return perm_obj


    def getPermsOfAdmin(self,admin_obj):
        """
            retrieve permissions of admin with id "admin_obj.admin_id",create and return AdminPermission instances
            in a dic with format {"PERM_NAME":ADMIN_PERM_OBJ} 
        """
        perms=self.__getPermsOfAdminDB(admin_obj.getAdminID())
        return self.__createAdminPermsDic(perms,admin_obj)


    def getPermsOfAdminFromRawPermList(self,raw_perms):
        """
            raw_perms is a list of permissions returned from db query "select * from admin_perms"
            Admin obj in admin_perm instance would be none, so it's just useful for simulating permissions
            and their values
        """
        return self.__createAdminPermsDic(raw_perms,None)

    def __createAdminPermsDic(self,perms,admin_obj):
        """
            return admin perms dic from perms
            perms is a list of dics returned from table admin_perms
        """
        admin_perms_dic={}
        for perm in perms:
            admin_perms_dic[perm["perm_name"]]=self.__createAdminPermObj(admin_obj,\
                                               self.__getPermObj(perm["perm_name"]),perm["perm_value"])
        return admin_perms_dic
    
    def __getPermsOfAdminDB(self,admin_id):
        """
            retrieve and return a list of dics, containing permissions of admin with id "admin_id" from db
            and from admin_perms table
        """
        return db_main.getHandle().get("admin_perms","admin_id=%s"%admin_id)    

    def __getPermObj(self,perm_name):
        """
            return instance of Permission class with name "perm_name"
        """
        try:
            return self.perm_objs[perm_name]
        except KeyError:
            raise IBSException(errorText("PERMISSION","NO_SUCH_PERMISSION")%perm_name)

    def __createAdminPermObj(self,admin_obj,perm_obj,perm_value):
        """
            create and return a new instance of AdminPermission for "admin_obj" and "perm_obj" and "perm_value"
        """
        return admin_perm.AdminPermission(admin_obj,perm_obj,perm_value)
