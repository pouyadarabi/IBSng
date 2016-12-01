from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE SAVED USERNAME PASSWORDS",SeeSavedUserPass)

class SeeSavedUserPass (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See List of Saved Username/Password.
         When adding Internet or VoIP username/password attribute to a user, it's possible to save the
         username and passwords in a list, so it can be accessed later. This permission allow admin to see this list.
         If value of permission is restricted, admin is only allowed to see username/passwords that he generated, and he
         won't be able to see other admins list.
         Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE NORMAL USER ATTRIBUTES
               """)
        self.addAffectedPage("User->Add User List")
        self.addDependency("GET USER INFORMATION")      

    def check(self,admin_obj,admin_perm_obj):
        pass
