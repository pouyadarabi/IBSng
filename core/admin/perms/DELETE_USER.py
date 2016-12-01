from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("DELETE USER",DeleteUser)

class DeleteUser (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Delete Users
                Admins with this permission can delete users. Admin with Restricted value of this permission
                only can delete his own users. Remaining credit of users would be added to admin deposit
                Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE NORMAL USER ATTRIBUTES, CHANGE_USER_ATTRIBUTES
               """)
        self.addAffectedPage("User->Edit Attributes")
        self.addDependency("GET USER INFORMATION")      

