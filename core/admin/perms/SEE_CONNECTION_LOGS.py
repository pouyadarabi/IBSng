from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE CONNECTION LOGS",SeeConnectionLogs)

class SeeConnectionLogs (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See User Connection Logs
                This Permission Allows admins to see history of user connections and credit consumption
                Restricted value lets admin to see its own user connections or see total usage of all his users
                Related Permissions:
                    SEE ONLINE USERS
               """)
        self.addAffectedPage("Report->Connection Logs")

    def check(self,admin_obj,admin_perm_obj):
        pass
