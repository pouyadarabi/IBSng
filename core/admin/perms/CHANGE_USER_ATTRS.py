from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("CHANGE USER ATTRIBUTES",ChangeUserAttrs)

class ChangeUserAttrs (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Change User Attributes And Informations
                This Permission is necassary to change all attributes of user. All other
                user attribute permissions are dependent to this permission.
                Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE NORMAL USER ATTRIBUTES
               """)
        self.addAffectedPage("User->Edit Attributes")
        self.addDependency("GET USER INFORMATION")      

