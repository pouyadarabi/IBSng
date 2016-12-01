from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("ADD NEW GROUP",AddNewGroup)

class AddNewGroup (NoValuePermission,GroupCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add and Delete Groups
                Admins can add new groups, and use them to add users
                
                Related Permissions: GROUP_ACCESS, ACCESS_ALL_GROUPS, CHANGE_GROUP
               """)
        self.addAffectedPage("Group->Add New Group","Group->Change Group Attributes")

        