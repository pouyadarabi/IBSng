from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE ADMIN DEPOSIT",ChangeAdminDeposit)

class ChangeAdminDeposit (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Change Admins Deposit.
                Related Permissions: SEE ADMIN INFO, CHANGE ADMIN INFO , DELETE ADMIN
               """)
        self.addAffectedPage("Admin->Admin Information")
        self.addDependency("CHANGE ADMIN INFO")
