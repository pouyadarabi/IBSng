from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText
from core.group import group_main


def init():
    perm_loader.getLoader().registerPerm("GROUP ACCESS",GroupAccess)

class GroupAccess (MultiValuePermission,GroupCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can use these group even they are not the owner of the gorup.
                if admin wants to use a group ibs checks :
                    1- if admin is GOD => PASS
                    2- if admin is owner of group => PASS
                    2- if admin has pemission ACCESS ALL GROUPS  => PASS
                    3- if group name  is in GROUP ACCESS values => PASS
                    4- FAIL
                
                Related Permissions: ACCESS ALL GROUPS, CHANGE GROUP, ADD NEW GROUP
               """)

        self.addAffectedPage("Group->Group List")

    def getValueCandidates(self):
        return group_main.getLoader().getAllGroupNames()
        
    def check(self,admin_obj,admin_perm_obj,group_name):
        if group_name not in admin_perm_obj.getValue():
            raise PermissionException(errorText("GROUPS","ACCESS_TO_GROUP_DENIED")%group_name)

    def checkNewValue(self,new_val):
        group_main.getLoader().checkGroupName(new_val)
