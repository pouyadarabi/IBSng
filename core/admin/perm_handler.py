from core.server import handler
from core.admin import admin_main,perm_actions,perm_loader
from core.lib.sort import SortedList
from core.ibs_exceptions import *
from core.errors import errorText


class PermHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"perm")
        self.registerHandlerMethod("hasPerm")
        self.registerHandlerMethod("canDo")
        self.registerHandlerMethod("getPermsOfAdmin")
        self.registerHandlerMethod("getAllPerms")
        self.registerHandlerMethod("getAdminPermVal")
        self.registerHandlerMethod("changePermission")
        self.registerHandlerMethod("delPermission")
        self.registerHandlerMethod("delPermissionValue")
        self.registerHandlerMethod("savePermsOfAdminToTemplate")
        self.registerHandlerMethod("getListOfPermTemplates")
        self.registerHandlerMethod("getPermsOfTemplate")
        self.registerHandlerMethod("loadPermTemplateToAdmin")
        self.registerHandlerMethod("deletePermTemplate")
        
    def canDo(self,request):
        """
            return True if "admin_username" canDo "perm_name" with params
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("perm_name","admin_username","params")
        if request.auth_name!=request["admin_username"]:        
            request.getAuthNameObj().canDo("SEE ADMIN PERMISSIONS")
        args=[request["perm_name"]]
        args.extend(request.fixList("params"))
        try:
            apply(admin_main.getLoader().getAdminByName(request["admin_username"]).canDo,args)
            return True
        except PermissionException:
            return False

    def hasPerm(self,request):
        """
            return True if admin has permission and else False
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("perm_name","admin_username")
        if request.auth_name!=request["admin_username"]:        
            request.getAuthNameObj().canDo("SEE ADMIN PERMISSIONS")
        return admin_main.getLoader().getAdminByName(request["admin_username"]).hasPerm(request["perm_name"])

############################
    def getAdminPermVal(self,request):
        """
            return value of perm_name for admin_username
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("perm_name","admin_username")
        if request.auth_name!=request["admin_username"]:        
            request.getAuthNameObj().canDo("SEE ADMIN PERMISSIONS")
        perms=admin_main.getLoader().getAdminByName(request["admin_username"]).getPerms()
        if not perms.has_key(request["perm_name"]):
            return request.getErrorResponse(errorText("PERMISSION","DONT_HAVE_PERMISSION"))
        return perms[request["perm_name"]].getValue()

############################
    def getPermsOfAdmin(self,request):
        """
            return a list of dics containing admin permission and sorted by permission name
            each dic has "name, value, description, value_type, category" keys
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("admin_username")
        admin_perms=admin_main.getLoader().getAdminByName(request["admin_username"]).getPerms()
        perms_list=self.__getPermsListFromAdminPerms(admin_perms)
        sorted=SortedList(perms_list)
        sorted.sortByPostText('["name"]',0)
        return sorted.getList()

    def __getPermsListFromAdminPerms(self,admin_perms):
        perms_list=[]
        for perm_name in admin_perms:
            admin_perm_obj=admin_perms[perm_name]
            perm_obj=admin_perm_obj.getPermObj()
            perms_list.append({   "name":perm_name,
                                  "value":admin_perm_obj.getValue(),
                                  "description":perm_obj.getDescription(),
                                  "value_type":perm_obj.getValueType(),
                                  "category":perm_obj.getCategory()
                                  })
        return perms_list
##################################
    def getAllPerms(self,request):
        """
            return a list of dics of all perms sorted by permission name
            optional argument category tells handler to return only permission of specified category
            each dic has "name, description, value_type, category, affected_pages, dependencies" keys
        """
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        all_perms_dic=perm_loader.getLoader().getAllPerms()
        if request.has_key("category"):
            category=request["category"]
        else:
            category="all"
        all_perms_list=self.__getPermsListFromPerms(all_perms_dic,category)
        sorted=SortedList(all_perms_list)
        sorted.sortByPostText('["name"]',0)
        return sorted.getList() 
        
    def __getPermsListFromPerms(self,perms_dic,category):
        perms_list=[]
        for perm_name in perms_dic:
            perm_obj=perms_dic[perm_name]
            if category!="all" and perm_obj.getCategory()!=category:
                continue
            perm_dic={"name":perm_name,
                      "description":perm_obj.getDescription(),
                      "value_type":perm_obj.getValueType(),
                      "category":perm_obj.getCategory(),
                      "affected_pages":perm_obj.getAffectedPages(),
                      "dependencies":perm_obj.getDependencies()
                     }
            if perm_obj.getValueCandidates() != None:
                perm_dic["value_candidates"]=perm_obj.getValueCandidates()
            perms_list.append(perm_dic)
        return perms_list

#############################    
    def changePermission(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")

        request.checkArgs("perm_name","admin_username","perm_value")
        perm_actions.getActionManager().changePermission(request["admin_username"],request["perm_name"],
                                                         request["perm_value"])

#############################
    def delPermission(self,request):
        """
            delete "perm_name" from "admin_username"
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("admin_username","perm_name")
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        perm_actions.getActionManager().deletePermission(request["admin_username"],request["perm_name"])

    def delPermissionValue(self,request):
        """
            delete "perm_value" from multivalue perm "perm_name" for admin "admin_username"
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("admin_username","perm_name","perm_value")
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        perm_actions.getActionManager().deleteFromPermValues(request["admin_username"],request["perm_name"],
                                                             request["perm_value"])
##############################
    def savePermsOfAdminToTemplate(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("admin_username","perm_template_name")
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        perm_actions.getActionManager().savePermsOfAdminToTemplate(request["admin_username"],
                                                                   request["perm_template_name"])
##############################
    def getListOfPermTemplates(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        return perm_actions.getActionManager().getListOfPermTemplates()
###############################
    def getPermsOfTemplate(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        request.checkArgs("perm_template_name")
        raw_perms=perm_actions.getActionManager().getPermsOfTemplate(request["perm_template_name"])
        admin_perms=self.__createAdminPermsFromRawPerms(raw_perms)
        return self.__getPermsListFromAdminPerms(admin_perms)

    def __createAdminPermsFromRawPerms(self,raw_perms):
        return perm_loader.getLoader().getPermsOfAdminFromRawPermList(raw_perms)
###############################
    def loadPermTemplateToAdmin(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        request.checkArgs("perm_template_name","admin_username")
        return perm_actions.getActionManager().loadPermTemplateToAdmin(request["perm_template_name"],request["admin_username"])
###############################
    def deletePermTemplate(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE ADMIN PERMISSIONS")
        request.checkArgs("perm_template_name")
        return perm_actions.getActionManager().deletePermTemplate(request["perm_template_name"])
        