from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("ADD NEW ADMIN",AddNewAdmin)

class AddNewAdmin (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add new admins to IBS
                Note: With only this permission admin can't change deposit, or add permissions to admins
                Related Permissions: CHANGE ADMIN DEPOSIT , CHANGE PERMISSIONS , DELETE ADMIN
               """)
        self.addAffectedPage("Admin->Add New Admin")