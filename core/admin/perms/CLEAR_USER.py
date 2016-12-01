from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("CLEAR USER",ClearUser)

class ClearUser (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Clear Online Users
                Admins with this permission can clear online users.
                The diffrence between kill and clear a user is, kill forces a user to disconnect
                from the ras, and deduct his credit usage while clear only delete user from online list
                of ibs, and doesn't deduct user credit usage. 
                So clear must be used with care and should be gived to trusted admins only.
               """)
        self.addAffectedPage("Report->Online Users")
        self.addDependency("SEE ONLINE USERS")  

