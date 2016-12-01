from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE ONLINE USERS",SeeOnlineUsers)

class SeeOnlineUsers (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See Online User Report
                This Permission Allows admins to see online users report and user session informations
                such as connection time, remaining credit,...
                Related Permissions: 
                    SEE CONNECTION LOGS
               """)
        self.addAffectedPage("Report->Online Users")

    def check(self,admin_obj,admin_perm_obj):
        pass
        