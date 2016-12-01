from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("CHANGE USER CREDIT",ChangeUserCredit)

class ChangeUserCredit (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Change User Credit
                Admins with this permission can increase/decrease user credits in limitations of their deposit.
                Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE NORMAL USER ATTRIBUTES, CHANGE_USER_ATTRIBUTES
               """)
        self.addAffectedPage("User->Edit Attributes")
        self.addDependency("GET USER INFORMATION")      

