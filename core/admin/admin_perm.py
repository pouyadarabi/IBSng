from core.ibs_exceptions import *
from core.errors import errorText
import string 
import re
import copy

class MultiValue:
    def __init__(self,value):
        self.value_list=self.__parseValue(value)

    def __parseValue(self,value):
        if not len(value):
            return []
        else:
            return value.split(",")
        
    def __compileValues(self,value_list):
        return ",".join(value_list)

    def addNewValue(self,new_val):
        """
            add a new value to current values
            and return new raw_value needed to place in db
        """
        return self.__compileValues(self.value_list+[new_val])

    def delValue(self,value):
        """
            delete value from values and return raw value suitable for db
        """
        new_list=copy.copy(self.value_list)
        new_list.pop(new_list.index(value))
        return self.__compileValues(new_list)

    def getList(self):
        return self.value_list

    def hasValue(self,value):
        return value in self.value_list

class AdminPermission:
    """
        Parent class of all admin permissions, 
        instances of this class would be kept in admin objects
    """
    def __init__(self,admin_obj,perm_obj,value):
        self.admin_obj=admin_obj
        self.perm_obj=perm_obj
        self.value=self.__parseValue(value)
        
    def check(self,*args):
        """
            check if self.admin_obj has self.perm_obj permission
            additional *args are used in situations where they are needed
            (ex. username where adding a new user)
        """
        return apply(self.perm_obj.check,[self.admin_obj,self]+list(args))
    
    
    def __parseValue(self,perm_value):
        """
            parse "perm_value" if self.perm_obj.getValueType is MULTIVALUE
            else return the perm_value itself ("perm_value" can be None or empty string 
            if permission don't care about values)
        """
        if self.perm_obj.getValueType()=="MULTIVALUE":
            return self.__parseMultiValue(perm_value)
        return perm_value

    def __parseMultiValue(self,perm_value):
        """
            return a list of values, that "perm_value" represents.
            values of MULTIVALUE permissions are delimited with a ","
        """
        self.multi_value=MultiValue(perm_value)
        return self.multi_value.getList()

    def getValue(self):
        return self.value

    def isRestricted(self):
        return self.getValue()=="Restricted"

    def getPermObj(self):
        return self.perm_obj
        
class Permission:
    """
        parent calss for all permission implemetion,
        permissions are kept in perms/ directory, and on instance of each of them
        will be kept in perm_loader instance
        AdminPermission is a wrapper for these instances.
        Permissions should override init
        then it can use setDescription addAffectedPage and addDependency to set it's own
        values
    """
    def __init__(self,name):
        self.name=name
        self.value_candidates=None
        self.description="No Description"
        self.dependencies=[]
        self.affected_pages=[]
        
    def init(self):
        """
            this function should override by children to do it's own initialization
        """
        pass

    def check(self,admin_obj,admin_perm_obj,*args):
        """
            check permission for admin_obj using args
            it should return on success or raise PermissionException on access denied
        """
        pass

    def getName(self):
        return self.name
        
    def getValueType(self):
        pass    
    
    def getValueCandidates(self):
        """
            return vaule lists for "MULTIVALUE" permissions,
            return a list of candidate values or None if user should enter a text as value
        """
        return self.value_candidates
    
    def checkNewValue(self,new_value):
        """
            if permission has value(s), this function is called to check new values for permission
            it should call self.newValueException(err_msg) method on error or return on success
        """
        return
        
    def newValueException(self,err_msg):
        raise GeneralException(errorText("PERMISSION","INVALID_PERMISSION_VALUE")%err_msg)
    
    def getDescription(self):
        return self.description
    
    def getCategory(self):
        pass

    def setDescription(self,description):
        self.description=self.__formatDescription(description)
        
    def __formatDescription(self,description):
        return re.sub("\n[\s\t]*"," \n",description) #delete space and tabs on start of lines
        
    def addAffectedPage(self,*args):
        for affected_page in args:
            self.affected_pages.append(affected_page)

    def addDependency(self,*args):
        for dependency in args:
            self.dependencies.append(dependency)

    def getAffectedPages(self):
        return self.affected_pages

    def getDependencies(self):
        """
            return a list of permission names, this permission depends on.
            if admin doesn't have these permissions, he can't have this permission too
        """
        return self.dependencies

    def setValueCandidates(self,value_candidates):
        self.value_candidates=value_candidates
        

#Abstract classes, each permission should inherit from Permission and then these classes

#VALUE_TYPE CLASSES
class NoValuePermission:
    def getValueType(self):
        return "NOVALUE"

class SingleValuePermission:
    def getValueType(self):
        return "SINGLEVALUE"


class MultiValuePermission:
    def getValueType(self):
        return "MULTIVALUE"

###

class AllRestrictedSingleValuePermission(SingleValuePermission):
    VALUES=["All","Restricted"]
    def getValueCandidates(self):
        return self.VALUES

    def checkNewValue(self,new_val):
        if new_val not in self.VALUES:
            self.newValueException(errorText("PERMISSION","INVALID_PERMISSION_VALUE")%new_val)

    def check(self,admin_obj,admin_perm_obj,user_id,owner_id):
        """
            user_id: id of user we want to check if we can change credit
            owner_id: owner of user
        """
        if admin_perm_obj.getValue()=="Restricted" and owner_id!=admin_obj.getAdminID():
            raise PermissionException(errorText("USER","ACCESS_TO_USER_DENIED")%user_id)


#CATEGORY CLASSES
class UserCatPermission:
    def getCategory(self):
        return "USER"

class AdminCatPermission:
    def getCategory(self):
        return "ADMIN"

class RasCatPermission:
    def getCategory(self):
        return "RAS"

class ChargeCatPermission:
    def getCategory(self):
        return "CHARGE"

class GroupCatPermission:
    def getCategory(self):
        return "GROUP"

class MiscCatPermission:
    def getCategory(self):
        return "MISC"
