from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE USERS OWNER",ChangeUsersOwner)

class ChangeUsersOwner (NoValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Change User owners when adding/editing users
                each user has an admin owner.It's important for resellers that 
                    1- should not be able to change owners
                    2- should be owner of their own users
                
                Related Permissions: GROUP_ACCESS, ADD NEW USER
               """)
        self.addAffectedPage("User->Add New User","User->Edit User")

        