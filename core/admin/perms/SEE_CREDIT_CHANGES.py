from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE CREDIT CHANGES",SeeCreditChanges)

class SeeCreditChanges (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See User Credit Change Report
                This Permission Allows admins to see history of credit changes including User Add, Change Credit, Delete User
                Restricted value lets admin to see its own users credit change
                Related Permissions:
                    SEE ONLINE USERS
               """)
        self.addAffectedPage("Report->Credit Change")

    def check(self,admin_obj,admin_perm_obj):
        pass
        