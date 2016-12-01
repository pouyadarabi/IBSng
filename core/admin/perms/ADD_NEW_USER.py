from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("ADD NEW USER",AddNewUser)

class AddNewUser (NoValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add new Users
                Admin with this permission can add new users (and multiple new users at once, 
                depends on admin deposit). Created users have not any specific attribute, and all
                attributes are same as their group.
                
                Related Permissions: GROUP_ACCESS, ACCESS_ALL_GROUPS, CHANGE_GROUP
               """)
        self.addAffectedPage("User->Add New User")

        