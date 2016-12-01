from core.admin.admin_perm import *
from core.ibs_exceptions import *
from core.errors import errorText
from core.admin import perm_loader
from core.group import group_main

def init():
    perm_loader.getLoader().registerPerm("CHANGE GROUP",ChangeGroup)

class ChangeGroup (AllRestrictedSingleValuePermission,GroupCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can edit and update group and group attributes
                This Permission can have 2 values:
                    1- RESTRICTED : Admin can change only groups that he is owner
                    2- ALL : Admin can change groups that he has access to , regardless of who is the owner

                Related Permissions: GROUP_ACCESS, ACCESS_ALL_GROUPS, ADD_NEW_GROUP
               """)

        self.addDependency("ADD NEW GROUP")
        self.addAffectedPage("Groups -> Group List")

    def check(self,admin_obj,admin_perm_obj,group_name):
        if admin_perm_obj.getValue()=="All" and not admin_obj.canUseGroup(group_name):
            raise GeneralException(errorText("GROUPS","GROUP_CHANGE_DENIED")%group_name)
            
        elif group_main.getLoader().getGroupByName(group_name).getOwnerID()!=admin_obj.getAdminID():
            raise GeneralException(errorText("GROUPS","GROUP_CHANGE_DENIED")%group_name)