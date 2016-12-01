from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("NO DEPOSIT LIMIT",NoDepositLimit)

class NoDepositLimit (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Allow admin to be able to spend infinit amount of deposit. This is done by allowing
                negative deposit for admin. Deposit always decreases after adding users/credit but this admins
                has no limitation on spending deposit.
                Related Permissions: CHANGE ADMIN DEPOSIT , SEE ADMIN INFO , GOD , CHANGE PERMISSIONS , DELETE ADMIN
               """)
        self.addAffectedPage("User->Add User","User->Change Credit")
    
