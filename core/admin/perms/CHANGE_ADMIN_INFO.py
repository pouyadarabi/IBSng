from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE ADMIN INFO",ChangeAdminInfo)

class ChangeAdminInfo (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Change Admins Name and Comment and Lock or Unlock Admins
                Related Permissions: SEE ADMIN INFO, CHANGE ADMIN DEPOSIT , CHANGE PERMISSIONS , DELETE ADMIN
               """)
        self.addAffectedPage("Admin->Admin Information")
        self.addDependency("SEE ADMIN INFO")
