from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE USER AUDIT LOGS",SeeUserAuditLogs)

class SeeUserAuditLogs (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See User Audit Logs
                This Permission Allows admins to see history of users attribute changes.
                Related Permissions:
                    SEE ONLINE USERS, SEE CREDIT LOGS, SEE CONNETION LOGS
               """)
        self.addAffectedPage("Report->User Audit Log")

    def check(self,admin_obj,admin_perm_obj):
        pass

        