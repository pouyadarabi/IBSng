from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("SEE ADMIN INFO",SeeAdminInfo)

class SeeAdminInfo (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can List and See Other Admins Informations (Name,Deposit,Deposit Ratio ...)
                Related Permissions: CHANGE ADMIN DEPOSIT , CHANGE PERMISSIONS , DELETE ADMIN
               """)
        self.addAffectedPage("Admin->Admin List","Admin->Admin Information")