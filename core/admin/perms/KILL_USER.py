from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("KILL USER",KillUser)

class KillUser (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Kill Online Users
                Admins with this permission can force disconnection users, via the link in online users page
               """)
        self.addAffectedPage("Report->Online Users")
        self.addDependency("SEE ONLINE USERS")  

