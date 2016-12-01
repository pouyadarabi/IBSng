from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE ADMIN PASSWORD",ChangeAdminPassword)

class ChangeAdminPassword (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Change Other Admins Password
                All Admins Can change their own password, This Permission allow them to change 
                other admins password
                Related Permissions: CHANGE ADMIN DEPOSIT , CHANGE PERMISSIONS , DELETE ADMIN
                """)
        self.addDependency("SEE ADMIN INFO")
        self.addAffectedPage("Admin->Change Password")